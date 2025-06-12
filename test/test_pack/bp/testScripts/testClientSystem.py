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


import mod.client.extraClientApi as clientApi
from mod.common.minecraftEnum import *
from modCommon.modConfig import *
from nuoyanlib import client as nyl
from nuoyanlib.client import (
    LvComp,
    PlrComp,
    CompFactory,
    PLAYER_ID,
    event,
)


clientEvent = event(namespace=MOD_NAME, system_name=CLIENT_SYSTEM_NAME)
serverEvent = event(namespace=MOD_NAME, system_name=SERVER_SYSTEM_NAME)


class TemplateClientSystem(nyl.ClientEventProxy, nyl.ClientSystem):
    def __init__(self, namespace, systemName):
        super(TemplateClientSystem, self).__init__(namespace, systemName)
        self.mgrs = {}

    # =========================================== Engine Event Callback ================================================

    def LoadClientAddonScriptsAfter(self, event):
        self._initMgrs()

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================

    def _initMgrs(self):
        for name, path in CLIENT_MGRS.items():
            sysName = path.split(".")[-1]
            self.mgrs[name] = clientApi.RegisterSystem(MOD_NAME, sysName, path)
        for mgr in self.mgrs.values():
            mgr.init()

    def getMgr(self, name):
        return self.mgrs.get(name)


















