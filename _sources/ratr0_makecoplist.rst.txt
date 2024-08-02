The ratr0-makecoplist tool
==========================

This utility takes a file representing a textual Amiga Copper list
description and generates a C source file and accompanying header file.

You can see the tool's available options when you enter ``ratr0-makecoplist -h``
at the command prompt:

.. highlight:: none

::

    usage: ratr0-makecoplist [-h] [--listname LISTNAME] infile outfile

    ratr0-makecoplist - RATR0 copper list compiler

    This tool turns a textual Copper list description into a
    byte array in C.

    positional arguments:
      infile         input copper list file
      outfile        output C source file

    optional arguments:
      -h, --help     show this help message and exit
      --listname     unique name of copper list within your project


Parameters in detail
--------------------

``ratr0-makecoplist`` expects at least these 2 arguments:

  * **infile:** This is the source copper list file.
  * **outfile:** This file will be created by the conversion tool to represent the copper list as a C source file.

Copper list format
------------------

The format of a copper list is hopefully intuitive enough for people with
some basic knowledge of copper list programming.

There are these basic commands

  * ``MOVE <dest>,<value>``: move a value to the destination address
  * ``WAIT <hpos>,<vpos>[,hmask=<mask>|vmask=<mask>|BLTWAIT]*``
  * ``SKIP <hpos>,<vpos>[,hmask=<mask>|vmask=<mask>|BLTWAIT]*``
  * ``END``: end of copper list

*Remarks about argument lists*

In comma-separated arguments, there should be no spaces before the comma.
Numeric values can either be specified in decimal or hexadecimal form.
Hexadecimal values are prefixed with ``0x``.

There are also a few predefined values, e.g. register names or constants
that can be used to set standard values for DMA and display window limits.

E.g. you can use all standard names for custom chip registers (``BPLCON0``,
``COLOR00``, ...), or predefined constants

  * ``DDFSTRT_VALUE_320``
  * ``DDFSTOP_VALUE_320``
  * ``DIWSTRT_VALUE_320``
  * ``DIWSTOP_VALUE_PAL_320``



*Comments*

Comment lines are supported. A comment line starts with the ``#`` character.

*Index labels*

Index labels are markers that will generate helpful indexes to aid with
replacing values in the copper list at run time.

Example list:
-------------

::

 # Default RATR0 copper list for 320x256 PAL display
    MOVE   FMODE,0
    MOVE   DDFSTRT,DDFSTRT_VALUE_320
    MOVE   DDFSTOP,DDFSTOP_VALUE_320
    MOVE   DIWSTRT,DIWSTRT_VALUE_320
    MOVE   DIWSTOP,DIWSTOP_VALUE_PAL_320
 BPLCON0_INDEX:
    MOVE  BPLCON0,0
    MOVE  BPLCON2,0x060
 BPL1MOD_INDEX:
    MOVE  BPL1MOD,0
    MOVE  BPL2MOD,0
 BPL1PTH_INDEX:
    MOVE  BPL1PTH,0
    MOVE  BPL1PTL,0
    MOVE  BPL2PTH,0
    MOVE  BPL2PTL,0
    MOVE  BPL3PTH,0
    MOVE  BPL3PTL,0
    MOVE  BPL4PTH,0
    MOVE  BPL4PTL,0
    MOVE  BPL5PTH,0
    MOVE  BPL5PTL,0
    MOVE  BPL6PTH,0
    MOVE  BPL6PTL,0
    ...

    END
