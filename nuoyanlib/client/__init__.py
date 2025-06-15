# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-15
|
|   nuoyanlib客户端库。
|
| ==============================================
"""


from time import clock
_t = clock()


from .._core._sys import check_env
from .._core._client._lib_client import NuoyanLibClientSystem


check_env("client")
NuoyanLibClientSystem.register()
del check_env, NuoyanLibClientSystem


from .._core._client.comp import (
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
    EventArgsProxy,
    ClientEventProxy,
    event,
    listen_event,
    unlisten_event,
    listen_all_events,
    unlisten_all_events,
)
from .._core._error import *
from .._core._utils import (
    cached_property,
    CachedObject,
    hook_method,
    cached_method,
    cached_func,
    singleton,
)
from .._core._types._events import (
    ClientEventEnum as Events,
    ALL_CLIENT_ENGINE_EVENTS,
    ALL_CLIENT_LIB_EVENTS,
)


from .effect import *
from .player import *
from .setting import *
from .sound import *
from .render import *
from .camera import *
from .ui import *
from ..utils import *


_consume = (clock() - _t) * 1000
from .._core._logging import info
info("nuoyanlib.client loaded in %.3fms" % _consume)
del clock, _t, info, _consume
