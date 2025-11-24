# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyInputPanel",
]


class NyInputPanel(NyControl):
    """
    输入面板控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 输入面板所在UI类的实例（需继承ScreenNodeExtension）
    :param InputPanelUIControl input_panel_control: 通过asInputPanel()等方式获取的InputPanelUIControl实例
    """

    CONTROL_TYPE = ControlType.INPUT_PANEL

    def __init__(self, screen_node_ex, input_panel_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, input_panel_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

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

        为 ``True`` 时，点击事件不会穿透到世界，如破坏方块、镜头转向不会被响应。

        :rtype: bool
        """
        return self._base_control.GetIsSwallow()

    @is_swallow.setter
    def is_swallow(self, val):
        """
        [可读写属性]

        当前面板输入是否会吞噬事件。

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
        self._base_control.SetOffsetDelta(tuple(val))

    # endregion











