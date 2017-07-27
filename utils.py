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
            config[cp] = os.environ[ep]
    return config
