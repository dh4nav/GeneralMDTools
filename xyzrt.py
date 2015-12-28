import AtomEnsemble as ae

import xyztools as xt

xr = xt.XYZReader("/tmp/test.xyz")
xs =  xt.XYZReader("/tmp/test.xyz")


#for f in xr:
#    print f
# print xr[0].copy().main_list.extend(xs.main_list)
print ".1."
xa = xr[0]
xb = xs[0]
xc = xa + xb
print xa
print xb
print xc
print ".2."
print xr[0]
#print xr[0]*3
print ".3."
