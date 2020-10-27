"""
Convert PNG image into a binary sprite sheet file. A sprite sheet file stores
sprites in series in the same data structur format as the Amiga hardware expects it.
Therefore the data for a sprite is always 16 pixel wide.


A tile sheet file has this format:
flags:

bit 0: not set -> big endian, set -> little endian

Header (20 bytes)

'RATR0SPR'     byte 0-7   identifier
version        byte 8     file format version
flags          byte 9     special flags
reserved1      byte 10
palette_size   byte 11    number of color entries in the palette (max 16)
num_sprites    byte 12-13 number of sprites in the data
imgdata_size   byte 14-17 size of image data
checksum       byte 18-19 checksum of the header (unused)

spr0_offset    byte 20-21 offset in the sprite data
...
palette_data   <palette_size> * 2-byte entries
image_data     <imgdata_size> bytes
"""

from PIL import Image
import struct
import math
import sys
import os

from ratr0.util import png_util

"""
Write a format that can be instantly used as a sprite sheet.
So, each sprite is

  - 1 word: VSTART/HSTART
  - 1 word: VSTOP+ctrl bits
  - n words of color data for planes 1 and 2, interleaved
  - 2 words of 0

if a 4 bitplane source was used, the following data structure will be the same,
except that the ATTACH flag is set

if the width was a multiple of 16, there will be data for up to 8 sprites in a row

"""
FILE_FORMAT_VERSION = 1

class SpriteInfoHeader:

    def __init__(self, version, flags, num_colors, num_sprites, imgdata_size):
        self.version = version
        self.flags = flags
        self.num_colors = num_colors
        self.imgdata_size = imgdata_size
        self.num_sprites = num_sprites
        self.checksum = 0

    def write(self, outfile):
        outfile.write(b'RATR0SPR')
        outfile.write(bytes([self.version, self.flags, 0, self.num_colors]))
        outfile.write(struct.pack(">H", self.num_sprites))
        outfile.write(struct.pack(">I", self.imgdata_size))
        outfile.write(struct.pack(">H", self.checksum))

    def __str__(self):
        out = "Version: %d\n" % self.version
        out += "flags: %d\n" % self.flags
        out += "# colors: %d\n" % self.num_colors
        out += "# sprites: %d\n" % self.num_sprites
        out += "# image data bytes: %d\n" % self.imgdata_size
        out += "# checksum: %d" % self.checksum
        return out



