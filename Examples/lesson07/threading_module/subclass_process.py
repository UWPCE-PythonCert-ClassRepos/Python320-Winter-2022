"""
A simple demonstration of subclassing threads

Same as the simple_threads.py example, but with a Process subclass

Note that subprocesses donot share the same objects
-- so appending to a passed-in list doesn't work.
"""

import random
import time
import multiprocessing


def working_function(max, storage=None):
    """
    an example function that does very little, but
    simulates a complex computation
    """
    num = random.randint(1, max)
    # pause for up to two seconds to simulate computation time
    time.sleep(random.random() * 2)

    if storage is not None:
        storage.append(num)
    print("computed", num)
    return num


class WorkingProcess(multiprocessing.Process):

    def __init__(self, max, storage=None):
        self.max = max
        self.storage = storage
        super().__init__()

    def run(self):
        working_function(self.max, self.storage)


# using it sequentially:

def run_sequential():
    results = []
    for i in range(10):
        working_function(100, results)
    print(f"{results=}")


def run_in_subprocesses():
    results = []
    for i in range(10):
        WorkingProcess(100, results).start()
    print(f"{results=}")
    return results


# waiting for the processes to complete:
def run_in_subprocesses_wait():
    results = []
    all_processes = []
    for i in range(10):
        wp = WorkingProcess(100, results)
        all_processes.append(wp)
        wp.start()

    # make sure they are all done before finishing.
    for wp in all_processes:
        print(f"waiting for process: {wp.ident}")
        wp.join()

    print(f"{results=}")
    return results


if __name__ == "__main__":
    # run_sequential()

    # results1 = run_in_subprocesses()
    # print("results after calling run_in_subprocesses", results1)

    results2 = run_in_subprocesses_wait()
    print("results after calling run_in_subprocesses_wait", results2)

    # print("results after waiting:", results1)
    # print("results after waiting:", results2)
