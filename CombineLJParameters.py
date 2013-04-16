#!/usr/bin/env python

import os, sys, math

r1 = input("First atom LJ radius or sigma: ")
e1 = input("First atom LJ epsilon: ")
r2 = input("Second atom LJ radius or sigma: ")
e2 = input("Second atom LJ epsilon: ")
c = input("Convert r or sigma? 0 = No, 1 = r -> sigma, 2 = sigma -> r ")

rc = 0.5*(r1+r2)
ec = math.sqrt(e1*e2)

ZWEIHOCHEINSECHSTEL = 1.122462048

if c == 1:
    rc = rc / ZWEIHOCHEINSECHSTEL
elif c == 2:
    rc = rc * ZWEIHOCHEINSECHSTEL

print "r or sigma: " + str(rc)
print "epsilon: " + str(ec)

