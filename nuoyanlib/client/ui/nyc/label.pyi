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


from typing import Optional, NoReturn
from mod.client.ui.controls.labelUIControl import LabelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check
from ...._core._types._typing import FTuple3, TextFontType, TextAlignmentType


class NyLabel(NyControl):
    base_control: LabelUIControl
    """
    | 文本 ``LabelUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        label_control: LabelUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3
    @property
    def text(self) -> Optional[str]: ...
    @text.setter
    def text(self, val: str) -> None: ...
    @property
    def text_alignment(self) -> TextAlignmentType: ...
    @text_alignment.setter
    def text_alignment(self, val: TextAlignmentType) -> None: ...
    @property
    def text_color(self) -> FTuple3: ...
    @text_color.setter
    def text_color(self, val: FTuple3) -> None: ...
    @property
    def line_padding(self) -> float: ...
    @line_padding.setter
    def line_padding(self, val: float) -> None: ...
    @property
    def font_scale(self) -> NoReturn: ...
    @font_scale.setter
    def font_scale(self, val: float) -> None: ...
    @property
    def text_shadow(self) -> bool: ...
    @text_shadow.setter
    def text_shadow(self, val: bool) -> None: ...
    @property
    def text_font(self) -> NoReturn: ...
    @text_font.setter
    def text_font(self, val: TextFontType) -> None: ...

    def DisableTextShadow(self) -> bool:
        """
        | 关闭文本控件显示阴影。

        -----

        :return: 是否成功
        :rtype: bool
        """
    def EnableTextShadow(self) -> bool:
        """
        | 使文本控件显示阴影。

        -----

        :return: 是否成功
        :rtype: bool
        """
    def IsTextShadowEnabled(self) -> bool:
        """
        | 判断文本控件是否显示阴影。

        -----

        :return: 是否显示阴影
        :rtype: bool
        """
    def SetText(self, text: str, sync_size: bool = False) -> None:
        """
        | 设置Label的文本信息。

        -----

        :param str text: 文本信息
        :param bool sync_size: 是否设置文本时同步更新文本框大小，默认值为False

        :return: 无
        :rtype: None
        """
    def GetText(self) -> str:
        """
        | 获取Label的文本信息，获取失败会返回None。

        -----

        :return: 文本信息
        :rtype: str
        """
    def SetTextColor(self, color: FTuple3) -> None:
        """
        | 设置Label文本的颜色。

        -----

        :param tuple[float,float,float] color: 文本颜色，(r, g, b)，取值[0, 1]

        :return: 无
        :rtype: None
        """
    def GetTextColor(self) -> FTuple3:
        """
        | 获取Label文本颜色。

        -----

        :return: 文本颜色
        :rtype: tuple[float,float,float]
        """
    def SetTextFontSize(self, scale: float) -> None:
        """
        | 设置文本字体大小缩放值。
        | Label的默认字体大小，取值有限为 ``"small"`` 、``"normal"`` 、``"large"`` ， 该接口是在这个默认字体的基础上进行字体大小缩放，默认为 ``1.0`` 。

        -----

        :param float scale: 字体大小缩放值

        :return: 无
        :rtype: None
        """
    def SetTextAlignment(self, text_alignment: TextAlignmentType) -> None:
        """
        | 设置文本控件的文本对齐方式。
        | 可选值：
        - ``"left"`` -- 文本左对齐（水平方向）
        - ``"right"`` -- 文本右对齐（水平方向）
        - ``"center"`` -- 文本居中对齐（水平方向）

        -----

        :param str text_alignment: 文本对齐方式

        :return: 无
        :rtype: None
        """
    def GetTextAlignment(self) -> TextAlignmentType:
        """
        | 获取文本控件的文本对齐方式。

        -----

        :return: 文本对齐方式
        :rtype: str
        """
    def SetTextLinePadding(self, text_line_padding: float) -> None:
        """
        | 设置文本控件的行间距。

        -----

        :param float text_line_padding: 文本行间距，单位为像素

        :return: 无
        :rtype: None
        """
    def GetTextLinePadding(self) -> float:
        """
        | 获取文本控件的行间距。

        -----

        :return: 行间距，单位为像素
        :rtype: float
        """
