#!/usr/bin/env python

import os, sys
import numpy as np
import scipy.cluster.hierarchy as sch
import argparse as ap
import scipy.spatial.distance as ssd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

parser = ap.ArgumentParser(description="Determine Clustering of Bi clusters and number of NO3 molecules on each cluster")
parser.add_argument("Infile")
parser.add_argument("Sizefile")
parser.add_argument("Popfile")
parser.add_argument("-d", "--distance", type=float)
args = parser.parse_args()

args.boxsize = 0.0
read_boxsize = 0.0
framelength = 0
filehandle = None

filehandle_p = None
filehandle_s = None

stepcounter = 0

class GetXYZIter:
    def __init__(self):
        global filehandle
        if filehandle:
            filehandle.close()
        filehandle = open(args.Infile)

        self.current = 0

    def reader(self):
        line = filehandle.readline()
        if len(line) == 0:
            raise StopIteration
        else:
            return line

    def __iter__(self):
        return self

    def next(self):
        self.current += 1
        global stepcounter
        stepcounter = self.current
        self.framelength = int(self.reader().strip()) #filehandle.readline().strip())
        global read_boxsize 
        read_boxsize = float(self.reader().strip()) #filehandle.readline().strip())
#    if args.boxsize != 0.0:
#        read_boxsize = args.boxsize
        elements = []
        coordinates = []

        for n in range(self.framelength):
            ele = self.reader().strip().split() #filehandle.readline().strip().split()
            elements.append(ele[0])
            coordinates.append([float(ele[1]), float(ele[2]), float(ele[3])])

        return (elements, np.array(coordinates))


def Filter(ec, remove=None, keep=None):
    out1 = []
    out2 = []
    if remove != None:
        for c in zip(ec[0], ec[1]):
            if c[0] in remove:
                pass
            else:
                out1.append(c[0])
                out2.append(c[1])
    elif keep != None:
        for c in zip(ec[0], ec[1]):
            if c[0] in remove:
                out1.append(c[0])
                out2.append(c[1])
    else:
        out1 = ec[0]
        out2 = ec[1]
    return (out1, np.array(out2))


def Dist(x0, x1, boxvect):
    delta = np.absolute(np.subtract(x0,x1))
    delta = np.where(delta > 0.5 * boxvect, boxvect - delta, delta)
    return np.sqrt((delta ** 2).sum(axis=-1))


def DistDist(x0, x1, boxvect):
    distvect = []
    for n, a in enumerate(x0):
        if n < (len(x1)-1):
            distvect.extend(Dist(a, np.array(x1[n+1:]), np.array(boxvect)))
    return np.array(distvect)



filehandle = open(args.Infile)
filehandle_s = open(args.Sizefile, "w")
filehandle_p = open(args.Popfile, "w")

for f in GetXYZIter():
#    print f

    ec = Filter(f, remove=['CD','OD','SD'])
    elem = ec[0]
    coord = ec[1]
#    print "read"
    distvect =  DistDist(coord, coord, [read_boxsize,read_boxsize,read_boxsize])
#    print "dist"
    fcl = sch.fcluster(sch.linkage(distvect), args.distance, criterion='distance')

#    print distvect
#    print fcl
#    print coord[:,0]
#    print fcl.max()
    histo = np.histogram(fcl,bins=fcl.max(),range=(1.0,fcl.max()+1))

    writevalues = {}
    for n, v in enumerate(histo[0]):
        if v in writevalues:
            writevalues[v] += 1
        else:
            writevalues[v] = 1

#    print writevalues

    for k in writevalues.keys():
#        print k
        filehandle_s.write(str(stepcounter) + " " + str(k) + " " + str(writevalues[k]) + "\n")

    ncount = []
    
    for i in range(1, fcl.max()+1):
        ncount.append(0)
        for n, a in enumerate(fcl):
            if a == i:
                if elem[n] == "NN":
                    ncount[-1] += 1
#                    print "NN " + str(n)
    writevalues = {}
    for n,v in enumerate(ncount):
        if v in writevalues:
            writevalues[v] += 1
        else:
            writevalues[v] = 1

    for k in writevalues.keys():
        filehandle_p.write(str(stepcounter) + " " + str(k) + " " + str(writevalues[k]) + "\n")



#    if (stepcounter % 100) == 0:
#        print stepcounter

exit()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(coord[:,0], coord[:,1],coord[:,2], c=fcl)
plt.show()
#print ssd.squareform(diffvect)


