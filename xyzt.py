import numpy as np
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd
#import unittest as ut


class GetXYZIter:
    """XYZ Iterator class

    Frame format specification:
        {'elements':[str, ...], 'coordinates':ndarray([[x,y,z],...]), 'boxvector':float, 'framenumber':int, 'filename':str}"""

    def __init__(self, filename):
        """Return XYZIter object from XYZ-file filename"""

        self.filehandle = open(filename)
        self.filename = filename
        self.current = 0

    def reader(self):
        """Return next line from file, or StopIteration on EOF"""
        line = self.filehandle.readline()
        if len(line) == 0:
            raise StopIteration
        else:
            return line

    def __iter__(self):
        """Return an iterator"""
        return self

    def get_last_frame(self):
        """Return the last-read frame"""
        frame = []
        for frame in self:
            pass
        return frame

    def next(self):
        """Return frame data dictionary of next frame,
                Raise *ValueError* if no float in comment line (boxsize),
                Raise *StopIteration* on EOF"""
        self.current += 1
        self.framelength = int(self.reader().strip()) #filehandle.readline().strip())
        line2 = self.reader().strip()
        try:
            self.boxsize = [float(line2), float(line2), float(line2)] #filehandle.readline().strip())
        except ValueError:
            self.boxsize = None

        elements = []
        coordinates = []

        for n in range(self.framelength):
            ele = self.reader().strip().split() #filehandle.readline().strip().split()
            elements.append(ele[0])
            coordinates.append([float(ele[1]), float(ele[2]), float(ele[3])])

        return {'elements':elements, 'coordinates':np.array(coordinates), 'boxvector':self.boxsize, 'framenumber':self.current, 'filename':self.filename}

    def __getitem__(self, index):
        """Return frame with index"""
        newiter = GetXYZIter(self.filename)

        for n in range(index):
            newiter.next()
        return newiter.next()


def get_extreme_value(vectors):
    """Return maximum of absolute of flattened vectors"""
    return np.absolute(vectors.flatten()).max()

def rotate_single_vector_around_origin(vector, angle_x, angle_y, angle_z, degrees=False):
    """Return vector rotated around origin by 3 angles"""

    if degrees:
        angle_x = angle_x * (np.pi / 180.0)
        angle_y = angle_y * (np.pi / 180.0)
        angle_z = angle_z * (np.pi / 180.0)

    outvector = [0.0,0.0,0.0]
    v1 = [0.0,0.0,0.0]
    v2 = [0.0,0.0,0.0]

    v1[0] = vector[0]
    v1[1] = (vector[1] * np.cos(angle_x)) + (vector[2] * np.sin(angle_x))
    v1[2] = (vector[1] * np.sin(angle_x) * -1.0) + (vector[2] * np.cos(angle_x))


    v2[0] = (v1[0] * np.cos(angle_y)) - (v1[2] * np.sin(angle_y))
    v2[1] = v1[1]
    v2[2] = (v1[0] * np.sin(angle_y)) + (v1[2] * np.cos(angle_y))

    outvector[0] = (v2[0] * np.cos(angle_z)) - (v2[1] * np.sin(angle_z))
    outvector[1] = (v2[0] * np.sin(angle_z)) + (v2[1] * np.cos(angle_z))
    outvector[2] = v2[2]

    return outvector

    # return np.array([
    #     (vector[0] * np.cos(angle_y) * np.cos(angle_z))
    #         + (vector[1] * ( (np.cos(angle_x) * np.sin(angle_z) ) + ( np.sin(angle_x) * np.sin(angle_y) * np.cos(angle_z) ) ))
    #         + (vector[2] * ( (np.sin(angle_x) * np.sin(angle_z) ) - ( np.cos(angle_x) * np.sin(angle_y) * np.cos(angle_z) ) )) ,
    #
    #     ( vector[0] * (-1.0 * np.cos(angle_y)) * np.sin(angle_z) )
    #         + (vector[1] * ( (np.cos(angle_x) * np.cos(angle_z) ) - ( np.sin(angle_x) * np.sin(angle_y) + np.sin(angle_z) ) ))
    #         + (vector[2] * ( (np.sin(angle_x) * np.cos(angle_z) ) + ( np.cos(angle_x) * np.sin(angle_y) + np.sin(angle_z) ) )) ,
    #
    #     (vector[0] * np.sin(angle_y) )
    #         + (vector[1] * (-1.0 * np.sin(angle_x)) * np.cos(angle_y))
    #         + (vector[2] * np.cos(angle_x) * np.cos(angle_y))])

