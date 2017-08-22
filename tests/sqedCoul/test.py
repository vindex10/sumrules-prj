from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import * # quite boldly but simply enough

import os
import matplotlib.pyplot as plt

from utils import timing, updConf, iwrite

import sumrules.config
sumrules.config.config = updConf(sumrules.config.config)

import sumrules.models.basic
sumrules.models.basic.config = updConf(sumrules.models.basic.config)
m = sumrules.models.basic.config["m"]
dimfactor = sumrules.models.basic.config["dimfactor"]

import sumrules.models.sqedCoul as model

config = updConf({"minS": 4*m**2+0.001
         ,"maxS": 200
         ,"points": 1
         ,"output": "output/tests/sqedCoul/"
         ,"interactive": False})

def pointwiseSigma(mp, points, label="", interactive=False):
    "Test sigma value per point"
    label = "_"+label

    if interactive:
        print("start pointwiseSigma: " + label[1:])

    ts=[0]
    with timing(ts=ts):
        res = list(map(lambda s: (s, dimfactor*model.sigma({"s": s, "MP": mp, "psiColP": model.psiColP})), points))
    with open(os.path.join(config["output"], "meta"), "a") as f:
        iwrite(f, "%s::sigma_evaltime(%d) %f" % (label[1:], len(points), ts[0]), interactive)

    with open(os.path.join(config["output"], "sigma"), "a") as f:
        iwrite(f, "# %s" % label[1:], interactive)
        iwrite(f, "s, sigma", interactive)
        for pair in res:
            iwrite(f, "%e, %e" % pair, interactive)

    plt.plot(*list(zip(*res)))
    plt.savefig(os.path.join(config["output"], "sigma_plot"+label+".png"))

    if interactive:
        print("end pointwiseSigma: " + label[1:])

def dosum(mp, label="", interactive=False):
    "evaluate sumrule for specific MP"
    label = "_" + label

    ts=[0]
    with timing(ts=ts):
        sr = model.sumrule({"minS": config["minS"], "maxS": config["maxS"], "MP": mp, "psiColP": model.psiColP})
    
    with open(os.path.join(config["output"], "meta"), "a") as f:
        iwrite(f, "%s::sumrule_evaltime %f" % (label[1:], ts[0]), interactive)

    with open(os.path.join(config["output"], "sumrule"), "a") as f:
        iwrite(f, "%s::sumrule %f" % (label[1:], sr), interactive)
    return sr

def run(interactive=False):
    if not os.path.exists(config["output"]):
        os.makedirs(config["output"])

    with open(os.path.join(config["output"], "params"), "a") as f:
        # model basic config
        iwrite(f, "# sumrules.models.basic.config", interactive)
        for k, v in sumrules.models.basic.config.items():
            iwrite(f, "%s %s" % (k, str(v)), interactive)

        # model config
        iwrite(f, "# sumrules.config.config", interactive)
        for k, v in sumrules.config.config.items():
            iwrite(f, "%s %s" % (k, str(v)), interactive)

        # test config
        iwrite(f, "# config", interactive)
        for k, v in config.items():
            iwrite(f, "%s %s" % (k, str(v)), interactive)

    points = [config["minS"] + (config["maxS"] - config["minS"])/config["points"]*i for i in range(config["points"])]

    pointwiseSigma(model.MP0, points, "MP0", interactive)
    pointwiseSigma(model.MP2, points, "MP2", interactive)

    s0 = dosum(model.MP0, "MP0", interactive)
    s2 = dosum(model.MP2, "MP2", interactive)


    with open(os.path.join(config["output"], "sumrule"), "a") as f:
        iwrite(f, "s0/s2-1 %f" % (s0/s2 - 1), interactive)

if __name__ == "__main__":
    run(interactive=config["interactive"])
