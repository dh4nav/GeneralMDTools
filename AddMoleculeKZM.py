import xyzt
import os, sys
import argparse as ap


parser = ap.ArgumentParser(description = "Add Molecule on surrounding sphere")
parser.add_argument("-i", "--infile", help="Infile from previous step, xyz format")
parser.add_argument("-a". "--add_molecule", help="Molecule to add, xyz format")
parser.add_argument("-o", "--outfile", help="Outfile, xyz format")

group = parser.add_mutually_exclusive_group()
group.add_argument("-r", "--radius_outer", type="float", help="radius from outmost atom to add new molecule at")
group.add_argument("-R", "--radius_center", type="float", help="radius from center to add new molecule at")

args = parser.parse_args()

iterin = xyzt.XYZIter(args.infile)
iteradd = xyzt.XYZIter(args.add_molecule)

inframe = iterin.get_last_frame()
addframe = iteradd.get_last_frame()

inframe = xyzt.center(inframe)
addframe = xyzt.center(addframe)

positioning_vector = [1.0,0.0,0.0]


