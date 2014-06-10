#!/usr/bin/env python
#-*- coding:utf-8 *-*

import argparse as ap
import xyzt

parser = ap.ArgumentParser()
parser.add_argument("-i", "--input", required=True)
parser.add_argument("-o", "--output", required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-l", "--molecule_lengths", type=int,
                    help="List of molecule lengths in number of atoms and in order as they appear in the file",
                    nargs="+")
group.add_argument("-L", "--molecule_lengths_tuples", type=int,
                    help="tuples of molecule lengths and molecule counts for the molecules in the order they appear in the molecule. Optionally, the last molecule length may omit the count, and will cover all remaining molecules",
                    nargs ="+")
parser.add_argument("-c", "--center_on",
                    help="molecule to center on. Zero-based index, negative indices permitted, default 0",
                    default=0, type=int)


args = parser.parse_args()

frameiterator = xyzt.GetXYZIter(args.input)

for f in frameiterator:

    runner = 0
    mollist = []

    if args.molecule_lengths != None:

        for m in args.molecule_lengths:
            mollist.append(xyzt.debox_intramolecule(xyzt.split(f, runner, runner+int(m)), f['boxvector'][0]))
            runner += int(m)

    else:
        for i in range(0, len(args.molecule_lengths_tuples), 2):
            if (i+2) > len(args.molecule_lengths_tuples):
                while runner < len(f['elements']):
                    mollist.append(xyzt.debox_intramolecule(xyzt.split(f, runner, runner+int(args.molecule_lengths_tuples[i])), f['boxvector'][0]))
                    runner += int(args.molecule_lengths_tuples[i])
            else:
                for k in range(args.molecule_lengths_tuples[i+1]):
                    mollist.append(xyzt.debox_intramolecule(xyzt.split(f, runner, runner+int(args.molecule_lengths_tuples[i])), f['boxvector'][0]))
                    runner += int(args.molecule_lengths_tuples[i])


    mollist_d = xyzt.debox_intermolecule(mollist, f['boxvector'][0], center_on=args.center_on)

    xyzt.write(xyzt.center(xyzt.merge(mollist)), args.output, append=True)
