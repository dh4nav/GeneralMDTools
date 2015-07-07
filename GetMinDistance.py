#!/usr/bin/env python
#*-* coding: utf-8 *-*

import argparse as ap
import xyzt
import sys 
import numpy as np
parser = ap.ArgumentParser()

parser.add_argument("-i", "--input", help="Input file, xyz format", required=True)
parser.add_argument("-o", "--output", help="Output file, text format. Contains frame numbers with hits", required=True)
parser.add_argument("-g1", "--group1", help="Elements in group 1", required=True, nargs="+")
parser.add_argument("-g2", "--group2", help="Elements in group 2. May overlap with group 1. Defaults to group 1.", nargs="+")
parser.add_argument("-d", "--distance", type=float, help="Distanc threshold", required=True)

args = parser.parse_args()

args.group2 = args.group2 if args.group2 else args.group1

xyz_iter =  xyzt.GetXYZIter(args.input)

print args

opf = open(args.output, "w")

for n, ec in enumerate(xyz_iter):
    distlist= np.ndarray.flatten(xyzt.GetDistsDiff(ec, ec))
#    print distlist
    distlist = distlist[distlist > 0.1]
#    print distlist
    distlist = distlist[distlist < args.distance]
#    print distlist
    if len(distlist):
        opf.write(str(n) + " " + str(len(distlist)/2) + "\n")



