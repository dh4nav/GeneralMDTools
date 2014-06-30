#!/usr/bin/env python
# -*- coding: utf-8 -*-


import scipy.spatial.distance as ssd
import sys, os
import fortranformat as ff

import numpy as np

import argparse as ap

import xyzt


parser = ap.ArgumentParser(description="Convert a DLPOLY2/DLPOLY Classic REVCON or CONFIG file into a XYZ file")

parser.add_argument("Infile", help="XYZ file")
parser.add_argument("Outfile", help="Config file")

parser.add_argument("-b", "--box", type=float, help="box size in Angstöm")
#", required=True)

parser.add_argument("-r", "--readbox", type=bool) 
#, action=store_true)
#parser.add_argument("-e", "--elements", required=True, type=str, nargs="+", help="list of element labels and weights label weight label weight ...")
args = parser.parse_args()
#print args
#exit()

boxsize = 0.0

def write_file(name, data, box, weights=[], Format='config'):

    if Format == 'xyz'or Format == 'both':
        opf = open(name+".xyz", "w")
        opf.write(str(len(elements)) + "\n\n")

        for t in range(len(data)):
            opf.write(data[t] + " " + str(data[t][1][0]) + " " + str(data[t][1][1]) + " " + str(data[t][1][2]) + "\n")

        opf.close()

    if Format == "config" or Format == 'both':
        opf = open(name, "w")
        line1 = ff.FortranRecordWriter('(I10, I10, I10, F20.10)')
        line_cell = ff.FortranRecordWriter('(3F20.10)')
        line_atom1 = ff.FortranRecordWriter('(A8, I10)') #, F20.10)')
        line_atom2 = ff.FortranRecordWriter('(3F20.10)')

        opf.write("\n"+line1.write([0, 3, len(data), 0.0])+"\n")
        opf.write(line_cell.write([box, 0,0 ])+"\n")
        opf.write(line_cell.write([0, box, 0 ])+"\n")
        opf.write(line_cell.write([0, 0, box ])+"\n")

#       print coords

        for t in range(len(data)):
            opf.write(line_atom1.write([data[t][0], t+1])+"\n") #, float(weights[data[t][0]])])+"\n")
            opf.write(line_atom2.write([data[t][1][0], data[t][1][1], data[t][1][2] ])+"\n" )

        opf.close()

def ReadXYZ(filename):
    inf = open(filename)

    outarray = []
    for n, l in enumerate(inf):
        if n == 0:
            pass
        elif n==1:
            if args.readbox:
                boxsize = float(l,strip())
            else:
                pass
        else:
            elem = l.strip().split()
            if len(elem) == 4:
                outarray.append([elem[0], [float(elem[1]), float(elem[2]), float(elem[3])]])
#            elif len(elem) == 0:
#                pass
            else:
                raise IOError("Line " + str(n) + " in File " + filename + " : Malformed line. 4 fields (str, float, float, float) expected, " + len(elem) + " found.")
    inf.close()
    return outarray

xyz_iter =  xyzt.GetXYZIter(args.Infile)


for n, ec in enumerate(xyz_iter):


    if args.box != None:
        boxsize = args.box

    else:
        boxsize = ec['boxvector'][0]

    print ec
    data = zip(ec['elements'], ec['coordinates'])

    write_file(args.Outfile, data, boxsize) #, ElementDict)

