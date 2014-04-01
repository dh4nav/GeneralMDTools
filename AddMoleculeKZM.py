#!/usr/bin/python

import xyzt
import os, sys
import argparse as ap
import numpy as np

parser = ap.ArgumentParser(description = "Add Molecule on surrounding sphere")
parser.add_argument("-i", "--infile", help="Infile from previous step, xyz format")
parser.add_argument("-a", "--add_molecule", help="Molecule to add, xyz format")
parser.add_argument("-o", "--outfile", help="Outfile, xyz format")

group = parser.add_mutually_exclusive_group()
group.add_argument("-r", "--radius_outer", type=float, help="radius from outmost atom to add new molecule at")
group.add_argument("-R", "--radius_center", type=float, help="radius from center to add new molecule at")

args = parser.parse_args()

iterin = xyzt.GetXYZIter(args.infile)
iteradd = xyzt.GetXYZIter(args.add_molecule)

inframe = iterin.get_last_frame()
addframe = iteradd.get_last_frame()

inframe = xyzt.Center(inframe)
addframe = xyzt.Center(addframe)

if args.radius_outer != None:
    radius = xyzt.get_extreme_value(inframe['coordinates']) + args.radius_outer
else:
    radius = args.radius_center

positioning_vector = np.multiply(np.array([1.0,0.0,0.0]), radius)

# positioning_vector = xyzt.rotate_single_vector_around_origin(positioning_vector, TODO: random rotation

xyzt.Move(addframe, positioning_vector)

outframe = addframe
print outframe
outframe['coordinates'] = np.append(outframe['coordinates'] , inframe['coordinates'], axis=0)
outframe['elements'] = outframe['elements'] + inframe['elements']

boxsize = xyzt.get_extreme_value(outframe['coordinates'])

outframe['boxvector'] = [boxsize, boxsize, boxsize]

xyzt.Write_XYZ(outframe, args.outfile, append=False)

print outframe

