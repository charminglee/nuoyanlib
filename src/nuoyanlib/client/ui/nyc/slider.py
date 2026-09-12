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


from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NySlider",
]


class NySlider(NyControl):
    """
    滑动条控件类。

    示例
    ----

    >>> self.slider = nyl.NySlider(self, "/panel/slider")
    >>> self.slider.value = 0.75

    参见
    ----

    - ``NySlider.value`` -- 获取/设置滑动条的值。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该滑动条控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.SLIDER

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def value(self):
        """
        [可读写属性]

        滑动条的值。

        :rtype: float
        """
        return self._base_control.GetSliderValue()

    @value.setter
    def value(self, val):
        """
        [可读写属性]

        滑动条的值。

        :type val: float
        """
        self._base_control.SetSliderValue(val)

    # endregion

    # region Compatibility =============================================================================================

    get_slider_value = GetSliderValue = lambda s, *a, **k: s._base_control.GetSliderValue(*a, **k)
    set_slider_value = SetSliderValue = lambda s, *a, **k: s._base_control.SetSliderValue(*a, **k)

    # endregion





