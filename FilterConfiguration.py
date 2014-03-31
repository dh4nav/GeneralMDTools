#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import xyzt 
import argparse as ap

parser = ap.ArgumentParser(description="Center a configuration in its bounding box and output minimum box dimensions")

parser.add_argument("-i", "--infile", help="XYZ input file")
parser.add_argument("-o", "--outfile", help="XYZ output file")
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-k", "--keep", help="Keep these atom types", nargs="+")
group1.add_argument("-r", "--remove", help="Remove these atom types", nargs="+")

args = parser.parse_args()
print args
xyz_in = xyzt.GetXYZIter(args.infile)

for ec in xyz_in:
    xyzt.Write_XYZ(xyzt.Filter(ec, remove=args.remove, keep=args.keep), args.outfile, append=True)

