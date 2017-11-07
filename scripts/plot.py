#!/usr/bin/env python
"""@file
Script to build a plot of a gathered data.

If there is no such file, look through subdirs to gather data.

plot.py <fname> [(x y)] [(-d | --dir)]

CLI Args:
    * fname: filename to look for.
    * x: column corresponding to x axis.
    * y: column corresponding to y axis.
    * -d, --dir: path to dir where to start looking for file.

Returns:
    Plot with name `fname.png` stored at `path`.
"""

import os
import sys
import getopt

import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt

def gather(path, fname, x, y):
    """ Gather data from `fname`.
        
        Take columns `x` and `y` only. In case, if `fname` does not exist,
        look through subdirs at `path`.

        Args:
            path: path to dir where to start looking for file.
            fname: filename to look for.
            x: column corresponding to x axis.
            y: column corresponding to y axis.
        
        Returns:
            NumPy array of (x, y) pairs, taken from found files.
    """

    fullname = os.path.join(path, fname)
    try:
        data = np.loadtxt(fullname, usecols=(x, y))
        if data.shape[0] == 0:
            raise FileNotFoundError
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

def parse_args(args):
    """ Parse cli arguments.
        
        According to prototype:

        plot.py <fname> [(x y)] [(-d | --dir)]

        CLI Args:
            * fname: filename to look for.
            * x: column corresponding to x axis.
            * y: column corresponding to y axis.
            * -d, --dir: path to dir where to start looking for file.

        Returns:
            Tuple. (searchdir, fname, x, y).
    """
    searchdir = "."
    x = 0
    y = 1

    opts, parsed_args = getopt.gnu_getopt(args, "d:", ["dir="])
    for o, a in opts:
        if o in ("-d", "--dir"):
            searchdir = a

    fname = parsed_args[0]

    if len(args) == 3:
        x = int(parsed_args[1])
        y = int(parsed_args[2])

    fname = os.path.basename(os.path.normpath(fname))

    return searchdir, fname, x, y

def integr(data):
    """ Estimate integral by given data.
        
        Use CubicSpline to interpolate `data`, then use quadrature for
        integration.

        Args:
            data: NumPy array of (x, y) pairs.

        Returns:
            NumPy array. (Integral, Error) pair.
    """
    cleaned = np.unique(data[data[:,0].argsort()], axis=0)
    inter = sp.interpolate.CubicSpline(cleaned[:, 0], cleaned[:, 1])
    return sp.integrate.quad(inter, cleaned[0, 0], cleaned[-1,0])

def plot(data, fname):
    """ Plot `data` and save to cwd.
        
        Args:
            data: NumPy array of (x,y) pairs.
            fname: Name of output file.

        Returns:
            Nothing.
    """
    plt.plot(*data.T, ".")
    int_est = integr(data)
    plt.figtext(.02, .02, "Integral: %s" % str(int_est))
    plt.savefig("%s.png" % fname)

if __name__ == "__main__":
    parsed_args = parse_args(sys.argv[1:])
    data = gather(*parsed_args)
    plot(data, parsed_args[1])
