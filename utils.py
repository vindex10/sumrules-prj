from types import ModuleType
from timeit import default_timer as timer
import os

class timing:
    def __init__(self, ts=[0], title="Eval time", interactive=True):
        self.title = title
        self.ts = ts
        self.interactive = interactive

    def __enter__(self):
        self.timestop = timer()
        return self.timestop
    
    def __exit__(self, type, value, traceback):
        self.ts[0] = timer() - self.timestop
        if self.interactive:
            out = str(self.ts[0])
            if len(self.title) > 0:
                out = self.title + ": " + out
            print(out)

def updConf(initConfig):
    config = initConfig.copy()
    for cp in config.keys():
        ep = cp.upper()
        if ep in os.environ.keys():
            config[cp] = parseStr(os.environ[ep])
    return config

def parseStr(a):
    res = None

    if a == "True":
        res = True
        return res

    if a == "False":
        res = False
        return res

    try:
        res = int(a) if float(int(a)) == float(a) else float(a)
        return res
    except ValueError:
        res = None
        pass

    res = a if res is None else res
    return res

def moduleVars(mod):
    return {k: v for k,v in mod.__dict__.items()
            if k in dir(mod)
            and not k.startswith("__")
            and not k.startswith("_")
            and not callable(mod.__dict__[k])
            and not isinstance(mod.__dict__[k], ModuleType)}
