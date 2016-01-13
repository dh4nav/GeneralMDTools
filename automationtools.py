import os
import datetime
#import shutil as su

def move_and_timestamp_file(filenames, postfix=None, add_date=True, separator="_"):

    if type(filenames) != list:
        filenames = [filenames]

    for fn in filenames:
        splitpath = os.path.split(fn)
        if len(splitpath[1]) == 0:
            raise OSError
        else:
            if postfix != None:
                splitpath[1] = splitpath[1] + separator + postfix
            if add_date == True:
                splitpath[1] = splitpath[1] + separator + datetime.datetime.isoformat(datetime.datetime.now())

            os.rename(fn, os.path.join(splitpath[0], splitpath[1]))



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

#def check_and_copy(filenames):
