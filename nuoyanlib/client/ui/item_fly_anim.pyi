# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-04-28
#
# ====================================================


from typing import Tuple, Union, List, Dict, Optional
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from mod.client.ui.viewBinder import ViewBinder


_ITEM_FLY_PANEL_NAME: str
_UI_NAME_ITEM_FLY_PANEL: str
_UI_PATH_FLY_ITEM_0: str


class ItemFlyAnim(ScreenNode):
    __screen_node: ScreenNode
    _item_fly_queue: Dict[int, Dict[str, Union[float, int, ItemRendererUIControl]]]
    _fly_ir: List[ItemRendererUIControl]
    __path: str
    item_fly_panel: Optional[BaseUIControl]
    def __init__(self: ..., namespace: str, name: str, param: Optional[dict]) -> None: ...
    def Create(self: ...) -> None: ...
    @ViewBinder.binding(ViewBinder.BF_BindString, "#NyItemFlyAnim.game_tick")
    def _OnGameTick(self: ...) -> None: ...
    def _clone_new_ir(self: ...) -> Optional[ItemRendererUIControl]: ...
    def _get_idle_ir_index(self: ...) -> int: ...
    def SetOneItemFlyAnim(
        self: ...,
        item_dict: dict,
        from_pos: Tuple[float, float],
        to_pos: Tuple[float, float],
        ui_size: Union[float, Tuple[float, float]],
    ) -> None: ...
    def SetItemsFlyAnim(
        self: ...,
        data: List[Dict[str, Union[dict, Tuple[float, float], float]]],
    ) -> None: ...
