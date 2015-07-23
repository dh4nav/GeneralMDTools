#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, sys
import argparse as ap
import xyzt


parser = ap.ArgumentParser(description="Multiply a solvent box")

parser.add_argument("-i", "--infile", required=True, help="XYZ Input file")
parser.add_argument("-o", "--outfile", required=True, help="XYZ Output file")

parser.add_argument("-x", "--xscale", type=float, help="scale box in x direction")
parser.add_argument("-y", "--yscale", type=float, help="scale box in y direction")
parser.add_argument("-z", "--zscale", type=float, help="scale box in z direction")

parser.add_argument("-G", "--cog", action='store_true', help="use center of geometry")
parser.add_argument("-M", "--com", action='store_true', help="use center of mass")

parser.add_argument("-e", "--elements", nargs='+', required=True, help="List of elements to scale")

#parser.add_argument("-e", "--elements", required=True, type=str, nargs="+", help="list of element labels and weights label weight label weight ...")
args = parser.parse_args()
print args
#exit()

#if args.yscale is None:
args.yscale = args.xscale

#if args.zscale is None:
args.zscale = args.xscale


xyziter = xyzt.GetXYZIter(args.infile)

print xyziter[0]
print xyziter[0]
moveatoms = xyzt.filter(xyziter[0], keep=args.elements)
staticatoms = xyzt.filter(xyziter[0], remove=args.elements)

print moveatoms
print staticatoms

center=xyzt.get_center_of_mass(moveatoms)

moveatoms['coordinates'] -= center
moveatoms['coordinates'] *= [args.xscale,args.yscale,args.zscale]
moveatoms['coordinates'] += center

allconf = xyzt.merge([moveatoms, staticatoms])

xyzt.write(allconf, args.outfile)
