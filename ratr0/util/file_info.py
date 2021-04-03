#!/usr/bin/env python3

"""
A tool to get the information of a RATR0 file type
"""
from . import tiles, sprites

RATR0_FILE_ID_LENGTH = 8


def print_tiles_info(infile):
    tiles_info = tiles.read_tiles_info(infile)
    print("RATR0 Tile File")
    print(tiles_info)


def print_sprite_info(infile):
    sprite_info = sprites.read_sprite_info(infile)
    print("RATR0 Sprite File")
    print(sprite_info)
    for i in range(sprite_info.num_sprites):
        spr_offset = int.from_bytes(infile.read(2), byteorder="big")
        print("Sprite %d, offset: %d" % (i, spr_offset))


class LevelInfo:

    def __init__(self, version, flags, width, height):
        self.version = version
        self.flags = flags
        self.width = width
        self.height = height

    def __str__(self):
        if self.flags & 0x01 == 1:
            big_endian = False
            byte_order = "little"
        else:
            big_endian = True
            byte_order = "big"

        out = "Version: %d\n" % self.version
        out += "Endianess: %s\n" % byte_order
        out += "size: %dx%d tiles\n" % (self.width, self.height)
        return out


def read_level_info(infile):
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
    return LevelInfo(version, flags, width, height)


def print_level_info(infile):
    level_info = read_level_info(infile)
    print("RATR0 Level File")
    print(level_info)


def file_info(infile):
    """infile is a file object opened in binary mode"""
    fileid = infile.read(RATR0_FILE_ID_LENGTH).decode('utf-8')
    if fileid == "RATR0TIL":
        print_tiles_info(infile)
    elif fileid == "RATR0LVL":
        print_level_info(infile)
    elif fileid == "RATR0SPR":
        print_sprite_info(infile)
    else:
        print("unknown file type")
