#!/usr/bin/python

import xyzt
import numpy as np
np.set_printoptions(suppress = True)
ipf = xyzt.GetXYZIter("unitvector.xyz")
lf = ipf.get_last_frame()
#print lf
rx = xyzt.rotate_around_origin(lf.copy(), 90, 0, 0)
#print xyzt.rotate_around_origin(lf, 180, 180, 0)
ry = xyzt.rotate_around_origin(lf.copy(), 0, 90, 0)
rz = xyzt.rotate_around_origin(lf.copy(), 0, 0, 90)

print lf['coordinates'][0] ,
print lf['coordinates'][1] ,
print lf['coordinates'][2] 

print rx['coordinates'][0] ,
print rx['coordinates'][1] ,
print rx['coordinates'][2] 

print ry['coordinates'][0] ,
print ry['coordinates'][1] ,
print ry['coordinates'][2] 

print rz['coordinates'][0] ,
print rz['coordinates'][1] ,
print rz['coordinates'][2] 


