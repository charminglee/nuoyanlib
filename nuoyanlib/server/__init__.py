# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-22
|
|   nuoyanlib服务端库。
|
| ==============================================
"""


from time import clock as _clock
_t = _clock()


from .._core._sys import check_env as _check_env
from .._core._server._lib_server import NuoyanLibServerSystem as _lib_sys


_check_env("server")
_lib_sys.register()
del _check_env, _lib_sys


from .._core._server.comp import (
    ENGINE_NAMESPACE,
    ENGINE_SYSTEM_NAME,
    ServerSystem,
    CompFactory,
    CF,
    LEVEL_ID,
    LvComp,
)
from .._core.listener import (
    EventArgsProxy,
    ServerEventProxy,
    event,
    listen_event,
    unlisten_event,
    listen_all_events,
    unlisten_all_events,
)
from .._core._error import *
from .._core._utils import (
    try_exec,
    iter_obj_attrs,
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


_consume = (_clock() - _t) * 1000
from .._core._logging import info as _info
_info("nuoyanlib.server loaded in %.3fms" % _consume)
del _clock, _t, _info, _consume
