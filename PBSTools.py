import subprocess as sb
import os, sys

def dictionarize_list(linestring):
    lines = linestring.split("\n")
    outlist = []
    last_indent = 0
    last_token = ""
    for line in lines:
        indent = 0
        if line.strip() == "":
            continue
        for char in line:
            if char == " ":
                indent += 1
            elif char == "\t":
                indent += 8
            else:
                break

        if indent == 0:
            outlist.append({"JobID": line.split(":")[1].strip()})
        elif indent == 4:
            outlist[-1][line.split("=")[0].strip()] = line.split("=")[1].strip()
            last_token = line.split("=")[0].strip()
        elif indent == 8:
            outlist[-1][last_token] += line.strip()

    return outlist


def qsub(nodes=1,ppn=1,walltime=86400,name=None,executable=None,options=None, queue=None, hold=False):
    outargs = []

    if nodes and ppn:
        outargs.append("-lnodes=" + str(nodes) + ":ppn=" + str(ppn))
    elif nodes:
        outargs.append("-lnodes=" + str(nodes))
    elif ppn:
        outargs.append("-lppn=" + str(nodes))

    if walltime:
        outargs.append("-lwalltime=" + str(walltime))

    if name:
        outargs.extend(["-N", name])

    if queue:
        outargs.extend(["-q", queue])

    if hold:
        outargs.append("-h")

    if executable:
        outargs.append(executable)
        proc = sb.Popen(outargs, executable="qsub", stdout=sb.PIPE)
        return proc.stdout.read()

    else:
        raise ValueError("qsub: Executable name missing")

def qstat():
    proc = sb.Popen(["qstat", "-f"],stdout=sb.PIPE)
    return dictionarize_list(proc.communicate()[0])
