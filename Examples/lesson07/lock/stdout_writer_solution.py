import random
import sys
import threading
import time

lock = threading.Lock()


def write():
    time.sleep(random.random() / 2)
    lock.acquire()
    sys.stdout.write(f"{threading.current_thread().name} writing..")
    time.sleep(random.random() / 2)
    sys.stdout.write("..done\n")
    lock.release()


threads = []
for i in range(50):
    thread = threading.Thread(target=write)
    thread.daemon = True  # allow ctrl-c to end
    thread.start()
    threads.append(thread)
    time.sleep(.01)

# Now join() them all so the program won't terminate early
# required because these are all daemon threads
for thread in threads:
    thread.join()

