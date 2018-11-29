"""
os.fork
"""
"""
import os

pid = os.fork()
if pid == 0:
    print(f"MAIN pid: {pid}")
else:
    print(f"CHILD pid: {pid}")
"""

"""
multiprocessing
"""
from multiprocessing import Process


def f(_str):
    print(f"amazing process! _str = {_str}")


prcs1 = Process(target=f, kwargs={"_str": "WOW"})
prcs1.start()  # creating process and start it
prcs1.join()  # waiting for our child...




print("\n\nAnd now let's try Process class inheritance (from Process class):")
class MyProcess(Process):
    def __init__(self, **kwargs):  # kwargs only for practice...
        super().__init__()
        self._str = kwargs["_str"]

    def run(self):
        print()
        print(f"amazing process! _str = {self._str}")


prcs2 = MyProcess(_str="DOUBLE WOW")
prcs2.start()
prcs2.join()




print("\n\nNow let's try multiprocessing.Pool:")
from multiprocessing import Pool
import os


def func_for_pool(x):
    print(f"{os.getpid()}: {x} ")
    return x**9


with Pool(5) as p:
    print(p.map(func_for_pool, [*range(5)]))




print("\n\nNow let's try thread with concurrent module:")
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randint
from time import sleep


def f(id_):
    slp_time = randint(0, 2)
    print(f"BEGIN: {id_:2}; slp_time: {slp_time}")
    sleep(slp_time)
    print(f"END    {id_:2};")
    return id_


with ThreadPoolExecutor(max_workers=2) as pool:
    thrds = [pool.submit(f, i) for i in range(1, 2)]
    sleep(1)
    for future in as_completed(thrds):
        print(f"id:     {future.result():2} completed")




print("\n\nRLock and Conditions...")
from concurrent.futures import ThreadPoolExecutor, as_completed
from random import randint
from time import sleep
import threading


class Queue(object):
    def __init__(self, size=5):
        self._size = size
        self._queue = []
        self._mutex = threading.RLock()
        self._empty = threading.Condition(self._mutex)
        self._full = threading.Condition(self._mutex)

    def put(self, val):
        with self._full:
            while len(self._queue) >= self._size:
                self._full.wait()
            self._queue.append(val)
            self._empty.notify()

    def get(self):
        with self._empty:
            while len(self._queue) == 0:
                self._empty.wait()
            ret = self._queue.pop(0)
            self._full.notify()
            return ret

def f_queue_put(queue, thread_id):
    print(f"Th {thread_id} put")
    queue.put(thread_id)
    print(f"Th {thread_id} end")


def f_queue_get(queue, thread_id):
    print(f"Th {thread_id} get")
    print(f"Th {thread_id} gotten: {queue.get()}")
    print(f"Th {thread_id} end")


queue = Queue()




print("\n\nThreadPoolExecutor...")
with ThreadPoolExecutor(max_workers=6) as pool:
    thrds_get = [pool.submit(f_queue_get, queue, i) for i in range(3)]
    sleep(3)
    thrds_put = [pool.submit(f_queue_put, queue, i+3) for i in range(3)]

    for thrd in as_completed(thrds_get):
        thrd.result()
    for thrd in as_completed(thrds_put):
        thrd.result()
print("That's all")
