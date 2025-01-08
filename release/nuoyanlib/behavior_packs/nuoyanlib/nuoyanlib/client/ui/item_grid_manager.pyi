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
#   Last Modified : 2024-07-02
#
# ====================================================


from typing import List, Dict, Optional, Tuple, Set, Callable, Any
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.screenNode import ScreenNode
from .item_fly_anim import ItemFlyAnim
from .item_tips_box import ItemTipsBox
from .screen_node import NuoyanScreenNode
from ..._core._typing import ItemCellPos, ItemCell, ItemDict, EventArgs, ItemGridKeys, ItemHeapData, ItemSelectedData
from ..._core._client._lib_client import NuoyanLibClientSystem
from ..._core._client._listener import event, lib_sys_event


_IMAGE_PATH_ITEM_CELL_SELECTED: str
_IMAGE_PATH_ITEM_CELL_DEFAULT: str
_UI_PATH_COUNT: str
_UI_PATH_ITEM_RENDERER: str
_UI_PATH_DURABILITY: str
_UI_PATH_DEFAULT: str
_UI_PATH_HEAP: str
_UI_PATH_ITEM_BG: str


_INV_POS_TYPE: int


class ItemGridManager(object):
    __lib_sys: NuoyanLibClientSystem
    __nsn_ins: NuoyanScreenNode
    __ifa_ins: ItemFlyAnim
    __itb_ins: ItemTipsBox
    __screen_node: ScreenNode
    _item_heap_data: ItemHeapData
    _selected_item: ItemSelectedData
    _cell_paths: Dict[ItemCellPos, str]
    _cell_poses: Dict[str, ItemCellPos]
    _cell_ui_ctrls: Dict[ItemCellPos, ButtonUIControl]
    _locked_cells: Set[ItemCellPos]
    _locked_grids: Set[str]
    __move_in_cell_list: List[str]
    _inited_keys: Set[str]
    _inv36_keys: Set[str]
    _inv27_keys: Set[str]
    _shortcut_keys: Set[str]
    __tick: int
    __src_item: ItemDict
    __cancel_hide_tips: int
    def __init__(
        self: ...,
        nuoyan_screen_node: NuoyanScreenNode,
        item_fly_anim: ItemFlyAnim,
        item_tips_box: ItemTipsBox,
    ) -> None: ...
    def Destroy(self: ...): ...
    def Update(self: ...): ...
    @property
    def _grid_path(self: ...) -> Dict[str, Tuple[str, bool]]: ...
    @property
    def _grid_size(self: ...) -> Dict[str, int]: ...
    @property
    def _grid_items(self: ...) -> Dict[str, List[ItemDict]]: ...
    @property
    def _registered_keys(self: ...) -> List[str]: ...
    @event("GetEntityByCoordReleaseClientEvent")
    def _on_get_entity_by_coord_release(self: ..., args: EventArgs) -> None: ...
    @lib_sys_event("_UpdateItemGrids")
    def _on_update_item_grids(self: ..., args: EventArgs) -> None: ...
    @event("InventoryItemChangedClientEvent")
    def _on_inv_item_changed(self: ..., args: EventArgs) -> None: ...
    def OnMoveItemsBefore(self: ..., args: EventArgs) -> None: ...
    def OnItemGridSelectOrUnselectItem(self: ..., args: EventArgs) -> None: ...
    def OnItemCellTouchUp(self: ..., args: EventArgs) -> None: ...
    def _on_item_cell_touch_up(self: ..., args: EventArgs) -> None: ...
    def OnItemCellTouchMoveIn(self: ..., args: EventArgs) -> None: ...
    def _on_item_cell_touch_move_in(self: ..., args: EventArgs) -> None: ...
    def OnItemCellDoubleClick(self: ..., args: EventArgs) -> None: ...
    def _on_item_cell_double_click(self: ..., args: EventArgs) -> None: ...
    def OnItemCellLongClick(self: ..., args: EventArgs) -> None: ...
    def _on_item_cell_long_click(self: ..., args: EventArgs) -> None: ...
    def OnItemCellTouchDown(self: ..., args: EventArgs) -> None: ...
    def _on_item_cell_touch_down(self: ..., args: EventArgs) -> None: ...
    def OnItemCellTouchMove(self: ..., args: EventArgs) -> None: ...
    def OnItemCellTouchMoveOut(self: ..., args: EventArgs) -> None: ...
    def OnItemCellTouchCancel(self: ..., args: EventArgs) -> None: ...
    def _on_item_cell_hover_in(self: ..., args: EventArgs) -> None: ...
    def _on_item_cell_hover_out(self: ..., args: EventArgs) -> None: ...
    def GetAllItemCellUIControls(self: ..., key: str) -> List[ButtonUIControl]: ...
    def GetItemCellUIControl(self: ..., cell: ItemCell) -> Optional[ButtonUIControl]: ...
    def SetItemCellDurabilityBar(
        self: ...,
        cell: ItemCell,
        val: float = 1.0,
        item_dict: ItemDict = None,
        auto: bool = False,
    ) -> bool: ...
    def SetItemCellRenderer(self: ..., cell: ItemCell, item_dict: ItemDict = None, auto: bool = False) -> bool: ...
    def SetItemCellCountLabel(
        self: ...,
        cell: ItemCell,
        count: int = 0,
        item_dict: ItemDict = None,
        auto: bool = False,
    ) -> bool: ...
    def UpdateItemGrids(self: ..., keys: ItemGridKeys = None) -> None: ...
    def _update_inv_grids(self: ..., keys: Tuple[str]) -> None: ...
    def ClearItemGridState(self: ...) -> None: ...
    def _set_item_fly_anim(self: ..., item_dict: ItemDict, from_cell: ItemCell, to_cell: ItemCell) -> None: ...
    def StartItemHeapProgressBar(self: ...) -> bool: ...
    def PauseItemHeapProgressBar(self: ...) -> bool: ...
    def LockItemGrid(self: ..., key: str, lock: bool) -> bool: ...
    def IsItemGridLocked(self: ..., key: str) -> bool: ...
    def LockItemCell(self: ..., cell: ItemCell, lock: bool) -> bool: ...
    def IsItemCellLocked(self: ..., cell: ItemCell) -> bool: ...
    def _sync_item_operation(self: ..., op: str, *args: Any) -> None: ...
    def _parse_keys(self: ..., keys: ItemGridKeys) -> Tuple[str, ...]: ...
    def _filter_registered_keys(self: ..., keys: Tuple[str, ...]) -> Tuple[str, ...]: ...
    def _filter_inited_keys(self: ..., keys: Tuple[str, ...]) -> Tuple[str, ...]: ...
    def _is_inv_key(self: ..., *keys: str) -> bool: ...
    def _is_inv36_key(self: ..., key: str) -> bool: ...
    def _is_inv27_key(self: ..., key: str) -> bool: ...
    def _is_shortcut_key(self: ..., key: str) -> bool: ...
    def _is_cell_exist(self: ..., *cell: ItemCell) -> bool: ...
    def _set_cell_ui_item(self: ..., cell: ItemCell, item_dict: ItemDict) -> None: ...
    def _set_grid_ui_item(self: ..., key: str, item_dict_list: List[ItemDict]) -> None: ...
    def SetItemGridItems(self: ..., key: str, item_dict_list: List[ItemDict]) -> bool: ...
    def _get_grid_items(self: ..., key: str, deepcopy: bool = False) -> List[ItemDict]: ...
    def GetItemGridItems(self: ..., key: str) -> List[ItemDict]: ...
    def SetItemCellItem(self: ..., cell: ItemCell, item_dict: ItemDict) -> bool: ...
    def _get_cell_item(self: ..., cell: ItemCell, deepcopy: bool = False) -> ItemDict: ...
    def GetItemCellItem(self: ..., cell: ItemCell) -> ItemDict: ...
    def MoveItem(
        self: ...,
        from_cell: ItemCell,
        to_cell: ItemCell,
        move_count: int = -1,
        fly_anim: bool = True,
        force: bool = False,
    ) -> bool: ...
    def _exchange_items(self: ..., from_cell: ItemCell, to_cell: ItemCell) -> None: ...
    def _move_item_to_empty(self: ..., from_cell: ItemCell, to_cell: ItemCell, count: int) -> None: ...
    def _move_item_to_same(self: ..., from_cell: ItemCell, to_cell: ItemCell, count: int) -> None: ...
    def MergeItems(self: ..., to_cell: ItemCell, fly_anim: bool = True) -> bool: ...
    def DivideItemEvenly(
        self: ...,
        from_cell: ItemCell,
        to_cell_list: List[ItemCell],
        override: bool = False,
        src_item: ItemDict = None,
    ) -> bool: ...
    def SetItemCellCount(self: ..., cell: ItemCell, count: int, absolute: int = 0) -> int: ...
    def GetItemCellCount(self: ..., cell: ItemCell) -> int: ...
    def ReturnItemsToInv(self: ..., keys: ItemGridKeys = None) -> None: ...
    def SpawnItemToItemGrid(self: ..., item_dict: dict, key: str) -> bool: ...
    def ThrowItemFromItemGrid(self: ..., cell: ItemCell, count: int = -1) -> bool: ...
    def SetSelectedItemData(self: ..., cell: ItemCell, selected: bool = True) -> bool: ...
    def GetSelectedItemData(self: ...) -> Optional[ItemSelectedData]: ...
    def IsCellSelected(self: ..., cell: ItemCell) -> bool: ...
    def SetItemHeapData(
        self: ...,
        cell: ItemCell,
        count: int,
    ) -> Optional[ItemHeapData]: ...
    def GetItemHeapData(self: ...) -> Optional[ItemHeapData]: ...
    def InitItemGrids(
        self: ...,
        keys: ItemGridKeys = None,
        callback: Optional[Callable[[Tuple[str, ...], Tuple[bool, ...]], ...]] = None,
    ) -> None: ...
    def _init_item_grids(
        self: ...,
        keys: Tuple[str, ...],
        callback: Optional[Callable[[Tuple[str, ...], Tuple[bool, ...]], ...]],
    ) -> None: ...
    def _is_grid_inited(self: ..., key: str) -> bool: ...
    def AllItemGridsInited(self: ..., keys: ItemGridKeys = None) -> bool: ...
    def GetItemGridKey(self: ..., cell: ItemCell) -> Optional[str]: ...
    def GetItemCellPath(self: ..., cell: ItemCell) -> Optional[str]: ...
    def GetItemCellPos(self: ..., cell: ItemCell) -> Optional[ItemCellPos]: ...