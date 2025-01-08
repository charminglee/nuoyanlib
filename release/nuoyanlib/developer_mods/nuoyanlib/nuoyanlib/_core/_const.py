# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-07-06
#
# ====================================================


from .. import __version__


LIB_VERSION = __version__[1:].replace("-beta", "")
LIB_VERSION_UL = LIB_VERSION.replace(".", "_")
LIB_NAME = "NuoyanLib_%s" % LIB_VERSION_UL
LIB_CLIENT_NAME = "NuoyanLibClientSystem_%s" % LIB_VERSION_UL
LIB_SERVER_NAME = "NuoyanLibServerSystem_%s" % LIB_VERSION_UL
ROOT = __file__.split("/" if "/" in __file__ else ".")[0] # pc: scripts.nuoyanlib._core._const   pe: scripts/nuoyanlib/_core/_const.py
LIB_CLIENT_PATH = "%s._core._client._lib_client.NuoyanLibClientSystem" % ROOT
LIB_SERVER_PATH = "%s._core._server._lib_server.NuoyanLibServerSystem" % ROOT


SHORTCUT = "_shortcut"
INV27 = "_inv27"
INV36 = "_inv36"









