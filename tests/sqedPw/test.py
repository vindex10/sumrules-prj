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
import sumrules.lib.evaluators as evals

from sumrules.utils import parallel
from sumrules.misc.Test import Test as BasicTest
from sumrules.misc.Monitor import Monitor

class Test(BasicTest):
    def __init__(self):
        super(self.__class__, self).__init__("sqedPw")

        self.SigmaEvaluatorInstance\
                = evals.SigmaEvaluator(None)
        self.SigmaEvaluatorInstance.cyclics.update({1: 0})
        self.SigmaEvaluatorInstance.vectorized = True
        self.SigmaEvaluatorInstance.mapper = parallel.npMap

        self.SumruleEvaluatorInstance\
                = evals.SumruleEvaluator(self.SigmaEvaluatorInstance)
        self.SumruleEvaluatorInstance.vectorized = True
        self.SumruleEvaluatorInstance.mapper = parallel.mpMap

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.SumruleEvaluatorInstance, "CSUMRULE")
        self.config.register(self.SigmaEvaluatorInstance, "CSIGMA")

        self.config.readEnv()
        self.config.readFile(self.configPath)
        self.config.readEnv()

        if not os.path.exists(self.config["TEST_outputPath"]):
            os.makedirs(self.config["TEST_outputPath"])

    def dosum(self, mp):
        "evaluate sumrule for specific MP"
        label = mp.__name__

        mpEvaluator = evals.TrivialEvaluator(mp)
        mpEvaluator.monitor = Monitor(self.path("monitor_%s" % label))

        self.SigmaEvaluatorInstance.MPEvaluatorInstance = mpEvaluator
        self.SigmaEvaluatorInstance.monitor =\
                Monitor(self.path("monitor_sigma-%s" % label))

        with t_utils.timing() as t:
            sr = self.SumruleEvaluatorInstance.compute()
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sumrule_evaltime %f" % (label, t()))

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "%s::sumrule %f" % (label, sr))
        return sr

    def run(self):
        super(self.__class__, self).run()

        s0 = self.dosum(alyt.sqedMP0)
        s2 = self.dosum(alyt.sqedMP2)

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "tot::sumrule %f" % (s0 - s2))



if __name__ == "__main__":
    instance = Test()
    instance.run()
