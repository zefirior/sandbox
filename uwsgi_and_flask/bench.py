from contextlib import contextmanager
import multiprocessing as mp
import requests
import sys
from time import time
import threading as thr


URL = sys.argv[1]
CORE_NUM = 4
WORKER_NUM = 50
REQUEST_NUM = int(sys.argv[2])


@contextmanager
def context_timeit(label):
    start = time()
    yield
    print(label, time() - start)


session = requests.Session()


def do_request(request_num):
    for _ in range(request_num):
        requests.get(URL)


with context_timeit("brutforce threading"):

    workers = []
    for _ in range(WORKER_NUM):
        thread = thr.Thread(target=do_request, args=(REQUEST_NUM, ))
        thread.start()
        workers.append(thread)

    for thread in workers:
        thread.join()


# with context_timeit("brutforce multiprocessing"):
#     with mp.Pool(CORE_NUM) as pool:
#         pool.map(do_request, [REQUEST_NUM for _ in range(WORKER_NUM)])
