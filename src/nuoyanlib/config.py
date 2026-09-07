# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


# region 一般配置 =======================================================================================================

ENABLED_LOG = True
"""
是否开启「nuoyanlib」日志输出。
"""

ENABLED_MODSDK_LOG = True
"""
[实验性]

是否开启 ModSDK 日志输出。
"""

ENABLED_TYPE_CHECKING = True
"""
是否启用「nuoyanlib」对某些函数的参数类型的运行时检查。
"""

ENABLED_EVENT_ARGS_WARPPING = True
"""
是否启用事件参数包装。

启用后所有通过「nuoyanlib」监听的事件的参数会被包装成 ``EventArgsWrapper`` 对象，详见 ``EventArgsWrapper`` 的说明。
"""

# endregion


# region spawn_ground_shatter_effect()函数配置 ==========================================================================

from math import cos, pi

GSE_IN_FUNC = lambda x: 1 if x == 1 else 1 - 2**(-10 * x)
"""
裂地效果上浮阶段使用的缓动函数。

如线性函数 ``lambda⠀x:⠀x`` ，参数 ``x`` 表示经过的时间比例，取值范围为 ``[0,⠀1]`` ，即只取缓动函数定义域中 ``[0,⠀1]`` 部分的值。
"""

GSE_OUT_FUNC = lambda x: 1 - cos(x * pi / 2)
"""
裂地效果下沉阶段使用的缓动函数。
如线性函数 ``lambda⠀x:⠀x`` ，参数 ``x`` 表示经过的时间比例，取值范围为 ``[0,⠀1]`` ，即只取缓动函数定义域中 ``[0,⠀1]`` 部分的值。
"""

GSE_USE_RENDER_TICK = False
"""
裂地效果是否使用渲染帧进行刷新。
"""

# endregion
