from calendar import timegm
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from functools import lru_cache
from time import time


@contextmanager
def timeit(label):
    start = time()
    yield
    print(label, time() - start)


@lru_cache(100)
def lstr2idate(date_string: str):
    return int(timegm(datetime.strptime(date_string, "%Y-%m-%d").timetuple()) / (24 * 60 * 60))


def decimal_if_not_empty(s):
    return Decimal(s) if s else None


def make_index(data, attrs):
    index = defaultdict(list)
    for obj in data:
        key = tuple(getattr(obj, attrib) for attrib in attrs)
        index[key].append(obj)
    return index
