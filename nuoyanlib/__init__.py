# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-01
|
| ==============================================
"""


# todo：为函数添加调用失败时输出异常信息的功能
# todo：Entity类、Player类
# todo：UI动画
# todo：完善Ny控件


from ._core import _logging


__version__ = "0.9.4-beta"
__author_name__ = "Nuoyan"
__author_qq__ = "1279735247"
__author_email__ = "1279735247@qq.com"


_logging.info("Start loading, ver: %s" % __version__)


def run(dct):
    """
    | 启动「nuoyanlib」。

    -----

    :param dict dct: 请传入globals()

    :return: 无
    :rtype: None
    """
    from mod.common.mod import Mod
    from ._core import _const

    @Mod.Binding(_const.LIB_NAME, _const.LIB_VERSION)
    class NuoyanLibMain(object):
        @Mod.InitServer()
        def server_init(self):
            from _core._server._lib_server import NuoyanLibServerSystem
            NuoyanLibServerSystem.register()

        @Mod.InitClient()
        def client_init(self):
            from _core._client._lib_client import NuoyanLibClientSystem
            NuoyanLibClientSystem.register()

    dct['NuoyanLibMain'] = NuoyanLibMain


del _logging




