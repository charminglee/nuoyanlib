# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-7
#  ⠀
#  ================================================


from ..nuoyanlib.common.enum import StrEnum, auto


MOD_NAME = "Test"
MOD_NAME_S = MOD_NAME.lower()
MOD_VERSION = "0.0.1"
CLIENT_SYSTEM_NAME = "MainClientSystem"
CLIENT_SYSTEM_CLASS_PATH = "%s_scripts.main_client.%s" % (MOD_NAME_S, CLIENT_SYSTEM_NAME)
SERVER_SYSTEM_NAME = "MainServerSystem"
SERVER_SYSTEM_CLASS_PATH = "%s_scripts.main_server.%s" % (MOD_NAME_S, SERVER_SYSTEM_NAME)


UI_NUOYANLIB_TEST = "NuoyanlibTest"
UI_PATH_NUOYANLIB_TEST = "%s_scripts.ui.nuoyanlib_test" % MOD_NAME_S


class ClientEvent(StrEnum):
    OnKeyPressInGame = auto()






