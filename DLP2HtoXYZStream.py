#!/usr/bin/env python

# -*- coding: utf-8 *-*

import os, sys

import argparse as ap

parser = ap.ArgumentParser(description="Convert from DLPOLY 2/DLPOLY Classic HISTORY to a XYZ format")

parser.add_argument("HISTORY", help="HISTORY file name")
parser.add_argument("XYZ", help="XYZ file name")
group1 = parser.add_mutually_exclusive_group()
group1.add_argument("-k", "--keepcomment", help="keep comment line from REVCON or CONFIG file", action="store_true")
group1.add_argument("-c", "--setcomment", metavar="COMMENT", help="set comment line")
group1.add_argument("-b", "--boxcomment", action="store_true", help="set comment line to box x size")
parser.add_argument("-s", "--split", help="split into separate files for each timestep", action="store_true")
parser.add_argument("-v", "--verbose", help="print progress", action="store_true")
parser.add_argument("-d", "--debug", help="debug output", action="store_true")
parser.add_argument("-n", "--noheader", help="missing history file header, file starts with timestep line. Useful for partial files", action="store_true")
args = parser.parse_args()

elements = []
coordinates = []
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

globallinenum = 0

lastelement = ""

framecounter = 0

inf = open(args.HISTORY, "r")
opf = open(args.XYZ, "w")
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
                opf.write(l.split()[0].strip() + "\n")

        elif tscounter <= numlines:
            if(tscounter % (typekey +2)) == 0:
                element = l.split()[0].strip()
            elif(tscounter % (typekey +2)) == 1:
                opf.write(element + " " + l.strip() + "\n")


        tscounter += 1
        globallinenum = n

except Exception as e:
    print "Error location: LN:" + str(linenum) + " GLN:" + str(globallinenum) + " TS:" + str(timestep)
    print e

#print elements
#exit()

inf.close()
opf.close()
