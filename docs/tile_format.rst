The Tiles File Format
=====================

Introduction
------------

One of the common tasks in game development is to arrange image files
into sets of rectangular areas, which are called **tiles**. Tiles are
generally used in classic 2D games, but even in modern 3D games,
a common task is still arranging two-dimensional textures into texture
atlasses in a similar fashion.

The RATR0 tiles format in its current form simply defines a regular
grid of rectangles on top of an image file. Since its initial and
primary target platform is the Commodore Amiga OCS (**O**\ riginal **C**\ hip **S**\ et)
hardware, the default settings of the :doc:`ratr0-maketiles <ratr0_maketiles>` utility
will generate image information that can be easily used on this platform.

However the file format was designed to be flexible enough to support a variety
of platforms and graphics technologies.

Specification
-------------

Header
~~~~~~

============== ============ ======================================================
Byte number(s) Name         Description
============== ============ ======================================================
0-7            ID           Always ``'RATR0TIL'``
8              version      file format version
9              flags        | bit 0: not set -> big endian, set -> little endian
                            | bit 1: not set -> 12 bit RGB, set -> 24 bit RGB
                            | bit 2: not set -> interleaved, set -> non-interleaved
                            | bit 3: not set -> no mask, set -> contains mask plane
10             reserved1    reserved byte, currently only used as padding
11             depth        image depth in number of bits
12-13          width        image width in pixels
14-15          height       image height in pixels
16-17          tile_size_h  horizontal tile size in pixels
18-19          tile_size_v  vertical tile size in pixels
20-21          num_tiles_h  number of tiles in horizontal direction
22-23          num_tiles_v  number of tiles in vertical direction
24-25          palette_size number of color entries in the palette
26-29          imgdata_size size of image data in bytes
30-31          checksum     checksum of the file (currently unused)
============== ============ ======================================================

Palette Data
~~~~~~~~~~~~

Following the file header is a block consisting of the palette entries.
If the colors are decoded in 12 bit (4 bit per color), this block will
have the size *(palette_size * 2)* bytes, if they are decoded as 1 byte
triplets per color (24 bit) the size of the block will be
*(palette_size * 3)* bytes

Image Data
~~~~~~~~~~

Immediately following the palette data is the image data encoding as
*depth* planes. This data is of the size *((width * height * depth) / 8)* bytes.
If bit 3 of flags is set, there will be an additional plane containing the
mask data, which is a bitwise "OR" of all the image bit planes
