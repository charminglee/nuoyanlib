# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from typing import Optional, List, overload, Type, Any, TypeVar, Dict
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ..._core._types._typing import UiPathOrControl, STuple
from ..._core._listener import ClientEventProxy
from .control import NyControl
from .button import NyButton
from .grid import NyGrid


_T = TypeVar("_T")


class ScreenNodeExtension(ClientEventProxy):
    ROOT_PANEL_PATH: str
    """
    | 使用基类画布时的根节点路径，所有自定义控件均挂接在该路径下。
    """
    _LIMIT_ATTR: STuple
    _ny_control_cache: Dict[str, NyControl]
    _ui_pos_data_key: str
    _screen_node: Optional[ScreenNode]
    cs: Optional[ClientSystem]
    """
    | 创建UI的客户端实例。
    """
    ny_controls: Dict[str, NyControl]
    """
    | 通过 ``CreateNyControl()`` 等接口创建的Ny控件的字典，key为控件路径，value为Ny控件实例。
    """
    root_panel: BaseUIControl
    """
    | 当前界面根节点的 ``BaseUIControl`` 实例。
    """
    @overload
    def __init__(self: ..., namespace: str, name: str, param: Optional[dict] = None, /) -> None: ...
    @overload
    def __init__(self: ..., screen_name: str, screen_node: ScreenNode, /) -> None: ...
    def __Create(self): ...
    def __Destroy(self): ...
    def CreateNyControl(self, path_or_control: UiPathOrControl) -> Optional[NyControl]: ...
    def CreateNyButton(
        self,
        path_or_control: UiPathOrControl,
        touch_event_params: Optional[dict] = None
    ) -> Optional[NyButton]: ...
    def CreateNyGrid(self, path_or_control: UiPathOrControl) -> Optional[NyGrid]: ...
    def GetAllChildrenPathByLevel(self, path_or_control: UiPathOrControl, level: int = 1) -> List[str]: ...
    def GetParentPath(self, path_or_control: UiPathOrControl) -> Optional[str]: ...
    def GetParentNyControl(self, path_or_control: UiPathOrControl) -> Optional[NyControl]: ...
    def ClearAllPosData(self) -> bool: ...
    def SaveAllPosData(self) -> bool: ...
    def _create_nyc(self, path: str, typ: Type[_T] = NyControl, **kwargs: Any) -> _T: ...
    def _recover_ui_pos(self) -> None: ...
