import collections as col
import copy
import numpy as np

class Atom(col.MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, **kwargs):
        self.store = {"element": None, "coordinate": None, "velocity": None, "force": None, "mass": 1.0, "charge": 0.0, "molecule_index": 0}
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

    def __getitem__(self, num):
        if type(num) == str:
            return [v for a in range(len(self.main_list)) for k, v in self.main_list[a].items() if k is num ]
        elif type(num) == int:
            return self.main_list[num]
        elif type(num) == slice:

            return self.main_list[num]
        elif type(num) == list:
            [self.__getitem__(a) for a in num]
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

    def __mod__(self, num):
        """Get rich copy"""
        rt = self.copy()
        #if type(num) == str:
        #    return [v for a in range(len(self.main_list)) for k, v in self.main_list[a].items() if k is num ]
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
            raise TypeError("Supported key types: int, slice, list")

    def __setitem__(self, num, val):
        if type(num) == str:
            for a in range(len(self.main_list)):
                self.main_list[a][num] = val
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

    def append(self, obj):
        self.main_list.append(obj)

    def extend(self, obj):
        self.main_list.extend(obj)

    def insert(self, idx, obj):
        self.main_list.insert(idx, obj)

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

    def __imul__(self, val):
        self.main_list = self.main_list * val

    def __mul__(self, val):
        return self.main_list * val

    def __str__(self):
        outstring = ""
        outstring += " ".join([str(i) + "\n" for i in self.main_list])
        return outstring

#    def shift_all(coords):