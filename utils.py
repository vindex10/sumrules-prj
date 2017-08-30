from timeit import default_timer as timer

class timing:
    def __enter__(self):
        timestop = timer()
        return lambda: timer() - timestop
    
    def __exit__(self, type, value, traceback):
        pass

