import AtomEnsemble as ae
import iotools as iot
import os, sys

import argparse as ap

parser = ap.ArgumentParser(description="Step 1 for Kavska-Zahn: Strip solvent & add new cluster")
parser.add_argument("-im", "--in_main", help="main in file name")
parser.add_argument("-ia", "--in_add", help="add molecule in file name")
parser.add_argument("-fm", "--field_main", help="main file FIELD file")
parser.add_argument("-fa", "--field_add", help="add file FIELD file")
parser.add_argument("-oc", "--config_out", help="CONFIG output file")
parser.add_argument("-of", "--field_out", help="FIELD outfut file")
parser.add_argument("-s", "--solvent", help="Solvent atoms", nargs="+")
args = parser.parse_args()

def reader(infile):
    file_name = ""
    if type(infile) == file:
        file_name = infile.name
    else:
        file_name = infile

    if ".xyz" in file_name:
        iot_reader = iot.XYZReader(fileobj=infile)

    elif ".dlpolyhist" in file_name:
        iot_reader = iot.DLP2HReader(fileobj=infile)
    elif "HISTORY" in file_name:
        iot_reader = iot.DLP2HReader(fileobj=infile)
    else:
        raise ImportError("File type not recognized")
        
