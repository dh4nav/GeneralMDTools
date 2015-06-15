#!/usr/bin/env python
import argparse as ap

parser = ap.ArgumentParser(description="Convert a Gaussian Output to XYZ")
parser.add_argument("-i", "--input" , type=ap.FileType('r'), help="Input File", required=True)
parser.add_argument("-o", "--output" , help="Output File", default=None)
parser.add_argument("-s", "--standardorientation", default=False, help="extract standard orientation instead of input orientation", action="store_true")
args = parser.parse_args()

atoms ={1: "H",
        2: "He",
        3: "Li", 
        4: "Be",
        5: "B",
        6: "C",
        7: "N", 
        8: "O",
        9: "F",
        10: "Ne",
        11: "Na",
        12: "Mg",
        13: "Al",
        14: "Si",
        15: "P",
        16: "S",
        17: "Cl",
        18: "Ar",
        19: "K",
        20: "Ca",
        21: "Sc",
        22: "Ti",
        23: "V",
        24: "Cr",
        25: "Mn",
        26: "Fe",
        27: "Co",
        28: "Ni",
        29: "Cu",
        30: "Zn", 
        31: "Ga",
        32: "Ge",
        33: "As",
        34: "Se",
        35: "Br",
        36: "Kr",
        83: "Bi"}

archive_buffer = []
archive_sections_buffer = []

def Process_Archivebuffer():
    global archive_buffer
    global archive_sections_buffer
    archive_sections_buffer.append([])
    interbuffer = archive_buffer.split("\\\\")
    for s in interbuffer:
        archive_sections_buffer[-1].append(s.split("\\"))
    archive_buffer = ""

def Print_XYZ(buf, filename):
    opf = open(filename, "w")
    for b in buf:
        opf.write(str(len(b)) + "\n\n")
        for l in b:
            opf.write(l)
    opf.close()

readmode = 0

if args.output == None:
    args.output = args.input.name

lines = args.input.readlines()
lines2 = [x for x in lines if x.strip() != ""]

# read coordinate blocks
for l in lines2:
    if readmode > 4:
        if "-----" in l:
            readmode = 0
        else:
            ll = l.strip().split()
            archive_buffer[-1].append(atoms[int(ll[1])] + " " + ll[3] + " " + ll[4] + " " + ll[5] + "\n")

    elif readmode > 0:
        readmode += 1

    elif args.standardorientation:
        if "Standard orientation:" in l:
            readmode = 1
            archive_buffer.append([]) 
    else:
        if "Input orientation:" in l:
            readmode = 1
            archive_buffer.append([])


if len(archive_buffer):
    Print_XYZ(archive_buffer, args.output + ".progress.xyz")


#args.output.write(str(len(lines2)) + "\n \n")
#args.output.writelines(lines2)

#print archive_buffer
#print archive_sections_buffer
