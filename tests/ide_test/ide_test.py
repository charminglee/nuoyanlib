# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-7
#  ⠀
#  ================================================


from importlib import import_module
from threading import Thread
import time


TESTS = [
    ("common.enum"           , "case.test_enum"),
    ("common.mc_math.vector" , "case.test_vector"),
    ("common.mc_math.mc_math", "case.test_mc_math"),
    ("common.utils"          , "case.test_utils"),
    ("common.item"           , "case.test_item"),
    ("core._types._checker"  , "case.test__checker"),
    ("core._utils"           , "case.test__utils"),
    ("core.server.comp"      , "case.test_comp"),
    ("core.listener"         , "case.test_listener"),
    ("client.ui.screen_node" , "case.test_screen_node"),
    ("client.ui.nyc.control" , "case.test_control"),
]


from nuoyanlib.core import _const
_const.DEBUG = True


# 导入测试
import nuoyanlib.client
def import_server():
    import nuoyanlib.server
t = Thread(target=import_server)
t.start()
t.join()


try:
    timer = time.perf_counter
except AttributeError:
    timer = time.clock


def run_test(name, module_name):
    n = 1
    t = timer()
    for _ in range(n):
        import_module(module_name)
    cost = (timer() - t) * 1000
    print(
        "Test passed: {:<35}".format(name)
        + " in {:<12.3f} avg {:<6.3f} (ms)".format(cost, cost / n)
    )


for name, module_name in TESTS:
    run_test(name, module_name)


print("\n\033[33mAll tests passed.")
