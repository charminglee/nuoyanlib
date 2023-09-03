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
#   Last Modified : 2023-09-03
#
# ====================================================


from typing import Tuple, Union, List, Dict, Optional
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from mod.client.ui.viewBinder import ViewBinder


_PATH: str
_NAMESPACE: str
_UI_NAME_ITEM_FLY_ANIM: str
_UI_PATH_ITEM_FLY_ANIM: str
_UI_DEF_ITEM_FLY_ANIM: str
_UI_PATH_FLY_ITEM_1: str
_UI_PATH_FLY_ITEM_2: str


class ItemFlyAnim(ScreenNode):
    _itemFlyAnimNode: _ItemFlyAnimUI
    def __init__(self, namespace: str, name: str, param: dict) -> None: ...
    def __registerItemFlyAnimUI(self) -> None: ...
    def SetOneItemFlyAnim(
        self,
        itemDict: dict,
        fromPos: Tuple[float, float],
        toPos: Tuple[float, float],
        uiSize: Union[float, Tuple[float, float]],
    ) -> None: ...
    def SetItemsFlyAnim(
        self,
        itemAnimDataList: List[Dict[str, Union[dict, Tuple[float, float], float]]],
    ) -> None: ...


class _ItemFlyAnimUI(ScreenNode):
    itemFlyQueue: Dict[str, Union[float, int, ItemRendererUIControl]]
    flyIRs: List[ItemRendererUIControl]
    def __init__(self, namespace: str, name: str, param: dict) -> None: ...
    def Create(self) -> None: ...
    @ViewBinder.binding(ViewBinder.BF_BindString, "#main.gametick")
    def OnGameTick(self) -> None: ...
    def _cloneNewIr(self) -> Optional[ItemRendererUIControl]: ...
    def _getIdleIrIndex(self) -> int: ...
    def SetOneItemFlyAnim(
        self,
        itemDict: dict,
        fromPos: Tuple[float, float],
        toPos: Tuple[float, float],
        uiSize: Union[float, Tuple[float, float]],
    ) -> None: ...
    def SetItemsFlyAnim(
        self,
        itemAnimDataList: List[Dict[str, Union[dict, Tuple[float, float], float]]]
    ) -> None: ...













