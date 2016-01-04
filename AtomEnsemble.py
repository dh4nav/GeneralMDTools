import collections as col
import copy
import numpy as np
import scipy.spatial.distance as ssd

class Atom(col.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, **kwargs):
        self.store = dict() #{
            #"element": None,
            #"coordinate": None,
            #"velocity": None,
            #"force": None,
            #"mass": 1.0,
            #"charge": 0.0,
            #"molecule_index": 0}
        self.nplist = ["coordinate", "velocity", "force"]
        for key in kwargs:
            self.__setitem__(key, kwargs[key])

    def __getitem__(self, key):
        #print self.store.keys()
        return self.store[key]

    def __setitem__(self, key, value):
        if key in self.nplist:
            value = np.array(value)
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __str__(self):
        return self.store.__str__()

    def copy(self):
        return copy.deepcopy(self)


class AtomEnsemble(col.MutableSequence):

    def __init__(self):
        self.main_list = []
        self.boxvector = 0.0
        self.filename = ""
        self.framenumber = 0
        self.header = ""

    def __iter__(self):
        return self.main_list.__iter__()

    def __len__(self):
        return self.main_list.__len__()

    def __delitem__(self, num):
        if type(num) == str:
            for a in range(len(self.main_list)):
                del self.main_list[a][num]
        elif type(num) == int:
            del self.main_list[num]
        else:
            raise TypeError("Supported key types: int, str")

        return self

    def get_pure_list(self, num):
        if type(num) == str:
            return [v for a in range(len(self.main_list)) for k, v in self.main_list[a].items() if k is num]
        elif type(num) == int:
            self.main_list = self.main_list[num]
            return self.main_list
        elif type(num) == slice:

            return self.main_list[num]
        elif type(num) == list:
            return  [self.__getitem__(a) for a in num]
        else:
            raise TypeError("Supported key types: int, str, slice, list")

    # def __div__(self, num):
    #     """Get numpyified copy"""
    #     if type(num) == str:
    #         return [v for a in range(len(self.main_list)) for k, v in self.main_list[a].items() if k is num ]
    #     elif type(num) == int:
    #         return self.main_list[num]
    #     elif type(num) == slice:
    #
    #         return self.main_list[num]
    #     elif type(num) == list:
    #         [self.__getitem__(a) for a in num]
    #     else:
    #         raise TypeError("Supported key types: int, str, slice, list")

    def __contains__(self, item):
        if len(self.main_list):
            return self.main_list[0].__contains__(item)
        else:
            return False

    def __getitem__(self, num):
        """Get rich copy"""

        if type(num) == str:
            ra = xrange(len(self.main_list))
            return [v for a in ra for k, v in self.main_list[a].items() if k is num]
        if type(num) == int:
            rt = self.copy()
            rt.main_list = rt.main_list[num]
            return rt
        elif type(num) == slice:
            rt = self.copy()
            rt.main_list = rt.main_list[num]
            return rt
        elif type(num) == list:
            rt = self.copy()
            rt.main_list = [rt.__getitem__(a) for a in num]
            return rt
        else:
            raise TypeError("Supported key types: int, str, slice, list")

        return self

    def __setitem__(self, num, val):
        if type(num) == str:
            for a in range(len(self.main_list)):
                self.main_list[a][num] = val[a]
        elif type(num) == int:
            self.main_list[num] = val
        elif type(num) == dict:
            for k in val:
                self.main_list[a][k] = val[k]
        elif type(num) == Atom:
            for k in val:
                self.main_list[a][k] = val[k]
        else:
            raise TypeError("Supported key types: int, str, dict, Atom")

        return self

    def append(self, obj):
        self.main_list.append(obj)
        return self

    def extend(self, obj):
        self.main_list.extend(obj)
        return self

    def insert(self, idx, obj):
        self.main_list.insert(idx, obj)
        return self

    def copy(self):
        return copy.deepcopy(self)

    def __iadd__(self, obj):
        if type(obj) == AtomEnsemble:
            self.main_list.extend(obj.main_list)
        elif type(obj) == list:
            self.main_list.extend(obj)
        elif type(obj) == Atom:
            self.main_list.append(obj)
        elif type(obj) == dict:
            self.main_list.append(Atom(**obj))
        else:
            raise TypeError("Supported types: AtomEnsemble, list, dict, Atom")

        return self

    def __add__(self, obj):
        #print obj
        #print self
        oa = self.copy()
        if type(obj) == AtomEnsemble:
            oa.main_list.extend(obj.main_list)
            return oa
            #return self.copy().main_list.extend(obj.main_list)
        elif type(obj) == list:
            oa.main_list.extend(obj)
            return oa
            #return self.copy().main_list.extend(obj)
        elif type(obj) == Atom:
            oa.main_list.append(obj)
            return oa
            #return self.copy().main_list.append(obj)
        elif type(obj) == dict:
            oa.main_list.append(Atom(**obj))
            return oa
            #return self.copy().main_list.append(Atom(**obj))
        else:
            raise TypeError("Supported types: AtomEnsemble, list, dict, Atom")

    def __radd__(self, obj):
        #print obj
        #print self
        oa = self.copy()
        if type(obj) == AtomEnsemble:
            oa.main_list.insert(0, obj.main_list)
            return oa
            #return self.copy().main_list.extend(obj.main_list)
        elif type(obj) == list:
            print "."
            print oa
            print ".."
            print oa.main_list
            print "..."
            oa.main_list.reverse()
            print oa.main_list
            print "...."
            obj.main_list.reverse()
            oa.main_list.append(obj.main_list)
            oa.main_list.reverse()
            print oa.main_list
            #reverse(reverse(oa.main_list).append(reverse(obj.main_list)))
            #oa.main_list.insert(0, obj)
            return oa
            #return self.copy().main_list.extend(obj)
        elif type(obj) == Atom:
            oa.main_list.insert(0, obj)
            return oa
            #return self.copy().main_list.append(obj)
        elif type(obj) == dict:
            oa.main_list.insert(0, Atom(**obj))
            return oa
            #return self.copy().main_list.append(Atom(**obj))
        else:
            raise TypeError("Supported types: AtomEnsemble, list, dict, Atom")

    def __imul__(self, val):
        self.main_list = self.main_list * val
        return self

    def __mul__(self, val):
        print "m"
        cp = self.copy()
        cp.main_list = cp.main_list * val
        return cp

    def __str__(self):
        outstring = ""
        outstring += " ".join([str(i) + "\n" for i in self.main_list])
        return outstring

    def filter(self, keep=None, remove=None):
        #cp = self.copy()

        counter = 0
        while counter < len(self.main_list):
            if remove:
                if self.main_list[counter]['element'] in remove:
                    del self.main_list[counter]
                    counter -= 1
            elif keep:
                if self.main_list[counter]['element'] not in keep:
                    del self.main_list[counter]
                    counter -= 1
            counter += 1

        #return cp

    # def alter_property(self, value, range=None, property="coordinate"):
    #     property_type = list()
    #     value_type = list()
    #
    #     flag = True
    #     while flag:
    #         try:
    #             property_type.append(self.main_list[0][property])
    #         except:
    #             flag = False
    #
    #
    #     flag = True
    #     while flag:
    #         try:
    #             value_type.append(value)
    #         except:
    #             flag = False

    def center(self, center_index=None, center_coordinates=None):
        if center_index != None:
            center_coordinates = self[center_index]['coordinate']
        elif center_coordinates != None:
            center_coordinates = np.array(center_coordinates)
        else:
            center_coordinates = self.get_center()
        self['coordinate'] = np.subtract(np.array(self['coordinate']), center_coordinates)

    def move(self, coords):
        self['coordinate'] = np.add(np.array(self['coordinate']), np.array(coords))

    def accellerate(self, magnitude=None, direction=None, zero=True):
        if magnitude == None:
            magnitude = 1.0
        if direction == None:
            direction = [0.0, 0.0, 0.0]
        acc_vect = np.divide(np.array(direction), np.linalg.norm(direction))
        acc_vect = np.multiply(acc_vect, magnitude)
        if zero:
            self['velocity'] = [acc_vect] * len(self['element'])
        else:
            self['velocity'] = np.add(np.array(self['velocity']), acc_vect)

    def get_center(self): #, weigh_by_mass=False):
        coords = np.array(self['coordinate'])
        return coords.sum(0)/len(coords.sum(1))

    def rotate_vector_around_origin(self, vector, angle_x, angle_y, angle_z, degrees=False):
        """Return vector rotated around origin by 3 angles"""

        if degrees:
            angle_x = angle_x * (np.pi / 180.0)
            angle_y = angle_y * (np.pi / 180.0)
            angle_z = angle_z * (np.pi / 180.0)

        outvector = [0.0, 0.0, 0.0]
        v1 = [0.0, 0.0, 0.0]
        v2 = [0.0, 0.0, 0.0]

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

    def rotate_around_origin(self, angle_x, angle_y, angle_z, degrees=False):
        """Return all vectors in frame rotated around origin by 3 vectors"""
        rotcoords = []
        for co in self['coordinate']:
            rotcoords.append(self.rotate_vector_around_origin(co, angle_x, angle_y, angle_z, degrees=degrees))
        self['coordinate'] = np.array(rotcoords)

    def get_enclosing_radius(self):
        coords = self['coordinate']
        norms = np.linalg.norm(coords, axis=1)
        maxindex = np.argmax(norms)
        return np.linalg.norm(coords[maxindex])

    def get_bounding_box(self):
        coords_flat = np.array(self['coordinate']).flatten()
        cmax = coords_flat.max()
        cmin = coords_flat.min() * -1.0

        if cmax > cmin:
            return cmax
        else:
            return cmin

    def intersect(self, other, mindist=2.0):
        o2 = other.copy()
        dmatrix = ssd.cdist(np.array(self['coordinate']), np.array(o2['coordinate']))
        dmatrix = dmatrix.min(axis=0)
        dellist = []
        for n, e in enumerate(dmatrix):
            if e < mindist:
                dellist.append(n)
        for e in reversed(dellist):
            del o2[e]
        self += o2

    def intersect_molecules(self, other, mindist=2.0, mollen=1):
        o2 = other.copy()
        dmatrix = ssd.cdist(np.array(self['coordinate']), np.array(o2['coordinate']))
        dmatrix = dmatrix.min(axis=0)
        dellist = []
        skipflag = False
        for n, e in enumerate(dmatrix):
            if n%mollen == 0:
                skipflag = False
            if skipflag:
                continue
            if e < mindist:
                dellist.extend(range(n-(n%mollen), n+mollen-((n%mollen))))
                skipflag = True
        #print dellist
        for e in reversed(dellist):
            del o2[e]
        self += o2

    def get_chains(self, dist=2.0):

        dmatrix = ssd.cdist(np.array(self['coordinate']), np.array(self['coordinate']))
        chains = range(1, len(self.main_list)+1)
        current_net = 0

        for n, e in enumerate(dmatrix):
            current_net = n+1
            for m, f in enumerate(e):
                if n == m:
                    continue
                else:
                    if f < dist:
                        if chains[m] == current_net:
                            continue
                        else:
                            if chains[m] < current_net:
                                for i in range(len(chains)):
                                    if chains[i] == current_net:
                                        chains[i] = chains[m]
                                current_net = chains[m]
                            else:
                                for i in range(len(chains)):
                                    if chains[i] == chains[m]:
                                        chains[i] = current_net

        counter = 0
        for i in range(1, len(chains)+1):
            if i in chains:
                counter += 1

        return counter

    def get_approaches(self, species_a, species_b, dmin, dmax):
        #copy self and filter to get desired groups of atoms
        if type(species_a) != list:
            species_a = [species_a]
        if type(species_b) != list:
            species_b = [species_b]
        copy_a = self.copy()
        copy_b = self.copy()
        copy_a.filter(keep=species_a)
        copy_b.filter(keep=species_b)

        #get distmatrix and filter out pairs that match the criteria
        dmatrix = ssd.cdist(np.array(copy_a['coordinate']), np.array(copy_b['coordinate']))
        pairlist = []
        for n, e in enumerate(dmatrix):
            for m, f in enumerate(e[:n]):
                if n == m:
                    continue
                elif (f < dmax) and (f > dmin):
                    pairlist.append((n, m))

        # get two lists (one for each species) that have the original index
        # on a position equivalent to the index in the filered lists
        translation_list_a = []
        translation_list_b = []

        for n, e in enumerate(self['element']):
            if e in species_a:
                translation_list_a.append(n)
            if e in species_b:
                translation_list_b.append(n)

        final_pair_list = []

        # translate back using these lists
        for e in pairlist:
            final_pair_list.append((translation_list_a[e[0]], translation_list_b[e[1]]))

        return final_pair_list
