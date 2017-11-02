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
        self.cmel.absErr = 10**(-50)
        self.cmel.relErr = 10**(-50)

        self.crsc = evals.SigmaEvaluator(self.cmel)
        self.crsc.cyclics.update({1: 0})
        self.crsc.absErr = 10**(-50)
        self.crsc.relErr = 10**(-50)

        # Discrete spectrum evaluators
        self.dmel = evals.McolPDiscEvaluator(None, None, alyt.energColDisc)
        self.dmel.vectorized = True
        self.dmel.mapper = parallel.npMap
        self.dmel.absErr = 10**(-50)
        self.dmel.relErr = 10**(-50)

        self.config.register(sumrules.config, "TECH")
        self.config.register(sumrules.constants, "G")
        self.config.register(self.crsc, "CSIGMA")
        self.config.register(self.cmel, "CMP")
        self.config.register(self.dmel, "DMP")

        self.config.readEnv() # get config filename from env
        self.config.readFile(self.configPath)
        self.config.readEnv() # get other data from env, rewrite file

        # Params:
        self.cmelargs = [5, 10, 0.1, 200]
        self.crscargs = [3, 5, 4*self.crsc.CONST["m"]**2 + 1, 200]
        self.dmelargs = [40, 20, 0.1, 200]
        self._keylist += ["cmelargs", "crscargs", "dmelargs"]

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
        fdata = open(self.path("cmel-%s.dat" % label), "w")

        prec, points, minP, maxP = self.cmelargs
        
        def evalPrec(p):
            answ.append([])
            self.cmel.relErr = 2**(-p)
            for point in range(points):
                thepoint = minP + (maxP - minP)/points*point
                
                with t_utils.timing() as t:
                    res = self.cmel.compute(thepoint, maxP/1.5, 0.2, 0)
                    answ[p].append((res, t()))
            answ[p] = sp.array(answ[p]).T
            self.iwrite(fdata, answ[p])

        evalPrec(0)
        for p in range(1,prec+1):
            evalPrec(p)
            ax.plot(sp.full_like(answ[p][0], p), sp.absolute(answ[p][0] - answ[p-1][0]), ".")
            fig.savefig(self.path("cmel-%s.png" % label))

        self.cmel.absErr = 10**(-50)
        self.cmel.relErr = 10**(-50)
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

        prec, points, minS, maxS = self.crscargs
        
        def evalPrec(p):
            answ.append([])
            self.crsc.relErr = 2**(-p)
            for point in range(points):
                thepoint = minS + (maxS - minS)/points*point
                
                with t_utils.timing() as t:
                    res = self.crsc.compute(thepoint)
                    answ[p].append(res)
            answ[p] = sp.array(answ[p]).T
            self.iwrite(fdata, answ[p])
        
        evalPrec(0)
        for p in range(1,prec+1):
            evalPrec(p)
            ax.plot(sp.full_like(answ[p][0], p), sp.absolute(answ[p][0] - answ[p-1][0]), ".")
            fig.savefig(self.path("crsc-%s.png" % label))

        
        self.cmel.absErr = 10**(-50)
        self.cmel.relErr = 10**(-50)
        self.crsc.absErr = 10**(-50)
        self.crsc.relErr = 10**(-50)
        self.cmel.MP = None
        fdata.close()

    def testDmel(self, themel, psicolp):
        self.dmel.MP = themel
        self.dmel.psiColP = psicolp
        label = themel.__name__
        answ = list()
        fig = plt.figure()
        ax = fig.gca()
        fdata = open(self.path("dmel-%s.dat" % label), "w")

        prec, points, minP, maxP = self.dmelargs
        
        def evalPrec(p):
            answ.append([])
            self.dmel.absErr = 2**(-p)
            n = 1
            l = 0
            while (n-1)*(n-2)/2 + l < points:
                with t_utils.timing() as t:
                    res = self.dmel.compute(n, l)
                    answ[p].append((res, t()))
                buf = l
                l = (buf+1)%n
                n += (buf+1)//n
            answ[p] = sp.array(answ[p]).T
            self.iwrite(fdata, answ[p])

        evalPrec(0)
        for p in range(1,prec+1):
            evalPrec(p)
            ax.plot(sp.full_like(answ[p][0], p), sp.absolute(answ[p][0] - answ[p-1][0]), ".")
            fig.savefig(self.path("dmel-%s.png" % label))

        self.dmel.absErr = 10**(-50)
        self.dmel.relErr = 10**(-50)
        self.dmel.MP = None
        self.dmel.psiColP = None
        fdata.close()

    def run(self):
        super(Test, self).run()

        self.testCmel(alyt.sqedMP0)
        self.testCmel(alyt.sqedMP2)

        self.testCrsc(alyt.sqedMP0)
        self.testCrsc(alyt.sqedMP2)

        self.testDmel(alyt.sqedMP0, alyt.psiColPdisc0)
        self.testDmel(alyt.sqedMP2, alyt.psiColPdisc2)


if __name__ == "__main__":
    instance = Test()
    instance.run()

