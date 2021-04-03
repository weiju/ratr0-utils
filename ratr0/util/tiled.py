#!/usr/bin/env python3
"""iled.py - TilED conversion tool

TilED is a great cross-platform tool to create level data. This conversion
tool converts the JSON data from TilED to generate level data for the
RATR0 engine.
"""
import json
import os
from PIL import Image

from ratr0.util import tiles, levels, png_util


def convert_tiles(intiles, indir, outfile, non_interleaved,
                  palette24, force_depth, verbose):
    imagepath = os.path.join(indir, intiles["image"])
    tile_width = intiles['tilewidth']
    tile_height = intiles['tileheight']
    im = Image.open(imagepath)
    colors = png_util.make_colors(im, force_depth, verbose)
    tiles.write_tiles(im, outfile, [tile_width, tile_height], colors,
                      palette24=palette24,
                      non_interleaved=non_interleaved,
                      create_mask=False,
                      verbose=verbose)


def convert_level(inlevel, outfile, verbose):
    if len(inlevel["layers"]) > 1:
        print("Warning: currently only a single layer is supported")
    inmap = inlevel["layers"][0]
    inmap_data = inmap["data"]

    ratr0_level = {
        "name": "level",
        "viewport": {
            "x": 0, "y": 0,
            "width": inmap["width"],
            "height": inmap["height"]
        },
        "width": inlevel['width'],
        "height": inlevel['height'],
        "map": inmap_data
    }
    levels.write_level(ratr0_level, outfile, verbose)
