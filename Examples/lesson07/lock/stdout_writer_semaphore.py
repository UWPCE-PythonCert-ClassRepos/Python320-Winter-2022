import random
import sys
import threading
import time

# A Semaphore allows up to N threads to run at once
# allowing more than 1 lets the stdout get intertwinded
# 4 makes it obvious
lock = threading.Semaphore(4)


def write():
    time.sleep(random.random() / 2)
    lock.acquire()
    sys.stdout.write(f"{threading.current_thread().name} writing..")
    time.sleep(random.random())
    sys.stdout.write("..done\n")
    lock.release()


for _ in range(50):
    thread = threading.Thread(target=write)
    thread.start()
    time.sleep(.01)


