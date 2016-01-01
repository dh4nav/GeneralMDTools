#import AtomEnsemble as ae
#import os, sys
import fieldtools as ft
import iotools as iot
import random
#import numpy as np

def frand(minval=0.0, maxval=1.0):
    return random.uniform(minval, maxval)

#seed random
random.seed()

#Get index
#index = int(sys.argv[1])

#Load last frame
last_frame = iot.DLP2HReader(fileobj="HIk")[-1]

#Load add cluster
add_cluster = iot.XYZReader(fileobj="AddCluster.xyz")[-1]

#Prepare last frame
last_frame.filter(remove=["SD", "CD", "OD"])
last_frame.center()
if 'velocity' not in last_frame:
    last_frame['velocity'] = [[0.0, 0.0, 0.0]] * len(last_frame['element'])
lf_radius = last_frame.get_enclosing_radius()
print lf_radius
#Prepare addcluster
add_cluster.center()
if 'velocity' not in add_cluster:
    add_cluster['velocity'] = [[0.0, 0.0, 0.0]]  * len(add_cluster['element'])
add_cluster.rotate_around_origin(frand(maxval=360.0), frand(maxval=360.0),
                                 frand(maxval=360.0), degrees=True)

movevect = add_cluster.rotate_vector_around_origin([lf_radius+20.0, 0.0, 0.0],
                                                   frand(maxval=360.0),
                                                   frand(maxval=360.0),
                                                   frand(maxval=360.0),
                                                   degrees=True)

add_cluster.move(movevect)
add_cluster.accellerate(magnitude=-0.001, direction=movevect)

#Join clusters
new_cluster = last_frame + add_cluster

#construct field file
ff = ft.FieldCollection(input_file="FIELD_vdw_minus")
for atom in new_cluster['element']:
    if atom == "BI":
        ff.append_molecule("FIELD_Mol_BI")
    elif atom == "OI":
        ff.append_molecule("FIELD_Mol_OI")
    elif atom == "OH":
        ff.append_molecule("FIELD_Mol_OH")
    elif atom == "NN":
        ff.append_molecule("FIELD_Mol_NO3")
    elif atom == "SD":
        ff.append_molecule("FIELD_Mol_DMSO")
    elif atom == "OW":
        ff.append_molecule("FIELD_Mol_H2O")

field_out = open("FIELD", "w")
field_out.write(str(ff))
field_out.close()

field_out = open("FIELD1", "w")
field_out.write(str(ff))
field_out.close()

conf_writer = iot.DLP2CWriter(fileobj="CONFIG", overwrite=True)
conf_writer.write(new_cluster)
del conf_writer

conf_writer = iot.DLP2CWriter(fileobj="CONFIG1", overwrite=True)
conf_writer.write(new_cluster)
del conf_writer

#start step2