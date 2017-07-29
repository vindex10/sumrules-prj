import os
import matplotlib.pyplot as plt
import sumrules.models.tmCoul as tmCoul
import sumrules.models.basic as basic
import sumrules.config
from utils import timing, updConf, moduleVars

sumrules.config = updConf(sumrules.config)
config = updConf({"minS": 4*basic.m**2 + 1
         ,"maxS": 200
         ,"points": 10
         ,"output": "output/tests/tmCoul/"
         ,"interactive": False})

def run(interactive=False):
    if not os.path.exists(config["output"]):
        os.makedirs(config["output"])

    with open(os.path.join(config["output"], "params"), "w") as f:
        # model basic config
        if interactive:
            print("\n# model basic config")
        f.write("# model basic config\n")
        for k, v in moduleVars(basic).items():
            pair = "%s %s" % (k, str(v))
            f.write(pair+"\n")
            if interactive:
                print(pair)

        # model config
        if interactive:
            print("\n# model config")
        f.write("# model config\n")
        for k, v in sumrules.config.items():
            pair = "%s %s" % (k, str(v))
            f.write(pair+"\n")
            if interactive:
                print(pair)

        # test config
        if interactive:
            print("\n# test config")
        f.write("# test config\n")
        for k, v in config.items():
            pair = "%s %s" % (k, str(v))
            f.write(pair+"\n")
            if interactive:
                print(pair)

    points = [config["minS"] + (config["maxS"] - config["minS"])/config["points"]*i for i in range(config["points"])]

    ts=[0]
    with timing(ts=ts, interactive=interactive):
        res = list(map(lambda s: (s, tmCoul.sigma({"s": s, "MP": tmCoul.MP, "psiColP": tmCoul.psiColP})), points))
    with open(os.path.join(config["output"], "meta"), "w") as f:
        f.write("evaltime %f\n" % ts[0])


    if interactive:
        print("s, sigma\n")
        for pair in res[-10:]:
            print("%e, %e\n" % pair)

    with open(os.path.join(config["output"], "sigma"), "a") as f:
        f.write("s, sigma")
        for pair in res:
            f.write("%e, %e\n" % pair)

    plt.plot(*list(zip(*res)))
    plt.savefig(os.path.join(config["output"], "sigma_plot.png"))

    if interactive:
        plt.show()

if __name__ == "__main__":
    run(interactive=config["interactive"])
