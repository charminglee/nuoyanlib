# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN AS IS BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-07-05
#
# ====================================================


from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
from ._core._const import LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH, LIB_VERSION


@Mod.Binding(LIB_NAME, LIB_VERSION)
class NuoyanLibMain(object):
    @Mod.InitClient()
    def init_client(self):
        clientApi.RegisterSystem(LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH)

