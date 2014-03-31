import xyzt
import os, sys
import argparse as ap


parser = ap.ArgumentParser(description = "Add Molecule on surrounding sphere")
parser.add_argument("-i", "--infile", help="Infile from previous step, xyz format")
parser.add_argument("-a". "--add_molecule", help="Molecule to add, xyz format")
parser.add_argument("-o", "--outfile", help="Outfile, xyz format")

args = parser.parse_args()

iterin = xyzt.XYZIter(args.infile)
iteradd = xyzt.XYZIter(args.add_molecule)

