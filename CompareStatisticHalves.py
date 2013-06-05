#!/usr/bin/env python

import os,sys, argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("datafile")
parser.add_argument("--rows", help="rows to analyze, space-separated, 0-based", default=-1, type=int)
parser.add_argument("--columns", help="columns to analyze, space-separated, 0-based", default=-1, type=int)
parser.add_argument("--rangemin", help="data range lower bound, inclusive", default=-1, type=int)
parser.add_argument("--rangemax", help="data range upper bound, inclusive", default=-1, type=int)

args = parser.parse_args()

def Read(filename, columns, rows):
    data = []
    if columns = -1:
        data = np.loadtxt(filename)
    elif len(columns) == 2:
        data = np.loadtxt(filename, usecols=tuple(range(columns[0], columns[1]+1)))
    else:
        data = np.loadtxt(filename, usecols=tuple(columns))

    if rows == -1:
        return data
    elif len(rows) == 2:
        return data[rows[0]:rows[1]+1]
    elif len(rows) != 0:
        outdata = []
        for r in rows:
            outdata.append(data[r])
        return np.array(outdata)



