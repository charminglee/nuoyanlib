# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-22
|
| ==============================================
"""


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyInputPanel",
]


class NyInputPanel(NyControl):
    """
    | 创建 ``NyInputPanel`` 输入面板实例。
    | 兼容ModSDK ``InputPanelUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 输入面板所在UI类的实例
    :param InputPanelUIControl input_panel_control: 通过asInputPanel()获取的输入面板实例
    """

    _CONTROL_TYPE = ControlType.input_panel

    def __init__(self, screen_node_ex, input_panel_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, input_panel_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region property proxy ============================================================================================

    @property
    def is_modal(self):
        """
        [可读写属性]

        | 当前面板是否为模态框。

        :rtype: bool
        """
        return self.base_control.GetIsModal()

    @is_modal.setter
    def is_modal(self, val):
        """
        [可读写属性]

        | 当前面板是否为模态框。

        :type val: bool
        """
        if isinstance(val, int):
            val = bool(val)
        self.base_control.SetIsModal(val)

    @property
    def is_swallow(self):
        """
        [可读写属性]

        | 当前面板输入是否会吞噬事件，为 ``True`` 时，点击事件不会穿透到世界，如破坏方块、镜头转向不会被响应。

        :rtype: bool
        """
        return self.base_control.GetIsSwallow()

    @is_swallow.setter
    def is_swallow(self, val):
        """
        [可读写属性]

        | 当前面板输入是否会吞噬事件，为 ``True`` 时，点击事件不会穿透到世界，如破坏方块、镜头转向不会被响应。

        :type val: bool
        """
        if isinstance(val, int):
            val = bool(val)
        self.base_control.SetIsSwallow(val)

    @property
    def offset_delta(self):
        """
        [可读写属性]

        | 拖拽偏移量。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetOffsetDelta()

    @offset_delta.setter
    def offset_delta(self, val):
        """
        [可读写属性]

        | 拖拽偏移量。

        :type val: tuple[float,float]
        """
        self.base_control.SetOffsetDelta(tuple(val))

    # endregion











