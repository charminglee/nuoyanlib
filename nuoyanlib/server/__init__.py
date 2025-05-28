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
#   Last Modified : 2025-05-28
#
# ====================================================


"""
nuoyanlib服务端库。
"""


from .._core._sys import check_env
from .._core._server._lib_server import NuoyanLibServerSystem


check_env("server")
NuoyanLibServerSystem.init()
del check_env, NuoyanLibServerSystem


from .._core._server._comp import (
    ENGINE_NAMESPACE,
    ENGINE_SYSTEM_NAME,
    ServerSystem,
    CompFactory,
    LEVEL_ID,
    LvComp,
)
from .._core._listener import (
    event,
    ServerEventProxy,
)
from .entity import *
from .hurt import *
from .inv import *
from .structure import *
from ..utils import *
