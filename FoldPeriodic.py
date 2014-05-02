#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

import argparse as ap

parser = ap.ArgumentParser(description="Correct periodic boundary folding")

parser.add_argument("Infile", help="XYZ input file")
parser.add_argument("Outfile", help="XYZ output file")

parser.add_argument("-b", "--box", default=0.0, type=float, help="box size in Angstöms. If not given, box size is read from the XYZ comment line")
parser.add_argument("-s", "--size", type=int, help="Molecule size in number of atoms (ex: H2O -> 3)", required=True)
args = parser.parse_args()


def ReadXYZ(filename):
    inputfile = open(filename, "r")
    outputdata = []
    trajectorylength = 0

    for num , line in enumerate(inputfile):
        if num == 0:
            trajectorylength = int(line.strip())+2
            outputdata.append([])
        elif num == 1:
            outputdata[-1].append(line)
        elif (num%trajectorylength) == 0:
            trajectorylength = int(line.strip())+2
            outputdata.append([])
        elif (num%trajectorylength) == 1:
            outputdata[-1].append(float(line))
        else:
            linebits = line.strip().split()
            outputdata[-1].append([linebits[0], float(linebits[1]), float(linebits[2]), float(linebits[3])])

    return outputdata

print args

print "read"
od = ReadXYZ(args.Infile)


#print od


fd = []

print "fold"
for t in od:
    fd.append([])
    traj = t[1:]
    if args.box != None:
        boxsizehalf = args.box/2
    else:
        boxsizehalf = float(t[0])/2.0
    print boxsizehalf
    #firstatom = traj[0]
    #print firstatom

    #fd[-1].append(traj[0])

    for n, a in enumerate(traj):
        if (n%args.size) == 0:
            firstatom = a
        fd[-1].append(a)

        if (a[1] - firstatom[1]) > boxsizehalf:
            fd[-1][-1][1] = a[1] - (2.0 * boxsizehalf)
        elif (a[1] - firstatom[1]) < (-1.0 * boxsizehalf):
            fd[-1][-1][1] = a[1] + (2.0 * boxsizehalf)

        if (a[2] - firstatom[2]) > boxsizehalf:
            fd[-1][-1][2] = a[2] - (2.0 * boxsizehalf)
        elif (a[2] - firstatom[2]) < (-1.0 * boxsizehalf):
            fd[-1][-1][2] = a[2] + (2.0 * boxsizehalf)

        if (a[3] - firstatom[3]) > boxsizehalf:
            fd[-1][-1][3] = a[3] - (2.0 * boxsizehalf)
        elif (a[3] - firstatom[3]) < (-1.0 * boxsizehalf):
            fd[-1][-1][3] = a[3] + (2.0 * boxsizehalf)

#print fd

print "write"
opf = open(args.Outfile, "w")
for traj in fd:
    opf.write(str(len(traj))+"\n \n")
    for a in traj:
        opf.write(a[0] + " " + str(a[1]) + " " + str(a[2]) + " " + str(a[3]) + "\n")
opf.close()
