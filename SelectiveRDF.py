#!/usr/bin/env python

import xyzt
import argparse as ap
import numpy as np


parser = ap.ArgumentParser(description="Generate RDF from pairs")
parser.add_argument("-i", "--input" , help="Input File, xyz", required=True)
parser.add_argument("-o", "--output" , help="RDF Output File", default=None, required=True)
parser.add_argument("-p", "--pairs", help="0-based index pairs for RDF", nargs="+", type=int)
parser.add_argument("-n", "--mindist", help="minimum distance", default=0.0, type=float)
parser.add_argument("-x", "--maxdist", help="maximum distance", type=float)
parser.add_argument("-b", "--bins", help="number of histogram bins", type=int, default=100)
args = parser.parse_args()

xyz_iter =  xyzt.GetXYZIter(args.input)

distances = []
accumulator = 0.0
rdf = []

#print args.pairs
#exit()

for frame in xyz_iter:

    #print frame
    #exit()

    for n in range(0, len(args.pairs), 2):
        dist = xyzt.Dist(frame['coordinates'][args.pairs[n]], frame['coordinates'][args.pairs[n+1]], frame['boxvector'])

        if dist < args.mindist:
            continue
        if args.maxdist:
            if dist > args.maxdist:
                continue

        distances.append(dist)

hist = np.histogram(distances, bins=args.bins)

for n, v in enumerate(hist[0]):
    accumulator += v
    rdf.append([hist[1][n]+((hist[1][n+1]-hist[1][n])/2.0), v, accumulator])

print hist
print rdf

opf = open(args.output, "w")

for l in rdf:
    opf.write(str(l[0]) + " " + str(l[1]) + " " + str(l[2]) + "\n")

opf.close()

#for n, b in enumerate(hist)
