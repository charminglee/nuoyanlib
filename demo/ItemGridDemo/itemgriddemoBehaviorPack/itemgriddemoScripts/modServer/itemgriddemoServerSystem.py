# -*- coding: utf-8 -*-
# ====================================================
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-05-30
#
# ====================================================


import mod.server.extraServerApi as serverApi
from ..modCommon.modConfig import *
# 导入服务端nuoyanlib
import itemgriddemoScripts.nuoyanlib.server as nyl
# 一些常用的工具可直接导入为模块变量
from itemgriddemoScripts.nuoyanlib.server import (
    NuoyanServerSystem,
    listen_for,
    LvComp,
    CompFactory,
)


# 将服务端类继承NuoyanServerSystem，以获得由NuoyanServerSystem提供的各种接口。
class ItemGridDemoServerSystem(NuoyanServerSystem):
    def __init__(self, namespace, systemName):
        super(ItemGridDemoServerSystem, self).__init__(namespace, systemName)

    # =========================================== Engine Event Callback ================================================

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================



















