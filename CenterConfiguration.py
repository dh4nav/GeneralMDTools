#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

import argparse as ap

parser = ap.ArgumentParser(description="Center a configuration in its bounding box and output minimum box dimensions")

parser.add_argument("Infile", help="XYZ input file")
parser.add_argument("Outfile", help="XYZ output file")

args = parser.parse_args()

ipf = open(args.Infile)
opf = open(args.Outfile, "w")

config = []
framlength = 0
count = 0
comment = ""
sums = [0.0,0.0,0.0]

mins = [0.0,0.0,0.0]
maxs = [0.0,0.0,0.0]

for n, l in enumerate(ipf):
    count = n
    print str(count) + " " + l
    if n== 0:
        framelength = int(l)
    elif n == 1:
        comment = l
    elif n < (framelength + 2):
        config.append([l.strip().split()[0], [float(l.strip().split()[1]),float(l.strip().split()[2]),float(l.strip().split()[3])]])
        sums[0] += config[-1][1][0]
        sums[1] += config[-1][1][1]
        sums[2] += config[-1][1][2]
    
if count < framelength+1:
    print "lines missing? " + str(count) +" lines found (including header), " + str(framelength) + " expected";
    exit()

mean = [sums[0]/float(framelength), sums[1]/float(framelength), sums[2]/float(framelength)]

print len(config)

for i in range(len(config)):
    config[i][1][0] = config[i][1][0] - mean[0]
    config[i][1][1] = config[i][1][1] - mean[1]
    config[i][1][2] = config[i][1][2] - mean[2]

for i in range(len(config)):

    if config[i][1][0] > maxs[0]:
        maxs[0] = config[i][1][0]
    if config[i][1][0] < mins[0]:
        mins[0] = config[i][1][0]

    if config[i][1][1] > maxs[1]:
        maxs[1] = config[i][1][1]
    if config[i][1][1] < mins[1]:
        mins[1] = config[i][1][1]

    if config[i][1][2] > maxs[2]:
        maxs[2] = config[i][1][2]
    if config[i][1][2] < mins[2]:
        mins[2] = config[i][1][2]

opf.write(str(framelength) + "\n" + comment )
for i in range(len(config)):
    opf.write(config[i][0] + " " + str(config[i][1][0]) + " " + str(config[i][1][1])+ " " + str(config[i][1][2]) + "\n")

print "Center: " + str(mean)
print "Maxs: " + str(maxs)
print "Mins: " + str(mins)
