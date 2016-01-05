import os
import datetime

def check_files_present(filenames, error_message=None):
    if type(filenames) != list:
        filenames = [filenames]

    for f in filenames:
        if os.path.isfile(f) == False:
            with open("STOP", "a") as of:
                of.write(datetime.datetime.isoformat(datetime.datetime.now()))
                if error_message != None:
                    of.write(" : " + error_message + "\n")
                else:
                    of.write("\n")

                    
