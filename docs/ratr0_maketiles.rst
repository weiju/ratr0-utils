The ratr0-maketiles tool
========================

This utility takes a PNG file and generates a RATR0 tiles file as specified
:doc:`here <tile_format>`.

You can see the tool's available options when you enter ``ratr0-maketiles -h``
at the command prompt:

.. highlight:: none

::

    usage: ratr0-maketiles [-h] [-ts TILE_SIZE] [-ni] [-p24] [-fd FORCE_DEPTH]
                           [-mf MASK_FILE] [-cm] [-v]
                           pngfile outfile

    make_tiles.py - Amiga Image Converter

    This tool converts a PNG image into a tile sheet file using parameters specified on the command line

    positional arguments:
      pngfile               input PNG file
      outfile               output tile sheet file

    optional arguments:
      -h, --help            show this help message and exit
      -ts TILE_SIZE, --tile_size TILE_SIZE
                            dimension of a tile, widthxheight
      -ni, --non_interleaved
                            store data in interleaved manner
      -p24, --palette24     use a 24 bit palette instead of 12 bit
      -fd FORCE_DEPTH, --force_depth FORCE_DEPTH
                            set depth to a value greater or equal the input
                            image's value
      -mf MASK_FILE, --mask_file MASK_FILE
                            writes a preview mask file in PNG format
      -cm, --create_mask    add a mask plane to the image data
      -v, --verbose         run in verbose mode

Parameters in detail
--------------------

``ratr0-maketiles`` expects at least these 2 arguments:

  * **pngfile:** This is the source image file in PNG format.
  * **outfile:** This file will be created by the conversion tool to store the tile set
    in RATR0 tiles format.

In addition, you can specify the following optional arguments:

  * ``--tile_size`` or ``--ts``: specify the size of a single tile in pixels. This takes
    an additional parameter of the form ``<width>x<height>``, for example ``16x16`` for
    a set of square-shaped tiles of 16 pixels. By default the tool will specify the
    entire image as a single tile.
  * ``--non-interleaved`` or ``--ni``: the tile set's image information will be stored
    as non-interleaved bitplanes rather than interleaved bitplanes
  * ``--palette24`` or ``-p24``: The palette's color entries will be saved as 24 bit
    information (r, g, b triplets with a size of 8 bit each). By default, color entries
    are of size 16 bit that encodes a 12 bit color triplet, 4 bit for each color component
  * ``--force-depth`` or ``-fd``: This argument takes an additional parameter that specifies
    the actual number of bitplanes that will be generated in the tiles file. By this means
    you can force the converter into generating more bitplanes if the program requires it
  * ``--create_mask`` or ``-cm``: Create an additional bit plane containing the bitwise "OR"
    of all the image bit planes. This mask plane can be used for Amiga Blitter operations
    with the "cookie cut", which allows for blits that treat color 0 as transparent.
  * ``--mask_file`` or ``-mf``: Writes a PNG file ``MASK_FILE`` that can be used to get an
    idea how the mask plane generated with ``--create_mask`` would look like.
