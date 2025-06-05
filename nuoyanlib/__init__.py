# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


# todo：为函数添加调用失败时输出异常信息的功能
# todo：Entity类、Player类
# todo：UI动画
# todo：完善Ny控件


from ._core._logging import info as _info


__version__ = "0.9.3-beta"
__author_name__ = "Nuoyan"
__author_qq__ = "1279735247"
__author_email__ = "1279735247@qq.com"


_info("Start loading, ver: %s" % __version__)
del _info


def run(dct):
    from mod.common.mod import Mod
    import mod.client.extraClientApi as client_api
    import mod.server.extraServerApi as server_api
    from _core import _const
    from . import config

    if config.DISABLED_MODSDK_LOG:
        _logging.disable_modsdk_loggers()

    @Mod.Binding(_const.LIB_NAME, _const.LIB_VERSION)
    class NuoyanLibMain(object):
        @Mod.InitServer()
        def server_init(self):
            from _core._server._lib_server import NuoyanLibServerSystem
            NuoyanLibServerSystem.register()
            if config.ENABLED_MCP_MOD_LOG_DUMPING:
                server_api.SetMcpModLogCanPostDump(True)

        @Mod.InitClient()
        def client_init(self):
            from _core._client._lib_client import NuoyanLibClientSystem
            NuoyanLibClientSystem.register()
            if config.ENABLED_MCP_MOD_LOG_DUMPING:
                client_api.SetMcpModLogCanPostDump(True)

    dct['NuoyanLibMain'] = NuoyanLibMain





