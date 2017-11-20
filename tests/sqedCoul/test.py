from __future__ import absolute_import\
                      ,division\
                      ,print_function\
                      ,unicode_literals
from builtins import *

import os

import matplotlib.pyplot as plt
import tools.utils as t_utils

import sumrules
import sumrules.lib.analytics as alyt
import sumrules.lib.legacy_analytics as legalyt
import sumrules.lib.evaluators as evals

from sumrules.utils import parallel
from sumrules.misc.Test import Test as BasicTest
from sumrules.misc.Monitor import Monitor

class Test(BasicTest):
    def __init__(self):
        super(self.__class__, self).__init__("sqedCoul")

        self.flags = []
        self._keylist.append("flags")

        # Continuous spectrum evaluators
        self.McolPEvaluatorInstance\
                = evals.McolPEvaluator(None, alyt.psiColP)
        self.McolPEvaluatorInstance.vectorized = True
        self.McolPEvaluatorInstance.mapper = parallel.npMap

        self.SigmaEvaluatorInstance\
                = evals.SigmaEvaluator(self.McolPEvaluatorInstance)
        self.SigmaEvaluatorInstance.cyclics.update({1: 0})

        self.SumruleEvaluatorInstance\
                = evals.SumruleLogEvaluator(self.SigmaEvaluatorInstance)
        self.SumruleEvaluatorInstance.vectorized = True
        self.SumruleEvaluatorInstance.mapper = parallel.mpMap

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.SumruleEvaluatorInstance, "CSUMRULE")
        self.config.register(self.SigmaEvaluatorInstance, "CSIGMA")
        self.config.register(self.McolPEvaluatorInstance, "CMP")

        self.config.readEnv() # get config filename from env
        self.config.readFile(self.configPath)
        self.config.readEnv() # get other data from env, overwrite file

        if self.config["G_g"] < 0:
            # Discrete spectrum evaluators
            self.McolPDiscEvaluatorInstance\
                    = evals.McolPDiscEvaluator(None, None, alyt.energColDisc)
            self.McolPDiscEvaluatorInstance.vectorized = True
            self.McolPDiscEvaluatorInstance.mapper = parallel.npMap

            self.GammaEvaluatorInstance\
                    = evals.GammaDiscEvaluator(self.McolPDiscEvaluatorInstance)

            self.SumruleDiscEvaluatorInstance\
                    = evals.SumruleDiscEvaluator(self.GammaEvaluatorInstance)

            self.config.register(self.SumruleDiscEvaluatorInstance, "DSUMRULE")
            self.config.register(self.GammaEvaluatorInstance, "DGAMMA")
            self.config.register(self.McolPDiscEvaluatorInstance, "DMP")

            self.config.readEnv() # get config filename from env
            self.config.readFile(self.configPath)
            self.config.readEnv() # get other data from env, overwrite file


        if not os.path.exists(self.config["TEST_outputPath"]):
            os.makedirs(self.config["TEST_outputPath"])


    def doContSum(self, mp):
        "evaluate sumrule for specific MP"
        label = "cont::"+mp.__name__

        self.McolPEvaluatorInstance.MP = mp
        self.SumruleEvaluatorInstance.monitor =\
                Monitor(self.path("monitor_sr-%s" % label))

        with t_utils.timing() as t:
            sr = self.SumruleEvaluatorInstance.compute()
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sumrule_evaltime %f" % (label, t()))

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "%s::sumrule %f" % (label, sr))

        # flush to initial
        self.McolPEvaluatorInstance.MP = None
        self.SumruleEvaluatorInstance.monitor = None
        return sr

    def doDiscSum(self, mp, psi):
        "evaluate sumrule for specific MP"
        label = "disc::"+mp.__name__

        self.McolPDiscEvaluatorInstance.MP = mp
        self.McolPDiscEvaluatorInstance.psiColP = psi

        with t_utils.timing() as t:
            sr = self.SumruleDiscEvaluatorInstance.compute()
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sumrule_evaltime %f" % (label, t()))

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "%s::sumrule %f" % (label, sr))

        # flush to initial
        self.McolPDiscEvaluatorInstance.MP = None
        self.McolPDiscEvaluatorInstance.psiColP = None
        return sr

    def run(self):
        super(self.__class__, self).run()

        if "nocont" not in self.flags:
            s0 = self.doContSum(alyt.sqedMP0)
            s2 = self.doContSum(alyt.sqedMP2)

            with open(self.path("sumrule"), "a") as f:
                self.iwrite(f, "tot::cont::sumrule %f" % (s0 - s2))

        if "nodisc" not in self.flags\
           and self.config["G_g"] < 0:
            ds0 = self.doDiscSum(alyt.sqedMP0, legalyt.psiColPdisc0)
            ds2 = self.doDiscSum(alyt.sqedMP2, legalyt.psiColPdisc2)

            with open(self.path("sumrule"), "a") as f:
                self.iwrite(f, "tot::disc::sumrule %f" % (ds0 - ds2))


if __name__ == "__main__":
    instance = Test()
    instance.run()
