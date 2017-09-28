import os
import sys
import subprocess
from collections import defaultdict
from getopt import gnu_getopt
from ast import literal_eval
import numpy as np
from tools.Batch import Batch

# Batch handlers
def sumruleDitor(data, spec, cfg):
    assert "C_SUMRULE_minS" in data.keys()\
            or\
            "G_m" in data.keys()

    tot = sum(spec.T[0])
    try:
        width = data["C_SUMRULE_maxS"]-data["C_SUMRULE_minS"]
        pos = data["C_SUMRULE_minS"]
    except KeyError:
        pos = 4*data["G_m"]**2 + 0.001
        width = data["C_SUMRULE_maxS"]-pos
        

    num = 0
    for part in spec:
        step = width/tot*part[0]/part[1]
        
        for i in range(part[1]):
            out = data.copy()

            if "TEST_title" not in out.keys():
                    out.update({"TEST_title": cfg["suffix"]})
            out["TEST_title"] += "-%d" % num
            
            out["C_SUMRULE_minS"] = pos
            out["C_SUMRULE_maxS"] = pos + step

            out.update({"TECH_numThreads": part[2]
                       ,"TEST_outputDir": cfg["outputDir"]})
            
            pos += step
            num += 1
            yield out

def qsubTestCall(prjPath\
               , testname\
               , jobName\
               , cfgPath\
               , numThreads\
               , logPath):
    
    pbs = "source %s/activate;\n" % prjPath
    pbs += "cd %s;\n" % os.getcwd()
    pbs += "PYTHONPATH=%s python %s/tests/%s/test.py --config=%s;\n"\
          % (prjPath\
           , prjPath\
           , testname\
           , cfgPath)

    qsub = "qsub -l nodes=1:ppn=%d -o %s -j oe -N %s  bash -c \"%s\";\n"\
            % (numThreads\
             , logPath\
             , jobName\
             , pbs)

    subprocess.call(qsub, shell=True)

def srReduce(path):
    reduced = defaultdict(lambda: 0)
    subtests = (os.path.join(path, d) for d in os.listdir(path)\
                    if os.path.isdir(os.path.join(path, d)))
    for subtest in subtests:
        with open(os.path.join(subtest, "sumrule"), "r") as f:
            for line in f:
                k, v = line.split(" ")
                reduced[k] += float(v)

    return reduced


# cli handlers
def batchRun(args):
    assert len(args) >= 3
    inst = Batch(sumruleDitor, qsubTestCall)

    inst.config["testName"] = args[0]
    inst.config["tplPath"] = args[1]

    opts, rem = gnu_getopt(args, "o:p:s:", ["odir="\
                                                   ,"ppath="\
                                                   ,"suffix="])
    for opt, arg in opts:
        if opt in ("-o", "--odir"):
            inst.config["outputDir"] = arg
        elif opt in ("-p", "--ppath"):
            inst.config["prjPath"] = arg
        elif opt in ("-s", "--suffix"):
            print(arg)
            inst.config["suffix"] = arg

    spec = np.array(literal_eval(args[2]))
    inst.run(spec)

def batchReduce(args):
    assert len(args) >= 1
    
    opts, rem = gnu_getopt(args, "o:", ["output="])

    output = None
    for opt, arg in opts:
        if opt in ("-o", "--output"):
            output = open(arg, "w")

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
