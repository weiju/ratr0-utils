#!/usr/bin/env python3

import os

STD_VARS = {
    # Registers
    "FMODE": 0x1fc,
    "DIWSTRT": 0x08e, "DIWSTOP": 0x090,
    "DDFSTRT": 0x092, "DDFSTOP": 0x094, "DMACON": 0x096,

    "BPL1PTH": 0x0e0, "BPL1PTL": 0x0e2, "BPL2PTH": 0x0e4, "BPL2PTL": 0x0e6,
    "BPL3PTH": 0x0e8, "BPL3PTL": 0x0ea, "BPL4PTH": 0x0ec, "BPL4PTL": 0x0ee,
    "BPL5PTH": 0x0f0, "BPL5PTL": 0x0f2, "BPL6PTH": 0x0f4, "BPL6PTL": 0x0f6,

    "BPLCON0": 0x100, "BPLCON1": 0x102, "BPLCON2": 0x104,
    "BPL1MOD": 0x108, "BPL2MOD": 0x10a,
    "SPR0PTH": 0x120, "SPR0PTL": 0x122, "SPR1PTH": 0x124, "SPR1PTL": 0x126,
    "SPR2PTH": 0x128, "SPR2PTL": 0x12a, "SPR3PTH": 0x12c, "SPR3PTL": 0x12e,
    "SPR4PTH": 0x130, "SPR4PTL": 0x132, "SPR5PTH": 0x134, "SPR5PTL": 0x136,
    "SPR6PTH": 0x138, "SPR6PTL": 0x13a, "SPR7PTH": 0x13c, "SPR7PTL": 0x13e,

    "COLOR00": 0x180, "COLOR01": 0x182, "COLOR02": 0x184, "COLOR03": 0x186,
    "COLOR04": 0x188, "COLOR05": 0x18a, "COLOR06": 0x18c, "COLOR07": 0x18e,
    "COLOR08": 0x190, "COLOR09": 0x192, "COLOR10": 0x194, "COLOR11": 0x196,
    "COLOR12": 0x198, "COLOR13": 0x19a, "COLOR14": 0x19c, "COLOR15": 0x19e,
    "COLOR16": 0x1a0, "COLOR17": 0x1a2, "COLOR18": 0x1a4, "COLOR19": 0x1a6,
    "COLOR20": 0x1a8, "COLOR21": 0x1aa, "COLOR22": 0x1ac, "COLOR23": 0x1ae,
    "COLOR24": 0x1b0, "COLOR25": 0x1b2, "COLOR26": 0x1b4, "COLOR27": 0x1b6,
    "COLOR28": 0x1b8, "COLOR29": 0x1ba, "COLOR30": 0x1bc, "COLOR31": 0x1be,

    # Values
    "DDFSTRT_VALUE_320": 0x0038, "DDFSTOP_VALUE_320": 0x00d0,
    "DIWSTRT_VALUE_320": 0x2c81, "DIWSTOP_VALUE_PAL_320": 0x2cc1,
}

def parse_int(s):
    return int(s, 0)


def compile_cmove(result, args):
    dest = args[0]
    value = args[1]
    try:
        dest = parse_int(dest)
    except ValueError:
        dest = STD_VARS[dest]
    try:
        value = parse_int(value)
    except:
        value = STD_VARS[value]
    result.extend([dest, value])

def compile_cwait(result, args):
    x = parse_int(args[0])
    y = parse_int(args[1])
    # convert to bit mask
    first_word = (y << 8) | (x << 1) | 1

    # TODO: 1. add optional masks for x and y positions
    # 2. add blitter wait enable
    second_word = 0xfffe
    result.extend([first_word, second_word])


def compile_clist(inpath):
    result = []
    indexes = {}
    list_index = 0
    with open(inpath, 'r') as infile:
        for line in infile:
            line = line.strip()
            # comment or empty line
            if len(line) == 0 or line.startswith('#'):
                continue
            comps = line.split()
            if comps[0] == 'CMOVE':
                compile_cmove(result, comps[1].split(","))
                list_index += 2
            elif comps[0] == 'CWAIT':
                compile_cwait(result, comps[1].split(","))
                list_index += 2
            elif comps[0] == 'CEND':
                result.extend([0xffff, 0xfffe])
            elif comps[0].endswith(":"):
                label = comps[0][:-1]
                indexes[label] = list_index
            else:
                raise Exception("can't recognize instruction: '%s'" % comps[0])
    return result, indexes


def write_clist(clist, indexes, outfile):
    src_file = os.path.basename(outfile)
    print("Writing %s" % src_file)
    header_file = src_file.replace(".c", ".h")
    parent_dir = os.path.dirname(outfile)
    print("Header %s" % os.path.join(parent_dir, header_file))

    with open(os.path.join(parent_dir, header_file), "w") as out:
        out.write("#pragma once\n")
        out.write("#ifndef __COPPER__\n")
        out.write("#define __COPPER__\n")

        for label, index in indexes.items():
            out.write("#define %s (%d)\n" % (label, index))

        out.write("#endif /* __COPPER__ */\n")

    out_values = ["0x%03x" % value for value in clist]
    with open(outfile, "w") as out:
        out.write("#include <ratr0/data_types.h>\n\n")
        out.write("\nUINT16 __chip clist[] = {\n")
        out.write("\t%s\n" % ', '.join(out_values))
        out.write("};\n")
