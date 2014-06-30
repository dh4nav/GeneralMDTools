#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pylab
import cmd
import sys
import matplotlib.colors as mc


#limits = []
datarows = []
datareduced = []
data = []



class MainLoop(cmd.Cmd):

    limits = []
    reduced_data = []    

    def consume(self, s):
        el = s.strip().split(';')
        if len(el) > 1:
            self.onecmd(';'.join(el[1:]))

    def get_this_command(self, s):
        el = s.strip().split(';')
        print el[0].strip().split()
        return el[0].strip().split()

    def do_range(self, s):
        el = self.get_this_command(s)

        if len(el) == 0:
            self.limits = []
            self.consume(s)

        elif el[0].lower().strip() == "reset":
            self.limits = []
            self.consume(s)

        else:
            el[0] = int(el[0])
            el[1] = float(el[1])
            el[2] = float(el[2])
    
            if el[2] < el[1]:
                el[2], el[1] = el[1], el[2]

            self.limits.append(el[0:3])
            print self.limits

        self.consume(s)

    def do_plot(self, s):
        el = self.get_this_command(s)

        if len(el) == 1:
            el = [0, el[0]]

        datareduced = self.reduce_data(data, el, self.limits)

        if len(datareduced[0]):

            pylab.plot(datareduced[0], datareduced[1], ".")
            pylab.show(block=False)

        else:
            print "No Data"

        self.consume(s)

    def do_hist(self, s):
        el = self.get_this_command(s)

        datareduced = self.reduce_data(data, [el[0]], self.limits)

        bins = 100

#        if len(el) > 1:
#            bins = int(el[1])

        if len(datareduced[0]):
            if len(el) > 1:
                print el[1].lower().strip()
                if el[1].lower().strip() == "log":
                    pylab.hist(datareduced[0], bins=bins, histtype="step")#, norm=mc.LogNorm(), normed=True)
                elif el[1].lower().strip() == "sw":
                    weights = []
                    print np.sin(datareduced[0])[0:2]
                    print (1.0 / np.sin(datareduced[0]))[0:2]
                    print datareduced[0][0:2]
                    pylab.hist(datareduced[0], bins=bins, histtype="step", weights = (1.0 / np.sin(datareduced[0])))
            else:
                pylab.hist(datareduced[0], bins=bins, histtype="step")#, normed=True)



        else:
            print "No Data"

        pylab.show(block=False)
        self.consume(s)

    def do_hist2(self, s):
        el = self.get_this_command(s)

        datareduced = self.reduce_data(data, [el[0], el[1]], self.limits)

        bins = 50

#        if len(el) > 1:
#            bins = int(el[1])

        if len(datareduced[0]):
            if len(el) > 2:
                if el[2].lower() == "log":
                    pylab.hist2d(datareduced[0], datareduced[1], bins=bins, norm=mc.LogNorm())#, normed=True)
            else:
                pylab.hist2d(datareduced[0], datareduced[1], bins=bins)#, normed=True)
            pylab.colorbar()
            pylab.show(block=False)

        else:
            print "No Data"

        self.consume(s)


    def do_average(self, s):
        el = self.get_this_command(s)

        datareduced = self.reduce_data(data, [el[0]], self.limits)

        adder = 0.0
        counter = 0.0

        for d in datareduced[0]:
            adder += d
            counter += 1.0

        print str(adder/counter)

    def do_quit(self, s):
        return True

    def do_exit(self, s):
        return True

    def reduce_data(self, alldata, rows, limits):
        reduced_data = []
        for e in rows:
            reduced_data.append([])

        for m, d in enumerate(alldata):
            if self.check_limits(d, limits):
               for n, r in enumerate(rows):
                   reduced_data[n].append(d[int(r)])
        return reduced_data


    def check_limits(self, data, limits):
        if len(limits):
            for l in limits:
                if data[l[0]] < l[1]:
                    return False
                elif data[l[0]] > l[2]:
                    return False
        return True

ipf = open(sys.argv[1])

for n,l in enumerate(ipf):
    el = l.strip().split()
    #print n
    dbuffer = [n]
    for e in el:
        dbuffer.append(float(e))

    data.append(dbuffer)

#print data

ML = MainLoop()

ML.cmdloop()
