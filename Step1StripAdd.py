#import AtomEnsemble as ae
#import os, sys
import iotools as iot
import random
import numpy as np

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

#print last_frame['elements']

#Prepare last frame
last_frame.filter(remove=["SD", "CD", "OD"])
last_frame.center()
lf_radius = last_frame.get_enclosing_radius()
print lf_radius
#Prepare addcluster
add_cluster.center()
add_cluster.rotate_around_origin(frand(maxval=360.0), frand(maxval=360.0),
                                 frand(maxval=360.0), degrees=True)
movevect = add_cluster.rotate_vector_around_origin([lf_radius+20.0, 0.0, 0.0],
                                                   frand(maxval=360.0),
                                                   frand(maxval=360.0),
                                                   frand(maxval=360.0),
                                                   degrees=True)

print movevect
add_cluster.move(movevect)

new_cluster = last_frame + add_cluster
print "\n\n"
print np.array(new_cluster['coordinate'])
