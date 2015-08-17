#!/usr/bin/env python
#*-* coding: utf-8 *-*

import argparse as ap
import xyzt
import sys 

parser = ap.ArgumentParser()

parser.add_argument("-i", "--input", help="Input file, xyz format", required=True)
parser.add_argument("-o", "--output", help="Output file, xyz format", required=True)
parser.add_argument("-f", "--frames", help="0-based indices of frames to filter out, in the given order", type=int, required=True, nargs='+')

args = parser.parse_args()

ensemblelist  = [{}] * len(args.frames)


xyz_iter =  xyzt.GetXYZIter(args.input)

print args

for n, ec in enumerate(xyz_iter):
    if n in args.frames:
        ensemblelist[args.frames.index(n)] = ec

    
        print ensemblelist
xyzt.Write_XYZ(ensemblelist, args.output , append=True)



