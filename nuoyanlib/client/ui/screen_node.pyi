# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-25
|
| ==============================================
"""


from typing import Optional, overload, Any, TypeVar, Dict, Type, Generator, Callable, Union
from types import FunctionType
from mod.client.ui.screenNode import ScreenNode
from mod.client.system.clientSystem import ClientSystem
from ..._core._types._typing import Args, Kwargs, UiPathOrControl, STuple, NyControlTypes, ArgsDict, FrameAnimData
from ..._core.event.listener import ClientEventProxy
from .nyc import *


_T = TypeVar("_T")


class ScreenNodeExtension(ClientEventProxy):
    ROOT_PANEL_PATH: str
    """
    | 使用基类画布时的根节点路径，所有自定义控件均挂接在该路径下。
    """
    _LIMIT_ATTR: STuple
    _nyc_cache: Dict[str, NyControlTypes]
    _ui_pos_data_key: str
    _screen_node: ScreenNode
    _frame_anim_data: Dict[str, FrameAnimData]
    cs: Union[ClientSystem, Any]
    """
    | 创建UI的客户端实例。
    """
    root_panel: NyControl
    """
    | 当前界面根节点的 ``NyControl`` 实例。
    """
    @overload
    def __init__(self: ..., namespace: str, name: str, param: Optional[dict] = None, /) -> None: ...
    @overload
    def __init__(self: ..., screen_name: str, screen_node: ScreenNode, /) -> None: ...
    def __create__(self): ...
    def __destroy__(self): ...
    def _GameRenderTickEvent(self, args: ArgsDict) -> None: ...
    @staticmethod
    def button_callback(
        btn_path: str,
        *callback_types: str,
        touch_event_params: Optional[dict] = None,
    ) -> Callable[[FunctionType], FunctionType]: ...
    def create_ny_control(self, path_or_control: UiPathOrControl) -> Optional[NyControl]: ...
    def create_ny_button(
        self,
        path_or_control: UiPathOrControl,
        *,
        touch_event_params: Optional[dict] = None
    ) -> Optional[NyButton]: ...
    def create_ny_grid(
        self,
        path_or_control: UiPathOrControl,
        *,
        is_stack_grid: bool = False,
    ) -> Optional[NyGrid]: ...
    def create_ny_label(self, path_or_control: str) -> Optional[NyLabel]: ...
    def create_ny_progress_bar(self, path_or_control: str) -> Optional[NyProgressBar]: ...
    def clear_all_pos_data(self) -> bool: ...
    def save_all_pos_data(self) -> bool: ...
    CreateNyControl = create_ny_control
    CreateNyButton = create_ny_button
    CreateNyGrid = create_ny_grid
    CreateNyLabel = create_ny_label
    CreateNyProgressBar = create_ny_progress_bar
    ClearAllPosData = clear_all_pos_data
    SaveAllPosData = save_all_pos_data
    def _play_frame_anim(
        self,
        ny_image: NyImage,
        tex_path: str,
        frame_count: int,
        frame_rate: int,
        stop_frame: int = -1,
        loop: bool = False,
        callback: Optional[Callable] = None,
        args: Optional[Args] = None,
        kwargs: Optional[Kwargs] = None,
    ) -> None: ...
    def _pause_frame_anim(self, ny_image: NyImage) -> None: ...
    def _stop_frame_anim(self, ny_image: NyImage) -> None: ...
    def _process_button_callback(self) -> None: ...
    def _expend_path(self, path: str) -> Generator[str]: ...
    def _create_nyc(self, path_or_control: UiPathOrControl, typ: Type[_T], **kwargs: Any) -> _T: ...
    def _destroy_nyc(self, nyc: NyControl) -> None: ...
    def _recover_ui_pos(self) -> None: ...
