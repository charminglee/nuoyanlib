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


from ...._core import _error
from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyEditBox",
]


class NyEditBox(NyControl):
    """
    | 创建 ``NyEditBox`` 文本编辑框实例。

    -----

    :param ScreenNodeExtension screen_node_ex: 文本编辑框所在UI类的实例（需继承ScreenNodeExtension）
    :param TextEditBoxUIControl edit_box_control: 通过asTextEditBox()等方式获取的NyEditBox实例
    """

    _CONTROL_TYPE = ControlType.EDIT_BOX

    def __init__(self, screen_node_ex, edit_box_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, edit_box_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    # endregion

    # region Properties ================================================================================================

    @property
    def edit_text(self):
        """
        [可读写属性]

        | 输入文本。

        :rtype: str
        """
        return self.base_control.GetEditText()

    @edit_text.setter
    def edit_text(self, val):
        """
        [可读写属性]

        | 输入文本。

        :type val: str
        """
        self.base_control.SetEditText(str(val))

    @property
    def max_length(self):
        """
        [只写属性]

        | 设置编辑框的最大输入长度。

        :rtype: None
        """
        raise _error.GetPropertyError("max_length")

    @max_length.setter
    def max_length(self, val):
        """
        [只写属性]

        | 设置编辑框的最大输入长度。

        :type val: int
        """
        self.base_control.SetEditTextMaxLength(val)

    # endregion











