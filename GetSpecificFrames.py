#!/usr/bin/env python
#*-* coding: utf-8 *-*

import argparse as ap
import xyzt
import sys 

parser = ap.ArgumentParser()

parser.add_argument("-i", "--input", help="Input file, xyz format", required=True)
parser.add_argument("-o", "--output", help="Output file, xyz format", required=True)
parser.add_argument("-f", "--frames", help="0-based indices of frames to filter out, in the given order", type=int, default=[], nargs='+')
parser.add_argument("-l", "--last", help="Get last frame", action="store_true", default=False)
args = parser.parse_args()

ensemblelist = []

if args.frames:
    ensemblelist  = [{}] * len(args.frames)


xyz_iter =  xyzt.GetXYZIter(args.input)

print args
ec = {}
n = 0

for n, ec in enumerate(xyz_iter):
    if n in args.frames:
        ensemblelist[args.frames.index(n)] = ec

    
        print ensemblelist
        print n

if args.last:
    if n not in args.frames:
        ensemblelist.append(ec)


xyzt.Write_XYZ(ensemblelist, args.output , append=True)



