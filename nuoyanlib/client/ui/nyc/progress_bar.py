# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from ..ui_utils import ControlType
from .control import NyControl


__all__ = [
    "NyProgressBar",
]


class NyProgressBar(NyControl):
    """
    | 创建 ``NyProgressBar`` 进度条实例。
    | 兼容ModSDK ``ProgressBarUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 进度条所在UI类的实例
    :param ProgressBarUIControl progress_bar_control: 通过asProgressBar()获取的进度条实例
    """

    _CONTROL_TYPE = ControlType.progress_bar

    def __init__(self, screen_node_ex, progress_bar_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, progress_bar_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API ===================================================================================

    # endregion

    # region property proxy ===================================================================================

    # endregion











