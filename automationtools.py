
import os, sys
import datetime
import ConfigParser
#import shutil as su

def move_and_timestamp_file(filenames, postfix=None, add_date=True, separator="_", copy=False):

    if type(filenames) != list:
        filenames = [filenames]

    for fn in filenames:
        splitpath = os.path.split(fn)
        spb1 = splitpath[1]
        if len(splitpath[1]) == 0:
            raise OSError
        else:
            if postfix != None:
                spb1 = spb1 + separator + postfix
            if add_date == True:
                spb1 = spb1 + separator + datetime.datetime.isoformat(datetime.datetime.now())

            if copy:
                os.system("cp " + fn + " " + os.path.join(splitpath[0], spb1))
                print "cp " + fn + " " + os.path.join(splitpath[0], spb1)
            else:
                os.rename(fn, os.path.join(splitpath[0], spb1))
                print "mv " + fn + " " + os.path.join(splitpath[0], spb1)



def check_files_present(filenames):

    if type(filenames) != list:
        filenames = [filenames]

    for f in filenames:
        if os.path.isfile(f) == False:
            raise OSError

def write_error_message(filename, error_message=None):
    with open(filename, "a") as of:
        of.write(datetime.datetime.isoformat(datetime.datetime.now()))
        if error_message != None:
            of.write(" : " + error_message + "\n")
        else:
            of.write("\n")

def check_and_write_error(filenames, postfix=None):
    for f in filenames:
        try:
            check_files_present(f)
        except OSError:
            if postfix != None:
                write_error_message("STOP", "Missing file: " + f + " ; Postfix: " + postfix)
            else:
                write_error_message("STOP", "Missing file: " + f)
            #return False
            continue

def check_and_copy(filenames, postfix=None):
    for f in filenames:
        try:
            check_files_present(f)
        except OSError:
            if postfix != None:
                write_error_message("STOP", "Missing file: " + f + " ; Postfix: " + postfix)
            else:
                write_error_message("STOP", "Missing file: " + f)
            #return False
            continue

        move_and_timestamp_file(f, postfix=postfix, copy=True)

def check_and_move(filenames, postfix=None):
    for f in filenames:
        try:
            check_files_present(f)
        except OSError:
            if postfix != None:
                write_error_message("STOP", "Missing file: " + f + " ; Postfix: " + postfix)
            else:
                write_error_message("STOP", "Missing file: " + f)
            #return False
            continue
        move_and_timestamp_file(f, postfix=postfix, copy=False)

def mod_parameters(filename_source, filename_target, parameters, modifications, actions):

    infilehandle = open(filename_source, "r")
    outfilehandle = open(filename_target, "w")

    for line in infilehandle:
        try:
            index = parameters.index(line.split()[0].strip())
            print index
            print actions[index]
            if (actions[index] == "REPLACE") | (actions[index] == "ADDREPLACE"):
                print "case 1"
                outfilehandle.write(modifications[index]+"\n")
                del actions[index]
                del modifications[index]
                del parameters[index]
            elif (actions[index] == "REMOVE") | (actions[index] == "ADD"):
                print "case 2"
                del actions[index]
                del modifications[index]
                del parameters[index]
            else:
                raise KeyError("Action must be either REPLACE, ADDREPLACE, REMOVE or ADD")

        except ValueError:
            outfilehandle.write(line)

    if len(parameters):
        for index, action in enumerate(actions):
            if (action == "ADD") | (action == "ADDREPLACE"):
                outfilehandle.write(modifications[index]+"\n")

def mangle_config(configfile, group):
    cp = GlobalConfigParser()
    cp.read(configfile)
    print "R0"

    if os.path.isfile(group+"R"):
        cpitems = cp.get(group, "control_changes_restart")
        os.system("mv REVCON CONFIG; mv REVIVE REVOLD")
        print "R1"
    else:
        cpitems = cp.get(group, "control_changes")
        if cp.has_option(group, "use_revcon"):
            os.system("mv REVCON CONFIG")
            print "R2"
        if cp.has_option(group, "control_changes_restart"):
            os.system("touch " + group + "R")
            print "R3"

    print "-+-"
    print cpitems

    params = ["finish"]
    mods = [""]
    acts = ["REMOVE"]

    cpsplit = cpitems.split(",")

    for n in range(0, len(cpsplit), 3):
        params.append(cpsplit[n].strip())
        mods.append(cpsplit[n+1].strip())
        acts.append(cpsplit[n+2].strip())

    params.append("finish")
    mods.append("finish")
    acts.append("ADD")

    print params
    print mods
    print acts

    mod_parameters(cp.get(group, "control_source"), cp.get(group, "control_target"), params, mods, acts)

