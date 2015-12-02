import collections as col
import copy

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
