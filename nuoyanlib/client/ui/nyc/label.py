# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-27
|
| ==============================================
"""


from ....utils.enum import ControlType
from .control import NyControl
from ...._core import _error


__all__ = [
    "NyLabel",
]


class NyLabel(NyControl):
    """
    | 创建 ``NyLabel`` 文本实例。
    | 兼容ModSDK ``LabelUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 文本所在UI类的实例（需继承ScreenNodeExtension）
    :param LabelUIControl label_control: 通过asLabel()获取等方式的LabelUIControl实例
    """

    _CONTROL_TYPE = ControlType.LABEL

    def __init__(self, screen_node_ex, label_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, label_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region Properties ================================================================================================

    @property
    def text(self):
        """
        [可读写属性]

        | 获取Label的文本信息，获取失败会返回None。

        :rtype: str|None
        """
        return self.base_control.GetText()

    @text.setter
    def text(self, val):
        """
        [可读写属性]

        | 设置Label的文本信息。

        :type val: str
        """
        self.base_control.SetText(str(val), True)

    @property
    def text_alignment(self):
        """
        [可读写属性]

        | 文本对齐方式。
        | 可选值：
        - ``"left"`` -- 文本左对齐（水平方向）
        - ``"right"`` -- 文本右对齐（水平方向）
        - ``"center"`` -- 文本居中对齐（水平方向）

        :rtype: str
        """
        return self.base_control.GetTextAlignment()

    @text_alignment.setter
    def text_alignment(self, val):
        """
        [可读写属性]

        | 文本对齐方式。
        | 可选值：
        - ``"left"`` -- 文本左对齐（水平方向）
        - ``"right"`` -- 文本右对齐（水平方向）
        - ``"center"`` -- 文本居中对齐（水平方向）

        :type val: str
        """
        self.base_control.SetTextAlignment(val)

    @property
    def text_color(self):
        """
        [可读写属性]

        | 文本颜色，(r, g, b)，取值[0, 1]。

        :rtype: tuple[float,float,float]
        """
        return self.base_control.GetTextColor()

    @text_color.setter
    def text_color(self, val):
        """
        [可读写属性]

        | 文本颜色，(r, g, b)，取值[0, 1]。

        :type val: tuple[float,float,float]
        """
        self.base_control.SetTextColor(tuple(val))

    @property
    def line_padding(self):
        """
        [可读写属性]

        | 文本行间距，单位为像素。

        :rtype: float
        """
        return self.base_control.GetTextLinePadding()

    @line_padding.setter
    def line_padding(self, val):
        """
        [可读写属性]

        | 文本行间距，单位为像素。

        :type val: float
        """
        self.base_control.SetTextLinePadding(val)

    @property
    def font_scale(self):
        """
        [只写属性]

        | 文本字体大小缩放值。
        | Label的默认字体大小，取值有限为 ``"small"`` 、``"normal"`` 、``"large"`` ， ``font_scale`` 是在这个默认字体的基础上进行字体大小缩放，默认为 ``1.0`` 。

        :rtype: None
        """
        raise _error.GetPropertyError("font_scale")

    @font_scale.setter
    def font_scale(self, val):
        """
        [只写属性]

        | 文本字体大小缩放值。
        | Label的默认字体大小，取值有限为 ``"small"`` 、``"normal"`` 、``"large"`` ， ``font_scale`` 是在这个默认字体的基础上进行字体大小缩放，默认为 ``1.0`` 。

        :type val: float
        """
        self.base_control.SetTextFontSize(val)

    @property
    def text_shadow(self):
        """
        [可读写属性]

        | 获取文本控件是否显示阴影。

        :rtype: bool
        """
        return self.base_control.IsTextShadowEnabled()

    @text_shadow.setter
    def text_shadow(self, val):
        """
        [可读写属性]

        | 设置文本控件是否显示阴影。

        :type val: bool
        """
        if val:
            self.base_control.EnableTextShadow()
        else:
            self.base_control.DisableTextShadow()

    @property
    def text_font(self):
        """
        [只写属性]

        | 文本字体。
        | 可选值：
        - ``"rune"`` -- 符文字体
        - ``"unicode"`` -- 统一字体
        - ``"smooth"`` -- 平滑字体
        - ``"default"`` -- 默认字体

        :rtype: None
        """
        raise _error.GetPropertyError("text_font")

    @text_font.setter
    def text_font(self, val):
        """
        [只写属性]

        | 文本字体。
        | 可选值：
        - ``"rune"`` -- 符文字体
        - ``"unicode"`` -- 统一字体
        - ``"smooth"`` -- 平滑字体
        - ``"default"`` -- 默认字体

        :type val: str
        """
        self.base_control.SetTextFont(val) # NOQA

    # endregion












