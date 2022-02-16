
import time

class Timer:
    def __init__(self):
        pass

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        stop = time.time()
        elapsed = stop - self.start
        if elapsed < 1:
            elapsed *= 1000
            print(f"elapsed time = {elapsed:.2f} milliseconds")
        else:
            print(f"elapsed time = {elapsed:.2f} seconds")
