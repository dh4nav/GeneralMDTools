import numpy as np
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd
#import unittest as ut

class GetXYZIter:
    def __init__(self, filename):
        self.filehandle = open(filename)
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

    def get_last_frame(self):
        frame = []
        for frame in self:
            pass
        return frame

    def next(self):
        self.current += 1
        self.framelength = int(self.reader().strip()) #filehandle.readline().strip())
        line2 = self.reader().strip()
        try:
            self.boxsize = [float(line2), float(line2), float(line2)] #filehandle.readline().strip())
        except ValueError:
            self.boxsize = None

#    if args.boxsize != 0.0:
#        read_boxsize = args.boxsize
        elements = []
        coordinates = []

        for n in range(self.framelength):
            ele = self.reader().strip().split() #filehandle.readline().strip().split()
            elements.append(ele[0])
            coordinates.append([float(ele[1]), float(ele[2]), float(ele[3])])

        return {'elements':elements, 'coordinates':np.array(coordinates), 'boxvector':self.boxsize, 'framenumber':self.current, 'filename':self.filename}

    def __getitem__(self, index):
        newiter = GetXYZIter(self.filename)

        for n in range(index):
            newiter.next()
        return newiter.next()


def get_extreme_value(vectors):
    #return vectors.flatten()
    return np.absolute(vectors.flatten()).max()

def rotate_single_vector_around_origin(vector, angle_x, angle_y, angle_z):
    return np.array([
        (vector[0] * np.cos(angle_y) * np.cos(angle_z))
            + (vector[1] * ( (np.cos(angle_x) * np.sin(angle_z) ) + ( np.sin(angle_x) * np.sin(angle_y) * np.cos(angle_z) ) ))
            + (vector[2] * ( (np.sin(angle_x) * np.sin(angle_z) ) - ( np.cos(angle_x) * np.sin(angle_y) * np.cos(angle_z) ) )) ,

        ( vector[0] * (-1.0 * np.cos(angle_y)) * np.sin(angle_z) )
            #+ (vector[1] * ( (np.cos(angle_x) * np.cos(angle_z) ) - ( np.sin(angle_x) * np.sin(angle_y) + np.sin(angle_z) ) ))
            + (vector[2] * ( (np.sin(angle_x) * np.cos(angle_z) ) + ( np.cos(angle_x) * np.sin(angle_y) + np.sin(angle_z) ) )) ,

        (vector[0] * np.sin(angle_y) )
            + (vector[1] * (-1.0 * np.sin(angle_x)) * np.cos(angle_y))
            + (vector[2] * np.cos(angle_x) * np.cos(angle_y))])

def rotate_around_origin(ec, angle_x, angle_y, angle_z):
    ec['coordinates'] = rotate_single_vector_around_origin(ec['coordinates'], angle_x * (np.pi / 180.0), angle_y * (np.pi / 180.0), angle_z* (np.pi / 180.0))
    return ec

def Filter(ec, remove=None, keep=None):
#    print "F"
    filter(ec, remove, keep)

def filter(ec, remove=None, keep=None):
    #print ec
    #print remove
    #print keep
    out1 = []
    out2 = []
    ecout = ec.copy()

    if remove is not None:
        for c in zip(ec['elements'], ec['coordinates']):
            if c[0] in remove:
                pass
            else:
                out1.append(c[0])
                out2.append(c[1])
    elif keep is not None:
        for c in zip(ec['elements'], ec['coordinates']):
            if c[0] in keep:
                out1.append(c[0])
                out2.append(c[1])
    ecout['elements'] = out1
    ecout['coordinates'] = np.array(out2)
#    print "f"
#    print ecout
    return ecout


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
    center(ec)

def center(ec):
    summator = np.array([0.0,0.0,0.0])
    for c in ec['coordinates']:
        summator = summator + c

    summator = summator / len(ec['coordinates'])
    outcoords = []
    ec['coordinates'] = np.array(ec['coordinates'] - summator)

    return ec

def Move(ec, vect):
    move(ec, vect)

def move(ec, vect):
    ec['coordinates'] = np.array(ec['coordinates'] + np.array(vect))
    return ec

def Write_XYZ(ec, filename, append=True):
    write(ec, filename, append=True)

def write(ec, filename, append=True):
    #print ec
    print ".",
    if type(ec) == dict:
        ec = [ec]

    if append:
        opf = open(filename, "a")
    else:
        opf = open(filename, "w")

    #print ec
    #exit()

    for f in ec:
        opf.write(str(len(f['elements'])) + "\n" + str(f['boxvector'][0]) + "\n")
        for e, c in zip(f['elements'], f['coordinates']):
            opf.write(str(e) + " " + str(c[0]) + " " + str(c[1]) + " " + str(c[2]) + "\n")

    opf.close()

def split(ec, start, end):
    ecout = ec.copy()

    ecout['elements'] = ec['elements'][start:end]
    ecout['coordinates'] = np.array(ec['coordinates'][start:end])

    return ecout

def merge(eclist):
    ecout = eclist[0].copy()
    ecout['coordinates'] = eclist[0]['coordinates'].tolist()

    for ec in eclist[1:]:
        ecout['elements'].extend(ec['elements'])
        ecout['coordinates'].extend(ec['coordinates'])

        if ecout['boxvector'][0] < ec['boxvector'][0]:
            ecout['boxvector'][0] = ec['boxvector'][0]
        if ecout['boxvector'][1] < ec['boxvector'][1]:
            ecout['boxvector'][1] = ec['boxvector'][1]
        if ecout['boxvector'][2] < ec['boxvector'][2]:
            ecout['boxvector'][2] = ec['boxvector'][2]

    ecout['coordinates'] = np.array(ecout['coordinates'])
    return ecout

def debox_coordinate(ref, val, box):
    if (ref - val) > (box/2.0):
        return (val + box)
    elif (ref - val) < ((-1.0) * (box/2.0)):
        return (val - box)
    else:
        return val

def get_center_of_mass(ec):
    summator = [0.0,0.0,0.0]

    for c in ec['coordinates']:
        summator[0] = summator[0] + c[0]
        summator[1] = summator[1] + c[1]
        summator[2] = summator[2] + c[2]

    summator[0] = summator[0] / float(len(ec['coordinates']))
    summator[1] = summator[1] / float(len(ec['coordinates']))
    summator[2] = summator[2] / float(len(ec['coordinates']))

    return summator

def debox_intramolecule(ec, box):
    ecout = ec.copy()
    newcoordinates = [ec['coordinates'][0]]

    for c in ec['coordinates'][1:]:
        newcoordinates.append([debox_coordinate(newcoordinates[0][0], c[0], box),debox_coordinate(newcoordinates[0][1], c[1], box),debox_coordinate(newcoordinates[0][2], c[2], box)])

    ecout['coordinates'] = np.array(newcoordinates)
    return ecout

def debox_intermolecule(eclist, box, center_on=0):

    if center_on < 0:
        center_on = len(eclist['coordinates']) + center_on

    centerref = get_center_of_mass(eclist[center_on])

    ecoutlist = []

    for n, e in enumerate(eclist[:]):
        if n == center_on:
            ecoutlist.append(e)
        else:
            center = get_center_of_mass(e)
            centerdeboxed = [debox_coordinate(centerref[0], get_center_of_mass(e)[0], box),debox_coordinate(centerref[1], get_center_of_mass(e)[1], box),debox_coordinate(centerref[2], get_center_of_mass(e)[2], box)]

            diff = [centerdeboxed[0] - center[0], centerdeboxed[1] - center[1], centerdeboxed[2] - center[2]]

            ecoutlist.append(move(e, diff))

    return ecoutlist
