#!/usr/bin/env python3
import argparse


DESCRIPTION = """compute_lf.py - compute the LF byte for the blitter

This tool takes a logical term of A, B and C and computes and prints the LF
byte value for it"""

def parse_expression(s):
    return []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=DESCRIPTION)
    parser.add_argument("expr", help="logical expression")
    args = parser.parse_args()
    expr = parse_expression(args.expr)
