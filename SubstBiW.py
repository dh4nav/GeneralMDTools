#!/usr/bin/env python

import sys

ipf = open(sys.argv[1])
opf = open(sys.argv[2], "a")

counter = 0

for l in ipf:
    if "BI" in l:
        counter += 1
        if counter < 7:
            opf.write(" ".join(["W "] + l.split()[1:] + ["\n"]))
        else:
            opf.write(l)
            if counter > 11:
                counter = 0
    else:
        opf.write(l)

