#!/usr/bin/env python3

"""
Convert PNG image into a binary tile sheet file. A tile sheet file can be
used for all image assets in a game: level tiles, whole screens and BOB images.
The only condition is that the tiles in a sheet all have the same size.


A tile sheet file has this format:
flags:

bit 0: not set -> big endian, set -> little endian
bit 1: not set -> palette entry RGB components are 4 bit, encoded in 16 bit words high
                  nibble of first byte unused
       set -> palette entries are 24 bit
bit 2: not set -> interleaved format
       set -> non-interleaved
bit 3: not set -> no mask
       set -> contains mask plane

Header (32 bytes)

'RATR0TIL'     byte 0-7   identifier
version        byte 8     file format version
flags          byte 9     special flags
reserved1      byte 10    reserved, currently padding
bmdepth        byte 11    image depth in number of bits
width          byte 12-13 image width in pixels
height         byte 14-15 image height in pixels
tile_size_h    byte 16-17 tile size horizontally
tile_size_v    byte 18-19 tile size vertically
num_tiles_h    byte 20-21 number of tiles horizontally
num_tiles_v    byte 22-23 number of tiles vertically
palette_size   byte 24-25 number of color entries in the palette
imgdata_size   byte 26-29 size of image data
checksum       byte 30-31 checksum of the header (unused)

palette_data   byte 30-<30 + |size palette_data|>
image_data     <palette_data + |size palette_data|>
"""
from PIL import Image
import struct
import math
import sys
import os

from ratr0.util import png_util

FILE_FORMAT_VERSION = 2  # revised to be more compact


class TilesInfo:
    def __init__(self, version, flags, depth, width, height,
                 tile_size_h, tile_size_v, num_tiles_h, num_tiles_v,
                 palette_size, imgdata_size, checksum, palette=None, palette24=False):
        self.version = version
        self.flags = flags
        self.depth = depth
        self.width = width
        self.height = height
        self.tile_size_h = tile_size_h
        self.tile_size_v = tile_size_v
        self.num_tiles_h = num_tiles_h
        self.num_tiles_v = num_tiles_v
        self.palette_size = palette_size
        self.imgdata_size = imgdata_size
        self.checksum = checksum
        self.palette = palette
        self.palette24 = palette24

    def __str__(self):
        if self.flags & 0x01 == 1:
            big_endian = False
            byte_order = "little"
        else:
            big_endian = True
            byte_order = "big"
        if self.flags & 0x02 == 2:
            rgb_format = 24
        else:
            rgb_format = 12
        interleaved = self.flags & 0x04 == 0
        contains_mask = self.flags & 0x08 == 8

        out = "Version: %d\n" % self.version
        out += "Endianess: %s\n" % byte_order
        out += "RGB Format: %d\n" % rgb_format
        out += "Interleaved: %s\n" % str(interleaved)
        out += "Contains Mask: %s\n" % str(contains_mask)
        out += "width: %d, height: %d\n" % (self.width, self.height)
        out += "# bitplanes: %d\n" % self.depth
        out += "tile size: %dx%d\n" % (self.tile_size_h, self.tile_size_v)
        out += "num tiles: %dx%d\n" % (self.num_tiles_h, self.num_tiles_v)
        out += "# image data bytes: %d\n" % self.imgdata_size
        out += "# checksum: %d\n" % self.checksum

        if self.palette is not None:
            out += "Palette entries (%d):\n" % len(self.palette)
            for i, color in enumerate(self.palette):
                out += '%02d: %03x\n' % (i, color)
        return out

    def write(self, out):
        out.write(b'RATR0TIL')
        out.write(bytes([FILE_FORMAT_VERSION, self.flags, 0, self.depth]))

        # unsigned short = H, unsigned int = I
        # > = big endian, < = little endian
        out.write(struct.pack(">H", self.width))
        out.write(struct.pack(">H", self.height))
        out.write(struct.pack(">H", self.tile_size_h))
        out.write(struct.pack(">H", self.tile_size_v))
        out.write(struct.pack(">H", self.num_tiles_h))
        out.write(struct.pack(">H", self.num_tiles_v))
        out.write(struct.pack(">H", self.palette_size))
        out.write(struct.pack(">I", self.imgdata_size))
        out.write(struct.pack(">H", self.checksum))
        for color in self.palette:
            if self.palette24:
                out.write(bytes(color))
            else:
                out.write(struct.pack(">H", color))


def read_tiles_info(infile):
    version = ord(infile.read(1))
    flags = ord(infile.read(1))
    if flags & 0x01 == 1:
        big_endian = False
        byte_order = "little"
    else:
        big_endian = True
        byte_order = "big"
    if flags & 0x02 == 2:
        rgb_format = 24
    else:
        rgb_format = 12

    reserved1 = infile.read(1)
    depth = ord(infile.read(1))

    width = int.from_bytes(infile.read(2), byteorder=byte_order)
    height = int.from_bytes(infile.read(2), byteorder=byte_order)

    tile_size_h = int.from_bytes(infile.read(2), byteorder=byte_order)
    tile_size_v = int.from_bytes(infile.read(2), byteorder=byte_order)
    num_tiles_h = int.from_bytes(infile.read(2), byteorder=byte_order)
    num_tiles_v = int.from_bytes(infile.read(2), byteorder=byte_order)
    palette_size = int.from_bytes(infile.read(2), byteorder=byte_order)
    imgdata_size = int.from_bytes(infile.read(4), byteorder=byte_order)
    checksum = int.from_bytes(infile.read(2), byteorder=byte_order)
    # store the palette
    if rgb_format == 12:
        num_colors = 2**depth
        palette = []
        for i in range(num_colors):
            color = int.from_bytes(infile.read(2), byteorder=byte_order)
            color &= 0x0fff
            palette.append(color)
    else:
        print("24 bit palette, num palette entries: %d" % palette_size)
        palette = None


    return TilesInfo(version, flags, depth, width, height,
                     tile_size_h, tile_size_v, num_tiles_h, num_tiles_v,
                     palette_size, imgdata_size, checksum,
                     palette)


