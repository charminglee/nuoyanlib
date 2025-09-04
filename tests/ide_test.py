# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-05
|
| ==============================================
"""


import threading
import time
import mod.client.extraClientApi as api


# 导入测试
import nuoyanlib.client
from nuoyanlib._core._sys import load_extensions
load_extensions()
def import_server():
    import nuoyanlib.server
    load_extensions()
threading.Thread(target=import_server).start()


def test(path):
    turns = 50
    t = time.clock()
    m = api.ImportModule(path)
    for _ in range(turns):
        m.__test__()
    c = (time.clock() - t) * 1000
    print(
        "Test passed: {:<25}".format(path + ",")
        + " in {:<8.3f}ms,".format(c)
        + " avg {:<6.3f}ms".format(c / turns)
    )


test("nuoyanlib._core._utils")
test("nuoyanlib._core.event.listener")
test("nuoyanlib._core.event._events")
test("nuoyanlib._core._types._checker")
test("nuoyanlib.client.ui.screen_node")
test("nuoyanlib.client.ui.nyc.control")
test("nuoyanlib.utils.enum")
test("nuoyanlib.utils.item")
test("nuoyanlib.utils.utils")


print("\n\033[33mAll tests passed.")




