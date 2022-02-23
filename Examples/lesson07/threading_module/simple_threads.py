"""
A simple demostration of using threads
"""

import random
import time
import threading


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

# using it sequentially:

def run_sequential():
    results = []
    for i in range(10):
        working_function(100, results)
    print(f"{results=}")
    return results


def run_in_threads():
    results = []
    for i in range(10):
        threading.Thread(target=working_function, args=(100, results)).start()
    print(f"{results=}")
    return results


# waiting for the threads to complete:
def run_in_threads_wait():
    results = []
    all_threads = []
    for i in range(10):
        t = threading.Thread(target=working_function, args=(100, results))
        all_threads.append(t)
        t.start()
    for t in all_threads:
        print(f"waiting for thread: {t.ident}")
        t.join()
    print(f"{results=}")
    return results

