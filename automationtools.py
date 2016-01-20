import os
import datetime
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
