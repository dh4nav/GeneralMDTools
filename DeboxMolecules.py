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
group.add_argument("-T", "--types", type=str, help="lists of atoms in a molecule. Separator between atoms inside a molecule: space, separator between molecules: comma", nargs="*")
group2 = parser.add_mutually_exclusive_group(required=False)
group2.add_argument("-c", "--center_on",
                    help="molecule to center on. Zero-based index, negative indices permitted, default 0",
                    type=int, default=None)
group2.add_argument("-C", "--center_on_coordinates",
                    help="coordinates to center on. 3 values required",
                    type=float, nargs=3, default=None)

args = parser.parse_args()

#print args
#exit()

frameiterator = xyzt.GetXYZIter(args.input)

moleculespecs = [[]]

if args.types:
    for a in args.types:
        if a is ",":
            moleculespecs.append([])
        else:
            moleculespecs[-1].append(a)
    args.types = moleculespecs

print args.types
#exit()

for f in frameiterator:

    runner = 0
    index = 0
    mollist = []

    if args.types:
        args.molecule_lengths = []
        for i in range(len(f['elements'])+1):
            #print i
            try:
                index = args.types.index(f['elements'][runner:i]) 
                print f['elements'][runner:i]
            except:
                continue
            
            args.molecule_lengths.append(len(args.types[index]))
            runner = i 
        if runner != (len(f['elements'])):
            raise ValueError("Element list length mismatch (Couldn't match to an even number of molecules") 



    if args.molecule_lengths:
        runner = 0
        for m in args.molecule_lengths:
            mollist.append(xyzt.debox_intramolecule(xyzt.split(f, runner, runner+int(m)), f['boxvector'][0]))
            runner += int(m)

    else: #if args.molecule_lengths_tuples:
        for i in range(0, len(args.molecule_lengths_tuples), 2):
            if (i+2) > len(args.molecule_lengths_tuples):
                while runner < len(f['elements']):
                    mollist.append(xyzt.debox_intramolecule(xyzt.split(f, runner, runner+int(args.molecule_lengths_tuples[i])), f['boxvector'][0]))
                    runner += int(args.molecule_lengths_tuples[i])
            else:
                for k in range(args.molecule_lengths_tuples[i+1]):
                    mollist.append(xyzt.debox_intramolecule(xyzt.split(f, runner, runner+int(args.molecule_lengths_tuples[i])), f['boxvector'][0]))
                    runner += int(args.molecule_lengths_tuples[i])

    #else:
    print mollist   

    mollist_d = xyzt.debox_intermolecule(mollist, f['boxvector'][0], center_on=args.center_on)
    xyzt.write(xyzt.center(xyzt.merge(mollist)), args.output, append=True)
