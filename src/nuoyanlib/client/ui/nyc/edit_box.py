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
    "NyEditBox",
]


class NyEditBox(NyControl):
    """
    文本编辑框控件类。

    示例
    ----

    >>> self.edit_box = nyl.NyEditBox(self, "/panel/edit_box")
    >>> self.edit_box.max_length = 32
    >>> self.edit_box.edit_text = "请输入名称"

    参见
    ----

    - ``NyEditBox.edit_text`` -- 获取/设置编辑框文本。
    - ``NyEditBox.max_length`` -- 设置编辑框的最大输入长度。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该文本编辑框控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.EDIT_BOX

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def edit_text(self):
        """
        [可读写属性]

        编辑框文本。

        :rtype: str
        """
        return self._base_control.GetEditText()

    @edit_text.setter
    def edit_text(self, val):
        """
        [可读写属性]

        编辑框文本。

        :type val: str
        """
        self._base_control.SetEditText(val)

    @property
    def max_length(self):
        """
        [只写属性]

        设置编辑框的最大输入长度。

        :rtype: None
        """
        raise error.GetPropertyError("max_length")

    @max_length.setter
    def max_length(self, val):
        """
        [只写属性]

        设置编辑框的最大输入长度。

        :type val: int
        """
        self._base_control.SetEditTextMaxLength(val)

    # endregion

    # region Compatibility =============================================================================================

    get_edit_text            = GetEditText          = lambda s, *a, **k: s._base_control.GetEditText(*a, **k)
    set_edit_text            = SetEditText          = lambda s, *a, **k: s._base_control.SetEditText(*a, **k)
    set_edit_text_max_length = SetEditTextMaxLength = lambda s, *a, **k: s._base_control.SetEditTextMaxLength(*a, **k)

    # endregion





