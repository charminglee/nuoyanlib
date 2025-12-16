# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


if 0:
    from ..screen_node import ScreenNodeExtension


from ....core import error
from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyEditBox",
]


class NyEditBox(NyControl):
    """
    文本编辑框控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 文本编辑框所在UI类的实例（需继承ScreenNodeExtension）
    :param TextEditBoxUIControl edit_box_control: 通过asTextEditBox()等方式获取的NyEditBox实例
    """

    CONTROL_TYPE = ControlType.EDIT_BOX

    def __init__(self, screen_node_ex, edit_box_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, edit_box_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

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
        self._base_control.SetEditText(str(val))

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











