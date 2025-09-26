# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-23
|
|   「nuoyanlib」客户端库。
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
from .._core._client._lib_client import NuoyanLibClientSystem as _lib_sys_cls
from .._core._logging import info as _info


_check_env("client")
_ins = _lib_sys_cls.register()
if not _ins:
    raise _error.NuoyanLibClientSystemRegisterError


if 1 or _ins.__lib_flag__ == 0:
    # 首次加载
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
    from .._core.event.listener import ClientEventProxy
    from .._core.event._events import (
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
    from .. import config

    _ins.__lib_flag__ = 1

    if _clock:
        _consume = (_clock() - _t) * 1000
        _info("Loaded in %.3fms (first loading)", _consume)
        del _consume
else:
    # 引用内存中已加载的对象，确保相同版本的代码只加载一次
    _dct = {
        k: v
        for k, v in _ins.get_lib_dict().items()
        if not k.startswith("_")
    }
    globals().update(_dct)
    del _dct

    if _clock:
        _consume = (_clock() - _t) * 1000
        _info("Loaded in %.3fms (ref)", _consume)
        del _consume


del _check_env, _lib_sys_cls, _ins, _error, _info
del _clock, _t
