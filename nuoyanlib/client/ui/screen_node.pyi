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


from typing import Callable, Optional, Tuple, Dict, Union, List, Set, Any
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ..._core._typing import EventArgs, Control
from ..._core._client._lib_client import NuoyanLibClientSystem
from ..._core._client._listener import event
from .item_fly_anim import ItemFlyAnim
from .item_tips_box import ItemTipsBox
from .item_grid_manager import ItemGridManager


def notify_server(func: Callable) -> Callable: ...


class NuoyanScreenNode(ScreenNode):
    __screen_node: Union[ScreenNode, NuoyanScreenNode]
    __lib_sys: NuoyanLibClientSystem
    __ifa_ins: ItemFlyAnim
    __itb_ins: ItemTipsBox
    __igm_ins: ItemGridManager
    __compose_ins: Tuple[Union[ItemFlyAnim, ItemTipsBox, ItemGridManager], ...]
    __btn_double_click_data: Dict[str, Dict[str, Callable]]
    __double_click_args: Optional[dict]
    _vibrate_time: int
    __btn_long_click_data: Dict[str, Dict[str, Union[Callable, bool]]]
    __btn_touch_data: Dict[str, Dict[str, Callable]]
    __touching_button_args: Optional[dict]
    __btn_movable_data: Dict[str, Dict[str, Union[bool, str, Callable]]]
    __btn_touch_up_data: Dict[str, List[Callable]]
    __move_after_lc_data: Dict[str, Dict[str, Union[bool, str, Callable]]]
    __save_pos_uis: Set[str]
    __double_click_tick: int
    __double_click_btn_path: str
    __finger_pos: Optional[Tuple[float, float]]
    __is_moving: bool
    __touching_btn_path: str
    __tick: int
    __ui_pos_key: str
    cs: Optional[ClientSystem]
    screen_size: Tuple[float, float]
    def __init__(self: ..., namespace: str, name: str, param: Optional[dict]) -> None: ...
    def __getattr__(self: ..., name: str) -> Any: ...
    def Create(self: ...): ...
    def Update(self: ...): ...
    def Destroy(self: ...): ...
    def GetDirectChildrenPath(self: ..., control: Control) -> List[str]: ...
    def GetParentPath(self: ..., control: Control) -> Optional[str]: ...
    def GetParentControl(self: ..., control: Control) -> Optional[BaseUIControl]: ...
    def SetButtonDoubleClickCallback(
        self: ...,
        btn_path: str,
        on_double_click: Callable,
        on_touch_up: Optional[Callable] = None,
    ) -> None: ...
    def SetButtonMovable(
        self: ...,
        btn_path: str,
        move_parent: bool = False,
        associated_path: Optional[Union[str, Tuple[str, ...]]] = None,
        on_touch_move: Optional[Callable] = None,
    ) -> None: ...
    def CancelButtonMovable(self: ..., btn_path: str) -> None: ...
    def SetButtonMovableAfterLongClick(
        self: ...,
        btn_path: str,
        move_parent: bool = False,
        associated_path: Optional[str, Tuple[str, ...]] = None,
        on_touch_up: Optional[Callable] = None,
        on_long_click: Optional[Callable] = None,
        on_touch_move: Optional[Callable] = None,
        on_touch_move_out: Optional[Callable] = None,
        on_touch_down: Optional[Callable] = None,
        on_touch_cancel: Optional[Callable] = None,
    ) -> Optional[ButtonUIControl]: ...
    def SetButtonLongClickCallback(
        self: ...,
        btn_path: str,
        on_long_click: Callable,
        on_touch_up: Optional[Callable] = None,
        on_touch_move_out: Optional[Callable] = None,
        on_touch_down: Optional[Callable] = None,
        on_touch_cancel: Optional[Callable] = None,
    ) -> Optional[ButtonUIControl]: ...
    def RemoveButtonLongClickCallback(self: ..., btn_path: str) -> None: ...
    def SetLongClickVibrateTime(self: ..., time: int) -> None: ...
    def HasLongClicked(self: ..., bp: str) -> bool: ...
    @event("ScreenSizeChangedClientEvent")
    def _on_screen_size_changed(self: ..., args: EventArgs) -> None: ...
    @event("GetEntityByCoordReleaseClientEvent")
    def _on_get_entity_by_coord_release(self: ..., args: EventArgs) -> None: ...
    def __super(self: ..., name: str) -> None: ...
    def __run_touch_up_list(self: ..., args: EventArgs) -> None: ...
    def __on_btn_touch_up(self: ..., args: EventArgs) -> None: ...
    def __on_touch_up(self: ..., args: EventArgs) -> None: ...
    def __on_touch_cancel(self: ..., args: EventArgs) -> None: ...
    def __on_touch_move_out(self: ..., args: EventArgs) -> None: ...
    def __on_touch_down(self: ..., args: EventArgs) -> None: ...
    def __on_long_click(self: ..., args: EventArgs) -> None: ...
    def __on_down(self: ..., args: EventArgs) -> None: ...
    def __on_move(self: ..., args: EventArgs) -> None: ...
    def _save_ui_pos(self: ...) -> None: ...
    def __vibrate(self: ...) -> None: ...
    def __set_widget_pos(self: ..., widget_ctrl: BaseUIControl, offset: Tuple[float, float]) -> None: ...
    PlayItemFlyAnim = ItemFlyAnim.PlayItemFlyAnim
    ShowItemHoverTipsBox = ItemTipsBox.ShowItemHoverTipsBox
    ShowHoverTipsBox = ItemTipsBox.ShowHoverTipsBox
    HideHoverTipsBox = ItemTipsBox.HideHoverTipsBox
    InitItemGrids = ItemGridManager.InitItemGrids
    AllItemGridsInited = ItemGridManager.AllItemGridsInited
    GetItemGridKey = ItemGridManager.GetItemGridKey
    GetItemCellPath = ItemGridManager.GetItemCellPath
    GetItemCellPos = ItemGridManager.GetItemCellPos
    GetAllItemCellUIControls = ItemGridManager.GetAllItemCellUIControls
    GetItemCellUIControl = ItemGridManager.GetItemCellUIControl
    SetItemCellDurabilityBar = ItemGridManager.SetItemCellDurabilityBar
    SetItemCellRenderer = ItemGridManager.SetItemCellRenderer
    SetItemCellCountLabel = ItemGridManager.SetItemCellCountLabel
    UpdateItemGrids = ItemGridManager.UpdateItemGrids
    ClearItemGridState = ItemGridManager.ClearItemGridState
    StartItemHeapProgressBar = ItemGridManager.StartItemHeapProgressBar
    PauseItemHeapProgressBar = ItemGridManager.PauseItemHeapProgressBar
    LockItemGrid = ItemGridManager.LockItemGrid
    IsItemGridLocked = ItemGridManager.IsItemGridLocked
    LockItemCell = ItemGridManager.LockItemCell
    IsItemCellLocked = ItemGridManager.IsItemCellLocked
    SetItemGridItems = ItemGridManager.SetItemGridItems
    GetItemGridItems = ItemGridManager.GetItemGridItems
    SetItemCellItem = ItemGridManager.SetItemCellItem
    GetItemCellItem = ItemGridManager.GetItemCellItem
    MoveItem = ItemGridManager.MoveItem
    MergeItems = ItemGridManager.MergeItems
    DivideItemEvenly = ItemGridManager.DivideItemEvenly
    SetItemCellCount = ItemGridManager.SetItemCellCount
    GetItemCellCount = ItemGridManager.GetItemCellCount
    ReturnItemsToInv = ItemGridManager.ReturnItemsToInv
    SpawnItemToItemGrid = ItemGridManager.SpawnItemToItemGrid
    ThrowItemFromItemGrid = ItemGridManager.ThrowItemFromItemGrid
    SetSelectedItemData = ItemGridManager.SetSelectedItemData
    GetSelectedItemData = ItemGridManager.GetSelectedItemData
    IsCellSelected = ItemGridManager.IsCellSelected
    SetItemHeapData = ItemGridManager.SetItemHeapData
    GetItemHeapData = ItemGridManager.GetItemHeapData
























