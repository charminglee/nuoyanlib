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
#   Last Modified : 2025-01-10
#
# ====================================================


"""
nuoyanlib服务端库。
"""


from .._core._const import LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH
import mod.server.extraServerApi as server_api
if not server_api.GetSystem(LIB_NAME, LIB_SERVER_NAME):
    server_api.RegisterSystem(LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH)
del server_api, LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH


from .._core._server._comp import *
from .._core._server._listener import (
    event,
)
from .server_system import *
from .entity import *
from .hurt import *
from .inv import *
from .structure import *
from ..utils import *
