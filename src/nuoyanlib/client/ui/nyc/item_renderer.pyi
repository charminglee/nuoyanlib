# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-04
|
| ====================================================
"""


from typing import Optional, TypedDict, NoReturn
from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import Self, UserData


class __UiItemDict(TypedDict):
    itemName: str
    auxValue: int
    isEnchanted: bool


class NyItemRenderer(NyControl):
    _base_control: ItemRendererUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        item_renderer_control: ItemRendererUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def item_name(self) -> str: ...
    @item_name.setter
    def item_name(self, val: str) -> None: ...
    @property
    def item_aux(self) -> int: ...
    @item_aux.setter
    def item_aux(self, val: int) -> None: ...
    @property
    def is_enchanted(self) -> bool: ...
    @is_enchanted.setter
    def is_enchanted(self, val: bool) -> None: ...
    @property
    def user_data(self) -> NoReturn: ...
    @user_data.setter
    def user_data(self, val: Optional[UserData]) -> None: ...
    SetUiItem = ItemRendererUIControl.SetUiItem
    GetUiItem = ItemRendererUIControl.GetUiItem
