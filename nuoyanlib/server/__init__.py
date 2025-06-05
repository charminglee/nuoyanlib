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
|   nuoyanlib服务端库。
|
| ==============================================
"""


from .._core._sys import check_env
from .._core._server._lib_server import NuoyanLibServerSystem


check_env("server")
NuoyanLibServerSystem.register()
del check_env, NuoyanLibServerSystem


from .._core._server._comp import (
    ENGINE_NAMESPACE,
    ENGINE_SYSTEM_NAME,
    ServerSystem,
    CompFactory,
    CF,
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
