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
    from typing import Any
    from ..screen_node import NyScreenNode, NyScreenProxy


from ....core._types._checker import args_type_check
from ..ui_utils import _UIControlType
from .control import NyControl, InteractableControl


__all__ = [
    "NyComboBox",
]


class NyComboBox(InteractableControl, NyControl):
    """
    下拉框控件类。

    示例
    ----

    >>> self.combo = nyl.NyComboBox(self, "/panel/combo_box")
    >>> self.combo.bind_data([
    ...     ("简单", "textures/ui/easy", {'mode': "easy"}),
    ...     ("普通", "textures/ui/normal", {'mode': "normal"}),
    ...     ("困难", "textures/ui/hard", {'mode': "hard"}),
    ... ])

    参见
    ----

    - ``NyControl.to_combo_box()`` -- 将通用控件实例转换为下拉框控件实例。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该下拉框控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.COMBO_BOX

    OPEN = 1 << 0
    CLOSE = 1 << 1
    SELECT = 1 << 2

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)
        InteractableControl.__init__(
            self,
            {
                NyComboBox.OPEN: (self._base_control.RegisterOpenComboBoxCallback, self._on_open),
                NyComboBox.CLOSE: (self._base_control.RegisterCloseComboBoxCallback, self._on_close),
                NyComboBox.SELECT: (self._base_control.RegisterSelectItemCallback, self._on_select),
            }
        )

        self.data = []

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)
        InteractableControl.__ui_destroy__(self)

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
        return self._base_control.GetSelectOptionIndex()

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

        当前选中项的显示文本，若无选中项则为 ``None`` 。

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

        示例
        ----

        >>> self.combo[0]
        <NyControl 'contentItemContent0' at '/panel/combo_box/comboBoxContent/.../contentItemContent0'>

        >>> self.combo['普通']
        <NyControl 'contentItemContent1' at '/panel/combo_box/comboBoxContent/.../contentItemContent1'>

        >>> self.combo[1:3]
        [
            <NyControl 'contentItemContent1' at '/panel/combo_box/comboBoxContent/.../contentItemContent1'>,
            <NyControl 'contentItemContent2' at '/panel/combo_box/comboBoxContent/.../contentItemContent2'>
        ]

        参见
        ----

        - ``NyComboBox.bind_data()`` -- 绑定下拉框项数据。
        - ``NyComboBox.__delitem__()`` -- 删除下拉框项。

        -----

        :param int|str|slice item: 索引或显示名称，支持负数索引与切片

        :return: 下拉框项的 NyControl 实例
        :rtype: NyControl|list[NyControl]

        :raise KeyError: 显示名称对应的下拉框项不存在
        :raise IndexError: 索引超出下拉框范围
        """
        indices = self._item_to_indices(item)
        controls = [
            NyControl(self.ny_screen_node, self._get_opt_path(i))
            for i in indices
        ]
        return controls[0] if len(controls) == 1 else controls

    @args_type_check((int, str, slice))
    def __delitem__(self, item):
        """
        删除指定索引或显示名称的下拉框项。

        示例
        ----

        >>> del self.combo[0]
        >>> self.combo.data
        [
            ('普通', 'textures/ui/normal', {'mode': 'normal'}),
            ('困难', 'textures/ui/hard', {'mode': 'hard'})
        ]

        >>> del self.combo['困难']
        >>> self.combo.data
        [('普通', 'textures/ui/normal', {'mode': 'normal'})]

        参见
        ----

        - ``NyComboBox.bind_data()`` -- 绑定下拉框项数据。
        - ``NyComboBox.__getitem__()`` -- 获取下拉框项的实例。

        -----

        :param int|str|slice item: 索引或显示名称，支持负数索引与切片

        :return: 无
        :rtype: None

        :raise KeyError: 显示名称对应的下拉框项不存在
        :raise IndexError: 索引超出下拉框范围
        """
        indices = self._item_to_indices(item)
        for i in indices:
            del self.data[i]
            self._base_control.RemoveOptionByIndex(i)

    def bind_data(self, data):
        """
        绑定下拉框项数据。

        下拉框项与数据一一对应，绑定数据后自动生成下拉框项。

        说明
        ----

        若重复绑定数据，新数据将覆盖旧数据。

        示例
        ----

        >>> self.combo.bind_data([
        ...     ("简单", "textures/ui/easy", {'mode': "easy"}),
        ...     ("普通", "textures/ui/normal", {'mode': "normal"}),
        ...     ("困难", "textures/ui/hard", {'mode': "hard"}),
        ... ])

        参见
        ----

        - ``NyComboBox.__getitem__()`` -- 获取下拉框项的实例。
        - ``NyComboBox.__delitem__()`` -- 删除下拉框项。
        - ``NyComboBox.selected_opt_index`` -- 获取或设置当前选中项。

        -----

        :param list[tuple[str,str|None,Any|None]] data: 数据列表，可以是任何可迭代对象，元素类型为元组： (显示名称, 图标贴图路径, 自定义数据) ，若无需图标或自定义数据，可填 None

        :return: 无
        :rtype: None
        """
        if self.data:
            self._base_control.ClearOptions()
        self.data = [
            tuple(i)
            for i in data
            if not isinstance(i, tuple)
        ]
        for d in data:
            self._base_control.AddOption(*d)

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func, *cb_types):
        """
        设置下拉框回调函数。

        说明
        ----

        支持同时设置多个同类型的回调，例如同时设置两个展开下拉框回调，按设置顺序依次触发。

        示例
        ----

        >>> def on_combo_select(args):
        ...     print(args)
        >>> self.combo.set_callback(on_combo_select, nyl.NyComboBox.SELECT)

        参见
        ----

        - ``NyComboBox.remove_callback()`` -- 移除下拉框回调函数。

        -----

        :param function func: 回调函数
        :param int cb_types: [变长位置参数] 回调类型，请使用 NyComboBox 枚举值；可同时传入多个类型

        :return: 无
        :rtype: None

        :raise ValueError: 回调类型错误时抛出
        """
        InteractableControl.set_callback(self, func, *cb_types)

    def remove_callback(self, func, *cb_types):
        """
        移除通过 ``.set_callback()`` 设置的下拉框回调函数。

        示例
        ----

        >>> self.combo.remove_callback(on_combo_select)

        参见
        ----

        - ``NyComboBox.set_callback()`` -- 设置下拉框回调函数。

        -----

        :param function func: 回调函数
        :param int cb_types: [变长位置参数] 回调类型，请使用 NyComboBox 的回调枚举值；可同时传入多个类型

        :return: 无
        :rtype: None

        :raise ValueError: 回调类型错误时抛出
        """
        InteractableControl.remove_callback(self, func, *cb_types)

    _on_open    = lambda s, *a: s.exec_callbacks(NyComboBox.OPEN, *a)
    _on_close   = lambda s, *a: s.exec_callbacks(NyComboBox.CLOSE, *a)
    _on_select  = lambda s, *a: s.exec_callbacks(NyComboBox.SELECT, *a)

    # endregion

    # region Compatibility =============================================================================================

    add_option                        = AddOption                     = lambda s, *a, **k: s._base_control.AddOption(*a, **k)
    clear_options                     = ClearOptions                  = lambda s, *a, **k: s._base_control.ClearOptions(*a, **k)
    clear_selection                   = ClearSelection                = lambda s, *a, **k: s._base_control.ClearSelection(*a, **k)
    get_option_index_by_show_name     = GetOptionIndexByShowName      = lambda s, *a, **k: s._base_control.GetOptionIndexByShowName(*a, **k)
    get_option_show_name_by_index     = GetOptionShowNameByIndex      = lambda s, *a, **k: s._base_control.GetOptionShowNameByIndex(*a, **k)
    get_option_count                  = GetOptionCount                = lambda s, *a, **k: s._base_control.GetOptionCount(*a, **k)
    get_select_option_index           = GetSelectOptionIndex          = lambda s, *a, **k: s._base_control.GetSelectOptionIndex(*a, **k)
    get_select_option_show_name       = GetSelectOptionShowName       = lambda s, *a, **k: s._base_control.GetSelectOptionShowName(*a, **k)
    remove_option_by_show_name        = RemoveOptionByShowName        = lambda s, *a, **k: s._base_control.RemoveOptionByShowName(*a, **k)
    remove_option_by_index            = RemoveOptionByIndex           = lambda s, *a, **k: s._base_control.RemoveOptionByIndex(*a, **k)
    set_select_option_by_index        = SetSelectOptionByIndex        = lambda s, *a, **k: s._base_control.SetSelectOptionByIndex(*a, **k)
    set_select_option_by_show_name    = SetSelectOptionByShowName     = lambda s, *a, **k: s._base_control.SetSelectOptionByShowName(*a, **k)
    register_open_combo_box_callback  = RegisterOpenComboBoxCallback  = lambda s, *a, **k: s._base_control.RegisterOpenComboBoxCallback(*a, **k)
    register_close_combo_box_callback = RegisterCloseComboBoxCallback = lambda s, *a, **k: s._base_control.RegisterCloseComboBoxCallback(*a, **k)
    register_select_item_callback     = RegisterSelectItemCallback    = lambda s, *a, **k: s._base_control.RegisterSelectItemCallback(*a, **k)

    # endregion


