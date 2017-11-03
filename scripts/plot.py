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

if len(sys.argv) == 5:
    fname = sys.argv[2]
    data = gather(sys.argv[1], fname, int(sys.argv[3]), int(sys.argv[4]))
else:
    fname = sys.argv[1]
    data = gather(".", fname, int(sys.argv[2]), int(sys.argv[3]))

plt.plot(*data.T, ".")
plt.savefig("%s.png" % fname)
