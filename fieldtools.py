from collections import OrderedDict #MutableSequence, Iterator
import copy
import math
# class FieldIterator(Iterator):
#     def __init__(self, itr):
#         self.itr = itr
#         self.pos = 0
#     def __iter__(self):
#         return self
#     def next(self):
#         self.pos += 1
#         if(len(itr))
#         return self.itr[self.pos-1]


class FieldCollection(object):
    def read_init(self, input_file):
        self.counter = 0
        self.lines = input_file.readlines()

    def read_next(self):
        self.counter += 1
        print str(self.counter-1) + ": " + self.lines[self.counter-1]
        return self.lines[self.counter-1].strip()

    """Base class representing a FIELD file"""
    def __init__(self, input_file=None):
        """Constructor
            argument input_file: optional file handle for a FIELD file"""
        self.itemlist = []
        self.title = "Title"
        self.units = "kcal"
        self.neutralchargegroups = False

        if input_file:
            with open(input_file) as f:
                self.read_init(f)
            typelist = []
            lenlist = []

            self.title = self.read_next() # comment/title
            self.units = self.read_next().split()[1] #unit
            #self.read_next() # neutral/charge groups TODO do something about neutral charge groups

            while True:
                elements = self.read_next().split()

                if elements[0].lower() == "close":
                    break

                typelist.append(elements[0].lower())
                lenlist.append(elements[1])

                if typelist[0] == "molecules":
                    self.itemlist.append(MoleculeCollection())
                    nummols = int(elements[1])
                    print "N"+str(nummols)
                    for n in range(nummols):
                        print "m"
                        self.itemlist[-1].molecules.append(Molecule())
                        self.itemlist[-1].molecules[-1].name = self.read_next() # molecule name
                        self.itemlist[-1].molecules[-1].nummols = self.read_next().split()[1]
                        while True:
                            elements = self.read_next().split()
                            elements[0] = elements[0].lower()
                            if elements[0] == "atoms":
                                for i in range(int(elements[1])):
                                    self.itemlist[-1].molecules[-1].fields['atoms'].append(atom(input_file=self.read_next()))
                            # TODO add shell directive
                            elif elements[0] == "bonds":
                                for i in range(int(elements[1])):
                                    self.itemlist[-1].molecules[-1].fields['bonds'].append(bond(input_file=self.read_next()))
                            # elif elements[0] == "constraints":
                            #     for i in range(int(elements[1])):
                            #         self.itemlist[-1].molecules[-1].fields['constraints'].append(constraint(input_file=self.read_next()))
                            # TODO add pmf
                            elif elements[0] == "angles":
                                for i in range(int(elements[1])):
                                    self.itemlist[-1].molecules[-1].fields['angles'].append(angle(input_file=self.read_next()))
                            elif elements[0] == "dihedrals":
                                for i in range(int(elements[1])):
                                    self.itemlist[-1].molecules[-1].fields['dihedrals'].append(dihedral(input_file=self.read_next()))
                            elif elements[0] == "inversions":
                                for i in range(int(elements[1])):
                                    self.itemlist[-1].molecules[-1].fields['inversions'].append(inversion(input_file=self.read_next()))
                            # elif elements[0] == "rigid":
                            #     for i in range(int(elements[1])):
                            #         self.itemlist[-1].molecules[-1].fields['rigid'].append(atom(input_file=self.read_next()))
                            # elif elements[0] == "teth":
                            #     for i in range(int(elements[1])):
                            #         self.itemlist[-1].molecules[-1].fields['teth'].append(tether(input_file=self.read_next()))
                            elif elements[0] == "finish":
                                break
                    typelist.pop()
                    lenlist.pop()
                elif typelist[0] == 'vdw':
                    print "v"
                    self.itemlist.append(vdws())
                    for n in range(int(lenlist[0])):
                        self.itemlist[-1].fields.append(vdw_special(self.read_next()))

                #
                # else:
                #     line = f.readline.strip().split()
                #     typelist.append(line[0].lower())
                #     lenlist.append(int(line[1]))


    def __str__(self):
        returnstring = [self.title]
        returnstring.extend(["UNITS " + self.units])
        if self.neutralchargegroups:
            returnstring.extend("SOMETHING")
        else:
            returnstring.extend([" "])

        for item in self.itemlist:
            returnstring.extend([item.__str__()])

        return "\n".join(returnstring)

    def __len__(self):
        return len(self.itemlist)

    def __getitem__(self, key):
        return self.itemlist[key]

    def __setitem__(self, key, value):
        self.itemlist[key] = value

    def __delitem__(self, key):
        del self.itemlist[key]

    def __iter__(self):
        return self.itemlist.__iter__()


