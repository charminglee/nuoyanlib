# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-18
|
| ==============================================
"""


from typing import Optional
from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check


class NyScrollView(NyControl):
    base_control: ScrollViewUIControl
    """
    | 滚动视图 ``ScrollViewUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        scroll_view_control: ScrollViewUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def scroll_pos(self) -> float: ...
    @scroll_pos.setter
    def scroll_pos(self, val: float) -> None: ...
    @property
    def scroll_pct(self) -> int: ...
    @scroll_pct.setter
    def scroll_pct(self, val: int) -> None: ...
    @property
    def scroll_content_path(self) -> str: ...
    @property
    def scroll_content(self) -> NyControl: ...

    def SetScrollViewPos(self, pos: float) -> None:
        """
        | 设置当前scroll_view内容的位置。

        -----

        :param float pos: 需要跳转到的位置，一般设置的位置会出现在scroll_view的最上方

        :return: 无
        :rtype: None
        """
    def GetScrollViewPos(self) -> float:
        """
        | 获得当前scroll_view最上方内容的位置。

        -----

        :return: 当前scroll_view最上方内容的位置
        :rtype: float
        """
    def SetScrollViewPercentValue(self, percent_value: int) -> None:
        """
        | 设置当前scroll_view内容的百分比位置。

        -----

        :param int percent_value: 需要跳转到的百分比位置，一般设置的位置会出现在scroll_view的最上方。该值取值范围0-100

        :return: 无
        :rtype: None
        """
    def GetScrollViewPercentValue(self) -> int:
        """
        | 获取当前scroll_view内容的百分比位置。

        -----

        :return: 当前scroll_view内容的百分比位置
        :rtype: int
        """
    def GetScrollViewContentPath(self) -> str:
        """
        | 返回该scroll_view内容的路径。

        -----

        :return: scroll_view内容的路径
        :rtype: str
        """
    def GetScrollViewContentControl(self) -> BaseUIControl:
        """
        | 返回该scroll_view内容的 ``BaseUIControl`` 实例。

        -----

        :return: BaseUIControl实例
        :rtype: BaseUIControl
        """
