# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-24
|
| ====================================================
"""


from collections import OrderedDict
from .nuoyanlib.server import get_time


_imp = globals()['__builtins__']['__import__']('importlib').import_module


class Timer(object):
    def __init__(self):
        self.start_time = {}
        self.part_cost = OrderedDict()

    def start(self, part_name=""):
        self.start_time[part_name] = get_time()

    def end(self, part_name=""):
        t = get_time()
        self.part_cost[part_name] = t - self.start_time[part_name]
        self.start_time[part_name] = 0

    def async_mode(self):
        pass


def run_benchmark(path, n=100000):
    module = _imp("test_scripts." + path)
    timer = Timer()
    module.__benchmark__(n, timer)
    print("=" * 45)
    print("[{}]".format(path))
    print("n={}".format(n))
    for part_name, cost in timer.part_cost.items():
        print_res(cost, n, part_name)


def print_res(cost, n, part_name=""):
    avg = (cost * 1000) / n
    if part_name:
        print("> ({}) total: {:.3f}s, avg: {:.6f}ms".format(part_name, cost, avg))
    else:
        print("total: {:.3f}s, avg: {:.6f}ms".format(cost, avg))













