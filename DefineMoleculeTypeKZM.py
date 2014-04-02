#!/usr/bin/python

import xyzt
import os, sys
import argparse as ap
import numpy as np

parser = ap.ArgumentParser(description = "Define molecule type - Dummy")

parser.add_argument("-i", "--infile",  help="infile, xyz format")

args = parser.parse_args()

frame = xyzt.Filter(xyzt.GetXYZIter(args.infile).get_last_frame(), keep=["NN"])

outstring = "1 " * len(frame['elements'])

print outstring
