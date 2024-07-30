The ratr0-makesprites tool
==========================

This utility takes a PNG file and generates either C source file or
a RATR0 sprites file as specified
:doc:`here <sprite_format>`.

You can see the tool's available options when you enter ``ratr0-makesprites -h``
at the command prompt:

.. highlight:: none

::

    usage: ratr0-makesprites [-h] [--generatec] [-v] pngfile outfile

    ratr0-makesprites - Amiga Sprite Sheet generator

    This tool converts a PNG image into a sprite sheet file using parameters specified on the command line

    positional arguments:
      pngfile        input PNG file
      outfile        output sprite sheet file

    optional arguments:
      -h, --help     show this help message and exit
      --generatec    generate a C source file instead of a sprite file
      -v, --verbose  run in verbose mode


Parameters in detail
--------------------

``ratr0-makesprites`` expects at least these 2 arguments:

  * **pngfile:** This is the source image file in PNG format.
  * **outfile:** This file will be created by the conversion tool to store a sprite sheet
    in RATR0 sprites format.

In addition, you can specify the following optional arguments:

  * ``--generatec``: instead of a RATR0 sprite file a C source code file will be generated. This
    can be useful for debugging or smaller programs.

Creating more than one sprite
-----------------------------

We can use ``ratr0-makesprites`` to create more than one sprite frame in a
sprite file. To do this, we design the source image so that the sprite
frames are laid out in a horizontal manner. By default this tool assumes
a sprite width of 16 pixels, so if the source image has a width that is
a true multiple of 16, it will automatically create new sprite frames
in the output file that are appended at the end.
