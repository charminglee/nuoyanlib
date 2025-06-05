# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


from mod.common.mod import Mod
import mod.client.extraClientApi as client_api
from ._core._const import LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH, LIB_VERSION


@Mod.Binding(LIB_NAME, LIB_VERSION)
class NuoyanLibMain(object):
    @Mod.InitClient()
    def init_client(self):
        if not client_api.GetSystem(LIB_NAME, LIB_CLIENT_NAME):
            client_api.RegisterSystem(LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH)

