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


from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from modCommon.constant import (
    MOD_NAME, MOD_VERSION,
    SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLASS_PATH,
    CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLASS_PATH
)


import nuoyanlib
nuoyanlib.run(globals())


@Mod.Binding(MOD_NAME, MOD_VERSION)
class NuoyanModMain(object):
    @Mod.InitServer()
    def modServerInit(self):
        serverApi.RegisterSystem(MOD_NAME, SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLASS_PATH)

    @Mod.InitClient()
    def modClientInit(self):
        clientApi.RegisterSystem(MOD_NAME, CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLASS_PATH)
