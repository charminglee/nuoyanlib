# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
|   nuoyanlib客户端库。
|
| ===================================
"""


from .._core._sys import check_env
from .._core._client._lib_client import NuoyanLibClientSystem


check_env("client")
NuoyanLibClientSystem.register()
del check_env, NuoyanLibClientSystem


from .._core._client._comp import (
    ENGINE_NAMESPACE,
    ENGINE_SYSTEM_NAME,
    ClientSystem,
    CompFactory,
    CF,
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
