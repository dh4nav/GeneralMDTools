#!/usr/bin/env python3
import os, sys, math

opf = open(sys.argv[2], "w")
ipf = open(sys.argv[1], "r")

values = []
results = []

def calculateRes(value1, value2):
    return [value1[0], value2[0], "LJ", str(math.sqrt(float(value1[1])*float(value2[1]))), str(0.5 * (float(value1[2]) + float(value2[2]))) ]

for l in ipf:
    values.append(l.strip().split())
    
for a in values[:]:
    for b in values[:]:
        opf.write(" ".join(calculateRes(a, b)) + "\n")

ipf.close()
opf.close()


    
   

