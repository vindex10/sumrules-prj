import os
import matplotlib.pyplot as plt

from utils import timing, updConf, iwrite

import sumrules
sumrules.config = updConf(sumrules.config)

import sumrules.models
sumrules.models.config = updConf(sumrules.models.config)
m = sumrules.models.config["m"]

import sumrules.models.tmPw as model

config = updConf({"minS": 4*m**2
         ,"maxS": 300
         ,"points": 1000
         ,"output": "output/tests/tmPw/"
         ,"interactive": False})

def run(interactive=False):
    if not os.path.exists(config["output"]):
        os.makedirs(config["output"])

    with open(os.path.join(config["output"], "params"), "a") as f:
        # model basic config
        iwrite(f, "# sumrules.models.config", interactive)
        for k, v in sumrules.models.config.items():
            iwrite(f, "%s %s" % (k, str(v)), interactive)

        # model config
        iwrite(f, "# sumrules.config", interactive)
        for k, v in sumrules.config.items():
            iwrite(f, "%s %s" % (k, str(v)), interactive)

        # test config
        iwrite(f, "# config", interactive)
        for k, v in config.items():
            iwrite(f, "%s %s" % (k, str(v)), interactive)

    points = [config["minS"] + (config["maxS"] - config["minS"])/config["points"]*i for i in range(config["points"])]

    ts=[0]
    with timing(ts=ts):
        res = list(map(lambda s: (s, model.sigma({"s": s, "MP": model.MP})), points))
    with open(os.path.join(config["output"], "meta"), "a") as f:
        iwrite(f, "evaltime %f" % ts[0], interactive)

    if interactive:
        print(res[-10:])

    with open(os.path.join(config["output"], "sigma"), "a") as f:
        iwrite(f, "s, sigma", interactive)
        for pair in res:
            f.write("%e, %e\n" % pair)
        if interactive:
            for pair in res[-10:]:
                print("%e, %e\n" % pair)

    plt.plot(*list(zip(*res)))
    plt.savefig(os.path.join(config["output"], "sigma_plot.png"))

    if interactive:
        plt.show()

if __name__ == "__main__":
    run(interactive=config["interactive"])
