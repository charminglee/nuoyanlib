# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-7-14
#  ⠀
# =================================================


# todo：库函数精简
# todo：完善接口的异常处理
# todo：完善Ny控件
# todo：UI动画框架
# todo：Entity类、Player类，对事件返回的entityId、playerId进行封装（可编写一个装饰器，仅对使用该装饰器的事件启用该功能，节约性能）
# todo：event热更新
# todo：nbt
# todo：@async
# todo：运镜框架
# todo：容器UI
# todo：event_filter


__version__ = "1.0.0-beta.1"
__author__ = "Nuoyan"
__author_qq__ = "1279735247"
__author_email__ = "1279735247@qq.com"


def run(dct):
    """
    启动「nuoyanlib」。

    -----

    :param dict dct: 固定传入 globals()

    :return: 无
    :rtype: None
    """
    from mod.common.mod import Mod
    from .core import _const, _logging

    _logging.info("Start loading, version: %s, script: %s" % (__version__, _const.ROOT), show_env=False)

    @Mod.Binding(_const.LIB_NAME, _const.LIB_VERSION)
    class NuoyanLibMain(object):
        @Mod.InitServer()
        def init_server(self):
            from .core.server._lib_server import NuoyanLibServerSystem
            NuoyanLibServerSystem.run()

        @Mod.InitClient()
        def init_client(self):
            from .core.client._lib_client import NuoyanLibClientSystem
            NuoyanLibClientSystem.run()

    dct['NuoyanLibMain'] = NuoyanLibMain








