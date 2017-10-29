from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import *

import os

import scipy as sp
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
        super(self.__class__, self).__init__("prec")

        # Continuous spectrum evaluators
        self.cmel = evals.McolPEvaluator(None, alyt.psiColP)
        self.cmel.vectorized = True
        self.cmel.mapper = parallel.npMap
        self.cmel.absErr = 10**(-10)
        self.cmel.relErr = 10**(-10)

        self.crsc = evals.SigmaEvaluator(self.cmel)
        self.crsc.cyclics.update({1: 0})
        self.crsc.absErr = 10**(-10)
        self.crsc.relErr = 10**(-10)

        # Discrete spectrum evaluators
        self.dmel = evals.McolPDiscEvaluator(None, None, alyt.energColDisc)
        self.dmel.vectorized = True
        self.dmel.mapper = parallel.npMap

        self.gamma = evals.GammaDiscEvaluator(self.dmel)

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.crsc, "CSIGMA")
        self.config.register(self.cmel, "CMP")
        self.config.register(self.gamma, "DGAMMA")
        self.config.register(self.dmel, "DMP")

        self.config.readEnv() # get config filename from env
        self.config.readFile(self.configPath)
        self.config.readEnv() # get other data from env, rewrite file

        # Params:
        self.Mprec = 5
        self.Cprec = 3
        self.Mpoints = 10
        self.Cpoints = 5
        self.minP = 0
        self.maxP = 200
        self.minS = 4*self.crsc.CONST["m"]**2 + 1
        self.maxS = 200
        self._keylist += ["Mprec", "Cprec", "Mpoints", "Cpoints"
                        ,"minP", "maxP", "minS", "maxS"]

        if not os.path.exists(self.path()):
            os.makedirs(self.path())

        if self.config["G_g"] > 0:
            with open(self.path("params"), "a") as f: 
                self.iwrite(f, "WARN! coupling was forced to become negative")
            self.config["G_g"] *= -1

    def testCmel(self, themel):
        self.cmel.MP = themel
        label = themel.__name__
        answ = list()
        fig = plt.figure()
        ax = fig.gca()
        fdata = open(self.path("mel-%s.dat" % label), "w")
        
        answ.append([])
        for point in range(self.Mpoints):
            thepoint = self.minS + (self.maxP - self.minP)/self.Mpoints*point
            self.cmel.relErr = 1
            with t_utils.timing() as t:
                res = self.cmel.compute(thepoint, self.maxP/1.5, 0.2, 0)
                answ[0].append((res, t()))
        answ[0] = sp.array(answ[0]).T
        self.iwrite(fdata, answ[0])
        
        for p in range(1,self.Mprec+1):
            answ.append([])
            for point in range(self.Mpoints):
                thepoint = self.minS + (self.maxP - self.minP)/self.Mpoints*point
                
                self.cmel.relErr = 2**(-p)
                with t_utils.timing() as t:
                    res = self.cmel.compute(thepoint, self.maxP/1.5, 0.2, 0)
                    answ[p].append((res, t()))
            answ[p] = sp.array(answ[p]).T
            self.iwrite(fdata, answ[p])
            ax.plot(sp.full_like(answ[p][0], p), sp.absolute(answ[p][0] - answ[p-1][0]), ".")
            fig.savefig(self.path("cmel-%s.png" % label))

        self.cmel.absErr = 10**(-10)
        self.cmel.relErr = 10**(-10)
        self.cmel.MP = None
        fdata.close()

    def testCrsc(self, themel):
        label = themel.__name__
        self.cmel.absErr = 10**(-4)
        self.cmel.relErr = 10**(-1)
        self.cmel.MP = themel
        answ = list()
        fig = plt.figure()
        ax = fig.gca()
        fdata = open(self.path("crsc-%s.dat" % label), "w")
        
        answ.append([])
        for point in range(self.Cpoints):
            thepoint = self.minS + (self.maxS - self.minS)/self.Cpoints*point
            self.crsc.relErr = 1
            with t_utils.timing() as t:
                res = self.crsc.compute(thepoint)
                answ[0].append(res)
        answ[0] = sp.array(answ[0]).T
        self.iwrite(fdata, answ[0])
        
        for p in range(1,self.Cprec+1):
            answ.append([])
            for point in range(self.Cpoints):
                thepoint = self.minS + (self.maxS - self.minS)/self.Cpoints*point
                
                self.crsc.relErr = 2**(-p)
                with t_utils.timing() as t:
                    res = self.crsc.compute(thepoint)
                    answ[p].append(res)
            answ[p] = sp.array(answ[p]).T
            self.iwrite(fdata, answ[p])
            ax.plot(sp.full_like(answ[p][0], p), sp.absolute(answ[p][0] - answ[p-1][0]), ".")
            fig.savefig(self.path("crsc-%s.png" % label))

        
        self.cmel.absErr = 10**(-10)
        self.cmel.relErr = 10**(-10)
        self.crsc.absErr = 10**(-10)
        self.crsc.relErr = 10**(-10)
        self.cmel.MP = None
        fdata.close()

    def run(self):
        super(Test, self).run()

        self.testCmel(alyt.sqedMP0)
        self.testCmel(alyt.sqedMP2)

        self.testCrsc(alyt.sqedMP0)
        self.testCrsc(alyt.sqedMP2)


if __name__ == "__main__":
    instance = Test()
    instance.run()

