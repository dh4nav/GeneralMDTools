import numpy as np
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd

class GetXYZIter:
    def __init__(self, filename):
        self.filehandle = open(args.Infile)
        self.filename = filename
        self.current = 0

    def reader(self):
        line = self.filehandle.readline()
        if len(line) == 0:
            raise StopIteration
        else:
            return line

    def __iter__(self):
        return self

    def next(self):
        self.current += 1
        self.framelength = int(self.reader().strip()) #filehandle.readline().strip())
        self.boxsize = float(self.reader().strip()) #filehandle.readline().strip())
#    if args.boxsize != 0.0:
#        read_boxsize = args.boxsize
        elements = []
        coordinates = []

        for n in range(self.framelength):
            ele = self.reader().strip().split() #filehandle.readline().strip().split()
            elements.append(ele[0])
            coordinates.append([float(ele[1]), float(ele[2]), float(ele[3])])

        return {'elements':elements, 'coordinates':np.array(coordinates), 'boxvector':[self.boxsize, self.boxsize, self.boxsize], 'framenumber':self.current, 'filename':self.filename}


def Filter(ec, remove=None, keep=None):
    out1 = []
    out2 = []
    if remove != None:
        for c in zip(ec['elements'], ec['coordinates']):
            if c[0] in remove:
                pass
            else:
                out1.append(c[0])
                out2.append(c[1])
    elif keep != None:
        for c in zip(ec['elements'], ec['coordinates']):
            if c[0] in remove:
                out1.append(c[0])
                out2.append(c[1])
    ec['elements'] = out1
    ec['coordinates'] = np.array(out2)

    return ec


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

