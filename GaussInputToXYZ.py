#!/usr/bin/env python
import argparse as ap

parser = ap.ArgumentParser(description="Convert a Gaussian Input to XYZ")
parser.add_argument("-i", "--input" , type=ap.FileType('r'), help="Input File")
parser.add_argument("-o", "--output" , type=ap.FileType('w'), help="Output File")
args = parser.parse_args()

lines = args.input.readlines()
lines2 = [x for x in lines if x.strip() != ""]

if "%chk" in lines2[0].strip().lower():
    lines2 = lines2[1:]

lines2 = lines2[3:]

args.output.write(str(len(lines2)) + "\n \n")
args.output.writelines(lines2)

print lines
print lines2





