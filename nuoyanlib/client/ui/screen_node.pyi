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
#   Last Modified : 2025-02-21
#
# ====================================================


from typing import Callable, Optional, Tuple, Dict, Union, List, Set
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ..._core._typing import EventArgs, UiControl, FTuple2
from ..._core._client._lib_client import NuoyanLibClientSystem
from ..._core._listener import event, quick_listen
# from .item_fly_anim import ItemFlyAnim
# from .item_tips_box import ItemTipsBox
# from .item_grid_manager import ItemGridManager


_BTN_TYPE = Union[str, ButtonUIControl]


def notify_server(func: Callable) -> Callable: ...
def _set_touch_up_callback(self: ButtonUIControl, func: Callable) -> None: ...
def _set_touch_down_callback(self: ButtonUIControl, func: Callable) -> None: ...
def _set_touch_move_callback(self: ButtonUIControl, func: Callable) -> None: ...


@quick_listen
class NuoyanScreenNode(ScreenNode):
    __screen_node: Union[ScreenNode, NuoyanScreenNode]
    __lib_sys: NuoyanLibClientSystem
    # __ifa_ins: ItemFlyAnim
    # __itb_ins: ItemTipsBox
    # __igm_ins: ItemGridManager
    # __compose_ins: Tuple[Union[ItemFlyAnim, ItemTipsBox, ItemGridManager], ...]
    _btn_double_click_data: Dict[str, Callable]
    __double_click_args: Optional[dict]
    _vibrate_time: int
    _btn_long_click_data: Dict[str, Dict[str, Union[Callable, bool]]]
    _btn_touch_down_data: Dict[str, Callable]
    __long_click_args: Optional[dict]
    __btn_movable_data: Dict[str, Dict[str, Union[bool, str, Callable]]]
    _btn_touch_up_data: Dict[str, Callable]
    __movable_by_lc_data: Dict[str, Dict[str, Union[bool, str, Callable]]]
    __save_pos_uis: Set[str]
    __double_click_tick: int
    __double_click_btn_path: str
    __finger_pos: Optional[FTuple2]
    __is_moving: bool
    __long_click_btn_path: str
    __long_click_tick: int
    __ui_pos_key: str
    _btn_touch_move_data: Dict[str, Callable]
    __long_click_threshold: int
    cs: Optional[ClientSystem]
    screen_size: FTuple2
    def __init__(self: ..., namespace: str, name: str, param: Optional[dict]) -> None: ...
    # def __getattr__(self: ..., name: str) -> Any: ...
    def Create(self: ...): ...
    def Update(self: ...): ...
    def Destroy(self: ...): ...
    def DelUiPosData(self, btn: Optional[_BTN_TYPE] = None) -> None: ...
    def GetDirectChildrenPath(self: ..., control: UiControl) -> List[str]: ...
    def GetParentPath(self: ..., control: UiControl) -> Optional[str]: ...
    def GetParentControl(self: ..., control: UiControl) -> Optional[BaseUIControl]: ...
    def SetButtonDoubleClickCallback(
        self: ...,
        btn: Union[str, ButtonUIControl],
        on_double_click: Callable,
    ) -> None: ...
    def RemoveButtonDoubleClickCallback(self: ..., btn: _BTN_TYPE) -> None: ...
    def SetButtonMovable(
        self: ...,
        btn: _BTN_TYPE,
        move_parent: bool = False,
        associated_uis: Optional[Union[str, List[str]]] = None,
        save: bool = True,
    ) -> None: ...
    def CancelButtonMovable(self: ..., btn: _BTN_TYPE) -> None: ...
    def SetButtonMovableByLongClick(
        self: ...,
        btn: _BTN_TYPE,
        move_parent: bool = False,
        associated_uis: Optional[str, List[str]] = None,
        save: bool = True,
    ) -> None: ...
    def SetButtonLongClickCallback(self: ..., btn: _BTN_TYPE, on_long_click: Callable) -> None: ...
    def RemoveButtonLongClickCallback(self: ..., btn: _BTN_TYPE) -> None: ...
    def SetLongClickVibrateTime(self: ..., time: int) -> None: ...
    def HasLongClicked(self: ..., btn: str) -> bool: ...
    @event("ScreenSizeChangedClientEvent")
    def _on_screen_size_changed(self: ..., args: EventArgs) -> None: ...
    @event("GetEntityByCoordReleaseClientEvent")
    def _on_get_entity_by_coord_release(self: ..., args: EventArgs) -> None: ...
    def __super(self: ..., name: str) -> None: ...
    def __override_method(self: ..., control: ButtonUIControl, method: str, func: Callable) -> None: ...
    def _get_control(self: ..., path: Union[str, BaseUIControl]) -> BaseUIControl: ...
    def _get_path(self: ..., control: Union[str, BaseUIControl]) -> str: ...
    def __on_touch_up(self: ..., args: EventArgs) -> None: ...
    def __on_touch_down(self: ..., args: EventArgs) -> None: ...
    def __on_movable_long_click(self: ..., args: EventArgs) -> None: ...
    def __on_move(self: ..., args: EventArgs) -> None: ...
    def _save_ui_pos(self: ...) -> None: ...
    def _get_ui_pos_data(self: ...) -> Dict[str, FTuple2]: ...
    def _recover_ui_pos(self: ...) -> None: ...
    def __vibrate(self: ...) -> None: ...
    def __set_widget_pos(self: ..., ctrl: str, offset: FTuple2) -> None: ...
    # PlayItemFlyAnim = ItemFlyAnim.PlayItemFlyAnim
    # ShowItemHoverTipsBox = ItemTipsBox.ShowItemHoverTipsBox
    # ShowHoverTipsBox = ItemTipsBox.ShowHoverTipsBox
    # HideHoverTipsBox = ItemTipsBox.HideHoverTipsBox
    # InitItemGrids = ItemGridManager.InitItemGrids
    # AllItemGridsInited = ItemGridManager.AllItemGridsInited
    # GetItemGridKey = ItemGridManager.GetItemGridKey
    # GetItemCellPath = ItemGridManager.GetItemCellPath
    # GetItemCellPos = ItemGridManager.GetItemCellPos
    # GetAllItemCellUIControls = ItemGridManager.GetAllItemCellUIControls
    # GetItemCellUIControl = ItemGridManager.GetItemCellUIControl
    # SetItemCellDurabilityBar = ItemGridManager.SetItemCellDurabilityBar
    # SetItemCellRenderer = ItemGridManager.SetItemCellRenderer
    # SetItemCellCountLabel = ItemGridManager.SetItemCellCountLabel
    # UpdateItemGrids = ItemGridManager.UpdateItemGrids
    # ClearItemGridState = ItemGridManager.ClearItemGridState
    # StartItemHeapProgressBar = ItemGridManager.StartItemHeapProgressBar
    # PauseItemHeapProgressBar = ItemGridManager.PauseItemHeapProgressBar
    # LockItemGrid = ItemGridManager.LockItemGrid
    # IsItemGridLocked = ItemGridManager.IsItemGridLocked
    # LockItemCell = ItemGridManager.LockItemCell
    # IsItemCellLocked = ItemGridManager.IsItemCellLocked
    # SetItemGridItems = ItemGridManager.SetItemGridItems
    # GetItemGridItems = ItemGridManager.GetItemGridItems
    # SetItemCellItem = ItemGridManager.SetItemCellItem
    # GetItemCellItem = ItemGridManager.GetItemCellItem
    # MoveItem = ItemGridManager.MoveItem
    # MergeItems = ItemGridManager.MergeItems
    # DivideItemEvenly = ItemGridManager.DivideItemEvenly
    # SetItemCellCount = ItemGridManager.SetItemCellCount
    # GetItemCellCount = ItemGridManager.GetItemCellCount
    # ReturnItemsToInv = ItemGridManager.ReturnItemsToInv
    # SpawnItemToItemGrid = ItemGridManager.SpawnItemToItemGrid
    # ThrowItemFromItemGrid = ItemGridManager.ThrowItemFromItemGrid
    # SetSelectedItemData = ItemGridManager.SetSelectedItemData
    # GetSelectedItemData = ItemGridManager.GetSelectedItemData
    # IsCellSelected = ItemGridManager.IsCellSelected
    # SetItemHeapData = ItemGridManager.SetItemHeapData
    # GetItemHeapData = ItemGridManager.GetItemHeapData
























