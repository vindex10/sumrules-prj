from __future__ import absolute_import, division, print_function, unicode_literals
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
        super(self.__class__, self).__init__("sqedRepCoul")

        self.McolPEvaluatorInstance\
                = evals.McolPEvaluator(None, alyt.psiColP)
        self.McolPEvaluatorInstance.vectorized = True
        self.McolPEvaluatorInstance.mapper = parallel.npMap

        self.SigmaEvaluatorInstance\
                = evals.SigmaEvaluator(self.McolPEvaluatorInstance)
        self.SigmaEvaluatorInstance.cyclics.update({1: 0})

        self.SumruleEvaluatorInstance\
                = evals.SumruleEvaluator(self.SigmaEvaluatorInstance)
        self.SumruleEvaluatorInstance.vectorized = True
        self.SumruleEvaluatorInstance.mapper = parallel.mpMap

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.SumruleEvaluatorInstance, "SUMRULE")
        self.config.register(self.SigmaEvaluatorInstance, "SIGMA")
        self.config.register(self.McolPEvaluatorInstance, "MP")

        self.points = 20
        self.skipPointwise = False
        self._keylist += ["points", "skipPointwise"]

        self.config.readEnv() # get config filename from env
        self.config.readFile(self.configPath)
        self.config.readEnv() # get other data from env, overwrite file

        if not os.path.exists(self.config["TEST_outputPath"]):
            os.makedirs(self.config["TEST_outputPath"])

    def pointwiseSigma(self, mp, points):
        "Test sigma value per point"

        m = self.config["G_m"]
        dimfactor = self.config["G_dimfactor"]
        outputPath = self.config["TEST_outputPath"]

        self.McolPEvaluatorInstance.MP = mp

        label = mp.__name__

        with t_utils.timing() as t:
            res = list(map(lambda s: (s, self.SigmaEvaluatorInstance.compute(s)), points))
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sigma_evaltime(%d) %f" % (label, len(points), t()))

        with open(self.path("sigma"), "a") as f:
            self.iwrite(f, "# %s" % label)
            self.iwrite(f, "s, sigma")
            for pair in res:
                self.iwrite(f, "%e, %e" % pair)

        plt.plot(*list(zip(*res)))
        plt.savefig(self.path("sigma_plot."+label+".png"))

    def dosum(self, mp):
        "evaluate sumrule for specific MP"
        m = self.config["G_m"]
        dimfactor = self.config["G_dimfactor"]
        outputPath = self.config["TEST_outputPath"]
        label = mp.__name__

        self.McolPEvaluatorInstance.MP = mp
        self.SumruleEvaluatorInstance.monitor =\
                Monitor(self.path("monitor_sr-%s" % label))

        with t_utils.timing() as t:
            sr = self.SumruleEvaluatorInstance.compute()
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sumrule_evaltime %f" % (label, t()))

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "%s::sumrule %f" % (label, sr))

        self.McolPEvaluatorInstance.MP = None
        self.SumruleEvaluatorInstance.monitor = None
        return sr

    def run(self):
        super(self.__class__, self).run()

        minS = self.config["SUMRULE_minS"]
        maxS = self.config["SUMRULE_maxS"]
        points = self.config["TEST_points"]
        outputPath = self.config["TEST_outputPath"]


        if not self.skipPointwise:
            thepoints = [minS + (maxS - minS)/points*i for i in range(points)]

            self.pointwiseSigma(alyt.sqedMP0, thepoints)
            self.pointwiseSigma(alyt.sqedMP2, thepoints)

        s0 = self.dosum(alyt.sqedMP0)
        s2 = self.dosum(alyt.sqedMP2)

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "s0/s2-1 %f" % (s0/s2 - 1))


if __name__ == "__main__":
    instance = Test()
    instance.run()
