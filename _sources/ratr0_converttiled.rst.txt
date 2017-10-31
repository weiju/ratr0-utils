The ratr0-converttiled tool
===========================

`Tiled <http://www.mapeditor.org/>`_ is a powerful and popular open source level
editor. Rather than implementing its own level editor, the RATR0 engine relies
on Tiled to provide this critital functionality.

The ``ratr0-converttiled`` utility can be used to convert Tiled's JSON format
to into RATR0's level and tile file formats


You can see the tool's available options when you enter ``ratr0-converttiled -h``
at the command prompt:

.. highlight:: none

::

  usage: ratr0-converttiled [-h] [-ni] [-p24] [-fd FORCE_DEPTH] [-v]
                            tiles_json level_json tileout levelout

  convert_tiled.py - TilED Conversion tool

  This tool takes 2 TilED files in JSON format, 1 for the tile set and one
  for the level map and converts them to RATR0 tileset and level files.

  positional arguments:
    tiles_json            tiles (JSON) file
    level_json            level map (JSON) file
    tileout               output tile file
    levelout              output level file

  optional arguments:
    -h, --help            show this help message and exit
    -ni, --noninterleaved store data in interleaved manner
    -p24, --palette24     use a 24 bit palette instead of 12 bit
    -fd FORCE_DEPTH, --force_depth FORCE_DEPTH
                          set depth to a value greater or equal the input
                          image's value
    -v, --verbose         run in verbose mode


Parameters in detail
--------------------

``ratr0-converttiled`` expects at least these 4 arguments:

  * **tiles_json:** This is the file that Tiled uses to store a tile set. Please note
    that this file also includes a reference to the image file the tile set is based
    on, so that image file needs to be in the same place that Tiled would expect it
  * **level_json:** This is the file that Tiled uses to store a level.
  * **tileout:** This file will be created by the conversion tool to store the tile set
    in RATR0 tiles format.
  * **levelout:** This file will be created by the conversion tool to store the level data
    in RATR0 level format

In addition, you can specify the following optional arguments:

  * ``--non-interleaved`` or ``--ni``: the tile set's image information will be stored
    as non-interleaved bitplanes rather than interleaved bitplanes
  * ``--palette24`` or ``-p24``: The palette's color entries will be saved as 24 bit
    information (r, g, b triplets with a size of 8 bit each). By default, color entries
    are of size 16 bit that encodes a 12 bit color triplet, 4 bit for each color component
  * ``--force-depth`` or ``-fd``: This argument takes an additional parameter that specifies
    the actual number of bitplanes that will be generated in the tiles file. By this means
    you can force the converter into generating more bitplanes if the program requires it
