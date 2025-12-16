# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from collections import OrderedDict
import mod.server.extraServerApi as s_api
from .nuoyanlib.server import get_time
from .nuoyanlib.core._sys import get_lv_comp, is_client


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


def print_msg(msg):
    print(msg)
    if is_client():
        get_lv_comp().TextNotifyClient.SetLeftCornerNotify(str(msg))
    else:
        get_lv_comp().Msg.NotifyOneMessage(s_api.GetPlayerList()[0], str(msg))


def run_benchmark(path, n=100000):
    module = _imp("test_scripts." + path)
    timer = Timer()
    info = []
    module.__benchmark__(n, timer, info)
    print_msg("=" * 45)
    print_msg("[{}]".format(path))
    print_msg("n={}".format(n))
    for part_name, cost in timer.part_cost.items():
        print_res(cost, n, part_name)
    for i in info:
        print_msg(i)


def print_res(cost, n, part_name=""):
    avg = (cost * 1000) / n
    if part_name:
        print_msg("> ({}) total: {:.3f}s, avg: {:.6f}ms".format(part_name, cost, avg))
    else:
        print_msg("total: {:.3f}s, avg: {:.6f}ms".format(cost, avg))