class MoleculeCollection(object):
    def __init__(self):
        self.molecules = []

    def __str__(self):
        nummols = 0
        for item in self.molecules:
            nummols += int(item.nummols)

        returnstring = ["MOLECULES " + str(nummols)]

        for item in self.molecules:
            returnstring.extend([item.__str__()])

        return "\n".join(returnstring)

    def __len__(self):
        return len(self.molecules)

    def __getitem__(self, key):
        return self.molecules[key]

    def __setitem__(self, key, value):
        self.molecules[key] = value

    def __delitem__(self, key):
        del self.molecules[key]

    def __iter__(self):
        return self.molecules.__iter__()


class Molecule(object):
    def __init__(self):

        self.fields = OrderedDict([('atoms', []), ('shells', []), ('bonds', []), ('constraints', []), ('pmf', []), ('angles', []), ('dihedrals', []), ('inversions', []), ('rigids', []), ('tethers', [])])
        self.nummols = 1
        self.name = "Name"

    def __str__(self):
        returnstring = [self.name + "\nnummols " + str(self.nummols)]

        returnstring += ["atoms " + str(len(self.fields['atoms']))]
        for item in self.fields['atoms']:
            returnstring.extend([item.__str__()])

        if self.fields['shells']:
            returnstring += ["shell " + str(len(self.fields['shells']))]
            for item in self.fields['shells']:
                returnstring.extend([item.__str__()])

        if self.fields['bonds']:
            returnstring += ["bonds " + str(len(self.fields['bonds']))]
            for item in self.fields['bonds']:
                returnstring.extend([item.__str__()])

        if self.fields['constraints']:
            returnstring += ["constraints " + str(len(self.fields['constraints']))]
            for item in self.fields['constraints']:
                returnstring.extend([item.__str__()])

        if self.fields['pmf']:
            returnstring += ["pmf " + str(len(self.fields['pmf']))]
            for item in self.fields['pmf']:
                returnstring.extend([item.__str__()])

        if self.fields['angles']:
            returnstring += ["angles " + str(len(self.fields['angles']))]
            for item in self.fields['angles']:
                returnstring.extend([item.__str__()])

        if self.fields['dihedrals']:
            returnstring += ["dihedrals " + str(len(self.fields['dihedrals']))]
            for item in self.fields['dihedrals']:
                returnstring.extend([item.__str__()])

        if self.fields['inversions']:
            returnstring += ["inversions " + str(len(self.fields['inversions']))]
            for item in self.fields['inversions']:
                returnstring.extend([item.__str__()])

        if self.fields['rigids']:
            returnstring += ["rigid " + str(len(self.fields['rigids']))]
            for item in self.fields['rigids']:
                returnstring.extend([item.__str__()])

        if self.fields['tethers']:
            returnstring += ["teth " + str(len(self.fields['tethers']))]
            for item in self.fields['tethers']:
                returnstring.extend([item.__str__()])

        returnstring.extend(["finish"])

        return "\n".join(returnstring)

