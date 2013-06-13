#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, sys
import argparse as ap

parser = ap.ArgumentParser(description="Convert a DLPOLY2/DLPOLY Classic REVCON or CONFIG file into a XYZ file")

parser.add_argument("Infile", help="XYZ Input file")
parser.add_argument("Outfile", help="XYZ Output file")

parser.add_argument("-b", "--box", type=float, help="box size in Angstöms", required=True)
parser.add_argument("-x", "--xsize", type=int, default=1, help="multiply box this many times in x direction")
parser.add_argument("-y", "--ysize", type=int, default=1, help="multiply box this many times in y direction")
parser.add_argument("-z", "--zsize", type=int, default=1, help="multiply box this many times in z direction")

#parser.add_argument("-e", "--elements", required=True, type=str, nargs="+", help="list of element labels and weights label weight label weight ...")
args = parser.parse_args()
#print args
#exit()

def write_file(name, data, box, weights=[], Format='config'):

    if Format == 'xyz'or Format == 'both':
        opf = open(name, "w")
        opf.write(str(len(data)) + "\n" +str(box[0])+","+str(box[1])+","+str(box[2])+"\n")

        for n, t in enumerate(data):
            opf.write(t[0] + " " + str(t[1][0]) + " " + str(t[1][1]) + " " + str(t[1][2]) + "\n")

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

        for n,t in enumerate(data):
            opf.write(line_atom1.write([t[0], n+1])+"\n") #, float(weights[data[t][0]])])+"\n")
            opf.write(line_atom2.write([t[1][0], t[1][1],t[1][2] ])+"\n" )

        opf.close()

def ReadXYZ(filename):
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
                outarray.append([elem[0], [float(elem[1]), float(elem[2]), float(elem[3])]])
#            elif len(elem) == 0:
#                pass
            else:
                raise IOError("Line " + str(n) + " in File " + filename + " : Malformed line. 4 fields (str, float, float, float) expected, " + str(len(elem)) + " found.")
    inf.close()
    return outarray

def Shift(data, shiftvector):
    outdata = []
    for datapoint in data:
        outdata.append([datapoint[0], [datapoint[1][0]+shiftvector[0], datapoint[1][1]+shiftvector[1], datapoint[1][2]+shiftvector[2]]])
        #print(str([datapoint[0], datapoint[1]+shiftvector[0], datapoint[2]+shiftvector[1], datapoint[3]+shiftvector[2]]))
#        print datapoint
#    print outdata
#    exit()
    return outdata

if args.xsize < 1:
    raise ValueError("xsize is required to be a positive integer")
if args.ysize < 1:
    raise ValueError("ysize is required to be a positive integer")
if args.zsize < 1:
    raise ValueError("zsize is required to be a positive integer")


data = ReadXYZ(args.Infile)
#print data

extendeddata = []

#shift x

for shift in range(args.xsize):
    extendeddata.extend(Shift(data, [args.box*(float(shift)-(float(args.xsize-1)/2.0)), 0.0, 0.0]))

data = extendeddata
extendeddata = []

#shift y

for shift in range(args.ysize):
    extendeddata.extend(Shift(data, [0.0,args.box*( float(shift)-(float(args.ysize-1)/2.0)), 0.0]))

data = extendeddata
extendeddata = []

#shift z

for shift in range(args.zsize):
    extendeddata.extend(Shift(data, [0.0, 0.0, args.box*(float(shift)-(float(args.zsize-1)/2.0))]))

data = extendeddata

write_file(args.Outfile, data, [args.box*float(args.xsize), args.box*float(args.ysize),args.box*float(args.zsize)], weights=[], Format='xyz')


