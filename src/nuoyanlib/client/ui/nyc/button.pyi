# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-11
#  ⠀
#  ================================================


from typing import Callable, ClassVar, Optional, Union, List, Any
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.common.utils.timer import CallLater
from ....core._types._typing import ArgsDict, FTuple2, UiPathOrNyControl
from ....core._types._checker import args_type_check
from ....core._utils import cached_property
from .control import NyControl, InteractableControl
from .image import NyImage
from .label import NyLabel
from ..screen_node import NyScreenBase


__BtnCallbackType = Callable[[dict], Any]


def _vibrate(t: int) -> bool: ...


class NyButton(InteractableControl, NyControl):
    UP: ClassVar[int]
    """ 触控在按钮范围内抬起。 """
    DOWN: ClassVar[int]
    """ 按钮按下。 """
    CANCEL: ClassVar[int]
    """ 触控在按钮范围外抬起。 """
    MOVE: ClassVar[int]
    """ 按下后触控移动。 """
    MOVE_IN: ClassVar[int]
    """ 按下按钮后触控进入按钮。 """
    MOVE_OUT: ClassVar[int]
    """ 按下按钮后触控退出按钮。 """
    DOUBLE_CLICK: ClassVar[int]
    """ 双击按钮。 """
    LONG_CLICK: ClassVar[int]
    """ 长按按钮。 """
    HOVER_IN: ClassVar[int]
    """ 鼠标进入按钮。 """
    HOVER_OUT: ClassVar[int]
    """ 鼠标退出按钮。 """
    SCREEN_EXIT: ClassVar[int]
    """ 按钮所在画布退出，且鼠标仍未抬起时触发。 """
    DEFAULT_IMAGE_PATH: ClassVar[str]
    """ 按钮默认图片控件相对路径。 """
    HOVER_IMAGE_PATH: ClassVar[str]
    """ 按钮悬浮图片控件的相对路径。 """
    PRESSED_IMAGE_PATH: ClassVar[str]
    """ 按钮按下图片控件的相对路径。 """
    BUTTON_LABEL_PATH: ClassVar[str]
    """ 按钮文本控件的相对路径。 """
    _base_control: ButtonUIControl
    _vibrate_time: int
    _double_click_time: float
    _long_click_timer: Optional[CallLater]
    _movable_controls: List[NyControl]
    _finger_pos: Optional[FTuple2]
    is_movable: bool
    """ 按钮是否可拖动。 """
    auto_save_pos: bool
    """ 是否自动保存按钮位置。 """
    has_long_clicked: bool
    """ 按钮最近一次的按下中是否触发了长按。 """
    touch_event_params: Optional[dict]
    """ 创建按钮时传入的 TouchEvent 参数。 """
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
        *,
        touch_event_params: Optional[dict] = None,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @cached_property
    def default_image(self) -> Optional[NyImage]: ...
    @cached_property
    def hover_image(self) -> Optional[NyImage]: ...
    @cached_property
    def pressed_image(self) -> Optional[NyImage]: ...
    @cached_property
    def button_label(self) -> Optional[NyLabel]: ...
    @property
    def vibrate_time(self) -> int: ...
    @vibrate_time.setter
    def vibrate_time(self, val: int) -> None: ...
    def set_default_texture(self, tex_path: str) -> None: ...
    def set_hover_texture(self, tex_path: str) -> None: ...
    def set_pressed_texture(self, tex_path: str) -> None: ...
    def set_text(self, text: str) -> None: ...
    def set_callback(self, func: __BtnCallbackType, *cb_types: int) -> None: ...
    def remove_callback(self, func: __BtnCallbackType, *cb_types: int) -> None: ...
    def _register_long_click_callback(self) -> None: ...
    def _register_double_click_callback(self) -> None: ...
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
    def set_movable(
        self,
        move_parent: bool = False,
        associated: Union[UiPathOrNyControl, List[UiPathOrNyControl], None] = None,
        auto_save: bool = False,
    ) -> None: ...
    def cancel_movable(self) -> None: ...
    def _on_move_mov(self, args: ArgsDict) -> None: ...
    def _on_long_click_mov(self, args: ArgsDict) -> None: ...
    def _on_touch_down_mov(self, args: ArgsDict) -> None: ...
    def clear_pos_data(self, with_associated: bool = True) -> bool: ...
    def save_pos(self, with_associated: bool = True) -> bool: ...
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
