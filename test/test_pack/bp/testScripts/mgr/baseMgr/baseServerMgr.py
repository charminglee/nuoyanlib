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
from ...nuoyanlib import server as nyl


class BaseServerMgr(nyl.ServerEventProxy, nyl.ServerSystem):
    def __init__(self, namespace, systemName):
        super(BaseServerMgr, self).__init__(namespace, systemName)
        self.ss = serverApi.GetSystem(MOD_NAME, SERVER_SYSTEM_NAME)

    # =========================================== Engine Event Callback ================================================

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================

    def init(self):
        # noinspection PyUnresolvedReferences
        for name, mgr in self.ss.mgrs.items():
            setattr(self, name + "Mgr", mgr)
















