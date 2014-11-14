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

datasets = []
current_dataset = -1

#Anonymous helper functions

f_str = lambda x: str(x['x'])

f_int = lambda x: int(x['x'])

f_float = lambda x: float(x['x'])

#f_tuple = lambda x: (x['fa'](x['x'].split(',')[0].strip()), x['fb'](x['x'].split(',')[1].strip()))

#f_tulist = lambda x: [x['fa'](x['x'].split(',')[0].strip()), x['fb'](x['x'].split(',')[1].strip())]


#def f_list_f(args):
#    elements = args['x'].split(',')
#    out_list = []

#    for e in elements:
#        out_list.append(args['fa'](e.strip()))

#    return out_list

#f_list = f_list_f(args)


#def f_list_np_f(args):
#    return np.array(f_list(args))

#f_list_np = f_list_np_f(args)


#converters = dict("bins"=(f_int, {}), "x"=(f_int, {}), "y"=(f_int, {})) #############################

int_keys = {"bins":1, "x":1, "y":1}
float_keys = {}
tuple_keys = {}
range_keys = {}

class MainLoop(cmd.Cmd):

    limits = []
    reduced_data = []    

    def consume(self, s):
        el = s.strip().split(';')
        if len(el) > 1:
            self.onecmd(';'.join(el[1:]))

    def get_this_command(self, s, min_args=0):
        el = s.strip().split(';')
        if len(el[0]) < min_args:
            print "Error: A minimum of " + str(min_args) + " arguments is required"
            return False

        arg_list = el[0].strip().split()[:min_args]
        dict_list = el[0].strip().split()[min_args:]

        #if len(dict_list)%2:
        #    print "Error: Additional arguments need to be supplied in pairs. Odd number of arguments found"
        #    return False

        dict_dict = {}

        for e in dict_list:

            key = e.split("=")[0].strip()
            val = e.split("=")[1].strip()
            
            dict_dict[key] = eval(val)

            #if key in int_keys:
            #    dict_dict[key] = int(val)
            #elif key in float_keys:
            #    dict_dict[key] = float(val)
            #elif key in tuple_keys:
            #    val2 = val.translate(None, '(),').strip().split()
            #    dict_dict[key] = (tuple_keys[key][0](val2[0]), tuple_keys[key][1](val2[1]))
            #################################
            #else:
            #    dict_dict[key] = val


        #for l in (dict_list[i:i+2] for i in xrange(0, len(dict_list), 2)):
        #    dict_dict[l[0]] = l[1]

        outtuple = (arg_list, dict_dict)

        return outtuple


    def do_rangereset(self, s):
        self.limits = []
        self.consume(s)


    def do_range(self, s):
        el = self.get_this_command(s, min_args = 3)

        el = el[0]

        el[0] = int(el[0])
        el[1] = float(el[1])
        el[2] = float(el[2])
    
        if el[2] < el[1]:
            el[2], el[1] = el[1], el[2]

        self.limits.append(el[0:3])
        print self.limits

        self.consume(s)


    def do_plot(self, s):
        el = self.get_this_command(s, min_args = 2)
        self.plot(el[0], el[1])
        self.consume(s)


    def do_plot0(self, s):
        el = self.get_this_command(s, min_args = 1)
        self.plot([0].extend(el[0]), el[1])
        self.consume(s)

    def plot(self, cols, argdict):
        datareduced = self.reduce_data(data, cols, self.limits)

        if len(datareduced[0]):
            pylab.plot(datareduced[0], datareduced[1], ".", **argdict)
            pylab.show(block=False)
        else:
            print "No Data"


    def do_hist(self, s):
        el = self.get_this_command(s, min_args=1)
        
        datareduced = self.reduce_data(data, el[0], self.limits)

        if len(datareduced[0]) == 0:
            print "No Data"
            return

        arg_dict = {'bins':100, 'histtype':'step', 'histtype':'step', 'normed':True}

        arg_dict.update(el[1])

        #if ’bins’ in el[1]:
        #     arg_dict['bins'] = int(el[1]['bins']

        #if ’normed’ in el[1]:
        #    arg_dict['normed'] = True

        #if 'log' in el[1]:
        #    arg_dict['norm'] = mc.LogNorm()


        pylab.hist(datareduced[0], **arg_dict)
            
            
            #if len(el) > 1:
            #    print el[1].lower().strip()
            #    if el[1].lower().strip() == "log":
            #        pylab.hist(datareduced[0], bins=bins, histtype="step")#, norm=mc.LogNorm(), normed=True)
            #    elif el[1].lower().strip() == "sw":
            #        weights = []
            #        print np.sin(datareduced[0])[0:2]
            #        print (1.0 / np.sin(datareduced[0]))[0:2]
            #        print datareduced[0][0:2]
            #        pylab.hist(datareduced[0], bins=bins, histtype="step", weights = (1.0 / np.sin(datareduced[0])))
            #else:
         #   pylab.hist(datareduced[0], bins=arg_dict['bins'], histtype="step", normed=True)




        pylab.show(block=False)
        self.consume(s)


    def do_rdf(self, s):
        el = self.get_this_command(s)

        datareduced = self.reduce_data(data, [el[0]], self.limits)

        bins = 100

        if len(datareduced[0]) == 0:

            print "No Data"
            return

        weights = np.reciprocal(np.square(datareduced[0]))

        hist, bins = np.histogram(datareduced[0], weights=weights, bins=bins)

        hist_reduced = []

        for n, h in enumerate(hist):
            hist_reduced.append(h / ((bins[n+1]**3) - (bins[n]**3)))

        bin_centers = []
        
        for n in range(len(bins)-1):
            bin_centers.append(bins[n] + ((bins[n+1]-bins[n]) * 0.5))

        pylab.plot(bin_centers, hist_reduced)
        

        #first_average_index = len(hist) - int(float(len(hist)) * 0.05)
        #average_counter = 0
        #average_summator = 0.0
        #for bin_index in range(first_average_index, len(hist)):
        #    average_counter += 1
        #    average_summator += hist[bin_index]
        #average = average_summator/float(average_counter)

        #weights_scaled = weights / average

        #pylab.figure(0)
        #pylab.hist(datareduced[0], bins=bins, histtype="step", weights=weights_scaled)#, weights = weights)
        pylab.show(block=False)

        #if "int" in el:
            #pylab.close(1)
        #    pylab.figure(1)
        #    pylab.hist(datareduced[0], bins=bins, histtype="step", cumulative=True) #,weights=weights_scaled)#, weights = weights)
        #    pylab.show(block=False)


        #pylab.figure(0)
        self.consume(s)



    def do_hist2(self, s):
        print s
        el = self.get_this_command(s, min_args=2)

        datareduced = self.reduce_data(data, el[0], self.limits)

        if len(datareduced[0]) == 0:
            print "No Data"
            return

        arg_dict = {'bins':25, 'range':[[0.0,30.0],[0.0,30.0]], 'normed':True}

        arg_dict.update(el[1])

        #if ’bins’ in el[1]:
        #     arg_dict['bins'] = int(el[1]['bins']

        #if ’normed’ in el[1]:
        #    arg_dict['normed'] = True

        #if 'log' in el[1]:
        #    arg_dict['norm'] = mc.LogNorm()


        pylab.hist2d(datareduced[0], datareduced[1], **arg_dict)

        #pylab.hist2d(datareduced[0], datareduced[1], bins=bins, normed=True, range=[[0.0,30.0],[0.0,30.0]])

        #bins = 25

