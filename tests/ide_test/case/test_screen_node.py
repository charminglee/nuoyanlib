# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


from nuoyanlib.client.ui.screen_node import NyScreenNode, screen


n = [0]


@screen("", enabled_deferred_init=True)
class SN(NyScreenNode):
    def __init__(self, namespace, name, param):
        super(SN, self).__init__(namespace, name, param)
        n[0] += 1
        assert (namespace, name, param) == args


args = "", "", {'x': 1}
sn = SN(*args)
assert n[0] == 0
sn.Create()
assert n[0] == 1
assert SN.n == 1
assert SN._nyl__instances[0] is sn
sn.Destroy()


args = "a", "b", {'x': 2}
sn = SN(*args)
assert len(SN._nyl__instances) == 1 and SN._nyl__instances[0] is sn
assert n[0] == 1
assert SN.n == 2
sn.Create()
assert n[0] == 2
sn.Destroy()


assert not SN._nyl__instances
