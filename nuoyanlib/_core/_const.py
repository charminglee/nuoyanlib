# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from .. import __version__


LIB_VERSION = __version__[1:].replace("-beta", "")
LIB_VERSION_UL = LIB_VERSION.replace(".", "_")
LIB_NAME = "NuoyanLib_%s" % LIB_VERSION_UL
LIB_CLIENT_NAME = "NuoyanLibClientSystem_%s" % LIB_VERSION_UL
LIB_SERVER_NAME = "NuoyanLibServerSystem_%s" % LIB_VERSION_UL
# __file__: (pc) scripts.nuoyanlib._core._const   (pe) scripts/nuoyanlib/_core/_const.py
ROOT = __file__.replace("/", ".").split("._const")[0]
LIB_CLIENT_PATH = "%s._client._lib_client.NuoyanLibClientSystem" % ROOT
LIB_SERVER_PATH = "%s._server._lib_server.NuoyanLibServerSystem" % ROOT


SHORTCUT = "_shortcut"
INV27 = "_inv27"
INV36 = "_inv36"









