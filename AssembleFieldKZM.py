#!/usr/bin/env python

import xyzt
import os, sys
import argparse as ap
import numpy as np

parser = ap.ArgumentParser(description = "Assemble Field file")
parser.add_argument("-o", "--outfile", help="Outfile, xyz format")

parser.add_argument("-f", "--flags", nargs="+", help="Files, or format strings starting with %")

args = parser.parse_args()

pre = open("FIELDPre").readlines()
t0 = open("FIELD0").readlines()
t1 = open("FIELD1").readlines()
post = open("FIELDPost").readlines()

nummols = len(args.flags)

outfile = open(args.outfile, "w")


outfile.writelines(pre)
outfile.write("Molecules " + str(nummols) + "\n")
for f in args.flags:
    if f == "0":
        outfile.writelines(t0)
    else:
        outfile.writelienes(t1)
outfile.writelines(post)

outfile.close()