class Molecule_Description_Item_Base(object):

    def __init__(self, input_file=None, factory=None, minimum_items=0):
        if factory:
            if input_file:
                listelements = []

                if type(input_file) == str:
                    listelements = input_file.strip().split()

                elif type(input_file) == str:
                    with open(input_file, "r") as f:
                        listelements = self.read_next().split()

            else:
                listelements = [''] * len(factory)

            if len(listelements) < len(factory):
                if len(listelements) < minimum_items:
                    raise ValueError("Fields Missing")
                else:
                    factory = factory[:len(listelements)]

            elif len(factory) < len(listelements):
                for n in range(1, 1 + len(listelements) - len(factory)):
                    factory.append("var"+str(n))

            self.fields = OrderedDict(zip(factory, listelements))
        else:
            raise ValueError("Factory missing")

    def __str__(self):
        return " ".join(self.fields.values())

class atom(Molecule_Description_Item_Base):
    def __init__(self, input_file=None):
        Molecule_Description_Item_Base.__init__(self, input_file=input_file, factory=['sitename', 'weight', 'charge', 'repetitions', 'frozen', 'groupnumber'], minimum_items=4)


class bond(Molecule_Description_Item_Base):
    def __init__(self, input_file=None):
        Molecule_Description_Item_Base.__init__(self, input_file=input_file, factory=['key', 'index1', 'index2'], minimum_items=3)


class angle(Molecule_Description_Item_Base):
    def __init__(self, input_file=None):
        Molecule_Description_Item_Base.__init__(self, input_file=input_file, factory=['key', 'index1', 'index2', 'index3'], minimum_items=4)


class dihedral(Molecule_Description_Item_Base):
    def __init__(self, input_file=None):
        Molecule_Description_Item_Base.__init__(self, input_file=input_file, factory=['key', 'index1', 'index2', 'index3', 'index4'], minimum_items=5)

class inversion(Molecule_Description_Item_Base):
    def __init__(self, input_file=None):
        Molecule_Description_Item_Base.__init__(self, input_file=input_file, factory=['key', 'index1', 'index2', 'index3', 'index4'], minimum_items=5)

# class rigid():
#     def __init__(self, input_file=None):
#         #TODO convert to list for variable number of sites
#         self.fields = OrderedDict([('m','0'),('index1', '1.0'),('index2', '0.0'), ('index3', '0.0'), ('index4', '1'), ('var1', '1'), ('var2', '0')])
#

class tether(Molecule_Description_Item_Base):
    def __init__(self, input_file=None):
        Molecule_Description_Item_Base.__init__(self, input_file=input_file, factory=['key', 'index1'], minimum_items=2)


class vdws(object):
    def __init__(self):
        self.fields = []
        self.bases = []

    def __str__(self):
        outstring = []
        outelements = []

        for n, e in enumerate(self.bases):
            for m, f in enumerate(self.bases[n:]):
                outstring.append(e.element + " " + f.element + " LJ " +  str(math.sqrt(float(e.epsilon) + float(f.epsilon))) + " " + str((float(e.sigma) + float(f.sigma))/2.0))
                outelements.append((e.element, f.element))

        for n, e in enumerate(self.fields):
            if (e.element1, e.element2) in outelements:
                outstring[outelements.index((e.element1, e.element2))] = e.__str__()
            elif (e.element2, e.element1) in outelements:
                outstring[outelements.index((e.element2, e.element1))] = e.__str__()
            else:
                outstring.append(e.__str__())

        outstring = ["vdw " + str(len(outstring))] + outstring

        return "\n".join(outstring)

class vdw_LJ_base(object):
    def __init__(self, input_file=None):
        self.element = ""
        self.epsilon = 0.0
        self.sigma = 0.0

        if type(input_file) == str:
            elements = input_file.strip().split()
            self.element = elements[0]
            self.epsilon = elements[1]
            self.sigma = elements[2]


class vdw_special(object):
    def __init__(self, input_file=None):
        self.element1 = ""
        self.element2 = ""
        self.key = ""
        self.variables = []

        if type(input_file) == str:
            elements = input_file.strip().split()
            self.element1 = elements[0]
            self.element2 = elements[1]
            self.key = elements[2]
            self.variables = copy.copy(elements[3:])

    def __str__(self):
        out = []
        out.append(self.element1)
        out.append(self.element2)
        out.append(self.key)
        out.extend(self.variables)
        return " ".join(out)
