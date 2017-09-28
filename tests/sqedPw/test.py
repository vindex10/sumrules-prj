from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import * # quite boldly but simply enough

import os

import matplotlib.pyplot as plt
from tools.utils import timing

import sumrules
from sumrules.analytics import sqedMP0 as MP0\
                             , sqedMP2 as MP2
from sumrules.evaluators import SumruleEvaluator\
                              , SigmaEvaluator\
                              , TrivialEvaluator
from sumrules.utils.parallel import npMap, mpMap
from sumrules.basics import BasicTest, BasicMonitor

class Test(BasicTest):
    def __init__(self):
        super(self.__class__, self).__init__("sqedPw")

        self.SigmaEvaluatorInstance\
                = SigmaEvaluator(None)
        self.SigmaEvaluatorInstance.cyclics.update({1: 0})
        self.SigmaEvaluatorInstance.vectorized = True
        self.SigmaEvaluatorInstance.mapper = npMap

        self.SumruleEvaluatorInstance\
                = SumruleEvaluator(self.SigmaEvaluatorInstance)
        self.SumruleEvaluatorInstance.vectorized = True
        self.SumruleEvaluatorInstance.mapper = mpMap

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.SumruleEvaluatorInstance, "SUMRULE")
        self.config.register(self.SigmaEvaluatorInstance, "SIGMA")

        self.points = 20
        self.skipPointwise = False
        self._keylist += ["points", "skipPointwise"]

        self.config.readEnv()
        self.config.readFile(self.configPath)

        if not os.path.exists(self.config["TEST_outputPath"]):
            os.makedirs(self.config["TEST_outputPath"])

    def pointwiseSigma(self, mp, points):
        "Test sigma value per point"

        m = self.config["G_m"]
        dimfactor = self.config["G_dimfactor"]
        outputPath = self.config["TEST_outputPath"]

        self.SigmaEvaluatorInstance.MPEvaluatorInstance = TrivialEvaluator(mp)

        label = mp.__name__

        with timing() as t:
            res = list(map(lambda s: (s, self.SigmaEvaluatorInstance.compute(s)), points))
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sigma_evaltime(%d) %f" % (label, len(points), t()))

        with open(self.path("sigma"), "a") as f:
            self.iwrite(f, "# %s" % label)
            self.iwrite(f, "s, sigma")
            for pair in res:
                self.iwrite(f, "%e, %e" % pair)

        plt.plot(*list(zip(*res)))
        plt.savefig(os.path.join(outputPath, "sigma_plot."+label+".png"))

    def dosum(self, mp):
        "evaluate sumrule for specific MP"
        m = self.config["G_m"]
        dimfactor = self.config["G_dimfactor"]
        outputPath = self.config["TEST_outputPath"]
        label = mp.__name__


        mpEvaluator = TrivialEvaluator(mp)
        mpEvaluator.monitor = BasicMonitor(self.path("monitor_%s" % label))

        self.SigmaEvaluatorInstance.MPEvaluatorInstance = mpEvaluator
        self.SigmaEvaluatorInstance.monitor =\
                BasicMonitor(self.path("monitor_sigma-%s" % label))

        with timing() as t:
            sr = self.SumruleEvaluatorInstance.compute()
            with open(self.path("meta"), "a") as f:
                self.iwrite(f, "%s::sumrule_evaltime %f" % (label, t()))

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "%s::sumrule %f" % (label, sr))
        return sr

    def run(self):
        super(self.__class__, self).run()

        minS = self.config["SUMRULE_minS"]
        maxS = self.config["SUMRULE_maxS"]
        points = self.config["TEST_points"]
        outputPath = self.config["TEST_outputPath"]


        if not self.skipPointwise:
            thepoints = [minS + (maxS - minS)/points*i for i in range(points)]

            self.pointwiseSigma(MP0, thepoints)
            self.pointwiseSigma(MP2, thepoints)

        s0 = self.dosum(MP0)
        s2 = self.dosum(MP2)

        with open(self.path("sumrule"), "a") as f:
            self.iwrite(f, "s0/s2-1 %f" % (s0/s2 - 1))


if __name__ == "__main__":
    instance = Test()
    instance.run()
