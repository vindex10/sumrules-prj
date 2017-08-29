from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import * # quite boldly but simply enough

import os

import matplotlib.pyplot as plt
from utils import timing

import sumrules
import sumrules.models
from tests.BasicTest import BasicTest

class Test(BasicTest):
    def __init__(self):
        super(self.__class__, self).__init__("sqedCoul")
        self.SumruleEvaluatorInstance = self.model.SumruleEvaluator()
        self.SigmaEvaluatorInstance = self.model.SigmaEvaluator()
        self.SumruleEvaluatorInstance\
            .SigmaEvaluatorInstance = self.SigmaEvaluatorInstance

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.models.config, "G")
        self.config.register(self.SumruleEvaluatorInstance, "SUMRULE")
        self.config.register(self.SigmaEvaluatorInstance, "SIGMA")
        self.config.register(self.SigmaEvaluatorInstance\
                                 .McolPEvaluatorInstance, "MCOLP")

        self.points = 20

        self.config.readEnv()
        self.config.readFile(self.configPath)

        if not os.path.exists(self.config["TEST_outputPath"]):
            os.makedirs(self.config["TEST_outputPath"])

    def params(self, paramdict=None):
        sup = super(self.__class__, self).params(paramdict)

        keylist = ("points", )
        
        if paramdict is None:
            # list here params of current test
            sup.update({k: getattr(self, k) for k in keylist})
            return sup
        
        # check if some values of paramdict correspond to current test properties
        for key, val in paramdict.items():
            if key in keylist:
                setattr(self, key, val)
        return True

    def pointwiseSigma(self, mp, points):
        "Test sigma value per point"

        m = self.config["G_m"]
        dimfactor = self.config["G_dimfactor"]
        outputPath = self.config["TEST_outputPath"]

        self.SumruleEvaluatorInstance\
            .SigmaEvaluatorInstance\
            .McolPEvaluatorInstance.MP = mp

        label = mp.__name__

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

    def dosum(self, mp):
        "evaluate sumrule for specific MP"
        m = self.config["G_m"]
        dimfactor = self.config["G_dimfactor"]
        outputPath = self.config["TEST_outputPath"]

        self.SumruleEvaluatorInstance\
            .SigmaEvaluatorInstance\
            .McolPEvaluatorInstance.MP = mp

        label = mp.__name__

        with timing() as t:
            sr = self.SumruleEvaluatorInstance.compute()
            with open(os.path.join(outputPath, "meta"), "a") as f:
                self.iwrite(f, "%s::sumrule_evaltime %f" % (label, t()))

        with open(os.path.join(outputPath, "sumrule"), "a") as f:
            self.iwrite(f, "%s::sumrule %f" % (label, sr))
        return sr

    def run(self):
        super(self.__class__, self).run()

        minS = self.config["SUMRULE_minS"]
        maxS = self.config["SUMRULE_maxS"]
        points = self.config["TEST_points"]
        outputPath = self.config["TEST_outputPath"]

        thepoints = [minS + (maxS - minS)/points*i for i in range(points)]

        self.pointwiseSigma(self.model.MP0, thepoints)
        self.pointwiseSigma(self.model.MP2, thepoints)

        s0 = self.dosum(self.model.MP0)
        s2 = self.dosum(self.model.MP2)

        with open(os.path.join(outputPath, "sumrule"), "a") as f:
            self.iwrite(f, "s0/s2-1 %f" % (s0/s2 - 1))


if __name__ == "__main__":
    instance = Test()
    instance.run()
