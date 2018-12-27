import multiprocessing as mp
import shlex
import sys

from fib import fib


PROC_COUNT = int(sys.argv[1])

procs = []

command_line = 'python fib.py'
# command_line = 'python sleep.py'
command = shlex.split(command_line)

tasks = [37 for _ in range(PROC_COUNT)]

with mp.Pool(4) as pool:
    print(pool.map(fib, tasks))
