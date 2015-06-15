#!/usr/bin/env python
import argparse as ap

parser = ap.ArgumentParser(description="Convert a Gaussian Output to XYZ")
parser.add_argument("-i", "--input" , type=ap.FileType('r'), help="Input File", required=True)
parser.add_argument("-o", "--output" , help="Output File", default=None)
args = parser.parse_args()


archive_buffer = ""
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
    opf.write(str(len(buf)) + "\n\n")
    for l in buf:
        opf.write(" ".join(l.split(",")) + "\n")
    opf.close()

readmode = 0

if args.output == None:
    args.output = args.input.name

lines = args.input.readlines()
lines2 = [x for x in lines if x.strip() != ""]

# read archive blocks
for l in lines2:
    if readmode:
        archive_buffer += l.strip()
        if "\\@" in l:
            readmode = 0
            Process_Archivebuffer()

    elif "1\\1\\" in l:
        readmode = 1
        archive_buffer += l.strip()

# print coordinate sections
if len(archive_sections_buffer) > 1:
    for n, b in enumerate(archive_sections_buffer):
        if len(b) > 3:
            Print_XYZ(b[3][1:], args.output + "." + str(n) + ".xyz")

else:
    if len(archive_sections_buffer[0]) > 3:
        Print_XYZ(archive_sections_buffer[0][3][1:], args.output + ".xyz")


#args.output.write(str(len(lines2)) + "\n \n")
#args.output.writelines(lines2)

#print archive_buffer
#print archive_sections_buffer
