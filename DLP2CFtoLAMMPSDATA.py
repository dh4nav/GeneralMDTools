#!/usr/bin/env python

import sys
sys.path.extend(["/home/hpc/bca1/bca109/bin/GeneralMDTools", "/home/t/Source/GeneralMDTools"])

import fieldtools as ft
import iotools as iot
import random
import numpy as np


#Load last frame
last_frame = iot.DLP2HReader(fileobj=sys.argv[1])[-1]

ff = ft.FieldCollection(input_file=sys.argv[2])

list_bonds_types = []
list_bonds_indices = []

list_angles_types = []
list_angles_indices = []

list_dihedrals_types = []
list_dihedrals_indices = []

list_atoms_types = []
list_atoms_masses = []

list_inversions_types = []
list_inversions_indices = []

#list molecules_attributes


for a in last_frame:
    if a['element'] not in list_atoms_types:
        list_atoms_types.append(a['element'])
        list_atoms_masses.append(a['mass'])

print("first pass: Determining connectivity types")

for molecule in ff.itemlist[0]:
    for prop in molecule.fields:
        if prop == "bonds":
            for bond in molecule.fields["bonds"]:
                bonddict = bond.fields.copy()
                bonddict["sitename1"] = molecule.fields["atoms"][int(bonddict["index1"])-1].fields["sitename"]
                bonddict["sitename2"] = molecule.fields["atoms"][int(bonddict["index2"])-1].fields["sitename"]
                del bonddict["index1"]
                del bonddict["index2"]
                if bonddict not in list_bonds_types:
                    list_bonds_types.append(bonddict)
                list_bonds_indices.append(list_bonds_types.index(bonddict))

                print(bonddict)
                print(list_bonds_types)
                print(list_bonds_indices)

        if prop == "angles":
            for angle in molecule.fields["angles"]:
                angledict = angle.fields.copy()
                angledict["sitename1"] = molecule.fields["atoms"][int(angledict["index1"])-1].fields["sitename"]
                angledict["sitename2"] = molecule.fields["atoms"][int(angledict["index2"])-1].fields["sitename"]
                del angledict["index1"]
                del angledict["index2"]
                if angledict not in list_angles_types:
                    list_angles_types.append(angledict)
                list_angles_indices.append(list_angles_types.index(angledict))
        if prop == "dihedrals":
            for dihedral in molecule.fields["dihedrals"]:
                dihedraldict = dihedral.fields.copy()
                dihedraldict["sitename1"] = molecule.fields["atoms"][int(dihedraldict["index1"])-1].fields["sitename"]
                dihedraldict["sitename2"] = molecule.fields["atoms"][int(dihedraldict["index2"])-1].fields["sitename"]
                del dihedraldict["index1"]
                del dihedraldict["index2"]
                if dihedraldict not in list_dihedrals_types:
                    list_dihedrals_types.append(dihedraldict)
                list_dihedrals_indices.append(list_dihedrals_types.index(dihedraldict))
        if prop == "inversions":
            for inversion in molecule.fields["inversions"]:
                inversiondict = inversion.fields.copy()
                inversiondict["sitename1"] = molecule.fields["atoms"][int(inversiondict["index1"])-1].fields["sitename"]
                inversiondict["sitename2"] = molecule.fields["atoms"][int(inversiondict["index2"])-1].fields["sitename"]
                del inversiondict["index1"]
                del inversiondict["index2"]
                if inversiondict not in list_inversions_types:
                    list_inversions_types.append(inversiondict)
                list_inversions_indices.append(list_inversions_types.index(inversiondict))





print(list_atoms_types)
print(list_atoms_masses)
