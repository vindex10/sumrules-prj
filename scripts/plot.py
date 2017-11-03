#!/usr/bin/env python

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

def gather(path, fname, x, y):
    fullname = os.path.join(path, fname)
    try:
        data = np.loadtxt(fullname, usecols=(x, y))
    except FileNotFoundError:
        datalist = list()
        for f in os.listdir(path):
            subpath = os.path.join(path, f)
            if os.path.isdir(subpath):
                datalist.append(gather(os.path.join(path, f)\
                                      ,fname
                                      ,x
                                      ,y))
        try:
            data = np.vstack(tuple(datalist))
        except ValueError:
            data = np.empty(shape=(0, 2))
    return data

searchdir = "."
x = 0
y = 1

if len(sys.argv) == 5:
    searchdir = sys.argv[1]
    fname = sys.argv[2]
    x = int(sys.argv[3])
    y = int(sys.argv[4])
elif len(sys.argv) == 4:
    fname = sys.argv[1]
    x = int(sys.argv[2])
    y = int(sys.argv[3])
elif len(sys.argv) == 2:
    fname = sys.argv[1]
else:
    raise TypeError("Wrong arguments for plot.py")

data = gather(searchdir, fname, x, y)
plt.plot(*data.T, ".")
plt.savefig("%s.png" % fname)
