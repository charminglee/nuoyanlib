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
#   Last Modified : 2025-05-28
#
# ====================================================


"""
nuoyanlib客户端库。
"""


from .._core._sys import check_env
from .._core._client._lib_client import NuoyanLibClientSystem


check_env("client")
NuoyanLibClientSystem.init()
del check_env, NuoyanLibClientSystem


from .._core._client._comp import (
    ENGINE_NAMESPACE,
    ENGINE_SYSTEM_NAME,
    ClientSystem,
    CompFactory,
    PLAYER_ID,
    LEVEL_ID,
    PlrComp,
    LvComp,
)
from .._core._listener import (
    event,
    ClientEventProxy,
)
from .effect import *
from .player import *
from .setting import *
from .sound import *
from .render import *
from .camera import *
from .ui import *
from ..utils import *
