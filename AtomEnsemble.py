import collections as col
import copy
import numpy as np

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
        rt = self.copy()
        if type(num) == str:
            ra = xrange(len(self.main_list))
            return [v for a in ra for k, v in self.main_list[a].items() if k is num]
        if type(num) == int:
            rt.main_list = rt.main_list[num]
            return rt
        elif type(num) == slice:
            rt.main_list = rt.main_list[num]
            return rt
        elif type(num) == list:
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
        cp = self.copy()

        counter = 0
        while counter < len(cp.main_list):
            if remove:
                if cp.main_list[counter]['element'] in remove:
                    del cp.main_list[counter]
                    counter -= 1
            elif keep:
                if cp.main_list[counter]['element'] not in keep:
                    del cp.main_list[counter]
                    counter -= 1
            counter += 1

        return cp

    def alter_property(self, value, range=None, property="coordinate"):
        property_type = list()
        value_type = list()

        flag = True
        while flag:
            try:
                property_type.append(self.main_list[0][property])
            except:
                flag = False


        flag = True
        while flag:
            try:
                value_type.append(value)
            except:
                flag = False



    def center(self, center_index=None, center_coordinates=None):
        if center_index != None:
            center_coordinates = self.main_list[center_index]['coordinate']
        center_coordinates = np.array(center_coordinates)
        self['coordinate'] = np.subtract(np.array(self['coordinate']), center_coordinates)

    def move(self, coords):
        self['coordinate'] = np.add(np.array(self['coordinate']), np.array(coords))
