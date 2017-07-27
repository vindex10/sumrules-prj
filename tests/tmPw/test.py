import os
import matplotlib.pyplot as plt
import sumrules.models.tmPw as tmPw
import sumrules.models.basic as basic
from utils import timing, updConf

config = updConf({"range": (4*basic.m**2, 300)
         ,"points": 1000
         ,"output": "output/tests/tmPw/"})

def run(interactive=False):
    if not os.path.exists(config["output"]):
        os.makedirs(config["output"])

    with open(os.path.join(config["output"], "sigma"), "w") as f:
        for k, v in config.items():
            pair = "%s %s" % (k, str(v))
            f.write(pair+"\n")
            if interactive:
                print(pair)

    points = [config["range"][0] + (config["range"][1] - config["range"][0])/config["points"]*i for i in range(config["points"])]

    ts=[0]
    with timing(ts=ts, interactive=interactive):
        res = list(map(lambda s: (s, tmPw.sigma({"s": s, "MP": tmPw.MP})), points))
    with open(os.path.join(config["output"], "sigma"), "a") as f:
        f.write("Eval time: %f\n" % ts[0])


    if interactive:
        print(res[-10:])

    with open(os.path.join(config["output"], "sigma"), "a") as f:
        for pair in res:
            f.write("%e, %e\n" % pair)

    plt.plot(*list(zip(*res)))
    plt.savefig(os.path.join(config["output"], "sigma_plot.png"))

    if interactive:
        plt.show()

if __name__ == "__main__":
    run()
