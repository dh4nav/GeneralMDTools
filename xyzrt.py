import AtomEnsemble as ae

import xyztools as xt

xr = xt.XYZReader("THV.xyz")
xs =  xt.XYZReader("THV.xyz")


#for f in xr:
#    print f
# print xr[0].copy().main_list.extend(xs.main_list)
print ".1."
xa = xr[0]
xb = xs[0]
xd = xs[0]
xe = xs[0]
xc = xa[:4] + xb + xa[4:]
print xa
print xb
print xc
xf = xb * 5
print xf
print ".x."

# xa *= 3
# print xa
# print ".2."
# print (xa.filter(keep=["OH", "HH"]))
# print xa
# print xb.filter(remove=["OH", "HH"])
# #print xr[0]*3
# print ".3."
