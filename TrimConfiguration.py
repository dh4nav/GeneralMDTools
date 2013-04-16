#!/usr/bin/env python

import os, sys, argparse
import numpy as np
import scipy.spatial.distance as ssd

parser = argparse.ArgumentParser(description="Trim a configuration to a certain size and shape")
parser.add_argument("Structure", help="Structure, in XYZ format")
parser.add_argument("OutputStructure", help="Output Structure, in XYZ format")
parser.add_argument("-m", default=1, type=int, help="Molecule size in structure 1. Program will drop entire molecule if at least one atom is located outside the intented box")
parser.add_argument("-s", "--shape",  type=str, nargs=1, choices=("box", "sphere"), help="valid options: cube, sphere")
parser.add_argument("-d", type=float, help="Box edge length or sphere diameter")
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


struct1 = ReadXYZ(args.Structure)
struct1mask = len(struct1) * [1]

struct1reduced = []
for s in struct1:
    struct1reduced.append(s[1])

struct1reduced = np.array(struct1reduced)


if args.shape[0] == 'sphere':
    for n, s in enumerate(struct1):
        dist = np.linalg.norm(struct1reduced[n])
        if dist > args.d:
            for m in range(n-(n%args.m), n+args.m-(n%args.m)):
                struct1mask[m] = 0

elif args.shape[0] == 'box':
    for n, s in enumerate(struct1):
        if (np.absolute(struct1reduced[n,0]) > (args.d/2)) or (np.absolute(struct1reduced[n,1]) > (args.d/2)) or (np.absolute(struct1reduced[n,2]) > (args.d/2)):
            for m in range(n-(n%args.m), n+args.m-(n%args.m)):
                struct1mask[m] = 0



structend = []

for n, s in enumerate(struct1):
    if struct1mask[n]:
        structend.append(s)

WriteXYZ(structend, args.OutputStructure)

