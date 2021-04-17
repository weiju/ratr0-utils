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
9              flags        | bit 0: not set -> big endian, set -> little endian
                            | rest: currently unused
10-11          width        level width in tiles
12-13          height       level height in tiles
14-15          checksum     checksum of the entire file
============== ============ ======================================================

Level Data
~~~~~~~~~~

The level data immediately follows the file header. Essentially, this encodes
*(width * height)* unsigned 8 bit values that are the 1-based tile number.

