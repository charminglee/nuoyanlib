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
from ...nuoyanlib import client as nyl


class BaseClientMgr(nyl.ClientEventProxy, nyl.ClientSystem):
    def __init__(self, namespace, systemName):
        super(BaseClientMgr, self).__init__(namespace, systemName)
        self.cs = clientApi.GetSystem(MOD_NAME, CLIENT_SYSTEM_NAME)

    # =========================================== Engine Event Callback ================================================

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================

    def init(self):
        # noinspection PyUnresolvedReferences
        for name, mgr in self.cs.mgrs.items():
            setattr(self, name + "Mgr", mgr)
















