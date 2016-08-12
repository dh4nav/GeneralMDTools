#!/usr/bin/env python

import sys
sys.path.extend(["/home/hpc/bca1/bca109/bin/GeneralMDTools", "/home/t/Source/GeneralMDTools"])

import iotools as iot

for f in sys.argv[1:]:
    if '.xyz' in f:
        inp = iot.XYZReader(fileobj=f)
    else:
        inp = iot.DLP2HReader(fileobj=f)

    print(f)

    for n, frame in enumerate(inp):
        frame.filter(keep=["BI", "NN", "ON"])
        #print frame.filter(keep=["NN", "ON"])
        ensemble_bi = frame.copy()
        ensemble_no3 = frame.copy()

        ensemble_bi.filter(keep=["BI"])
        ensemble_no3.filter(keep=["NN", "ON"])

        ensemble_bi.debox_intermolecule()

        ensemble_no3.debox_intermolecule(center_on_coordinates=ensemble_bi['coordinate'][0])
        for i in range(0, len(ensemble_no3), 4):
            ensemble_no3.debox_intermolecule(start=i, end=i+4)

        joined = ensemble_bi + ensemble_no3

        print(str(n) + " " + str(joined.get_chains(dist=7.5)))

    print("----------")
