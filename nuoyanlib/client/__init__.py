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
#   Last Modified : 2025-02-21
#
# ====================================================


"""
nuoyanlib客户端库。
"""


from .._core._sys import is_client
if not is_client():
    raise ImportError("Cannot import nuoyanlib.client in server environment.")
del is_client


from .._core._const import LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH
import mod.client.extraClientApi as client_api
if not client_api.GetSystem(LIB_NAME, LIB_CLIENT_NAME):
    client_api.RegisterSystem(LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH)
del client_api, LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH


from .._core._client._comp import (
    CLIENT_ENGINE_NAMESPACE,
    CLIENT_ENGINE_SYSTEM_NAME,
    ClientSystem,
    CompFactory,
    PLAYER_ID,
    LEVEL_ID,
    PlrComp,
    LvComp,
)
from .._core._listener import (
    quick_listen,
    event,
)


from .client_system import *
from .effect import *
from .player import *
from .setting import *
from .sound import *
from .render import *
from .camera import *


from .ui import *


from ..utils import *
