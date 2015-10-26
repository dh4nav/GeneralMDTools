#!/usr/bin/env python

import numpy as np

import argparse as ap

parser = ap.ArgumentParser()

parser.add_argument("-i", "--input", help="Input file, STO format", required=True)
parser.add_argument("-o", "--output", help="Output file STO format", required=True)
parser.add_argument("-t", "--timeaxis", help="1-based index of time axis (0 is added as iteration axis)", type=int, required=True)
parser.add_argument("-d", "--dataaxis", help="1-based index of data axis (0 is added as iteration axis)", type=int, required=True)
parser.add_argument("-s", "--steps", help="expansion steps in time axis units", type=float, required=True)
args = parser.parse_args()

print args.input

data = np.genfromtxt(open(args.input), delimiter=" ")[:,[args.timeaxis-1, args.dataaxis-1]]
#print data
interdata = np.linspace(0, len(data), endpoint=False, num=len(data)).reshape(-1,1)

data = np.hstack( (interdata, data) )
#print data
#exit()
steps = []
step = 0.0
flag = True
counter = 0
opf = open(args.output, "w")

while step < data[-1][1]:
    step += args.steps
    stepsinter = []

    for n, a in enumerate(data[:]):
        #print a #if(a[])
        if a[1] <= step:
            stepsinter.append(n)

    #print stepsinter

    if(len(stepsinter)):
        opf.write(str(counter) + " " + str(step) + " " + str(stepsinter[-1]) + " "  + str(len(stepsinter)) + " " + str(data[stepsinter,[2]].min()) + " \n" )
        #print data[stepsinter,[2]].min()
        counter += 1

opf.close()
