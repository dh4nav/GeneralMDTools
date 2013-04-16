#!/usr/bin/env python

import os, sys, argparse
import numpy as np
import scipy.spatial.distance as ssd

parser = argparse.ArgumentParser(description="Cuts structure 2 into structure 1, dropping atoms or molecules from structure 1 as nessecary")
parser.add_argument("Structure1", help="Structure 1, in XYZ format")
parser.add_argument("Structure2", help="Structure 2, in XYZ format")
parser.add_argument("OutputStructure", help="Output Structure, in XYZ format")
parser.add_argument("-m", default=1, type=int, help="Molecule size in structure 1. Program will drop entire molecule if at least one atom intersects with an atom in Structure 2.")
parser.add_argument("-d", default=3.5,  type=float, help="Minimum distance between positions below which two atoms will be considered intersecting")
parser.add_argument("-e", type=bool, default=0,help="Append Structure 1 to Structure 2. Opposite of default behaviour")
parser.add_argument("-c", type=str, default="",help="Comment to add to output file")
args = parser.parse_args()

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
                raise IOError("Line " + str(n) + " in File " + filename + " : Malformed line. 4 fields (str, float, float, float) expected, " + len(elem) + " found.")
    inf.close()
    return outarray


def WriteXYZ(data,  filename):
    opf = open(filename, "w")

    opf.write(str(len(data)) + "\n"+args.c+"\n")
    for d in data:
        opf.write(d[0] + " " + str(d[1][0]) + " " + str(d[1][1]) + " " + str(d[1][2]) + "\n")
    opf.close()


struct1 = ReadXYZ(args.Structure1)
struct2 = ReadXYZ(args.Structure2)
struct1mask = len(struct1) * [1]

struct2reduced = []
for s in struct2:
    struct2reduced.append(s[1])

struct2reduced = np.array(struct2reduced)
for n, s in enumerate(struct1):
    dmatrix = ssd.cdist(np.array([s[1]]), struct2reduced)
    if dmatrix.min() < args.d:
        for m in range(n-(n%args.m), n+args.m-(n%args.m)):
            struct1mask[m] = 0


structend = []

if args.e == 1:
    for s in struct2:
        structend.append(s)

for n, s in enumerate(struct1):
    if struct1mask[n]:
        structend.append(s)

if args.e != 1:
    for s in struct2:
        structend.append(s)


WriteXYZ(structend, args.OutputStructure)

