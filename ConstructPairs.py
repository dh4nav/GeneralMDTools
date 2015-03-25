#!/usr/bin/env python

import xyzt
import argparse as ap
import numpy as np


parser = ap.ArgumentParser(description="Generate RDF from pairs")
parser.add_argument("-i", "--input" , help="Input File, xyz", required=True)
parser.add_argument("-a", "--setaname" , help="Set A atom names", nargs="+")
parser.add_argument("-b", "--setbname", help="Set B atom names", nargs="+")
parser.add_argument("-m", "--setanum" , help="Set A atom indices, zero-based", nargs="+")
parser.add_argument("-n", "--setbnum", help="Set B atom indices, zero-based", nargs="+")
#parser.add_argument("-f", "--filter" , help="filter function", required=True)
args = parser.parse_args()

xyz_iter =  xyzt.GetXYZIter(args.input)

def filter(ec, seta, setb):
    outpairs = []

    for a in seta:
        for b in setb:
            if b != (a-1):
                outpairs.append(a)
                outpairs.append(b)

    return outpairs


seta = []
setb = []

if args.setanum:
    seta = args.setanum

if args.setbnum:
    setb = args.setbnum

frame = xyz_iter[0]

for n, e in enumerate(frame['elements']):
    if e in args.setaname:
        if n not in seta:
            seta.append(n)

    if e in args.setbname:
        if n not in setb:
            setb.append(n)

for v in filter(frame, seta, setb):
    print str(v) + " ",
