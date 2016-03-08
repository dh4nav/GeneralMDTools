import pandas as pd
#import numpy as np
#import os
import sys
import bokeh.charts as bc

df = None

defaultcolumns = ["timestep", "time", "total energy", "temperature", "configuration energy", "VdW/Metal/Tersoff energy", "electrostatic energy", "chemical bond energy",
                  "valence ange/3-body potential energy", "dihedral/inversion/four body energy", "tethering energy", "enthalpy", "rotational temperature", "total virial",
                  "VdW/Metal/Tersoff virial", "electrostatic virial", "bond virial", "valence angle/3-body virial", "constraint virial", "tethering virial", "volume",
                  "core-shell temperature", "core-shell potential energy", "core-shell virial", "MD cell angle alpha", "MD cell angle beta", "MD cell angle gamma", "Potential of mean force", "pressure"]

datastore = []
dslen = None


with open(sys.argv[1]) as f:

    for n, line in enumerate(f):
        if line.strip() == "":
            pass
        elif line.strip().split()[0] == "ENERGY":
            pass
        else:
            line_elements = line.split()
            if "." in line_elements[0]:
                for datafield in line_elements:
                    datastore[-1].append(float(datafield))
            else:
                if dslen == None:
                    dslen = int(line_elements[2])+2

                    for num in range(29, dslen):
                        defaultcolumns.append(str(num))

                elif len(datastore[-1]) != dslen:
                    datastore.pop()

                datastore.append([])
                datastore[-1].append(int(line_elements[0]))
                datastore[-1].append(float(line_elements[1]))

if len(datastore):
    df = pd.DataFrame(data=datastore, columns=defaultcolumns)

#print df.idx(3)

#print len(df)

p = bc.Scatter(df, x='time', y='total energy', color='configuration energy', legend="top_left")

bc.output_file('/tmp/opt.html')

bc.show(p)