def pbs_runner(configfile, group):
    cp = GlobalConfigParser()
    cp.read(configfile)

    print cp.items(group)
    print [x[0] for x in cp.items(group)]

    if cp.has_option(group, "finish"):
        return

    if cp.has_option(group, "next_group_any"):
        os.system("cd $PBS_O_WORKDIR ; qsub -l " +cp.get(group, "qsub_l_any")+" -N " + cp.get(group, "next_script_any") + "-" + cp.get(group, "next_group_any") + "-" + cp.get(group, "designator") + " -W depend=afterany:${PBS_JOBID} -v STEP_CONFIG=" + configfile + ",STEP_GROUP=" + cp.get(group, "next_group_any") + " " +cp.get(group, "next_script_any"))

    else:
        os.system("cd $PBS_O_WORKDIR ; qsub -l "+cp.get(group, "qsub_l_ok")+" -N " + cp.get(group, "next_script_ok") + "-" + cp.get(group, "next_group_ok") + "-" + cp.get(group, "designator") + " -W depend=afterok:${PBS_JOBID} -v STEP_CONFIG=" + configfile + ",STEP_GROUP=" + cp.get(group, "next_group_ok") + " " +cp.get(group, "next_script_ok"))
        os.system("cd $PBS_O_WORKDIR ; qsub -l "+cp.get(group, "qsub_l_notok")+" -N " + cp.get(group, "next_script_notok") + "-" + cp.get(group, "next_group_notok") + "-" + cp.get(group, "designator") + " -W depend=afternotok:${PBS_JOBID} -v STEP_CONFIG=" + configfile + ",STEP_GROUP=" + cp.get(group, "next_group_notok") + " " +cp.get(group, "next_script_notok"))

class GlobalConfigParser(ConfigParser.SafeConfigParser, object):

    def get(self, section, option, use_global=True, global_section="global"):
        if use_global:
            if super(GlobalConfigParser, self).has_option(section, option):
                return super(GlobalConfigParser, self).get(section, option)
            elif super(GlobalConfigParser, self).has_option(global_section, option):
                return super(GlobalConfigParser, self).get(global_section, option)
            else:
                return super(GlobalConfigParser, self).get(section, option)

        else:
            return super(GlobalConfigParser, self).get(section, option)

    def has_option(self, section, option, use_global=True, global_section="global"):
        if use_global:
            if super(GlobalConfigParser, self).has_option(section, option):
                return True
            elif super(GlobalConfigParser, self).has_option(global_section, option):
                return True
            else:
                return False
        else:
            return super(GlobalConfigParser, self).has_option(section, option)


def argsinit():
    if 'PBS_O_WORKDIR' in os.environ:
        os.chdir(os.environ['PBS_O_WORKDIR'])

    if 'STEP_GROUP' in os.environ:
        group = os.environ['STEP_GROUP']
    else:
        group = sys.argv[2]

    if 'STEP_CONFIG' in os.environ:
        configfile = os.environ['STEP_CONFIG']
    else:
        configfile = sys.argv[1]

    cp = GlobalConfigParser()
    cp.read(configfile)

    return (group, configfile, cp)

def condition(cond):
    return eval(cond)

def check_clustering(filename, dist=3.5):
    import iotools as iot
    last_frame = iot.DLP2HReader(fileobj=filename)[-1]

    if last_frame.get_chains(dist) == 1:
        return True
    else:
        return False

def test_conf():

    if os.path.isfile("test1"):
        if os.path.isfile("test2"):
            return True
        else:
            os.system("touch test2")
            return False
    else:
        os.system("touch test1")
        return False
