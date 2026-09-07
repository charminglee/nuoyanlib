# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-7
#  ⠀
#  ================================================


from typing import Type


from ..core._const import (
    MOD_NAME,
    CLIENT_MODULES,
    SERVER_MODULES,
    CLIENT_SYSTEMS,
    SERVER_SYSTEMS,
)
from ..core.client.comp import *
from ..core.listener import *
from ..core.error import *


from .effect import *
from .setting import *
from .render import *
from .camera import *
from .ui import *


from ..common import *
from .. import (
    config,
    __version__,
    __author__,
    __author_qq__,
    __author_email__,
)


from ..core.system import __NyClientSystem


NyClientSystem: Type[__NyClientSystem]
"""
客户端事件代理类。

继承 ``NyClientSystem`` 后，所有 ModSDK 客户端事件无需监听，编写一个与事件同名的方法即可使用，
且事件参数采用对象形式，支持参数名补全。

对于使用 ``@event`` 装饰器监听事件，无需在 ``__init__()`` 方法手动调用 ``listen_all_events()``。
"""
