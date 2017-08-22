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

import sumrules.models.tmCoul as model

config = updConf({"minS": 4*m**2 + 1
         ,"maxS": 200
         ,"points": 10
         ,"output": "output/tests/tmCoul/"
         ,"interactive": False})

def run(interactive=False):
    if not os.path.exists(config["output"]):
        os.makedirs(config["output"])

    with open(os.path.join(config["output"], "params"), "w") as f:
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

    ts=[0]
    with timing(ts=ts):
        res = list(map(lambda s: (s, model.sigma({"s": s, "MP": model.MP, "psiColP": model.psiColP})), points))
    with open(os.path.join(config["output"], "meta"), "w") as f:
        iwrite(f, "evaltime %f" % ts[0], interactive)

    with open(os.path.join(config["output"], "sigma"), "a") as f:
        iwrite(f, "s, sigma", interactive)
        for pair in res:
            f.write("%e, %e\n" % pair)
        if interactive:
            for pair in res[-10:]:
                print("%e, %e\n" % pair)

    plt.plot(*list(zip(*res)))
    plt.savefig(os.path.join(config["output"], "sigma_plot.png"))

if __name__ == "__main__":
    run(interactive=config["interactive"])
