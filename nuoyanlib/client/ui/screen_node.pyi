# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from typing import Optional, overload, Any, TypeVar, Dict, Type, Generator
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.system.clientSystem import ClientSystem
from ..._core._types._typing import UiPathOrControl, STuple, NyControlTypes
from ..._core._listener import ClientEventProxy
from .nyc import *


_T = TypeVar("_T")


_UI_CONTROL_TYPE_2_NY_CLS: Dict[int, NyControlTypes]


class ScreenNodeExtension(ClientEventProxy):
    ROOT_PANEL_PATH: str
    """
    | 使用基类画布时的根节点路径，所有自定义控件均挂接在该路径下。
    """
    _LIMIT_ATTR: STuple
    _nyc_cache: Dict[str, NyControlTypes]
    _ui_pos_data_key: str
    _screen_node: ScreenNode
    cs: Optional[ClientSystem]
    """
    | 创建UI的客户端实例。
    """
    root_panel: BaseUIControl
    """
    | 当前界面根节点的 ``BaseUIControl`` 实例。
    """
    @overload
    def __init__(self: ..., namespace: str, name: str, param: Optional[dict] = None, /) -> None: ...
    @overload
    def __init__(self: ..., screen_name: str, screen_node: ScreenNode, /) -> None: ...
    def __create__(self): ...
    def __destroy__(self): ...
    def create_ny_control(self, path_or_control: UiPathOrControl) -> Optional[NyControl]: ...
    def create_ny_button(self, path_or_control: UiPathOrControl, touch_event_params: Optional[dict] = None) -> Optional[NyButton]: ...
    def create_ny_grid(self, path_or_control: UiPathOrControl, is_stack_grid: bool = False) -> Optional[NyGrid]: ...
    def get_children_path_by_level(
        self,
        path_or_control: UiPathOrControl,
        level: int = 1
    ) -> Generator[str, None, None]: ...
    def get_children_ny_control_by_level(
        self,
        path_or_control: UiPathOrControl,
        level: int = 1
    ) -> Generator[NyControl, None, None]: ...
    def get_parent_path(self, path_or_control: UiPathOrControl) -> Optional[str]: ...
    def get_parent_ny_control(self, path_or_control: UiPathOrControl) -> Optional[NyControl]: ...
    def clear_all_pos_data(self) -> bool: ...
    def save_all_pos_data(self) -> bool: ...
    CreateNyControl = create_ny_control
    CreateNyButton = create_ny_button
    CreateNyGrid = create_ny_grid
    GetChildrenPathByLevel = get_children_path_by_level
    GetChildrenNyControlByLevel = get_children_ny_control_by_level
    GetParentPath = get_parent_path
    GetParentNyControl = get_parent_ny_control
    ClearAllPosData = clear_all_pos_data
    SaveAllPosData = save_all_pos_data
    def _create_nyc(self, path_or_control: UiPathOrControl, typ: Type[_T], **kwargs: Any) -> _T: ...
    def _destroy_nyc(self, nyc: NyControl) -> None: ...
    def _recover_ui_pos(self) -> None: ...
