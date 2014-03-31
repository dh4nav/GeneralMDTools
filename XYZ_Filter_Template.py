#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import xyzt 
import argparse as ap

parser = ap.ArgumentParser(description="Center a configuration in its bounding box and output minimum box dimensions")

parser.add_argument("-i", "--infile", help="XYZ input file")
parser.add_argument("-o", "--outfile", help="XYZ output file")

args = parser.parse_args()

xyz_in = xyzt.GetXYZIter(args.infile)

for ec in xyz_in:
    xyzt.Write_XYZ(ec, args.outfile, append=True)

