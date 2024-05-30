# -*- coding: utf-8 -*-
# ====================================================
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-05-30
#
# ====================================================


from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from nuoyanlib import enable_nuoyanlib
from modCommon.constant import (
    MOD_NAME, MOD_VERSION,
    SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLASS_PATH,
    CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLASS_PATH
)


# 在当前模组启用nuoyanlib，必须在其他系统注册前调用
# enable_nuoyanlib()


# @Mod.Binding(name=MOD_NAME, version=MOD_VERSION)
# class ModMain(object):
#     @Mod.InitServer()
#     def modServerInit(self):
#         print 22222
#         serverApi.RegisterSystem(MOD_NAME, SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLASS_PATH)
#
#     @Mod.InitClient()
#     def modClientInit(self):
#         clientApi.RegisterSystem(MOD_NAME, CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLASS_PATH)


LIB_VERSION = "0.5.0"
LIB_VERSION_UL = LIB_VERSION.replace(".", "_")
LIB_NAME = "NuoyanLib_%s" % LIB_VERSION_UL
LIB_CLIENT_NAME = "NuoyanLibClientSystem_%s" % LIB_VERSION_UL
LIB_SERVER_NAME = "NuoyanLibServerSystem_%s" % LIB_VERSION_UL
ROOT = __file__.split(".")[0]
LIB_CLIENT_PATH = "%s.nuoyanlib._core._client._lib_client.NuoyanLibClientSystem" % ROOT
LIB_SERVER_PATH = "%s.nuoyanlib._core._server._lib_server.NuoyanLibServerSystem" % ROOT
@Mod.Binding(LIB_NAME, LIB_VERSION)
class NuoyanLibMain(object):
    @Mod.InitServer()
    def server_init(self):
        if not serverApi.GetSystem(LIB_NAME, LIB_SERVER_NAME):
            serverApi.RegisterSystem(LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH)

    @Mod.InitClient()
    def client_init(self):
        if not clientApi.GetSystem(LIB_NAME, LIB_CLIENT_NAME):
            clientApi.RegisterSystem(LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH)
