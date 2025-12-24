# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-23
#  ⠀
# =================================================


# todo：Entity类、Player类，对事件返回的entityId、playerId进行封装
# todo：完善Ny控件
# todo：UI动画框架
# todo：event热更新
# todo：完善接口的异常处理
# todo：@async
# todo：容器UI
# todo：nbt


__version__ = "1.0.0-beta.1"
__author__ = "Nuoyan"
__author_qq__ = "1279735247"
__author_email__ = "1279735247@qq.com"


def run(dct):
    """
    | 启动「nuoyanlib」。

    -----

    :param dict dct: 请传入globals()

    :return: 无
    :rtype: None
    """
    from mod.common.mod import Mod
    from .core import _const, _logging

    _logging.info("Start loading, version: %s, script: %s" % (__version__, _const.ROOT), show_env=False)

    @Mod.Binding(_const.LIB_NAME, _const.LIB_VERSION)
    class NuoyanLibMain(object):
        @Mod.InitServer()
        def server_init(self):
            from core.server._lib_server import NuoyanLibServerSystem
            NuoyanLibServerSystem.register()

        @Mod.InitClient()
        def client_init(self):
            from core.client._lib_client import NuoyanLibClientSystem
            NuoyanLibClientSystem.register()

    dct['NuoyanLibMain'] = NuoyanLibMain








