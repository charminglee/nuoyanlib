# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-08
|
|   nuoyanlib服务端库。
|
| ==============================================
"""


try:
    from time import clock as _clock
    _t = _clock()
except ImportError:
    _clock = None
    _t = 0


from .._core._sys import check_env as _check_env
from .._core import _error
from .._core._server._lib_server import NuoyanLibServerSystem as _lib_sys_cls
from .._core._logging import info as _info


_check_env("server")
_ins = _lib_sys_cls.register()
if not _ins:
    raise _error.NuoyanLibServerSystemRegisterError


if _ins.__lib_flag__ == 0:
    # 首次加载
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

    _ins.__lib_flag__ = 1

    if _clock:
        _consume = (_clock() - _t) * 1000
        _info("nuoyanlib.server loaded in %.3fms (first loading)" % _consume)
        del _consume
else:
    # 引用内存中已加载的库，确保相同版本的代码只加载一次
    _dct = {
        k: v
        for k, v in _ins.get_lib_dict().items()
        if not k.startswith("_")
    }
    globals().update(_dct)
    del _dct

    if _clock:
        _consume = (_clock() - _t) * 1000
        _info("nuoyanlib.server loaded in %.3fms (ref)" % _consume)
        del _consume


del _check_env, _lib_sys_cls, _ins, _error, _info
del _clock, _t

