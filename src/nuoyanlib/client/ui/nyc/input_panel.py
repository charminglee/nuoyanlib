# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyInputPanel",
]


class NyInputPanel(NyControl):
    """
    输入面板控件类。

    示例
    ----

    >>> self.input_panel = nyl.NyInputPanel(self, "/panel/input_panel")
    >>> self.input_panel.is_modal = True
    >>> self.input_panel.is_swallow = True

    参见
    ----

    - ``NyControl.to_input_panel()`` -- 将通用控件实例转换为输入面板控件实例。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该输入面板控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.INPUT_PANEL

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def is_modal(self):
        """
        [可读写属性]

        当前面板是否为模态框。

        :rtype: bool
        """
        return self._base_control.GetIsModal()

    @is_modal.setter
    def is_modal(self, val):
        """
        [可读写属性]

        当前面板是否为模态框。

        :type val: bool
        """
        if isinstance(val, int):
            val = bool(val)
        self._base_control.SetIsModal(val)

    @property
    def is_swallow(self):
        """
        [可读写属性]

        当前面板输入是否会吞噬事件。

        说明
        ----

        为 ``True`` 时，点击事件不会穿透到世界，如破坏方块、镜头转向不会被响应。

        :rtype: bool
        """
        return self._base_control.GetIsSwallow()

    @is_swallow.setter
    def is_swallow(self, val):
        """
        [可读写属性]

        当前面板输入是否会吞噬事件。

        说明
        ----

        为 ``True`` 时，点击事件不会穿透到世界，如破坏方块、镜头转向不会被响应。

        :type val: bool
        """
        if isinstance(val, int):
            val = bool(val)
        self._base_control.SetIsSwallow(val)

    @property
    def offset_delta(self):
        """
        [可读写属性]

        拖拽偏移量。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetOffsetDelta()

    @offset_delta.setter
    def offset_delta(self, val):
        """
        [可读写属性]

        拖拽偏移量。

        :type val: tuple[float,float]
        """
        self._base_control.SetOffsetDelta(val)

    # endregion

    # region Compatibility =============================================================================================

    set_is_modal     = SetIsModal     = lambda s, *a, **k: s._base_control.SetIsModal(*a, **k)
    get_is_modal     = GetIsModal     = lambda s, *a, **k: s._base_control.GetIsModal(*a, **k)
    set_is_swallow   = SetIsSwallow   = lambda s, *a, **k: s._base_control.SetIsSwallow(*a, **k)
    get_is_swallow   = GetIsSwallow   = lambda s, *a, **k: s._base_control.GetIsSwallow(*a, **k)
    set_offset_delta = SetOffsetDelta = lambda s, *a, **k: s._base_control.SetOffsetDelta(*a, **k)
    get_offset_delta = GetOffsetDelta = lambda s, *a, **k: s._base_control.GetOffsetDelta(*a, **k)

    # endregion





