# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  ================================================


from ..core._const import *
from ..core.server.comp import *
from ..core.listener import *
from ..core.error import *


from .entity import *
from .hurt import *
from .inv import *
from .block import *
from .lobby import *
from .motion import *


from ..common import *
from .. import config, __version__, __author__, __author_qq__, __author_email__


from ..core.system import __NyServerSystem


class NyServerSystem(__NyServerSystem):
    """
    服务端事件代理类。

    继承 ``NyServerSystem`` 后，所有 ModSDK 服务端事件无需监听，编写一个与事件同名的方法即可使用，
    且事件参数采用对象形式，支持参数名补全。

    对于使用 ``@event`` 装饰器监听事件，无需在 ``__init__()`` 方法手动调用 ``listen_all_events()``。
    """
