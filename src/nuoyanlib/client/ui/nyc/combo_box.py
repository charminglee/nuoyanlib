# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-18
#  ⠀
# =================================================


if 0:
    from typing import Any
    from ..screen_node import ScreenNodeExtension


from ....core._types._checker import args_type_check
from ....utils.enum import ControlType, ComboBoxCallbackType
from .control import NyControl, InteractableControl


__all__ = [
    "NyComboBox",
]


class NyComboBox(InteractableControl, NyControl):
    """
    下拉框控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 下拉框所在UI类的实例（需继承 ScreenNodeExtension）
    :param NeteaseComboBoxUIControl combo_box_control: 通过 asNeteaseComboBox() 等方式获取的 NeteaseComboBoxUIControl 实例
    """

    CONTROL_TYPE = ControlType.COMBO_BOX
    CALLBACK_TYPE = ComboBoxCallbackType

    def __init__(self, screen_node_ex, combo_box_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, combo_box_control)
        InteractableControl.__init__(
            self,
            {
                ComboBoxCallbackType.OPEN: (combo_box_control.RegisterOpenComboBoxCallback, self._on_open),
                ComboBoxCallbackType.CLOSE: (combo_box_control.RegisterCloseComboBoxCallback, self._on_close),
                ComboBoxCallbackType.SELECT: (combo_box_control.RegisterSelectItemCallback, self._on_select),
            },
        )
        self.data = []

    def __destroy__(self):
        NyControl.__destroy__(self)
        InteractableControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def opt_count(self):
        """
        [只读属性]

        选项数量。

        :rtype: int
        """
        return self._base_control.GetOptionCount()

    @property
    def selected_opt_index(self):
        """
        [可读写属性]

        当前选中项的索引，若无选中项则为 ``-1`` 。

        :rtype: int
        """
        return self._base_control.GetOptionCount()

    @selected_opt_index.setter
    def selected_opt_index(self, val):
        """
        [可读写属性]

        根据索引选中下拉框项，传入 ``-1`` 则清除选中。

        :type val: int
        """
        if val < 0:
            self._base_control.ClearSelection()
        else:
            self._base_control.SetSelectOptionByIndex(val)

    @property
    def selected_opt_name(self):
        """
        [可读写属性]

        当前选中项的显示文本，所无选中项则为 ``None`` 。

        :rtype: str|None
        """
        return self._base_control.GetSelectOptionShowName()

    @selected_opt_name.setter
    def selected_opt_name(self, val):
        """
        [可读写属性]

        根据显示文本选中下拉框项，传入 ``None`` 则清除选中。

        :type val: str|None
        """
        if val is None:
            self._base_control.ClearSelection()
        else:
            self._base_control.SetSelectOptionByShowName(val)

    # endregion

    # region Common ====================================================================================================

    def _item_to_indices(self, item):
        opt_count = self.opt_count
        if isinstance(item, str):
            index = self._base_control.GetOptionIndexByShowName(item)
            if index == -1:
                raise KeyError(item)
            return [index]
        elif isinstance(item, slice):
            return range(*item.indices(opt_count))
        else:
            index = item if item >= 0 else opt_count + item
            if index >= opt_count:
                raise IndexError("NyComboBox index out of range")
            return [index]

    def _get_opt_path(self, index):
        return self._base_control.comboBox.uiControlPathList[index] # noqa

    @args_type_check((int, str, slice))
    def __getitem__(self, item):
        """
        按索引或显示名称获取下拉框项的 ``NyControl`` 实例。

        -----

        :param int|str|slice item: 索引或显示名称，支持负数索引与切片

        :return: 下拉框项的NyControl实例
        :rtype: NyControl|list[NyControl]

        :raise KeyError: 显示名称对应的下拉框项不存在
        :raise IndexError: 索引超出下拉框范围
        """
        indices = self._item_to_indices(item)
        controls = [
            NyControl.from_path(self.ui_node, self._get_opt_path(i))
            for i in indices
        ]
        return controls[0] if len(controls) == 1 else controls

    @args_type_check((int, str, slice))
    def __delitem__(self, item):
        """
        删除指定索引或显示名称的下拉框项。

        -----

        :param int|str|slice item: 索引或显示名称，支持负数索引与切片

        :return: 无
        :rtype: None

        :raise KeyError: 显示名称对应的下拉框项不存在
        :raise IndexError: 索引超出下拉框范围
        """
        indices = self._item_to_indices(item)
        for i in indices:
            self._base_control.RemoveOptionByIndex(i)

    def bind_data(self, data):
        """
        绑定下拉框项数据。

        -----

        :param list[tuple[str,str|None,Any|None]] data: 数据列表，列表元素为元组：(显示名称, 图标贴图路径, 自定义数据) ，若无需图标或绑定数据，可填 None

        :return: 无
        :rtype: None
        """
        self.data = data
        for d in data:
            self._base_control.AddOption(*d)

    BindData = bind_data

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func, cb_type=ComboBoxCallbackType.SELECT):
        """
        设置下拉框回调函数。

        说明
        ----

        支持同时设置多个同类型的回调，按设置顺序依次触发。

        调用本方法后请勿再调用 ModSDK 的注册下拉框回调的接口（如 ``.RegisterSelectItemCallback()`` ），
        否则所有通过本方法设置的回调函数将无效。

        -----

        :param function func: 回调函数
        :param ComboBoxCallbackType cb_type: 回调类型，请使用 ComboBoxCallbackType 枚举值；默认为 ComboBoxCallbackType.SELECT

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型无效
        """
        return InteractableControl.set_callback(self, func, cb_type)

    def remove_callback(self, func, cb_type=ComboBoxCallbackType.SELECT):
        """
        移除通过 ``.set_callback()`` 设置的下拉框回调函数。

        -----

        :param function func: 回调函数
        :param ComboBoxCallbackType cb_type: 回调类型，请使用 ComboBoxCallbackType 枚举值；默认为 ComboBoxCallbackType.SELECT

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型无效
        """
        return InteractableControl.remove_callback(self, func, cb_type)

    _on_open    = lambda self, *args: self._exec_callbacks(ComboBoxCallbackType.OPEN, *args)
    _on_close   = lambda self, *args: self._exec_callbacks(ComboBoxCallbackType.CLOSE, *args)
    _on_select  = lambda self, *args: self._exec_callbacks(ComboBoxCallbackType.SELECT, *args)

    SetCallback = set_callback
    RemoveCallback = remove_callback

    # endregion











