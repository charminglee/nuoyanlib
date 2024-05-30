# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-05-30
#
# ====================================================


from mod.common.mod import Mod
import mod.client.extraClientApi as client_api
import mod.server.extraServerApi as server_api
from _const import (
    LIB_NAME,
    LIB_VERSION,
    LIB_CLIENT_NAME,
    LIB_SERVER_NAME,
    LIB_SERVER_PATH,
    LIB_CLIENT_PATH,
)


@Mod.Binding(LIB_NAME, LIB_VERSION)
class NuoyanLibMain(object):
    @Mod.InitServer()
    def server_init(self):
        if not server_api.GetSystem(LIB_NAME, LIB_SERVER_NAME):
            server_api.RegisterSystem(LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH)

    @Mod.InitClient()
    def client_init(self):
        if not client_api.GetSystem(LIB_NAME, LIB_CLIENT_NAME):
            client_api.RegisterSystem(LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH)









