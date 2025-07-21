# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-21
|
| ==============================================
"""


import threading
import time
import mod.client.extraClientApi as api


# 导入测试
from . import client
def import_server():
    from . import server
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


test("._core._utils")
test("._core.listener")
test("._core._types._events")
test(".client.ui.screen_node")
test(".client.ui.nyc.control")
test(".utils.enum")
test(".utils.item")
test(".utils.utils")




