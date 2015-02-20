#!/usr/bin/env python
# -*- coding: utf-8 -*-


import scipy.spatial.distance as ssd
import sys, os
import fortranformat as ff

import numpy as np

import argparse as ap

import xyzt


parser = ap.ArgumentParser(description="Determine maximum values along the axes to get box size")

parser.add_argument("Infile", help="XYZ file")
#, action=store_true)
#parser.add_argument("-e", "--elements", required=True, type=str, nargs="+", help="list of element labels and weights label weight label weight ...")
args = parser.parse_args()
#print args
#exit()


mx = 0.0
my = 0.0
mz = 0.0

px = 0.0
py = 0.0
pz = 0.0

def ReadXYZ(filename):
    
    mx = 0.0
    my = 0.0
    mz = 0.0

    px = 0.0
    py = 0.0
    pz = 0.0


    inf = open(filename)

    outarray = []
    for n, l in enumerate(inf):
        if n == 0:
            pass
        elif n==1:
            pass
        else:
            elem = l.strip().split()
            if len(elem) == 4:
                if float(elem[1]) < mx: mx = float(elem[1])
                elif float(elem[1]) > px: px = float(elem[1]) 

                if float(elem[2]) < my: my = float(elem[2])
                elif float(elem[2]) > py: py = float(elem[2])

                if float(elem[3]) < mz: mz = float(elem[3])
                elif float(elem[3]) > pz: pz = float(elem[3])

            else:
                raise IOError("Line " + str(n) + " in File " + filename + " : Malformed line. 4 fields (str, float, float, float) expected, " + len(elem) + " found.")
    inf.close()




    print "X: " + str(mx) + " - " + str(px) + " / " + str(abs(mx) + abs(px)) 
    print "Y: " + str(my) + " - " + str(py) + " / " + str(abs(my) + abs(py))
    print "Z: " + str(mz) + " - " + str(pz) + " / " + str(abs(mz) + abs(pz))


ReadXYZ(args.Infile)
