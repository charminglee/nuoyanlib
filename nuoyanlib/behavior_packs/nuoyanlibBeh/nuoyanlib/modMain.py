# -*- coding: utf-8 -*-


from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
from .constants import *


@Mod.Binding(name=MOD_NAME, version="1.0.0")
class NuoyanLibMain(object):
    @Mod.InitClient()
    def init_client(self):
        clientApi.RegisterSystem(MOD_NAME, MOD_SERVER_NAME, MOD_SERVER_PATH)

