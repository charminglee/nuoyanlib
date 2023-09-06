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


from typing import Callable, Optional, Tuple, Dict, Union, List, Set
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ..nuoyanClientSystem import client_listener


def notify_server(func: Callable) -> Callable: ...


class NuoyanScreenNode(ScreenNode):
    cs: ClientSystem
    screenSize: Tuple[float, float]
    _btnDoubleClickData: Dict[str, Dict[str, Callable]]
    _doubleClickArgs: Optional[dict]
    _vibrateTime: int
    _btnLongClickData: Dict[str, Dict[str, Union[Callable, bool]]]
    _btnTouchData: Dict[str, Dict[str, Callable]]
    _touchingButtonArgs: Optional[dict]
    _btnMovableData: Dict[str, Dict[str, Union[bool, str, Callable]]]
    _btnTouchUpCallbackData: Dict[str, List[Callable]]
    _moveAfterLCData: Dict[str, Dict[str, Union[bool, str, Callable]]]
    _savePosUis: Set[str]
    __doubleClickTick: int
    __doubleClickBtnPath: str
    __fingerPos: Optional[Tuple[float, float]]
    __isMoving: bool
    __touchingButtonPath: str
    __tick: int
    __uiPosKey: str
    def __init__(self, namespace: str, name: str, param: dict) -> None: ...
    def Create(self) -> None: ...
    def Update(self) -> None: ...
    def Destroy(self) -> None: ...
    def OnDeactive(self) -> None: ...
    def OnActive(self) -> None: ...
    def SetButtonDoubleClickCallback(
        self,
        buttonPath: str,
        doubleClickCallback: Callable,
        touchUpCallback: Optional[Callable] = None,
    ) -> None: ...
    def SetButtonMovable(
        self,
        btnPath: str,
        moveParent: bool = False,
        associatedPath: Optional[Union[str, Tuple[str, ...]]] = None,
        touchMoveCallback: Optional[Callable] = None,
    ) -> None: ...
    def CancelButtonMovable(self, btnPath: str) -> None: ...
    def SetButtonMovableAfterLongClick(
        self,
        btnPath: str,
        moveParent: bool = False,
        associatedPath: Optional[str, Tuple[str, ...]] = None,
        touchUpFunc: Optional[Callable] = None,
        longClickFunc: Optional[Callable] = None,
        touchMoveCallback: Optional[Callable] = None,
        touchMoveOutFunc: Optional[Callable] = None,
        touchDownFunc: Optional[Callable] = None,
        touchCancelFunc: Optional[Callable] = None,
    ) -> Optional[ButtonUIControl]: ...
    def SetButtonLongClickCallback(
        self,
        btnPath: str,
        longClickFunc: Callable,
        touchUpFunc: Optional[Callable] = None,
        touchMoveOutFunc: Optional[Callable] = None,
        touchDownFunc: Optional[Callable] = None,
        touchCancelFunc: Optional[Callable] = None,
    ) -> Optional[ButtonUIControl]: ...
    def RemoveButtonLongClickCallback(self, btnPath: str) -> None: ...
    def SetLongClickVibrateTime(self, time: int) -> None: ...
    def HasLongClicked(self, bp: str) -> bool: ...
    def _runTouchUpList(self, args: dict) -> None: ...
    @client_listener("GetEntityByCoordReleaseClientEvent")
    def _OnCoordRelease(self, args: dict) -> None: ...
    def _saveUiPosition(self) -> None: ...
    def _onBtnTouchUp(self, args: dict) -> None: ...
    def _onTouchUp(self, args: dict) -> None: ...
    def _onTouchCancel(self, args: dict) -> None: ...
    def _onTouchMoveOut(self, args: dict) -> None: ...
    def _onTouchDown(self, args: dict) -> None: ...
    def _vibrate(self) -> None: ...
    def _onLongClick(self, args: dict) -> None: ...
    def _onDown(self, args: dict) -> None: ...
    def _testPosIsOut(self, pos: List[float, float], buttonSize: Tuple[float, float]) -> None: ...
    def _setWidgetPosition(self, widgetControl: BaseUIControl, offset: Tuple[float, float]) -> None: ...
    def _onMove(self, args: dict) -> None: ...
    @client_listener("ScreenSizeChangedClientEvent")
    def _OnScreenSizeChanged(self, args: dict) -> None: ...
