#        if len(el) > 1:
#            bins = int(el[1])

        #if len(datareduced[0]):
        #    if len(el) > 2:
        #        if el[2].lower() == "log":
        #            pylab.hist2d(datareduced[0], datareduced[1], bins=bins, norm=mc.LogNorm())#, normed=True)
        #    else:
        #        pylab.hist2d(datareduced[0], datareduced[1], bins=bins, normed=True, range=[[0.0,30.0],[0.0,30.0]])
        
        pylab.colorbar()
        pylab.show(block=False)

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

    def do_load(self, s):

        global current_dataset
        global data
        global datasets

        el0 = self.get_this_command(s, min_args=1)
        
        datasets.append([[], "", ""])

        current_dataset = len(datasets)-1

        ipf = open(el0[0][0], "r")
        
        for n,l in enumerate(ipf):
            el1 = l.strip().split()
            #print n
            dbuffer = [n]

            for e in el1:
                dbuffer.append(float(e))

            datasets[-1][0].append(dbuffer)

        datasets[-1][1] = el0[0][0]
        if 'name' in el0[1]:
            datasets[-1][2] = el0[1]['name']
        else:
            datasets[-1][2] = el0[0][0]

        data = datasets[-1][0]

#        print datasets

    def do_set(self,s):

        global current_dataset
        global data
        el0 = self.get_this_command(s, min_args=1)

        num = int(el0[0][0])
        if num > 0 and num < len(datasets):
            data = datasets[num][0]

        current_dataset = num

        print "Current Dataset #" + str(num) + ": " + datasets[num][2]

    def do_list(self, s):
        for n, l in enumerate(datasets):
            print "Dataset #" + str(n) + ": " + l[2]

        print " -------\r\nCurrent Dataset #" + str(current_dataset) + ": " + datasets[current_dataset][2]

       # print data

#print data

ML = MainLoop()

ML.cmdloop()

