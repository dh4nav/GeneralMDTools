import os, sys
import numpy as np
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd

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

def Center(ec):
    summator = np.array([0.0,0.0,0.0])
    for c in ec[coordinates]:
        summator = summator + c

    summator = summator / len(ec[coordinates])

    outcoords = []

#    for c in ec[coordinates]:
#        outcoords.append(c-summator)

    ec[coordinates] = np.array(ec[coordinates] - summator)

    return ec

def Move(ec, vect):
    
    ec[coordinates] = np.array(ec[coordinates] + np.array(vect))
    return ec
