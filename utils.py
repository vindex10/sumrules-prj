from types import ModuleType
from timeit import default_timer as timer
import os
import re

class timing:
    def __enter__(self):
        timestop = timer()
        return lambda: timer() - timestop
    
    def __exit__(self, type, value, traceback):
        pass

# mark as deprecated
def moduleVars(mod):
    return {k: v for k,v in mod.__dict__.items()
            if k in dir(mod)
            and not k.startswith("__")
            and not k.startswith("_")
            and not callable(mod.__dict__[k])
            and not isinstance(mod.__dict__[k], ModuleType)}
