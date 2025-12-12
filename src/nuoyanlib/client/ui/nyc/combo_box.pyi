# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-13
|
| ====================================================
"""


from typing import Any, Optional, Callable, Tuple, Union, List, Iterable
from mod.client.ui.controls.neteaseComboBoxUIControl import NeteaseComboBoxUIControl
from .control import NyControl, InteractableControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self
from ....utils.enum import ComboBoxCallbackType


__OnOpenOrCloseCallbackType = Callable[[], Any]
__OnSelectCallbackType = Callable[[int, str, Any], Any]
__ComboBoxCallbackType = Union[__OnOpenOrCloseCallbackType, __OnSelectCallbackType]


class NyComboBox(InteractableControl, NyControl):
    _base_control: NeteaseComboBoxUIControl
    data: List[Tuple[str, Optional[str], Optional[Any]]]
    """
    下拉框项数据。
    """
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        combo_box_control: NeteaseComboBoxUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
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
    @args_type_check((int, str, slice), is_method=True)
    def __getitem__(self, item: Union[int, str, slice]) -> Union[NyControl, List[NyControl]]: ...
    @args_type_check((int, str, slice), is_method=True)
    def __delitem__(self, item: Union[int, str, slice]) -> None: ...
    def bind_data(self, data: Iterable[Tuple[str, Optional[str], Optional[Any]]]) -> None: ...
    BindData = bind_data
    def set_callback(
        self,
        func: __ComboBoxCallbackType,
        cb_type: ComboBoxCallbackType = ComboBoxCallbackType.SELECT,
    ) -> bool: ...
    def remove_callback(
        self,
        func: __ComboBoxCallbackType,
        cb_type: ComboBoxCallbackType = ComboBoxCallbackType.SELECT,
    ) -> bool: ...
    def _on_open(self, *args: Any) -> None: ...
    def _on_close(self, *args: Any) -> None: ...
    def _on_select(self, *args: Any) -> None: ...
    SetCallback = set_callback
    RemoveCallback = remove_callback
    AddOption = NeteaseComboBoxUIControl.AddOption
    ClearOptions = NeteaseComboBoxUIControl.ClearOptions
    ClearSelection = NeteaseComboBoxUIControl.ClearSelection
    GetOptionIndexByShowName = NeteaseComboBoxUIControl.GetOptionIndexByShowName
    GetOptionShowNameByIndex = NeteaseComboBoxUIControl.GetOptionShowNameByIndex
    GetOptionCount = NeteaseComboBoxUIControl.GetOptionCount
    GetSelectOptionIndex = NeteaseComboBoxUIControl.GetSelectOptionIndex
    GetSelectOptionShowName = NeteaseComboBoxUIControl.GetSelectOptionShowName
    RemoveOptionByShowName = NeteaseComboBoxUIControl.RemoveOptionByShowName
    RemoveOptionByIndex = NeteaseComboBoxUIControl.RemoveOptionByIndex
    SetSelectOptionByIndex = NeteaseComboBoxUIControl.SetSelectOptionByIndex
    SetSelectOptionByShowName = NeteaseComboBoxUIControl.SetSelectOptionByShowName
    RegisterOpenComboBoxCallback = NeteaseComboBoxUIControl.RegisterOpenComboBoxCallback
    RegisterCloseComboBoxCallback = NeteaseComboBoxUIControl.RegisterCloseComboBoxCallback
    RegisterSelectItemCallback = NeteaseComboBoxUIControl.RegisterSelectItemCallback
