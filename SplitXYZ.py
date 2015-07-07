#!/usr/bin/env python
#*-* coding: utf-8 *-*

import argparse as ap
import xyzt
import sys 

parser = ap.ArgumentParser()

parser.add_argument("-i", "--input", help="Input file, xyz format", required=True)
parser.add_argument("-o", "--output", help="Output file, xyz format", required=True)
parser.add_argument("-l", "--length", help="chunk size", type=int)

args = parser.parse_args()

xyz_iter =  xyzt.GetXYZIter(args.input)

print args

for n, ec in enumerate(xyz_iter):
    #print n
    #print xyzt.Filter(ec, keep=args.keep, remove=args.remove)
    #print xyzt.filter(ec, keep=args.keep, remove=args.remove)
    #exit()
    xyzt.Write_XYZ(ec, args.output + "p" + str(n/args.length) + ".xyz", append=True)



