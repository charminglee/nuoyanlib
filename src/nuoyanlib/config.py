# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-07
|
| ==============================================
"""


# region 一般配置 =======================================================================================================

ENABLED_LOG = True
"""
| [需要重载]
| 是否输出「nuoyanlib」日志信息。
"""

DISABLED_MODSDK_LOG = False
"""
| [需要重载] [实验性]
| 是否关闭ModSDK日志输出。
"""

ENABLED_TYPE_CHECKING = True
"""
| [需要重载]
| 是否启用「nuoyanlib」对某些函数的参数类型的运行时检查（关闭可获得少许性能提升）。
"""

ENABLED_MCP_MOD_LOG_DUMPING = False
"""
| [需要重载]
| 是否将当前Mod的错误信息输出到McpModLog日志（目前正式服已阉割该功能）。
"""

# endregion

# region spawn_ground_shatter_effect()函数配置 ==========================================================================

from .utils.time_ease import TimeEaseFunc

GSE_IN_FUNC = TimeEaseFunc.out_expo
"""
| 裂地效果上浮阶段使用的缓动函数，如线性函数 ``lambda⠀x:⠀x`` ，参数 ``x`` 表示经过的时间比例，取值范围为 [0,⠀1] ，即只取缓动函数定义域中 [0,⠀1] 部分的值。
"""

GSE_OUT_FUNC = TimeEaseFunc.in_sine
"""
| 裂地效果下沉阶段使用的缓动函数，如线性函数 ``lambda⠀x:⠀x`` ，参数 ``x`` 表示经过的时间比例，取值范围为 [0,⠀1] ，即只取缓动函数定义域中 [0,⠀1] 部分的值。
"""

GSE_USE_RENDER_TICK = False
"""
| [需要重载]
| 裂地效果是否使用渲染帧进行刷新。
"""

# endregion
