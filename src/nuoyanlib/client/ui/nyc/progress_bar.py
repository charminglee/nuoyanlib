# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ....core import error
from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyProgressBar",
]


class NyProgressBar(NyControl):
    """
    进度条控件类。

    示例
    ----

    >>> self.progress_bar = nyl.NyProgressBar(self, "/panel/progress")
    >>> self.progress_bar.progress = 0.5

    参见
    ----

    - ``NyProgressBar.progress`` -- 获取/设置进度条的进度值。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该进度条控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.PROGRESS_BAR

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

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

    # region Compatibility =============================================================================================

    set_value = SetValue = lambda s, *a, **k: s._base_control.SetValue(*a, **k)

    # endregion





