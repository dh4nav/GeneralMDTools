#!/usr/bin/env python

# -*- coding: utf-8 *-*

import os, sys

import argparse as ap

parser = ap.ArgumentParser(description="Convert from DLPOLY 2/DLPOLY Classic HISTORY to a XYZ format")

parser.add_argument("-i", "--history", help="HISTORY file name")
parser.add_argument("-o", "--xyz", help="XYZ file name")
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-k", "--keepcomment", help="keep comment line from REVCON or CONFIG file", action="store_true")
group1.add_argument("-c", "--setcomment", metavar="COMMENT", help="set comment line")
group1.add_argument("-b", "--boxcomment", action="store_true", help="set comment line to box x size")
parser.add_argument("-s", "--split", help="split into separate files for each timestep", action="store_true")
parser.add_argument("-v", "--verbose", help="print progress", action="store_true")
parser.add_argument("-d", "--debug", help="debug output", action="store_true")
parser.add_argument("-n", "--noheader", help="missing history file header, file starts with timestep line. Useful for partial files", action="store_true")
parser.add_argument("-V", "--velocity", help="Read velocity data were available, insert a zero vector if not available", action="store_true")
parser.add_argument("-F", "--force", help="Read force data where available, insert a zero vector if not available", action="store_true")
parser.add_argument("-M", "--mass", help="Read atomic mass data where available, insert one if not available", action="store_true")
parser.add_argument("-C", "--charge", help="Read atomic charge, insert 0 if not available", action="store_true")
args = parser.parse_args()

elements = []
coordinates = []
velocities = []
forces = []
masses = []
charge = []
boxes = []
timesteps = []
comment = ""
timestep = 0

linenum = -2

if args.noheader:
    linenum = 0

typekey = 0
boxkey = 0
tscounter = 0
stepcounter = 0
numlines = -10

element = ""
charge = 0.0
mass = 1.0
pos = "0.0, 0.0, 0.0"
vel = "0.0, 0.0, 0.0"
force = "0.0, 0.0, 0.0"

globallinenum = 0

lastelement = ""

framecounter = 0

inf = open(args.history, "r")
opf = open(args.xyz, "w")

try:
    for n,l in enumerate(inf):
        if l.find("timestep") != -1:
            if args.verbose:
                framecounter += 1
                if (framecounter%1000 == 0):
                    print framecounter

            typekey = int(l.split()[3].strip())
            boxkey = int(l.split()[4].strip())
            numlines = int(l.split()[2].strip()) * (typekey + 2)
            if boxkey != 0:
                numlines += 3
            tscounter = 0
            opf.write(l.split()[2].strip() + "\n")

        elif (boxkey > 0) and (tscounter < 4):
            if tscounter == 1:
                opf.write( l.split()[0].strip() + "\n")

        elif tscounter <= numlines:
            if(tscounter % (typekey + 2)) == 0:
                element = l.split()[0].strip()
                mass = l.split()[2].strip()
                charge = l.split()[3].strip()
                vel = "0.0, 0.0, 0.0"
                force = "0.0, 0.0, 0.0"
            elif(tscounter % (typekey + 2)) == 1:
                pos = l.strip()
            elif(tscounter % (typekey + 2)) == 2:
                vel = l.strip()
            elif(tscounter % (typekey + 2)) == 3:
                force = l.strip()

            if (tscounter % (typekey + 2)) == (typekey + 1):
                if args.force:
                    opf.write(element + " " + pos + " " + mass + " " + charge + " " + vel + " " + force + "\n")
                elif args.velocity:
                    opf.write(element + " " + pos + " " + mass + " " + charge + " " + vel + "\n")
                elif args.charge:
                    opf.write(element + " " + pos + " " + mass + " " + charge + "\n")
                elif args.mass:
                    opf.write(element + " " + pos + " " + mass + "\n")

        tscounter += 1
        globallinenum = n

except Exception as e:
    print "Error location: LN:" + str(linenum) + " GLN:" + str(globallinenum) + " TS:" + str(timestep)
    print e

#print elements
#exit()

inf.close()
opf.close()
