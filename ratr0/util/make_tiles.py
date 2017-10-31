#!/usr/bin/env python3

"""
Convert PNG image into a binary tile sheet file. A tile sheet file can be
used for all image assets in a game: level tiles, whole screens and sprite images.
The only condition is that the tiles in a sheet all have the same size.


A tile sheet file has this format:
flags:

bit 0: not set -> big endian, set -> little endian
bit 1: not set -> palette entry RGB components are 4 bit, encoded in 16 bit words high
                  nibble of first byte unused
       set -> palette entries are 24 bit
bit 2: not set -> interleaved format
       set -> non-interleaved

Header (36 bytes)

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
reserved2      byte 26-27 reserved, currently padding
imgdata_size   byte 28-31 size of image data
checksum       byte 32-36 checksum of the entire file

palette_data   byte 36-<36 + |size palette_data|>
image_data     <palette_data + |size palette_data|>

For license, see gpl-3.0.txt
"""
from PIL import Image
import struct
import math
import sys
import os

from ratr0.util import png_util

FILE_FORMAT_VERSION = 1

def make_colors(im, force_depth, verbose):
    if im.palette is not None:
        palette_bytes = list(im.palette.palette) if im.palette.rawmode else im.palette.tobytes()
        colors = [i for i in png_util.chunks([b for b in palette_bytes], 3)]
        depth =  round(math.log(len(colors), 2))
    else:
        colors = [[0, 0, 0], [255, 255, 255]]
        depth = 1

    if verbose:
        print("input image depth: %d" % depth)

    if depth == 0:
        raise Exception("images with only 1 color can't be handled")
    elif force_depth is not None:
        if force_depth < depth:
            raise Exception('force_depth must be greater or equal actual depth !')
        if verbose:
            print('overriding input depth (%d) with %d' % (depth, force_depth))
        depth = force_depth
    num_missing_colors = 2 ** depth - len(colors)

    if verbose:
        print('adding %d missing colors' % num_missing_colors)
    colors += [[0, 0, 0]] * num_missing_colors
    return colors


def write_tiles(im, outfile, tile_size, colors, palette24,
                force_depth, non_interleaved, verbose):
    """write tile file using the specifications"""
    depth = int(math.log2(len(colors)))
    planes, map_words_per_row = png_util.extract_planes(im, depth, verbose)
    write_tile_file(outfile, im, tile_size, planes, colors, map_words_per_row,
                    palette24, non_interleaved, verbose)


def write_tile_file(outfile, im, tile_size,
                    planes, colors, map_words_per_row,
                    palette24, non_interleaved, verbose):
    checksum = 0  # TODO: add adler-32
    flags = 4 if non_interleaved else 0
    if palette24:
        flags |= 2
    else:
        # convert colors by or'ing them into a 12 bit value
        # this changes colors from a list of triples into a flat list
        colors = [(((r >> 4) & 0x0f) << 8) | (((g >> 4) & 0x0f) << 4) | ((b >> 4) & 0x0f)
                  for r, g, b in colors]

    palette_size = len(colors)
    depth = int(math.log2(palette_size))
    imgdata_size = map_words_per_row * 2 * im.height * depth
    tile_sheet_dim = (int(im.width / tile_size[0]), int(im.height / tile_size[1]))
    if verbose:
        print('tile size h: %d v: %d' % (tile_size[0], tile_size[1]))
        print('tile sheet width: %d height: %d' % (tile_sheet_dim[0], tile_sheet_dim[1]))

    with open(outfile, 'wb') as out:
        out.write(b'RATR0TIL')
        out.write(bytes([FILE_FORMAT_VERSION, flags, 0, depth]))
        # unsigned short = H, unsigned int = I
        # > = big endian, < = little endian
        out.write(struct.pack(">H", im.width))
        out.write(struct.pack(">H", im.height))
        out.write(struct.pack(">H", tile_size[0]))
        out.write(struct.pack(">H", tile_size[1]))
        out.write(struct.pack(">H", tile_sheet_dim[0]))
        out.write(struct.pack(">H", tile_sheet_dim[1]))
        out.write(struct.pack(">H", palette_size))
        out.write(struct.pack(">H", 0))  # reserved2
        out.write(struct.pack(">I", imgdata_size))
        out.write(struct.pack(">I", checksum))
        for color in colors:
            if palette24:
                out.write(bytes(color))
            else:
                out.write(struct.pack(">H", color))

        if non_interleaved:
            for plane in planes:
                for word in plane:
                    out.write(struct.pack(">H", word))
        else:
            interleaved_data = png_util.interleave_planes(planes, map_words_per_row)
            for row in interleaved_data:
                for word in row:
                    out.write(struct.pack(">H", word))


def setornot(v):
    return 1 if v > 0 else 0


def write_mask(outfile, im, tile_size, depth,
               non_interleaved, verbose):
    colors = [setornot(c) for c in im.getdata()]
    mask_img = Image.new(mode="1", size=im.size)
    mask_img.putdata(colors)

    # workaround to fix a strange bug when calling write_files()
    # is called directly, so we save it as a PNG first and
    # call write_tiles() on the PNG file
    mask_img.save("tmp_mask.png")
    mask_img = Image.open('tmp_mask.png')
    mask_colors = make_colors(mask_img, depth, verbose)
    write_tiles(mask_img, outfile, tile_size, mask_colors,
                force_depth=depth,
                non_interleaved=non_interleaved, verbose=verbose)
