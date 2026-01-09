# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-9
#  ⠀
# =================================================


from .. import __version__


LIB_VERSION = __version__.split("-")[0]
LIB_VERSION_UL = __version__.replace(".", "_").replace("-", "_")
LIB_NAME = "NuoyanLib_%s" % LIB_VERSION_UL
LIB_CLIENT_NAME = "NuoyanLibClientSystem_%s" % LIB_VERSION_UL
LIB_SERVER_NAME = "NuoyanLibServerSystem_%s" % LIB_VERSION_UL


class __C: pass
ROOT = __C.__module__.split(".")[0]
del __C


# SHORTCUT = "_shortcut"
# INV27 = "_inv27"
# INV36 = "_inv36"


class TypeStr:
    GROUND_SHATTER_EFFECT = "nuoyanlib:ground_shatter_effect"


GSE_ATTR = "nuoyanlib:ground_shatter_effect_args"