def write_sprites(im, outpath, verbose, generatec):
    colors = png_util.make_colors(im, None, verbose)
    depth = int(math.log2(len(colors)))
    colors = [(((r >> 4) & 0x0f) << 8) | (((g >> 4) & 0x0f) << 4) | ((b >> 4) & 0x0f)
              for r, g, b in colors]

    if verbose:
        print("Sprite Colors:")
        print(['%03x' % c for c in colors])

    planes, map_words_per_row = png_util.extract_planes(im, depth, verbose)
    # introduce a zero plane if the number of planes is 1 or 3
    if len(planes) == 1 or len(planes) == 3:
        ref_plane = planes[-1]
        add_plane = [0] * len(ref_plane)
        planes.append(add_plane)
        depth += 1

    if im.width % 16 > 0:
        raise Exception("Image width must be a multiple of 16 (was %d)" % im.width)
    if len(planes) > 4:
        raise Exception('%d exceeded maximum number of planes (should be at most %d)' % (len(planes), 4))
    num_sprites = int((im.width / 16) * (depth / 2))
    if num_sprites > 8:
        raise Exception("Exceeded the depth + width maximum (2 planes+128 pixels or 4 planes*64 pixels) ")

    imgdata_size = 0
    if len(planes) == 4:
        attach = 0x80
        if verbose:
            print("writing %d sprites (attached)" % num_sprites)
    else:
        attach = 0x00
        if verbose:
            print("writing %d sprites" % num_sprites)

    for i, plane in enumerate(planes):
        if verbose:
            print('--  PLANE %d ---------------' % i)
        for w in plane:
            hexstr = '%04x' % w
            binstr = format(w, '016b')
            if verbose:
                print('%s %s' % (hexstr, binstr))
            imgdata_size += 2  # add up the size
    imgdata_size += 8 * num_sprites  # add the sprite control words for each sprite


    # subdivide image data by planes and horizontal size
    if len(planes) == 2:
        vbatches = [planes]
    else:  # 4 planes
        vbatches = [planes[:2], planes[2:]]
    xparts = int(im.width / 16)
    sprite_height = len(vbatches[0][0])

    if generatec:
        outstr = ""  # for generating C source code
        outstr += "UWORD palette[] = {\n"
        outcols = []
        for color in colors:
            outcols.append('0x%04x' % (color & 0x0fff))
        outstr += "  " + ', '.join(outcols)
        outstr += "\n};\n\n"

        sprite_num = 0
        xpos = 0  # xpos if we have wide sprites
        while xpos < xparts:
            for write_planes in vbatches:
                p0 = write_planes[0]
                p1 = write_planes[1]

                if verbose:
                    print("writing sprite number %d (height: %d, attach: %02x)" % (sprite_num, sprite_height, attach))
                outstr += "UWORD __chip sprdata%d[] = {\n" % sprite_num
                outstr += "  0x%04x, 0x%04x,\n" % (sprite_height, attach)

                num_rows = int(len(p0) / xparts)
                for i in range(num_rows):
                    idx = i * xparts + xpos
                    outstr += "  0x%04x, 0x%04x,\n" % (p0[idx], p1[idx])

                # end-of-data
                outstr += "  0x0000, 0x0000\n"
                outstr += "};\n\n"

                # next sprite
                sprite_num += 1
            xpos += 1  # advance x position by 16 pixel in case the sprite is wide

        with open(outpath, 'w') as outfile:
            outfile.write(outstr)
    else:
        header = SpriteInfoHeader(FILE_FORMAT_VERSION, 0, len(colors), num_sprites, imgdata_size)
        with open(outpath, 'wb') as outfile:
            header.write(outfile)

            # 1. write sprite descriptors
            for i in range(num_sprites):
                # offset into the data, height * num planes * 2 bytes (16 pixels) + 8 bytes overhead
                outfile.write(struct.pack(">H", i * (im.height * 4 + 8)))

            # 2. write the palette entries used
            for color in colors:
                outfile.write(struct.pack(">H", (color & 0x0fff)))

            # 3. write sprite data
            sprite_num = 0
            xpos = 0  # xpos if we have wide sprites
            while xpos < xparts:
                for write_planes in vbatches:
                    p0 = write_planes[0]
                    p1 = write_planes[1]

                    if verbose:
                        print("writing sprite number %d (height: %d, attach: %02x)" % (sprite_num, sprite_height, attach))
                    # now write the sprite structures
                    # The 2 start words, write the height in rows into the sprite
                    # so the reader knows where the next sprite is
                    outfile.write(struct.pack('>H', sprite_height))  # vstart/hstart
                    outfile.write(struct.pack('>H', attach))  # vstop+control

                    num_rows = int(len(p0) / xparts)
                    for i in range(num_rows):
                        idx = i * xparts + xpos
                        outfile.write(struct.pack('>H', p0[idx]))
                        outfile.write(struct.pack('>H', p1[idx]))

                    # end-of-data
                    outfile.write(struct.pack('>H', 0))
                    outfile.write(struct.pack('>H', 0))

                    # next sprite
                    sprite_num += 1
                xpos += 1  # advance x position by 16 pixel in case the sprite is wide


def read_sprite_info(infile):
    byte_order = "big"
    version = ord(infile.read(1))
    flags = ord(infile.read(1))
    reserved1 = ord(infile.read(1))
    num_colors = ord(infile.read(1))
    num_sprites = int.from_bytes(infile.read(2), byteorder=byte_order)
    imgdata_size = int.from_bytes(infile.read(4), byteorder=byte_order)
    checksum = int.from_bytes(infile.read(2), byteorder=byte_order)
    return SpriteInfoHeader(version, flags, num_colors, num_sprites, imgdata_size)
