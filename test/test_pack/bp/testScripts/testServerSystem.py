# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-09
|
| ==============================================
"""


import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import *
from ..modCommon.modConfig import *
from ..nuoyanlib import server as nyl
from ..nuoyanlib.server import (
    LvComp,
    CompFactory,
    event,
)


class TemplateServerSystem(nyl.ServerEventProxy, nyl.ServerSystem):
    def __init__(self, namespace, systemName):
        super(TemplateServerSystem, self).__init__(namespace, systemName)
        self.mgrs = {}

    # =========================================== Engine Event Callback ================================================

    def LoadServerAddonScriptsAfter(self, event):
        self._initMgrs()

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================

    def _initMgrs(self):
        for name, path in SERVER_MGRS.items():
            sysName = path.split(".")[-1]
            self.mgrs[name] = serverApi.RegisterSystem(MOD_NAME, sysName, path)
        for mgr in self.mgrs.values():
            mgr.init()

    def getMgr(self, name):
        return self.mgrs.get(name)





















