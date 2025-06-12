# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
|   nuoyanlib服务端库。
|
| ==============================================
"""


from time import clock
t = clock()


from .._core._sys import check_env
from .._core._server._lib_server import NuoyanLibServerSystem


check_env("server")
NuoyanLibServerSystem.register()
del check_env, NuoyanLibServerSystem


from .._core._server.comp import (
    ENGINE_NAMESPACE,
    ENGINE_SYSTEM_NAME,
    ServerSystem,
    CompFactory,
    CF,
    LEVEL_ID,
    LvComp,
)
from .._core._listener import (
    listen_for,
    unlisten_for,
    EventArgsProxy,
    event,
    ServerEventProxy,
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
    ServerEventEnum as Events,
    ALL_SERVER_ENGINE_EVENTS,
    ALL_SERVER_LIB_EVENTS,
)


from .entity import *
from .hurt import *
from .inv import *
from .structure import *
from ..utils import *


consume = (clock() - t) * 1000
from .._core._logging import info
info("nuoyanlib.server loaded in %.3fms" % consume)
del clock, t, info, consume
