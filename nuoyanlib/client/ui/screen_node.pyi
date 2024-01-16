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
#   Last Modified : 2024-01-14
#
# ====================================================


from typing import Callable, Optional, Tuple, Dict, Union, List, Set
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ...config import SERVER_SYSTEM_NAME, MOD_NAME


_lsn_func_args: List[Tuple[str, str, str, str, int]]


def ui_listener(
    event_name: str = "",
    namespace: str = "",
    system_name: str = "",
    priority: int = 0
) -> Callable[[Callable], Callable]: ...
def _add_listener(
    func: Callable,
    event_name: str = "",
    namespace: str = MOD_NAME,
    system_name: str = SERVER_SYSTEM_NAME,
    priority: int = 0
) -> None: ...
def _listen(self: ScreenNode) -> None: ...
def notify_server(func: Callable) -> Callable: ...


class NuoyanScreenNode(ScreenNode):
    cs: ClientSystem
    screen_size: Tuple[float, float]
    _btn_double_click_data: Dict[str, Dict[str, Callable]]
    _double_click_args: Optional[dict]
    _vibrate_time: int
    _btn_long_click_data: Dict[str, Dict[str, Union[Callable, bool]]]
    _btn_touch_data: Dict[str, Dict[str, Callable]]
    _touching_button_args: Optional[dict]
    _btn_movable_data: Dict[str, Dict[str, Union[bool, str, Callable]]]
    _btn_touch_up_data: Dict[str, List[Callable]]
    _move_after_lc_data: Dict[str, Dict[str, Union[bool, str, Callable]]]
    _save_pos_uis: Set[str]
    __double_click_tick: int
    __double_click_btn_path: str
    __finger_pos: Optional[Tuple[float, float]]
    __is_moving: bool
    __touching_btn_path: str
    __tick: int
    __ui_pos_key: str
    def __init__(self, namespace: str, name: str, param: Optional[dict]) -> None: ...
    def Create(self) -> None: ...
    def OnTick(self) -> None: ...
    def Update(self) -> None: ...
    def Destroy(self) -> None: ...
    def OnDeactive(self) -> None: ...
    def OnActive(self) -> None: ...
    def SetButtonDoubleClickCallback(
        self,
        btn_path: str,
        on_double_click: Callable,
        on_touch_up: Optional[Callable] = None,
    ) -> None: ...
    def SetButtonMovable(
        self,
        btn_path: str,
        move_parent: bool = False,
        associated_path: Optional[Union[str, Tuple[str, ...]]] = None,
        on_touch_move: Optional[Callable] = None,
    ) -> None: ...
    def CancelButtonMovable(self, btn_path: str) -> None: ...
    def SetButtonMovableAfterLongClick(
        self,
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
        self,
        btn_path: str,
        on_long_click: Callable,
        on_touch_up: Optional[Callable] = None,
        on_touch_move_out: Optional[Callable] = None,
        on_touch_down: Optional[Callable] = None,
        on_touch_cancel: Optional[Callable] = None,
    ) -> Optional[ButtonUIControl]: ...
    def RemoveButtonLongClickCallback(self, btn_path: str) -> None: ...
    def SetLongClickVibrateTime(self, time: int) -> None: ...
    def HasLongClicked(self, bp: str) -> bool: ...
    @ui_listener("OnScriptTickClient")
    def _OnScriptTickClient(self) -> None: ...
    @ui_listener("ScreenSizeChangedClientEvent")
    def _ScreenSizeChangedClientEvent(self, args: dict) -> None: ...
    @ui_listener("GetEntityByCoordReleaseClientEvent")
    def _GetEntityByCoordReleaseClientEvent(self, args: dict) -> None: ...
    def _run_touch_up_list(self, args: dict) -> None: ...
    def _on_btn_touch_up(self, args: dict) -> None: ...
    def _on_touch_up(self, args: dict) -> None: ...
    def _on_touch_cancel(self, args: dict) -> None: ...
    def _on_touch_move_out(self, args: dict) -> None: ...
    def _on_touch_down(self, args: dict) -> None: ...
    def _on_long_click(self, args: dict) -> None: ...
    def _on_down(self, args: dict) -> None: ...
    def _on_move(self, args: dict) -> None: ...
    def _save_ui_pos(self) -> None: ...
    def _vibrate(self) -> None: ...
    def _test_pos_is_out(self, pos: List[float, float], button_size: Tuple[float, float]) -> None: ...
    def _set_widget_pos(self, widget_ctrl: BaseUIControl, offset: Tuple[float, float]) -> None: ...
























