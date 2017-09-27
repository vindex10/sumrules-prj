import os
import sys
import subprocess
from getopt import gnu_getopt
from ast import literal_eval
from datetime import datetime
import numpy as np
from sumrules.basics import BasicConfigManager
from sumrules.Config import Config

class Batch(object):
    def __init__(self, ditor, call):
        self._tpl = dict()
        self.config = Config({"outputDir": "output"
                             ,"prjPath": "."
                             ,"testName": ""
                             ,"tplPath": "template.cfg"
                             ,"suffix": datetime.now().strftime("%Y%m%d%H%M%S")
                        })
        self.ditor = ditor
        self.call = call
    
    def readFile(self, f):
        for line in f:
            matching = BasicConfigManager._cfgre.match(line)
            if not matching:
                continue
            pair = [v for v in matching.groups()\
                        if v is not None]
            if len(pair) > 0:
                self._tpl.update({
                    pair[0]: BasicConfigManager._parseStr(pair[1])
                })
    def path(self, *paths):
        return os.path.join(self.config["outputDir"]\
                          , self.config["suffix"]\
                          , *paths)

    def envInit(self):
        dirs = ["logs", "output", "configs"]
        if not os.path.isdir(self.path()):
            os.makedirs(self.path())

        for d in dirs:
            if not os.path.isdir(self.path(d)):
                os.makedirs(self.path(d))

    def writeConfigs(self, spec):
        cfgs = list()
        for cfg in self.ditor(self._tpl, spec, self.config.copy()):
            config = "\n".join((k+" = "+str(v) for k,v in cfg.items()))
            cfgs.append(cfg)
            with open(self.path("configs", "%s.conf" % cfg["TEST_title"]), "w") as f:
                f.write(config+"\n")
        return cfgs

    def doCalls(self, cfgs):
        for cfg in cfgs:
            self.call(self.config["prjPath"]\
                    , self.config["testName"]\
                    , cfg["TEST_title"]\
                    , self.path("configs", "%s.conf" % cfg["TEST_title"])
                    , cfg["TECH_numThreads"]
                    , self.path("logs", "%s.log" % cfg["TEST_title"]))

    def run(self, spec):
        with open(self.config["tplPath"], "r") as f:
            self.readFile(f)
        self.envInit()
        cfgs = self.writeConfigs(spec)
        self.doCalls(cfgs)

def sumruleDitor(data, spec, cfg):
    tot = sum(spec.T[0])
    width = data["C_SUMRULE_maxS"]-data["C_SUMRULE_minS"]

    pos = data["C_SUMRULE_minS"]
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

    subprocess.call(qsub)



if __name__ == "__main__":
    assert len(sys.argv) >= 4

    spec = np.array(literal_eval(sys.argv[3]))


    inst = Batch(sumruleDitor, qsubTestCall)

    inst.config["testName"] = sys.argv[1]
    inst.config["tplPath"] = sys.argv[2]

    opts, rem = gnu_getopt(sys.argv[1:], "o:p:s:", ["odir="\
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

    inst.run(spec)


