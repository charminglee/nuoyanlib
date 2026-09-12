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


from typing import Optional, Tuple, TypedDict, NoReturn
from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check
from ....core._types._typing import UserData


class __UiItemDict(TypedDict):
    itemName: str
    auxValue: int
    isEnchanted: bool


class NyItemRenderer(NyControl):
    _base_control: ItemRendererUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def item(self) -> Tuple[str, int]: ...
    @item.setter
    def item(self, val: Tuple[str, int]) -> None: ...
    @property
    def is_enchanted(self) -> bool: ...
    @is_enchanted.setter
    def is_enchanted(self, val: bool) -> None: ...
    @property
    def user_data(self) -> NoReturn: ...
    @user_data.setter
    def user_data(self, val: Optional[UserData]) -> None: ...
    set_ui_item = SetUiItem = ItemRendererUIControl.SetUiItem
    get_ui_item = GetUiItem = ItemRendererUIControl.GetUiItem
