# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


if 0:
    from ..screen_node import ScreenNodeExtension


from ....utils.enum import ControlType
from .control import NyControl
from ....core import error


__all__ = [
    "NyProgressBar",
]


class NyProgressBar(NyControl):
    """
    进度条控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 进度条所在UI类的实例（需继承 ScreenNodeExtension）
    :param ProgressBarUIControl progress_bar_control: 通过 asProgressBar() 等方式获取的 ProgressBarUIControl 实例
    """

    CONTROL_TYPE = ControlType.PROGRESS_BAR

    def __init__(self, screen_node_ex, progress_bar_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, progress_bar_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def progress(self):
        """
        [只写属性]

        进度条进度，范围为 [0, 1]。

        :rtype: None
        """
        raise error.GetPropertyError("value")

    @progress.setter
    def progress(self, val):
        """
        [只写属性]

        进度条进度，范围为 [0, 1]。

        :type val: float
        """
        self._base_control.SetValue(val)

    # endregion











