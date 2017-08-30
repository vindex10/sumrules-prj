from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import *

import os

import matplotlib.pyplot as plt
from utils import timing

import sumrules
from sumrules.analytics import tmMP as MP
from sumrules.evaluators import SigmaEvaluator\
                              , TrivialEvaluator
from sumrules.parallel import npMap, mpMap
from BasicTest import BasicTest

class Test(BasicTest):
    def __init__(self):
        super(self.__class__, self).__init__("tmPw")

        self.MPEvaluatorInstance = TrivialEvaluator(MP)
        self.SigmaEvaluatorInstance\
                = SigmaEvaluator(self.MPEvaluatorInstance)
        self.SigmaEvaluatorInstance.vectorized = True
        self.SigmaEvaluatorInstance.mapper = npMap

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.SigmaEvaluatorInstance, "SIGMA")

        self.points = 20
        self.minS = 4*self.config["G_m"]**2
        self.maxS = 1000
        self._keylist += ["points", "minS", "maxS"]

        self.config.readEnv()
        self.config.readFile(self.configPath)

        if not os.path.exists(self.config["TEST_outputPath"]):
            os.makedirs(self.config["TEST_outputPath"])

    def pointwiseSigma(self, points):
        "Test sigma value per point"

        m = self.config["G_m"]
        dimfactor = self.config["G_dimfactor"]
        outputPath = self.config["TEST_outputPath"]

        label = "MP"

        with timing() as t:
            res = list(map(lambda s: (s, self.SigmaEvaluatorInstance.compute(s)), points))
            with open(os.path.join(outputPath, "meta"), "a") as f:
                self.iwrite(f, "%s::sigma_evaltime(%d) %f" % (label, len(points), t()))

        with open(os.path.join(outputPath, "sigma"), "a") as f:
            self.iwrite(f, "# %s" % label)
            self.iwrite(f, "s, sigma")
            for pair in res:
                self.iwrite(f, "%e, %e" % pair)

        plt.plot(*list(zip(*res)))
        plt.savefig(os.path.join(outputPath, "sigma_plot."+label+".png"))

    def run(self):
        super(self.__class__, self).run()

        points = self.config["TEST_points"]
        minS = self.config["TEST_minS"]
        maxS = self.config["TEST_maxS"]
        outputPath = self.config["TEST_outputPath"]

        thepoints = [minS + (maxS - minS)/points*i for i in range(points)]
        self.pointwiseSigma(thepoints)

if __name__ == "__main__":
    instance = Test()
    instance.run()
