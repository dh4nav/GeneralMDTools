#!/bin/env python
import argparse as ap

parser = ap.ArgumentParser(description="Extract XYZ files from Gaussian output archive entries")
parser.add_argument("-i", "--input" , type=ap.FileType('r'), help="Input File")
parser.add_argument("-o", "--output" , type=ap.FileType('w'), help="Output File")
args = parser.parse_args()

lines = args.input.readlines()

archives = []
state = 0

for l in lines:
    if state == 0:
        if "l9999.exe" in l:
            state = 1
            archives.append("")
    else:
        archives[-1] = archives[-1] + l.strip()
        if "\@" in l:
            state = 0

for a in archives:
    print a.replace("\\", "\n")
        





