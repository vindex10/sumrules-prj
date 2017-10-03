from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import *

import os

import scipy as sp
import matplotlib.pyplot as plt
from tools import utils as t_utils

import sumrules
import sumrules.lib.analytics as alyt
import sumrules.lib.evaluators as evals

from sumrules.utils import parallel
from sumrules.misc.Test import Test as BasicTest
from sumrules.misc.Monitor import Monitor

class Test(BasicTest):
    def __init__(self):
        super(Test, self).__init__("tmPw")

        self.MPEvaluatorInstance = evals.TrivialEvaluator(alyt.tmMP)
        self.SigmaEvaluatorInstance\
                = evals.SigmaEvaluator(self.MPEvaluatorInstance)
        self.SigmaEvaluatorInstance.cyclics.update({1: sp.pi})
        self.SigmaEvaluatorInstance.vectorized = True
        self.SigmaEvaluatorInstance.mapper = parallel.npMap

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

    def run(self):
        super(Test, self).run()

        points = self.config["TEST_points"]
        minS = self.config["TEST_minS"]
        maxS = self.config["TEST_maxS"]
        outputPath = self.config["TEST_outputPath"]

        thepoints = [minS + (maxS - minS)/points*i for i in range(points)]
        self.pointwiseSigma(thepoints)

if __name__ == "__main__":
    instance = Test()
    instance.run()
