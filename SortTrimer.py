#!/usr/bin/env python

import sys
sys.path.extend(["/home/hpc/bca1/bca109/bin/GeneralMDTools", "/home/t/Source/GeneralMDTools"])

import iotools as iot

if '.xyz' in sys.argv[1]:
    inp = iot.XYZReader(fileobj=sys.argv[1])
else:
    inp = iot.DLP2HReader(fileobj=sys.argv[1])

oup = iot.XYZWriter(fileobj=sys.argv[2], overwrite=False)

for f in inp:
    f.filter(remove=["SD", "CD", "OD"])

    #print f

    if sys.argv[3] is '1':
        cut1 = f[:14]
        cut2 = f[14:50]
        cut3 = f[50:51]
        cut4 = f[51:57]
        cut5 = f[57:119]
        cut6 = f[119:120]
        cut7 = f[120:121]
        cut8 = f[121:122]

        #print cut1

        reassembly = cut1 + cut6 + cut7 + cut2 + cut4 + cut3 + cut8 + cut5


        # cut1.append(cut6)
        # cut1.append(cut7)
        # cut1.append(cut2)
        # cut1.append(cut4)
        # cut1.append(cut3)
        # cut1.append(cut8)
        # cut1.append(cut5)

        #print reassembly

        #exit()

        oup.write(reassembly)

    else:
        oup.write(f)

del oup
