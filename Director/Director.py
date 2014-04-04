#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse as ap
import os, sys, datetime
import unittest as ut
import ConfigParser as cp
import subprocess as sb

#if mainargs.test:
#    #sys.argv = sys.argv[:1]
#    suite = ut.TestLoader().loadTestsFromTestCase(TestsHighLevel)
#    ut.TextTestRunner(verbosity=2).run(suite)
    #ut.main()
#    exit()

current_state = "Initial"
loghandle = False

def run_subprocess(config_object, state, option, log_handle, basedir):

    command = config_object.get(state, option)
    if log_handle:
        log_handle.write("--- State: " + state + " ; Option " + option + " @ " + str(datetime.datetime.now()) + "\n----- Command: " + command + "\n----- Output:\n")
    command_list = command.strip().split()
    if os.path.isabs(command_list[0]) == False:
        command_list[0] = os.path.join(basedir, command_list[0])
        command = " ".join(command_list)
    try:
        process_output = sb.check_output(command_list, shell=True)
    except sb.CalledProcessError, e:
        if log_handle:
            log_handle.write(e.output + "\n----- Process ended with return code " + str(e.returncode) + "@ " + str(datetime.datetime.now()) + "\n")
            return True
    else:
        if log_handle:
            log_handle.write(process_output + "\n----- Process ended with return code 0 @ " + str(datetime.datetime.now()) + "\n")
            return False


if __name__ == '__main__':
    parser = ap.ArgumentParser(
        description="Director Script for the Kawska-Zahn Method Toolchain",
        prog=sys.argv[0])

    parser.add_argument("-d", "--directory", help="Working Directory. Default is current directory", default=os.getcwd())
    parser.add_argument("-c", "--configuration", help="Configuration file. Default is Director.conf inside the working directory", default="Director.conf")
    parser.add_argument("-t", "--test", help="Run Unittests", action="store_true")
    parser.add_argument("-g", "--generate", help="Generate default configuratioin file in specified directory", action="store_true")
    parser.add_argument("-l", "--logfile", help="Logfile name", default="Director.log")
    parser.add_argument("-L", "--log", help="Write log", action="store_true")



    args = parser.parse_args()
 

    if args.generate:
        if not os.path.isfile(args.configuration):
            print "not implemented"
            exit()
        else:
            print "config file exists. Move or rename it first"
            exit()

    cfg = cp.SafeConfigParser(allow_no_value=True)
    
    if os.path.isabs(args.configuration):
        cfg.read(args.configuration)
    else:
        cfg.read(os.path.join(args.directory, args.configuration))

    if args.log:
        if os.path.isabs(args.logfile):
            loghandle = open(args.logfile, "a")
        else:
            loghandle = open(os.path.join(args.directory, args.logfile), "a")


    os.chdir(args.directory)
    loghandle.write("- Start @ " + str(datetime.datetime.now()) + "\n")
    while(1):
        fail = False
 
        if cfg.has_option(current_state, 'Run'):
            fail = run_subprocess(cfg, current_state, 'Run', loghandle, args.directory)

        if cfg.has_option(current_state, 'Condition'):
            fail = run_subprocess(cfg, current_state, 'Condition', loghandle, args.directory)

        if fail:
            if cfg.has_option(current_state, 'Error'):
                current_state = cfg.get(current_state, 'Error')
            else:
                if loghandle:
                    loghandle.write("Ended with Error @ " + str(datetime.datetime.now()) + "\n")
                exit()

        else:
            if cfg.has_option(current_state, 'Next'):
                current_state = cfg.get(current_state, 'Next')
            else:
                if loghandle:
                    loghandle.write("Ended without Error @ " + str(datetime.datetime.now()) + "\n")
                exit()
