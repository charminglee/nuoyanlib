# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


from typing import List, Dict, Union, overload, Optional
from mod.server.system.serverSystem import ServerSystem
from ...._core._types._typing import ItemDict, ItemCellPos, ArgsDict
from ...._core._listener import lib_sys_event, ServerEventProxy
from ...._core._utils import singleton


_DATA_KEY_ITEMS_DATA: str
_INV_POS_TYPE: int


@singleton
class ItemGridServer(ServerEventProxy, ServerSystem):
    item_grid_items: Dict[str, Dict[str, List[Optional[ItemDict]]]]
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    def Destroy(self): ...
    @lib_sys_event
    def _RegisterItemGrid(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _OnClientItemGridInitFinished(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _UpdateItemGrids(self, args: ArgsDict) -> bool: ...
    @lib_sys_event
    def _ThrowItem(self, args: ArgsDict) -> None: ...
    @lib_sys_event
    def _SyncItemOperation(self, args: ArgsDict) -> None: ...
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
        item_dict_list: List[Optional[ItemDict]],
        deepcopy: bool = False,
    ) -> List[bool]: ...
    def set_item(
        self,
        player_id: str,
        pos_list: Union[List[ItemCellPos], ItemCellPos],
        item_dict_list: Union[List[Optional[ItemDict]], Optional[ItemDict]],
        deepcopy: bool = False,
    ) -> bool: ...
    def _set_item(
        self,
        player_id: str, 
        pos: ItemCellPos, 
        item_dict: Optional[ItemDict], 
        deepcopy: bool = False,
    ) -> bool: ...
    def _broadcast_item_grid_changed(self, player_id: str, pos: ItemCellPos, new_item: Optional[ItemDict]) -> bool: ...
    def get_all_items(self, player_id: str, key: str) -> List[Optional[ItemDict]]: ...
    def get_item(self, player_id: str, pos: ItemCellPos, deepcopy: bool = False) -> Optional[ItemDict]: ...
    @overload
    def _get_not_inv_items(self, player_id: str, key: str) -> List[Optional[ItemDict]]: ...
    @overload
    def _get_not_inv_items(self, player_id: str, key: str, index: int) -> Optional[ItemDict]: ...
