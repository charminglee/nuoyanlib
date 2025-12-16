# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from mod.common.mod import Mod
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from common.constant import (
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
        s_api.RegisterSystem(MOD_NAME, SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLASS_PATH)

    @Mod.InitClient()
    def modClientInit(self):
        c_api.RegisterSystem(MOD_NAME, CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLASS_PATH)
