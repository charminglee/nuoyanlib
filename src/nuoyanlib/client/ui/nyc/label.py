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
    "NyLabel",
]


class NyLabel(NyControl):
    """
    文本控件类。

    示例
    ----

    >>> self.label = nyl.NyLabel(self, "/panel/label")
    >>> self.label.text = "准备就绪"
    >>> self.label.text_alignment = "center"

    参见
    ----

    - ``NyControl.to_label()`` -- 将通用控件实例转换为文本控件实例。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该文本控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.LABEL

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)
        self.__font_scale = 1.0

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def text(self):
        """
        [可读写属性]

        文本信息。

        :rtype: str|None
        """
        return self._base_control.GetText()

    @text.setter
    def text(self, val):
        """
        [可读写属性]

        文本信息。

        :type val: str
        """
        self._base_control.SetText(val, True)

    @property
    def text_alignment(self):
        """
        [可读写属性]

        文本对齐方式。

        可选值：

        - ``"left"`` -- 文本左对齐（水平方向）
        - ``"right"`` -- 文本右对齐（水平方向）
        - ``"center"`` -- 文本居中对齐（水平方向）

        :rtype: str
        """
        return self._base_control.GetTextAlignment()

    @text_alignment.setter
    def text_alignment(self, val):
        """
        [可读写属性]

        文本对齐方式。

        可选值：

        - ``"left"`` -- 文本左对齐（水平方向）
        - ``"right"`` -- 文本右对齐（水平方向）
        - ``"center"`` -- 文本居中对齐（水平方向）

        :type val: str
        """
        self._base_control.SetTextAlignment(val)

    @property
    def text_color(self):
        """
        [可读写属性]

        文本颜色，(r, g, b)，取值 [0, 1]。

        :rtype: tuple[float,float,float]
        """
        return self._base_control.GetTextColor()

    @text_color.setter
    def text_color(self, val):
        """
        [可读写属性]

        文本颜色，(r, g, b)，取值 [0, 1]。

        :type val: tuple[float,float,float]
        """
        self._base_control.SetTextColor(val)

    @property
    def line_padding(self):
        """
        [可读写属性]

        文本行间距，单位为像素。

        :rtype: float
        """
        return self._base_control.GetTextLinePadding()

    @line_padding.setter
    def line_padding(self, val):
        """
        [可读写属性]

        文本行间距，单位为像素。

        :type val: float
        """
        self._base_control.SetTextLinePadding(val)

    @property
    def font_scale(self):
        """
        [可读写属性]

        文本字体大小缩放值。

        说明
        ----

        默认字体大小，取值有限为 ``"small"`` 、``"normal"`` 、``"large"`` ，
        ``font_scale`` 是在这个默认字体的基础上进行字体大小缩放；默认为 ``1.0`` 。

        :rtype: float
        """
        return self.__font_scale

    @font_scale.setter
    def font_scale(self, val):
        """
        [可读写属性]

        文本字体大小缩放值。

        说明
        ----

        默认字体大小，取值有限为 ``"small"`` 、``"normal"`` 、``"large"`` ，
        ``font_scale`` 是在这个默认字体的基础上进行字体大小缩放；默认为 ``1.0`` 。

        :type val: float
        """
        self.__font_scale = val
        self._base_control.SetTextFontSize(val)

    @property
    def text_shadow(self):
        """
        [可读写属性]

        文本控件是否显示阴影。

        :rtype: bool
        """
        return self._base_control.IsTextShadowEnabled()

    @text_shadow.setter
    def text_shadow(self, val):
        """
        [可读写属性]

        文本控件是否显示阴影。

        :type val: bool
        """
        if val:
            self._base_control.EnableTextShadow()
        else:
            self._base_control.DisableTextShadow()

    # endregion

    def set_text_font(self, font):
        """
        [只写属性]

        设置文本字体。

        可选值：

        - ``"rune"`` -- 符文字体
        - ``"unicode"`` -- 统一字体
        - ``"smooth"`` -- 平滑字体
        - ``"default"`` -- 默认字体

        示例
        ----

        >>> self.label.set_text_font("unicode")

        -----

        :param str font: 文本字体

        :return: 无
        :rtype: None
        """
        self._base_control.SetTextFont(font) # noqa

    # region Compatibility =============================================================================================

    disable_text_shadow    = DisableTextShadow   = lambda s, *a, **k: s._base_control.DisableTextShadow(*a, **k)
    enable_text_shadow     = EnableTextShadow    = lambda s, *a, **k: s._base_control.EnableTextShadow(*a, **k)
    is_text_shadow_enabled = IsTextShadowEnabled = lambda s, *a, **k: s._base_control.IsTextShadowEnabled(*a, **k)
    set_text               = SetText             = lambda s, *a, **k: s._base_control.SetText(*a, **k)
    get_text               = GetText             = lambda s, *a, **k: s._base_control.GetText(*a, **k)
    set_text_color         = SetTextColor        = lambda s, *a, **k: s._base_control.SetTextColor(*a, **k)
    get_text_color         = GetTextColor        = lambda s, *a, **k: s._base_control.GetTextColor(*a, **k)
    set_text_font_size     = SetTextFontSize     = lambda s, *a, **k: s._base_control.SetTextFontSize(*a, **k)
    set_text_alignment     = SetTextAlignment    = lambda s, *a, **k: s._base_control.SetTextAlignment(*a, **k)
    get_text_alignment     = GetTextAlignment    = lambda s, *a, **k: s._base_control.GetTextAlignment(*a, **k)
    set_text_line_padding  = SetTextLinePadding  = lambda s, *a, **k: s._base_control.SetTextLinePadding(*a, **k)
    get_text_line_padding  = GetTextLinePadding  = lambda s, *a, **k: s._base_control.GetTextLinePadding(*a, **k)

    # endregion






