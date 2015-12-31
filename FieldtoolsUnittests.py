import fieldtools as ft

f = ft.FieldCollection(input_file="FIELD_vdw_plus")
f.append_molecule(input_file="FIELD_Mol_BI", nummols=1)
f.append_molecule(input_file="FIELD_Mol_NO3", nummols=1)
f.append_molecule(input_file="FIELD_Mol_BI", nummols=1)
print f
