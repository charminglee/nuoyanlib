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


from nuoyanlib.core.server.comp import CF, LvComp


assert CF("-1") is CF("-1")
assert CF("-1") is not CF("-2")
assert LvComp.BlockInfo is LvComp.BlockInfo
