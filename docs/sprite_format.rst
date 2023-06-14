The Sprites File Format
=======================

Introduction
------------

**Sprites** are an important technology in game development. Since
the Amiga sprite hardware expects sprite data in a specific format
it is useful to arrange sprite sheet data in a format that requires
no or just minimal processing after it is loaded. Therefore the RATR0
utilities generate a separate file format for Amiga sprites to
help with this. In contrast to the tiles format the sprite format
is specifically tailored to Amiga sprites.

Specification
-------------

Header
~~~~~~

============== ============ ======================================================
Byte number(s) Name         Description
============== ============ ======================================================
0-7            ID           Always ``'RATR0SPR'``
8              version      file format version
9              flags        | bit 0: not set -> big endian, set -> little endian
10             reserved1    reserved byte, currently only used as padding
11             palette_size number of palette entries
12-13          num_sprites  number of sprites in the file
14-17          imgdata_size size of image data in bytes
18-19          checksum     checksum of the file (currently unused)
============== ============ ======================================================

Sprite Offset Data
~~~~~~~~~~~~~~~~~~

Following the file header are ``num_sprites`` 16 bit words of offset numbers which
represent the byte offsets where each sprite's data structure starts.

Palette Data
~~~~~~~~~~~~

Following the sprite offset data is a block consisting of the palette entries.
These are ``palette_size`` 16 bit words containing the RGB values of each entry.
Typically only the least significant 12 bits will be valid.

Sprite Data
~~~~~~~~~~~

Immediately following the palette data is the sprite data. The data is in the same
format as the Amiga sprite structure:

============== ======================================================
Word number(s) Description
============== ======================================================
0              Height of the Sprite
1              contains a set attachment bit if more than 4 colors
2-             height * 2 words of actual sprite image data
last 2 words   always 0 to denote the end of the sprite structure
============== ======================================================
