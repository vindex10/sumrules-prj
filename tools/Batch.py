import os
import datetime

from sumrules.misc.ConfigManager import ConfigManager
from sumrules.Config import Config

class Batch(object):
    def __init__(self, ditor, call):
        self._tpl = dict()
        self.config = Config({"outputDir": "output"
                             ,"prjPath": "."
                             ,"testName": ""
                             ,"tplPath": "template.cfg"
                             ,"suffix": datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                        })
        self.ditor = ditor
        self.call = call
    
    def readFile(self, f):
        for line in f:
            matching = ConfigManager._cfgre.match(line)
            if not matching:
                continue
            pair = [v for v in matching.groups()\
                        if v is not None]
            if len(pair) > 0:
                self._tpl.update({
                    pair[0]: ConfigManager._parseStr(pair[1])
                })
    def path(self, *paths):
        return os.path.join(self.config["outputDir"]\
                          , self.config["suffix"]\
                          , *paths)

    def envInit(self):
        dirs = ("logs", "output", "configs")
        if not os.path.isdir(self.path()):
            os.makedirs(self.path())

        for d in dirs:
            if not os.path.isdir(self.path(d)):
                os.makedirs(self.path(d))

    def writeConfigs(self, spec):
        with open(self.path("template.conf"), "w") as f:
            tpl = "".join(("%s = %s\n" % entry\
                           for entry in self._tpl.items()))
            f.write(tpl)

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
                     ,self.config["testName"]\
                     ,cfg["TEST_title"]\
                     ,self.path("configs", "%s.conf" % cfg["TEST_title"])
                     ,cfg["TECH_numThreads"]
                     ,self.path("logs", "%s.log" % cfg["TEST_title"]))

    def run(self, spec):
        with open(self.config["tplPath"], "r") as f:
            self.readFile(f)
        self.envInit()
        cfgs = self.writeConfigs(spec)
        self.doCalls(cfgs)

