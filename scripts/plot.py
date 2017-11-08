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
    * -e, --export: whether to export merged data.
    * -i, --integrate: whether to integrate.
    * -l, --logscale:
        - -1: no logscale (default).
        - 0: logscale for x.
        - 1: logscale for y.
        - 2: logscale for xy.

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

def clean_data(data):
    """ Sort and remove duplicates. """
    return np.unique(data[data[:,0].argsort()], axis=0)

def parse_args(args):
    """ Parse cli arguments.
        
        According to prototype:

        plot.py <fname> [(x y)] [(-d | --dir)]

        CLI Args:
            * fname: filename to look for.
            * x: column corresponding to x axis.
            * y: column corresponding to y axis.
            * -d, --dir: path to dir where to start looking for file.
            * -e, --export: whether to export merged data.
            * -i, --integrate: whether to integrate.
            * -l, --logscale:
                - -1: no logscale (default).
                - 0: logscale for x.
                - 1: logscale for y.
                - 2: logscale for xy.

        Returns:
            Dict:

                {"searchdir": str
                ,"fname": str
                ,"x": int
                ,"y": int
                ,"export": bool
                ,"integrate": bool}
    """
    searchdir = "."
    x = 0
    y = 1
    integrate = False
    export = False
    logscale=-1

    opts, parsed_args = getopt.gnu_getopt(args, "d:eil:", ["dir="
                                                        ,"export"
                                                        ,"integrate"
                                                        ,"log="])
    for o, a in opts:
        if o in ("-d", "--dir"):
            searchdir = a
        elif o in ("-e", "--export"):
            export = True
        elif o in ("-i", "--integrate"):
            integrate = True
        elif o in ("-l", "--log"):
            logscale = int(str(a).strip())

    fname = parsed_args[0]

    if len(parsed_args) == 3:
        x = int(parsed_args[1])
        y = int(parsed_args[2])

    fname = os.path.basename(os.path.normpath(fname))

    return {"searchdir": searchdir
           ,"fname": fname
           ,"x": x
           ,"y": y
           ,"export": export
           ,"integrate": integrate
           ,"logscale": logscale}

def integr(rawdata):
    """ Estimate integral by given data.
        
        Use CubicSpline to interpolate `data`, then use quadrature for
        integration.

        Args:
            rawdata: NumPy array of (x, y) pairs.

        Returns:
            NumPy array. (Integral, Error) pair.
    """
    data = clean_data(rawdata)
    inter = sp.interpolate.CubicSpline(data[:, 0], data[:, 1])
    return sp.integrate.quad(inter, data[0, 0], data[-1,0])

def plot(data, fname, integrate=False, logscale=-1):
    """ Plot `data` and save to cwd.
        
        Args:
            data: NumPy array of (x,y) pairs.
            fname: Name of output file.

        KWargs:
            integrate: set to True if you want to compute
                integral by the data.
            logscale: whether to take a log of axes.
                * -1: no logscale (default).
                *  0: logscale for x.
                *  1: logscale for y.
                *  2: logscale for xy.

        Returns:
            Nothing.
    """
    data = sp.copy(data)
    if integrate:
        int_est = integr(data)
        print("Integral (%s): %s" % (fname, int_est))

    if logscale in (0, 2):
        data[:, 0] = np.log(data[:, 0])
    if logscale in (1, 2):
        data[:, 1] = np.log(data[:, 1])

    plt.plot(*data.T, ".")
    if integrate:
        plt.figtext(.02, .02, "Integral: %s" % str(int_est))

    plt.savefig("%s.png" % fname)

if __name__ == "__main__":
    pa = parse_args(sys.argv[1:])
    data = gather(pa["searchdir"], pa["fname"], pa["x"], pa["y"])
    data = clean_data(data)
    plot(data, pa["fname"]\
        ,integrate=pa["integrate"]\
        ,logscale=pa["logscale"])
    if pa["export"]:
        sp.savetxt("%s.dat" % pa["fname"], data)

