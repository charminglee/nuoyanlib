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


from typing import Any, Optional, Callable, Tuple, Union, List, ClassVar, Iterable
from mod.client.ui.controls.neteaseComboBoxUIControl import NeteaseComboBoxUIControl
from .control import NyControl, InteractableControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check


__OnOpenOrCloseCallbackType = Callable[[], Any]
__OnSelectCallbackType = Callable[[int, str, Any], Any]
__ComboBoxCallbackType = Union[__OnOpenOrCloseCallbackType, __OnSelectCallbackType]


class NyComboBox(InteractableControl, NyControl):
    OPEN: ClassVar[int]
    """ 展开下拉框。 """
    CLOSE: ClassVar[int]
    """ 关闭下拉框。 """
    SELECT: ClassVar[int]
    """ 选中下拉框内容。 """
    _base_control: NeteaseComboBoxUIControl
    data: List[Tuple[str, Optional[str], Optional[Any]]]
    """ 下拉框项数据。 """
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def opt_count(self) -> int: ...
    @property
    def selected_opt_index(self) -> int: ...
    @selected_opt_index.setter
    def selected_opt_index(self, val: int) -> None: ...
    @property
    def selected_opt_name(self) -> Optional[str]: ...
    @selected_opt_name.setter
    def selected_opt_name(self, val: Optional[str]) -> None: ...
    def _item_to_indices(self, item: Union[int, str, slice]) -> List[int]: ...
    def _get_opt_path(self, index: int) -> str: ...
    @args_type_check((int, str, slice))
    def __getitem__(self, item: Union[int, str, slice]) -> Union[NyControl, List[NyControl]]: ...
    @args_type_check((int, str, slice))
    def __delitem__(self, item: Union[int, str, slice]) -> None: ...
    def bind_data(self, data: Iterable[Tuple[str, Optional[str], Any]]) -> None: ...
    def set_callback(self, func: __ComboBoxCallbackType, *cb_types: int) -> None: ...
    def remove_callback(self, func: __ComboBoxCallbackType, *cb_types: int) -> None: ...
    def _on_open(self, *args: Any) -> None: ...
    def _on_close(self, *args: Any) -> None: ...
    def _on_select(self, *args: Any) -> None: ...
    add_option = AddOption = NeteaseComboBoxUIControl.AddOption
    clear_options = ClearOptions = NeteaseComboBoxUIControl.ClearOptions
    clear_selection = ClearSelection = NeteaseComboBoxUIControl.ClearSelection
    get_option_index_by_show_name = GetOptionIndexByShowName = NeteaseComboBoxUIControl.GetOptionIndexByShowName
    get_option_show_name_by_index = GetOptionShowNameByIndex = NeteaseComboBoxUIControl.GetOptionShowNameByIndex
    get_option_count = GetOptionCount = NeteaseComboBoxUIControl.GetOptionCount
    get_select_option_index = GetSelectOptionIndex = NeteaseComboBoxUIControl.GetSelectOptionIndex
    get_select_option_show_name = GetSelectOptionShowName = NeteaseComboBoxUIControl.GetSelectOptionShowName
    remove_option_by_show_name = RemoveOptionByShowName = NeteaseComboBoxUIControl.RemoveOptionByShowName
    remove_option_by_index = RemoveOptionByIndex = NeteaseComboBoxUIControl.RemoveOptionByIndex
    set_select_option_by_index = SetSelectOptionByIndex = NeteaseComboBoxUIControl.SetSelectOptionByIndex
    set_select_option_by_show_name = SetSelectOptionByShowName = NeteaseComboBoxUIControl.SetSelectOptionByShowName
    register_open_combo_box_callback = RegisterOpenComboBoxCallback = NeteaseComboBoxUIControl.RegisterOpenComboBoxCallback
    register_close_combo_box_callback = RegisterCloseComboBoxCallback = NeteaseComboBoxUIControl.RegisterCloseComboBoxCallback
    register_select_item_callback = RegisterSelectItemCallback = NeteaseComboBoxUIControl.RegisterSelectItemCallback
