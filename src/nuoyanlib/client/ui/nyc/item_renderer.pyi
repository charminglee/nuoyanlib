# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-26
|
| ==============================================
"""


from typing import Optional, TypedDict, NoReturn
from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check
from ...._core._types._typing import UserData


class __UiItem(TypedDict):
    itemName: str
    auxValue: int
    isEnchanted: bool


class NyItemRenderer(NyControl):
    base_control: ItemRendererUIControl
    """
    | 物品渲染器 ``ItemRendererUIControl`` 实例。
    """
    def __init__(
        self: ...,
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

    def SetUiItem(
        self,
        item_name: str,
        aux_value: int,
        is_enchanted: bool = False,
        user_data: Optional[UserData] = None
    ) -> bool:
        """
        | 设置ItemRenderer控件显示的物品。

        -----

        :param str item_name: 物品identifier
        :param int aux_value: 物品附加值
        :param bool is_enchanted: 是否附魔，默认为False
        :param Optional[UserData] user_data: 物品UserData，默认为None

        :return: 是否成功
        :rtype: bool
        """
    def GetUiItem(self) -> __UiItem:
        """
        | 获取ItemRenderer控件显示的物品。
        | 返回的字典参数如下：
        - ``itemName`` -- str，物品identifier
        - ``auxValue`` -- int，物品附加值
        - ``isEnchanted`` -- bool，是否附魔

        -----

        :return: 物品字典
        :rtype: dict[str,str|int|bool]
        """
