#!/usr/bin/env python

import sys

ipf = open(sys.argv[1])
opf = open(sys.argv[2], "w")

confkey = 0
periodickey = 0

def mangle(line):
    changeflag = 0
    for n, l in enumerate(line[:]):
        if l == "-":
            if (n == 0) or (line[n-1] == " "):
                line = line[:n] + " " + line[n+1:]
                changeflag = 1
        elif l.isdigit():
            if changeflag:
                changeflag = 0
            elif (n==0):
                print "no space before first digit"
                exit() 
            elif line[n-1] == " ":
                line = line[:n-1] + "-" + line[n:]
    return line


for n, l in enumerate(ipf):
    if n == 0:
        opf.write(l)
    elif n == 1:
        elem = l.strip().split()
        confkey = int(elem[0])
        periodickey = int(elem[1])
    elif periodickey != 0:
        if n == 2:
            opf.write(l)
        elif n == 3:
            opf.write(l)
        elif n == 4:
            opf.write(l)
        elif (n-5)%(confkey+2) == 0:
            opf.write(l)
        elif (n-6)%(confkey+2) == 0:
            opf.write(l)
            opf.write(mangle(l))
        elif (confkey == 2) and ((n-8)%4 == 0):
            opf.write(l)
    else:
        if (n-2)%(confkey+2) == 0:
            opf.write(l)
        elif (n-3)%(confkey+2) == 0:
            opf.write(l)
            opf.write(mangle(l))
        elif (confkey == 2) and ((n-5)%4 == 0):
            opf.write(l)

        