def write_planes_to_c(im, outfile, colors, non_interleaved, verbose, indent=4):
    """write tile file using the specifications"""
    depth = int(math.log2(len(colors)))
    planes, map_words_per_row = png_util.extract_planes(im, depth, verbose)
    print("#Planes: %d map words per row: %d" % (len(planes), map_words_per_row))
    with open(outfile, 'w') as out:
        out.write("UINT16 data[] = {\n")
        out_data = []
        if non_interleaved:
            for plane in planes:
                for word in plane:
                    out_data.append("0x%04x" % word)
        else:
            interleaved_data = png_util.interleave_planes(planes, map_words_per_row)
            for row in interleaved_data:
                for word in row:
                    out_data.append("0x%04x" % word)
        out_rows = png_util.chunks(out_data, map_words_per_row)
        for row in out_rows:
            out.write(" " * indent)
            out.write(", ".join(row))
            out.write(",\n")
        out.write("\n};\n")


def write_tiles(im, outfile, tile_size, colors, palette24,
                non_interleaved, create_mask, verbose):
    """write tile file using the specifications"""
    depth = int(math.log2(len(colors)))
    planes, map_words_per_row = png_util.extract_planes(im, depth, verbose)
    write_tile_file(outfile, im, tile_size, planes, colors, map_words_per_row,
                    palette24, non_interleaved, create_mask, verbose)


def write_tile_file(outfile, im, tile_size,
                    planes, colors, map_words_per_row,
                    palette24, non_interleaved, create_mask, verbose):
    checksum = 0  # TODO: add adler-32
    mask_depth = 0
    flags = 4 if non_interleaved else 0
    if palette24:
        flags |= 2
    else:
        # convert colors by or'ing them into a 12 bit value
        # this changes colors from a list of triples into a flat list
        colors = [(((r >> 4) & 0x0f) << 8) | (((g >> 4) & 0x0f) << 4) | ((b >> 4) & 0x0f)
                  for r, g, b in colors]
        #print(['%03x' % c for c in colors])

    palette_size = len(colors)
    depth = int(math.log2(palette_size))

    if create_mask:
        flags |= 8
        # if interleaved, mask depth is same as image depth
        mask_depth = 1 if non_interleaved else depth


    imgdata_size = map_words_per_row * 2 * im.height * (depth + mask_depth)
    tile_sheet_dim = (int(im.width / tile_size[0]), int(im.height / tile_size[1]))
    if verbose:
        print('tile size h: %d v: %d' % (tile_size[0], tile_size[1]))
        print('tile sheet width: %d height: %d' % (tile_sheet_dim[0], tile_sheet_dim[1]))

    # add an additional plane that merges down the 1 bits of the planes list
    if create_mask:
        mask_plane = [0] * len(planes[0])
        for i in range(len(mask_plane)):
            w = 0
            for plane in planes:
                w |= plane[i]
            mask_plane[i] = w

    with open(outfile, 'wb') as out:
        tiles_info = TilesInfo(FILE_FORMAT_VERSION, flags,
                               depth, im.width, im.height,
                               tile_size[0], tile_size[1],
                               tile_sheet_dim[0], tile_sheet_dim[1],
                               palette_size, imgdata_size, checksum,
                               colors)
        tiles_info.write(out)
        if non_interleaved:
            planes.append(mask_plane)
            for plane in planes:
                for word in plane:
                    out.write(struct.pack(">H", word))
        else:
            interleaved_data = png_util.interleave_planes(planes, map_words_per_row)
            for row in interleaved_data:
                for word in row:
                    out.write(struct.pack(">H", word))
            if create_mask:
                # interleaved mask
                # we need to multiply the mask plane data
                mask_planes = [mask_plane for i in range(depth)]
                interleaved_mask = png_util.interleave_planes(mask_planes, map_words_per_row)
                for row in interleaved_mask:
                    for word in row:
                        out.write(struct.pack(">H", word))


def setornot(v):
    return 1 if v > 0 else 0


def write_mask(outfile, im, tile_size, depth,
               palette24,
               non_interleaved, verbose):
    """Write a preview mask in png format, as a quick visual control"""
    # Non-interleaved: just write one bitplane at the end
    if non_interleaved:
        colors = [setornot(c) for c in im.getdata()]
        mask_img = Image.new(mode="1", size=im.size)
        mask_img.putdata(colors)
        # write a debug PNG file as visual control
        mask_img.save(outfile)
    else:
        # interleaved: duplicate each row times the depth
        colors = [setornot(c) for c in im.getdata()]
        color_rows = list(png_util.chunks(colors, im.width))
        final_colors = []
        for row in color_rows:
            new_row = row * depth
            final_colors.extend(row * depth)
        mask_img = Image.new(mode="1", size=(im.width, im.height * depth))
        mask_img.putdata(final_colors)
        # write a debug PNG file as visual control
        mask_img.save(outfile)
