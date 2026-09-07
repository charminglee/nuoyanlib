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


from nuoyanlib.client.ui.screen_node import NyScreenNode, screen


n = [0]
@screen("", enabled_deferred_init=True)
class SN(NyScreenNode):
    def __init__(self, namespace, name, param):
        super(SN, self).__init__(namespace, name, param)
        n[0] += 1
sn = SN("", "", {'x': 1})
assert n[0] == 0
sn.Create()
assert n[0] == 1
assert sn.n == 1 # noqa
