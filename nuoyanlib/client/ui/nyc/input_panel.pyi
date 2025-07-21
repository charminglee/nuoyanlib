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


from typing import Optional
from mod.client.ui.controls.inputPanelUIControl import InputPanelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check
from ...._core._types._typing import FTuple2


class NyInputPanel(NyControl):
    base_control: InputPanelUIControl
    """
    | 输入面板 ``InputPanelUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        input_panel_control: InputPanelUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3
    @property
    def is_modal(self) -> bool: ...
    @is_modal.setter
    def is_modal(self, val: bool) -> None: ...
    @property
    def is_swallow(self) -> bool: ...
    @is_swallow.setter
    def is_swallow(self, val: bool) -> None: ...
    @property
    def offset_delta(self) -> FTuple2: ...
    @offset_delta.setter
    def offset_delta(self, val: FTuple2) -> None: ...

    def SetIsModal(self, is_modal) -> bool:
        """
        | 设置当前面板是否为模态框。

        -----

        :param bool is_modal: 是否为模态框

        :return: 是否成功
        :rtype: bool
        """
    def GetIsModal(self) -> bool:
        """
        | 判断当前面板是否为模态框。

        -----

        :return: 当前面板是否为模态框
        :rtype: bool
        """
    def SetIsSwallow(self, is_swallow: bool) -> bool:
        """
        | 设置当前面板输入是否会吞噬事件， ``is_swallow`` 为 ``Ture`` 时，点击时，点击事件不会穿透到世界。如破坏方块、镜头转向不会被响应。

        -----

        :param bool is_swallow: 是否吞噬事件

        :return: 是否成功
        :rtype: bool
        """
    def GetIsSwallow(self) -> bool:
        """
        | 判断当前面板输入是否会吞噬事件， ``is_swallow`` 为 ``Ture`` 时，点击时，点击事件不会穿透到世界。如破坏方块、镜头转向不会被响应。

        -----

        :return: 当前面板输入是否会吞噬事件
        :rtype: bool
        """
    def SetOffsetDelta(self, offset_delta: FTuple2) -> bool:
        """
        | 设置点击面板的拖拽偏移量。

        -----

        :param tuple[float,float] offset_delta: 拖拽偏移量

        :return: 是否成功
        :rtype: bool
        """
    def GetOffsetDelta(self) -> FTuple2:
        """
        | 获得点击面板的拖拽偏移量。

        -----

        :return: 拖拽偏移量
        :rtype: tuple[float,float]
        """