def rotate_around_origin(ec, angle_x, angle_y, angle_z, degrees=False):
    """Return all vectors in frame rotated around origin by 3 vectors"""
    ecout = ec.copy()
    rotcoords = []
    if degrees:
        angle_x = angle_x * (np.pi / 180.0)
        angle_y = angle_y * (np.pi / 180.0)
        angle_z = angle_z * (np.pi / 180.0)

    for co in ecout['coordinates']:
        rotcoords.append(rotate_single_vector_around_origin(co, angle_x, angle_y, angle_z))
    ecout['coordinates'] = np.array(rotcoords)
    return ecout

def Filter(ec, remove=None, keep=None):
    """**DEPRECATED** Alias method for filter"""
#    print "F"
    filter(ec, remove, keep)

def filter(ec, remove=None, keep=None):
    """Return frame dict with elements in remove removed, or with just the elements in keep.
        Return may be empty"""
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
    """Return the minimum image convention distance between x0 and x1 with boxvector[0] as box diameter"""
    delta = np.absolute(np.subtract(x0,x1))
    delta = np.where(delta > 0.5 * boxvect[0], boxvect[0] - delta, delta)
    return np.sqrt((delta ** 2).sum(axis=-1))


def DistDist(x0, x1, boxvect):
    """Return the minimum image convention distances for all pairs x0[n], x1[n] with boxvector[0] as box diameter"""
    distvect = []
    for n, a in enumerate(x0):
        if n < (len(x1)-1):
            distvect.extend(Dist(a, np.array(x1[n+1:]), np.array(boxvect)))
    return np.array(distvect)

def GetDistSame(ec):
    """Return the distance matrix between all atoms in the supplied frame"""
    return ssd.pdist(ec['coordinates'])

def GetDistsDiff(ec1, ec2):
    """Return the distance matrix between all atoms in frame ec1 and all atoms in frame ec2"""
    return ssd.cdist(ec1['coordinates'],ec2['coordinates'])

def Center(ec):
    """**DEPRECATED** Alias method for center"""
    center(ec)

def center(ec):
    """Vector of frame geometric center"""
    summator = np.array([0.0,0.0,0.0])
    for c in ec['coordinates']:
        summator = summator + c

    summator = summator / len(ec['coordinates'])
    outcoords = []
    ec['coordinates'] = np.array(ec['coordinates'] - summator)

    return ec

def Move(ec, vect):
    """**DEPRECATED** Alias method for move"""
    move(ec, vect)

def move(ec, vect):
    """Return frame with all atoms moved my vector vect"""
    ec['coordinates'] = np.array(ec['coordinates'] + np.array(vect))
    return ec

def Write_XYZ(ec, filename, append=True):
    """**DEPRECATED** Alias method for write"""
    write(ec, filename, append=True)

def write(ec, filename, append=True):
    """Write frame to xyz file"""
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
    """Return index slice of frame from start to end"""
    ecout = ec.copy()

    ecout['elements'] = ec['elements'][start:end]
    ecout['coordinates'] = np.array(ec['coordinates'][start:end])

    return ecout

def merge(eclist):
    """Return all frames in list eclist merged, in order. Use largest box vector"""
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

def cut_into(ec1, ec2, mindist):
    """Return merged frames with all atoms in ec1 closer than *mindist* to any atom in ec2 removed"""
    ecout1 = ec1.copy()

    ecout1['coordinates'] = ec1['coordinates'].tolist()

    dist = GetDistsDiff(ec1, ec2)
    dmin = dist.min(axis=1)

    for n in range(len(dmin)-1,-1,-1):
        if dmin[n] < mindist:
            del ecout1['coordinates'][n]
            del ecout1['elements'][n]

    ecout1['coordinates'] = np.array(ecout1['coordinates'])
    return merge([ecout1, ec2])

def debox_coordinate(ref, val, box):
    """Return minum image convention distance between ref and var with box size *box*"""
    if (ref - val) > (box/2.0):
        return (val + box)
    elif (ref - val) < ((-1.0) * (box/2.0)):
        return (val - box)
    else:
        return val

def get_center_of_mass(ec):
    """Return center of mass of frame"""
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
    """Return frame with atoms placed at minimum image convention positions, with first atom used as reference, for box diameter *box*"""
    ecout = ec.copy()
    newcoordinates = [ec['coordinates'][0]]

    for c in ec['coordinates'][1:]:
        newcoordinates.append([debox_coordinate(newcoordinates[0][0], c[0], box),debox_coordinate(newcoordinates[0][1], c[1], box),debox_coordinate(newcoordinates[0][2], c[2], box)])

    ecout['coordinates'] = np.array(newcoordinates)
    return ecout

def debox_intermolecule(eclist, box, center_on=0):
    """Return frame with atoms placed at minimum image convention positions, with atom *center_on* used as reference, for box diameter *box*"""
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
