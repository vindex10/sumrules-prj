from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import * # quite boldly but simply enough

import os

import matplotlib.pyplot as plt
from tools.utils import timing

import sumrules

from sumrules.analytics import psiColP\
                             , psiColPdisc\
                             , energColDisc\
                             , sqedMP0 as MP0\
                             , sqedMP2 as MP2

from sumrules.evaluators import SumruleEvaluator\
                              , SigmaEvaluator\
                              , McolPEvaluator\
                              , SumruleDiscEvaluator\
                              , GammaDiscEvaluator\
                              , McolPDiscEvaluator

from sumrules.utils.parallel import npMap, mpMap
from sumrules.basics import BasicTest, BasicMonitor

class Test(BasicTest):
    def __init__(self):
        super(self.__class__, self).__init__("sqedCoul")


        # Continuous spectrum evaluators
        self.McolPEvaluatorInstance\
                = McolPEvaluator(None, psiColP)
        self.McolPEvaluatorInstance.vectorized = True
        self.McolPEvaluatorInstance.mapper = npMap

        self.SigmaEvaluatorInstance\
                = SigmaEvaluator(self.McolPEvaluatorInstance)
        self.SigmaEvaluatorInstance.cyclics.update({1: 0})

        self.SumruleEvaluatorInstance\
                = SumruleEvaluator(self.SigmaEvaluatorInstance)
        self.SumruleEvaluatorInstance.vectorized = True
        self.SumruleEvaluatorInstance.mapper = mpMap


        # Discrete spectrum evaluators
        self.McolPDiscEvaluatorInstance\
                = McolPDiscEvaluator(None, None, energColDisc)
        self.McolPDiscEvaluatorInstance.vectorized = True
        self.McolPDiscEvaluatorInstance.mapper = npMap

        self.GammaEvaluatorInstance\
                = GammaDiscEvaluator(self.McolPDiscEvaluatorInstance)

        self.SumruleDiscEvaluatorInstance\
                = SumruleDiscEvaluator(self.GammaEvaluatorInstance)

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.SumruleEvaluatorInstance, "C_SUMRULE")
        self.config.register(self.SigmaEvaluatorInstance, "C_SIGMA")
        self.config.register(self.McolPEvaluatorInstance, "C_MP")
        self.config.register(self.SumruleDiscEvaluatorInstance, "D_SUMRULE")
        self.config.register(self.GammaEvaluatorInstance, "D_GAMMA")
        self.config.register(self.McolPDiscEvaluatorInstance, "D_MP")

        self.config.readEnv() # get config filename from env
        self.config.readFile(self.configPath)
        self.config.readEnv() # get other data from env, overwrite file

        assert self.config["G_g"]<0

        if not os.path.exists(self.config["TEST_outputPath"]):
            os.makedirs(self.config["TEST_outputPath"])

    def doContSum(self, mp):
        "evaluate sumrule for specific MP"
        label = "cont::"+mp.__name__

        self.McolPEvaluatorInstance.MP = mp
        self.SigmaEvaluatorInstance.monitor =\
                BasicMonitor(self.path("monitor_sigma-%s" % label))

        with timing() as t:
            sr = self.SumruleEvaluatorInstance.compute()
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sumrule_evaltime %f" % (label, t()))

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "%s::sumrule %f" % (label, sr))

        # flush to initial
        self.McolPEvaluatorInstance.MP = None
        self.SigmaEvaluatorInstance.monitor = None
        return sr

    def doDiscSum(self, mp, psi):
        "evaluate sumrule for specific MP"
        label = "disc::"+mp.__name__

        self.McolPDiscEvaluatorInstance.MP = mp
        self.McolPDiscEvaluatorInstance.psiColP = psi

        with timing() as t:
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

        s0 = self.doContSum(MP0)
        s2 = self.doContSum(MP2)

        ds0 = self.doDiscSum(MP0\
                           , lambda n,l,p,T,F: psiColPdisc(n, l, 0, p, T, F))
        ds2 = self.doDiscSum(MP2\
                           , lambda n,l,p,T,F: psiColPdisc(n, l, 2, p, T, F))

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "ratio %f" % (((s0+ds0) - (s2+ds2))/(s2+ds2) - 1))


if __name__ == "__main__":
    instance = Test()
    instance.run()
