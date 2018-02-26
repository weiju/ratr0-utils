#!/usr/bin/env python3

"""
A tool to get the information of a RATR0 file type
"""

RATR0_FILE_ID_LENGTH = 8


def print_tiles_info(infile):
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
    if flags & 0x04 == 4:
        interleaved = False
    else:
        interleaved = True

    reserved1 = infile.read(1)
    depth = ord(infile.read(1))

    width = int.from_bytes(infile.read(2), byteorder=byte_order)
    height = int.from_bytes(infile.read(2), byteorder=byte_order)

    tile_size_h = int.from_bytes(infile.read(2), byteorder=byte_order)
    tile_size_v = int.from_bytes(infile.read(2), byteorder=byte_order)
    num_tiles_h = int.from_bytes(infile.read(2), byteorder=byte_order)
    num_tiles_v = int.from_bytes(infile.read(2), byteorder=byte_order)
    palette_size = int.from_bytes(infile.read(2), byteorder=byte_order)
    reserved2 = infile.read(2)
    imgdata_size = int.from_bytes(infile.read(4), byteorder=byte_order)

    print("RATR0 Tile File")
    print("Version: %d" % version)
    print("Endianess: %s" % byte_order)
    print("RGB Format: %d" % rgb_format)
    print("Interleaved: %s" % str(interleaved))
    print("width: %d, height: %d" % (width, height))
    print("# bitplanes: %d" % depth)
    print("tile size: %dx%d" % (tile_size_h, tile_size_v))
    print("num tiles: %dx%d" % (num_tiles_h, num_tiles_v))
    print("num palette entries: %d" % palette_size)
    print("# image data bytes: %d" % imgdata_size)


def print_level_info(infile):
    version = ord(infile.read(1))
    flags = ord(infile.read(1))

    if flags & 0x01 == 1:
        big_endian = False
        byte_order = "little"
    else:
        big_endian = True
        byte_order = "big"

    width = int.from_bytes(infile.read(2), byteorder=byte_order)
    height = int.from_bytes(infile.read(2), byteorder=byte_order)
    vp_width = int.from_bytes(infile.read(2), byteorder=byte_order)
    vp_height = int.from_bytes(infile.read(2), byteorder=byte_order)
    init_vp_row = int.from_bytes(infile.read(2), byteorder=byte_order)
    init_vp_col = int.from_bytes(infile.read(2), byteorder=byte_order)

    print("RATR0 Level File")
    print("Version: %d" % version)
    print("Endianess: %s" % byte_order)
    print("size: %dx%d tiles" % (width, height))
    print("viewport size: %dx%d tiles" % (vp_width, vp_height))
    print("initial viewport pos: (%d, %d)" % (init_vp_col, init_vp_row))


def file_info(infile):
    """infile is a file object opened in binary mode"""
    fileid = infile.read(RATR0_FILE_ID_LENGTH).decode('utf-8')
    if fileid == "RATR0TIL":
        print_tiles_info(infile)
    elif fileid == "RATR0LVL":
        print_level_info(infile)
    else:
        print("unknown file type")
