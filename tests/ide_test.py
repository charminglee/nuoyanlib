# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-11
|
| ====================================================
"""


from importlib import import_module
import threading
import time


# 导入测试
import nuoyanlib.client
from nuoyanlib.core._sys import load_extensions
load_extensions()
def import_server():
    import nuoyanlib.server
    load_extensions()
t = threading.Thread(target=import_server)
t.start()
t.join()


try:
    timer = time.perf_counter
except AttributeError:
    timer = time.clock


def test(path):
    n = 10000
    path = "nuoyanlib." + path
    module = import_module(path)
    t = timer()
    for _ in xrange(n):
        module.__test__()
    cost = (timer() - t) * 1000
    print(
        "Test passed: {:<35}".format(path)
        + " in {:<12.3f} avg {:<6.3f} (ms)".format(cost, cost / n)
    )


test("utils.enum")
test("core._types._checker")
test("core._utils")
test("core.server.comp")
test("core.listener")
test("client.ui.screen_node")
test("client.ui.nyc.control")
test("utils.item")
test("utils.utils")
test("utils.vector")


print("\n\033[33mAll tests passed.")




