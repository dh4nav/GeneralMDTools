#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import argparse as ap

parser = ap.ArgumentParser(description="Sort STATIS file into single lines per entry for easier plotting")

parser.add_argument("-i", "--infile", help="Statis file", type=ap.FileType(mode="r"), default="STATIS")
parser.add_argument("-o", "--outfile", help="Output file", type=ap.FileType(mode="w"))

args = parser.parse_args()

elementbuffer = []
elementnumber = 0
for n, l in enumerate(args.infile):
    if n < 2:
        continue

    splitline = l.strip().split()

    if elementnumber == 0:
        elementbuffer.append(int(splitline[0]))
        elementbuffer.append(float(splitline[1]))
        elementnumber = int(splitline[2]) + 2

    else:
        for e in splitline:
            elementbuffer.append(float(e))
        if len(elementbuffer) == elementnumber:
            writebuffer = ""
            for e in elementbuffer:
                writebuffer += (str(e) + " ")
            #writebuffer[-1] = "\n"
            args.outfile.write(writebuffer[:-1]+"\n")
            elementnumber = 0
            elementbuffer = []


