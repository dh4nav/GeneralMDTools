import iotools as iot

import AtomEnsemble as ae

rc = iot.XYZReader(fileobj="THV.xyz")

f1 = rc[0]
print f1['mass']
if 'mass' in f1:
    print "in" 
f1 = rc[-1]
print f1.main_list[1]
#f1.move([1222.0,111.0,20.2])
print f1.get_center()
for i in xrange(len(f1)):
    print f1.main_list[i]
f1.rotate_around_origin(30.0,20.0,0.0,degrees=True)
for i in xrange(len(f1)):
    print f1.main_list[i]
wx = iot.XYZWriter(fileobj="XXX.xyz", overwrite=True)
wx.write(f1)
del wx
wd = iot.DLP2CWriter(fileobj="XXX.dlpolyconf", overwrite=True)
wd.write(f1)
del wd
