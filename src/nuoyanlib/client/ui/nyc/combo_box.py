# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-04
|
| ==============================================
"""


from ...._core._types._checker import args_type_check
from ....utils.enum import ControlType, ComboBoxCallbackType
from .control import NyControl


__all__ = [
    "NyComboBox",
]


class NyComboBox(NyControl):
    """
    | 创建 ``NyComboBox`` 下拉框实例。

    -----

    :param ScreenNodeExtension screen_node_ex: 下拉框所在UI类的实例（需继承ScreenNodeExtension）
    :param NeteaseComboBoxUIControl combo_box_control: 通过asNeteaseComboBox()等方式获取的NeteaseComboBoxUIControl实例
    """

    _CONTROL_TYPE = ControlType.COMBO_BOX

    def __init__(self, screen_node_ex, combo_box_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, combo_box_control)
        self._callback_map = {
            ComboBoxCallbackType.OPEN: self.RegisterOpenComboBoxCallback,
            ComboBoxCallbackType.CLOSE: self.RegisterCloseComboBoxCallback,
            ComboBoxCallbackType.SELECT: self.RegisterSelectItemCallback,
        }

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    def _item_to_index(self, item):
        if isinstance(item, str):
            index = self.base_control.GetOptionIndexByShowName(item)
            if index == -1:
                raise KeyError(repr(item))
            return index
        else:
            index = item if item >= 0 else self.opt_count + item
            if index >= self.opt_count:
                raise KeyError(repr(item))
            return index

    @args_type_check((int, str), is_method=True)
    def __getitem__(self, item):
        """
        | 按索引或显示名称获取下拉框项的 ``NyControl`` 实例。

        -----

        :param int|str item: 索引或显示名称；支持负数索引，-1表示最后一项，-2表示倒数第二项，以此类推

        :return: 下拉框项的NyControl实例
        :rtype: NyControl

        :raise KeyError: 下拉框项不存在
        """
        index = self._item_to_index(item)
        # todo

    @args_type_check((int, str), is_method=True)
    def __delitem__(self, item):
        """
        | 删除指定索引或显示名称的下拉框项。

        -----

        :param int|str item: 索引或显示名称；支持负数索引，-1表示最后一项，-2表示倒数第二项，以此类推

        :return: 无
        :rtype: None

        :raise KeyError: 下拉框项不存在或已删除
        """
        index = self._item_to_index(item)
        self.RemoveOptionByIndex(index)

    def set_callback(self, func, cb_type=ComboBoxCallbackType.SELECT):
        """
        | 设置下拉框回调函数。

        -----

        :param function func: 回调函数
        :param str cb_type: 回调类型，请使用ComboBoxCallbackType枚举值，默认为ComboBoxCallbackType.SELECT

        :return: 无
        :rtype: None

        :raise ValueError: 回调类型无效
        """
        if cb_type not in self._callback_map:
            raise ValueError("invalid callback type: %s, use 'ComboBoxCallbackType' instead" % repr(cb_type))
        self._callback_map[cb_type](func)

    # endregion

    # region Properties ================================================================================================

    @property
    def opt_count(self):
        """
        [只读属性]

        | 选项数量。

        :rtype: int
        """
        return self.base_control.GetOptionCount()

    @property
    def selected_opt_index(self):
        """
        [可读写属性]

        | 当前选中项的索引，若无选中项则为 ``-1`` 。

        :rtype: int
        """
        return self.base_control.GetOptionCount()

    @selected_opt_index.setter
    def selected_opt_index(self, val):
        """
        [可读写属性]

        | 当前选中项的索引，若无选中项则为 ``-1`` 。

        :type val: int
        """
        if val < 0:
            self.base_control.ClearSelection()
        else:
            self.base_control.SetSelectOptionByIndex(val)

    @property
    def selected_opt_name(self):
        """
        [可读写属性]

        | 当前选中项的显示文本，所无选中项则为 ``None`` 。

        :rtype: str|None
        """
        return self.base_control.GetSelectOptionShowName()

    @selected_opt_name.setter
    def selected_opt_name(self, val):
        """
        [可读写属性]

        | 当前选中项的显示文本，所无选中项则为 ``None`` 。

        :type val: str|None
        """
        if val is None:
            self.base_control.ClearSelection()
        else:
            self.base_control.SetSelectOptionByShowName(val)

    # endregion











