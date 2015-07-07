#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys



ipf = open(sys.argv[1])
opf = open(sys.argv[2], "w")

opv = []
end = True
count = 0
mode = 1

#ipf.read()

#if "ENERGY" in ipf.read():
#    mode = 0

#ipf.close()
#ipf = open(sys.argv[1])

for n, l in enumerate(ipf):
    if l.strip() == "":
        pass
    elif "ENERGY" in l:
        pass
#    elif n == 0 & mode:
#        print mode
#        pass
#    elif n == 1 & mode:
#        pass
    elif end == True:
        el = l.strip().split()
        #print el
        count = 2 + int(el[2])
        opv.append([int(el[0]) , float(el[1])])
        end = False
    else:
        el = l.strip().split()
        for e in el:
            opv[-1].append(float(e))
        if len(opv[-1]) == count:
            end = True


for l in opv:
    for e in l:
        opf.write(str(e) + " ")
    opf.write("\n")

