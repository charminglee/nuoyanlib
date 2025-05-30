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
#   Last Modified : 2025-05-30
#
# ====================================================


from typing import List, Dict, Union, overload
from mod.server.system.serverSystem import ServerSystem
from ...._core._types._typing import ItemDict, ItemCellPos, EventArgs
from ...._core._listener import lib_sys_event, ServerEventProxy
from ...._core._utils import singleton


_DATA_KEY_ITEMS_DATA: str
_INV_POS_TYPE: int


@singleton
class ItemGridServer(ServerEventProxy, ServerSystem):
    item_grid_items: Dict[str, Dict[str, List[ItemDict]]]
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    def Destroy(self): ...
    @lib_sys_event
    def _RegisterItemGrid(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _OnClientItemGridInitFinished(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _UpdateItemGrids(self, args: EventArgs) -> bool: ...
    @lib_sys_event
    def _ThrowItem(self, args: EventArgs) -> None: ...
    @lib_sys_event
    def _SyncItemOperation(self, args: EventArgs) -> None: ...
    def _set_grid(self, player_id: str, args: tuple) -> None: ...
    def _set_cell(self, player_id: str, args: tuple) -> None: ...
    def _exchange(self, player_id: str, args: tuple) -> None: ...
    def _move(self, player_id: str, args: tuple) -> None: ...
    def _divide(self, player_id: str, args: tuple) -> None: ...
    def _set_count(self, player_id: str, args: tuple) -> None: ...
    def _ret_items(self, player_id: str, args: tuple) -> None: ...
    def set_all_items(
        self,
        player_id: str,
        key: str,
        item_dict_list: List[ItemDict],
        deepcopy: bool = False,
    ) -> List[bool]: ...
    def set_item(
        self,
        player_id: str,
        pos_list: Union[List[ItemCellPos], ItemCellPos],
        item_dict_list: Union[List[ItemDict], ItemDict],
        deepcopy: bool = False,
    ) -> bool: ...
    def _set_item(self, player_id: str, pos: ItemCellPos, item_dict: ItemDict, deepcopy: bool = False) -> bool: ...
    def _broadcast_item_grid_changed(self, player_id: str, pos: ItemCellPos, new_item: ItemDict) -> bool: ...
    def get_all_items(self, player_id: str, key: str) -> List[ItemDict]: ...
    def get_item(self, player_id: str, pos: ItemCellPos, deepcopy: bool = False) -> ItemDict: ...
    @overload
    def _get_not_inv_items(self, player_id: str, key: str) -> List[ItemDict]: ...
    @overload
    def _get_not_inv_items(self, player_id: str, key: str, index: int) -> ItemDict: ...
