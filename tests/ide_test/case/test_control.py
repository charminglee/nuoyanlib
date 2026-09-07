# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


from nuoyanlib.client.ui.nyc.control import NyControl
from nuoyanlib.client.ui.screen_node import NyScreenNode


class SN(NyScreenNode):
    pass
sn = SN("", "")


n = [0]
class NC(NyControl):
    def __init__(self, ny_screen_node, path):
        NyControl.__init__(self, ny_screen_node, path)
        n[0] += 1
abc = NC(sn, "/abc")
assert NC(sn, "/abc") is abc
assert NC(sn, "/abc2") is not abc
assert n[0] == 2


print(abc)
assert "/abc" in sn._nyc_cache_map
ch = abc / "child"
assert ch.GetPath() == ch.path == "/abc/child"
abc.destroy()
assert "/abc" not in sn._nyc_cache_map
