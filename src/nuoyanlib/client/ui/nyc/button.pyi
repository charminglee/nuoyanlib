# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-04
|
| ====================================================
"""


from typing import Callable, ClassVar, Optional, Dict, Union, List, Any
from types import MethodType
from typing_extensions import Self
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.common.utils.timer import CallLater
from ....core._types._typing import ArgsDict, FTuple2, UiPathOrNyControl, ItemDict
from ....core._types._checker import args_type_check
from .control import NyControl, InteractableControl
from .image import NyImage
from .label import NyLabel
from ..screen_node import ScreenNodeExtension
from ....utils.enum import ButtonCallbackType


__BtnCallbackType = Callable[[dict], Any]


def _vibrate(t: int) -> bool: ...


class NyButton(InteractableControl, NyControl):
    DEFAULT_IMG_PATH: ClassVar[str]
    """
    按钮默认图片控件相对路径。
    """
    HOVER_IMG_PATH: ClassVar[str]
    """
    按钮悬浮图片控件相对路径。
    """
    PRESSED_IMG_PATH: ClassVar[str]
    """
    按钮按下图片控件相对路径。
    """
    BTN_LABEL_PATH: ClassVar[str]
    """
    按钮文本控件相对路径。
    """
    _vibrate_time: int
    _callbacks: Dict[str, List[__BtnCallbackType]]
    _callback_flag: List[str]
    _callback_api_map: Dict[str, MethodType]
    _callback_func_map: Dict[str, MethodType]
    _double_click_time: float
    _long_click_timer: Optional[CallLater]
    _movable_controls: List[NyControl]
    _finger_pos: Optional[FTuple2]
    _base_control: ButtonUIControl
    is_movable: ItemDict
    """
    按钮是否可拖动。
    """
    auto_save_pos: bool
    """
    是否自动保存按钮位置。
    """
    has_long_clicked: bool
    """
    按钮最近一次的按下中是否触发了长按。
    """
    touch_event_params: Optional[dict]
    """
    按钮TouchEvent参数。
    """
    default_img: Optional[NyImage]
    """
    按钮默认（default）图片控件的 ``NyImage`` 实例。
    """
    hover_img: Optional[NyImage]
    """
    按钮悬浮（hover）图片控件的 ``NyImage`` 实例。
    """
    pressed_img: Optional[NyImage]
    """
    按钮按下（pressed）图片控件的 ``NyImage`` 实例。
    """
    btn_label: Optional[NyLabel]
    """
    按钮文本控件的 ``NyLabel`` 实例。
    """
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        btn_control: ButtonUIControl,
        /,
        *,
        touch_event_params: Optional[dict] = None,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def vibrate_time(self) -> int: ...
    @vibrate_time.setter
    @args_type_check(int, is_method=True)
    def vibrate_time(self, val: int) -> None: ...
    def set_default_texture(self, tex_path: str) -> None: ...
    def set_hover_texture(self, tex_path: str) -> None: ...
    def set_pressed_texture(self, tex_path: str) -> None: ...
    def set_text(self, text: str) -> None: ...
    SetDefaultTexture = set_default_texture
    SetHoverTexture = set_hover_texture
    SetPressedTexture = set_pressed_texture
    SetText = set_text
    def set_callback(self, func: __BtnCallbackType, cb_type: str = ButtonCallbackType.UP) -> bool: ...
    def remove_callback(self, func: __BtnCallbackType, cb_type: str = ButtonCallbackType.UP) -> bool: ...
    def _register_long_click_callback(self, _) -> None: ...
    def _register_double_click_callback(self, _) -> None: ...
    def _on_up(self, *args: Any) -> None: ...
    def _on_down(self, *args: Any) -> None: ...
    def _on_cancel(self, *args: Any) -> None: ...
    def _on_move(self, *args: Any) -> None: ...
    def _on_move_in(self, *args: Any) -> None: ...
    def _on_move_out(self, *args: Any) -> None: ...
    def _on_double_click(self, *args: Any) -> None: ...
    def _on_long_click(self, *args: Any) -> None: ...
    def _on_hover_in(self, *args: Any) -> None: ...
    def _on_hover_out(self, *args: Any) -> None: ...
    def _on_screen_exit(self, *args: Any) -> None: ...
    def _on_touch_up_dc(self, args: ArgsDict) -> None: ...
    def _on_touch_down_lc(self, args: ArgsDict) -> None: ...
    def _cancel_long_click(self, args: ArgsDict) -> None: ...
    SetCallback = set_callback
    RemoveCallback = remove_callback
    def set_movable(
        self,
        move_parent: bool = False,
        associated_uis: Union[UiPathOrNyControl, List[UiPathOrNyControl], None] = None,
        auto_save: bool = False,
    ) -> None: ...
    def set_movable_by_long_click(
        self,
        move_parent: bool = False,
        associated_uis: Union[UiPathOrNyControl, List[UiPathOrNyControl], None] = None,
        auto_save: bool = False,
    ) -> None: ...
    def cancel_movable(self) -> None: ...
    def _set_movable_data(
        self,
        movable: bool,
        move_parent: bool = False,
        associated_uis: Union[UiPathOrNyControl, List[UiPathOrNyControl], None] = None,
        auto_save: bool = False,
    ) -> None: ...
    def _OnClickScreen(self, args: ArgsDict) -> None: ...
    def _on_move_mov(self, args: ArgsDict) -> None: ...
    def _on_long_click_mov(self, args: ArgsDict) -> None: ...
    def _on_touch_down_mov(self, args: ArgsDict) -> None: ...
    def clear_pos_data(self) -> bool: ...
    def save_pos_data(self) -> bool: ...
    SetMovable = set_movable
    SetMovableByLongClick = set_movable_by_long_click
    CancelMovable = cancel_movable
    ClearPosData = clear_pos_data
    SavePosData = save_pos_data
    AddTouchEventParams = ButtonUIControl.AddTouchEventParams
    AddHoverEventParams = ButtonUIControl.AddHoverEventParams
    SetButtonTouchDownCallback = ButtonUIControl.SetButtonTouchDownCallback
    SetButtonHoverInCallback = ButtonUIControl.SetButtonHoverInCallback
    SetButtonHoverOutCallback = ButtonUIControl.SetButtonHoverOutCallback
    SetButtonTouchUpCallback = ButtonUIControl.SetButtonTouchUpCallback
    SetButtonTouchCancelCallback = ButtonUIControl.SetButtonTouchCancelCallback
    SetButtonTouchMoveCallback = ButtonUIControl.SetButtonTouchMoveCallback
    SetButtonTouchMoveInCallback = ButtonUIControl.SetButtonTouchMoveInCallback
    SetButtonTouchMoveOutCallback = ButtonUIControl.SetButtonTouchMoveOutCallback
    SetButtonScreenExitCallback = ButtonUIControl.SetButtonScreenExitCallback
