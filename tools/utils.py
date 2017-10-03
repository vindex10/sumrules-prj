import timeit

class timing:
    def __enter__(self):
        timestop = timeit.default_timer()
        return lambda: timeit.default_timer() - timestop
    
    def __exit__(self, type, value, traceback):
        pass

