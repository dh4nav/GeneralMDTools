import collections as col
import copy
import numpy as np

class AtomEnsemble(col.Iterable, col.MutableSequence):

    def __init__(self):
        self.main_list = []

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
        else:
            raise TypeError("Supported key types: int, str")

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
        elif type(obj) == dict:
            self.main_list.append(obj)
        else:
            raise TypeError("Supported types: AtomEnsemble, list, dict")

    def __add__(self, obj):
        if type(obj) == AtomEnsemble:
            return self.copy().main_list.extend(obj.main_list)
        elif type(obj) == list:
            return self.copy().main_list.extend(obj)
        elif type(obj) == dict:
            return self.copy().main_list.append(obj)
        else:
            raise TypeError("Supported types: AtomEnsemble, list, dict")

    def __imul__(self, val):
        self.main_list = self.main_list * val

    def __mul__(self, val):
        return self.main_list * val

    def __str__(self):
        outstring = ""
        [outstring = outstring + str(i) + "\n" for i in self.main_list]
        return outstring

    def shift_all(coords):
