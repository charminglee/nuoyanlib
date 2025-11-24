# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-01
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
    timer = time.clock
except AttributeError:
    timer = time.perf_counter


def test(path):
    path = "nuoyanlib." + path
    module = import_module(path)
    t = timer()
    module.__test__()
    cost = (timer() - t) * 1000
    print(
        "Test passed: {:<40}".format(path + ",")
        + " in {:<6.3f}ms,".format(cost)
    )


test("core._utils")
test("core.listener")
test("core._types._checker")
test("core.server.comp")
test("client.ui.screen_node")
test("client.ui.nyc.control")
test("utils.enum")
test("utils.item")
test("utils.utils")
test("utils.vector")


print("\n\033[33mAll tests passed.")




