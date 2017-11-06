#!/usr/bin/env python
"""@file
Implementation of functions to feed into tools::Batch::Batch, and
become able to run tests in parallel way at a cluster.

CLI Args for `batch`:
    * -o, --odir: where to store batch outputs, logs, configs, etc.
    * -p, -ppath: path to sumrule-prj root.
    * -s, --suffix: name to distinguish different runs of the same test.
    * -t, --shift: set shift to start numbering not from 0.

CLI Args for `reduce`:
    * -o, --output: path to where `reduce` should store its output,
        if not defined, output goes to stdout.
"""

import ast
import collections
import getopt
import os
import subprocess
import sys

import numpy as np
from tools.Batch import Batch

def sumruleDitor(data, spec, cfg):
    """ Sumrule distributor.
        
        Breaks `data` into a group of configs according to `spec`,
        taking into account Batch config `cfg`.

        Args:
            data: dict of config file entries.
            spec: list of tuples. A rule according to which configs
                should be distributed.

                For spec:

                    >>> [[3, 4, 2], [2, 6, 1]]
                
                integration range over `s` will be broken as 3:2,
                then first part will be broken in 4 equal parts by `s`.
                For each of these 4 parts will be allocated 2 processors.
                The second part will be broken in 6 equal parts by `s`, and
                for each of these 6 parts will be allocated 1 processor.
            cfg: stores key-value pairs of Batch configuration.

        Yields:
            A config file.
    """
    assert "CSUMRULE_minS" in data.keys()\
            or\
            "G_m" in data.keys()

    tot = sum(spec.T[0])
    try:
        width = data["CSUMRULE_maxS"]-data["CSUMRULE_minS"]
        pos = data["CSUMRULE_minS"]
    except KeyError:
        pos = 4*data["G_m"]**2 + 0.001
        width = data["CSUMRULE_maxS"]-pos
        

    num = cfg["shift"]
    for part in spec:
        step = width/tot*part[0]/part[1]
        
        for i in range(part[1]):
            out = data.copy()

            if "TEST_title" not in out.keys():
                    out.update({"TEST_title": cfg["suffix"]})
            out["TEST_title"] += "-%d" % num
            
            out["CSUMRULE_minS"] = pos
            out["CSUMRULE_maxS"] = pos + step

            out.update({"TECH_numThreads": part[2]
                       ,"TEST_outputPath": os.path.join(cfg["outputDir"]\
                                                      , cfg["suffix"]\
                                                      , "output"\
                                                      , out["TEST_title"])})
            
            pos += step
            num += 1
            yield out

def qsubTestCall(prjPath\
               , testname\
               , jobName\
               , cfgPath\
               , numThreads\
               , logPath):
    """ Call qsub with corresponding args.
        
        Args:
            prjPath: a path to sumrules-prj root.
            testname: name of dir with a test.
            jobName: job title for `qstat` output.
            cfgPath: path to config file for test.
            numThreads: number of threads to allocate for job.
            logPath: path to log file, for qsub output.

        Returns:
            Nothig.
    """
    
    pbs = "cd %s;\n" % os.getcwd()
    pbs += "source %s/activate;\n" % prjPath
    pbs += "PYTHONPATH=%s python %s/tests/%s/test.py --config=%s;\n"\
          % (prjPath\
           , prjPath\
           , testname\
           , cfgPath)

    qsub = "echo \"%s\" | qsub -l nodes=1:ppn=%d -o %s -j oe -N %s\n"\
            % (pbs\
             , numThreads\
             , logPath\
             , jobName)

    print(qsub)
    subprocess.call(qsub, shell=True)

def srReduce(path):
    """ Compute total for each field stored in `sumrule` output file.

        Args:
            path: path to where dirs with test outputs stored.

        Returns:
            A dict with totals per field through all outputs.
    """
    reduced = collections.defaultdict(lambda: 0)
    subtests = (os.path.join(path, d) for d in os.listdir(path)\
                    if os.path.isdir(os.path.join(path, d)))
    for subtest in subtests:
        try:
            with open(os.path.join(subtest, "sumrule"), "r") as f:
                for line in f:
                    k, v = line.split(" ")
                    reduced[k] += float(v)
        except FileNotFoundError:
            pass

    return reduced


# cli handlers
def batchRun(args):
    """ Command to call when `batcher.py batch *args` is called.
        
        Args:
            args: rest of `*args` after command `batch`.
                * args[0] - test name.
                * args[1] - path to config, which will be pralellized.
                * args[2] - spec in usual format (list of lists).

        Returns:
            Nothing.
    """
    assert len(args) >= 3
    inst = Batch(sumruleDitor, qsubTestCall)

    inst.config["testName"] = args[0]
    inst.config["tplPath"] = args[1]

    opts, rem = getopt.gnu_getopt(args, "o:p:s:t:",("odir="\
                                           ,"ppath="\
                                           ,"suffix="
                                           ,"shift="))
    for opt, arg in opts:
        if opt in ("-o", "--odir"):
            inst.config["outputDir"] = arg
        elif opt in ("-p", "--ppath"):
            inst.config["prjPath"] = arg
        elif opt in ("-s", "--suffix"):
            inst.config["suffix"] = arg
        elif opt in ("-t", "--shift"):
            try:
                inst.config["shift"] = int(arg)
            except ValueError:
                pass

    spec = np.array(ast.literal_eval(args[2]))
    inst.run(spec)

def batchReduce(args):
    """ A command to be called when `batcher.py reduce` called.
        
        Args:
            args: rest of cli args after `reduce` command.
                * args[0] - path to dir where test stores outputs.
    """
    assert len(args) >= 1
    
    opts, rem = getopt.gnu_getopt(args, "o:", ("output=",))

    output = None
    for opt, arg in opts:
        if opt in ("-o", "--output"):
            output = arg

    reduced = srReduce(args[0])
    
    contents = "".join(("%s %s\n" % entry for entry in reduced.items()))
    print(contents)
    try:
        with open(output, "w") as f:
            f.write(contents)
    except TypeError:
        pass

if __name__ == "__main__":
    command = sys.argv[1]

    if command == "run":
        batchRun(sys.argv[2:])
    elif command == "reduce":
        batchReduce(sys.argv[2:])
