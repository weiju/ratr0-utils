The Level File Format
=====================

Introduction
------------

This file format is used to specify level maps in tile-based 2D games.


Specification
-------------

Header
~~~~~~

============== ============ ======================================================
Byte number(s) Name         Description
============== ============ ======================================================
0-7            ID           Always ``'RATR0LVL'``
8              version      file format version
9              flags        special flags
10-11          width        level width in tiles
12-13          height       level height in tiles
14-15          vp_width     viewport width in tiles
16-17          vp_height    viewport height in tiles
18-19          init_vp_row  initial row position for viewport
20-21          init_vp_col  initial column position for viewport
22-23          reserved     reserved, currently only padding
24-27          checksum     checksum of the entire file
============== ============ ======================================================

Level Data
~~~~~~~~~~

The level data immediately follows the file header. Essentially, this encodes
*(width * height)* pairs of 16 bit integers that are horizontal and vertical
indexes into a tiles map.

