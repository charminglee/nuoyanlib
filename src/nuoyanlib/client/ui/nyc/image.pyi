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


from typing_extensions import Self
from typing import Callable, Optional, Tuple, NoReturn, Literal
from mod.client.ui.controls.imageUIControl import ImageUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check
from ....core._types._typing import FTuple2, FTuple3, Args, Kwargs


__ClipDirection = Literal[
    "fromLeftToRight",
    "fromRightToLeft",
    "fromOutsideToInside",
    "fromTopToBottom",
    "fromBottomToTop",
]
__ImageAdaption = Literal[
    "normal",
    "filled",
    "oldNineSlice",
    "originNineSlice",
]


class NyImage(NyControl):
    _base_control: ImageUIControl
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        image_control: ImageUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def texture(self) -> NoReturn: ...
    @texture.setter
    def texture(self, val: str) -> None: ...
    @property
    def color(self) -> NoReturn: ...
    @color.setter
    def color(self, val: FTuple3) -> None: ...
    @property
    def uv(self) -> NoReturn: ...
    @uv.setter
    def uv(self, val: FTuple2) -> None: ...
    @property
    def uv_size(self) -> NoReturn: ...
    @uv_size.setter
    def uv_size(self, val: FTuple2) -> None: ...
    @property
    def clip_ratio(self) -> NoReturn: ...
    @clip_ratio.setter
    def clip_ratio(self, val: float) -> None: ...
    @property
    def clip_direction(self) -> __ClipDirection: ...
    @clip_direction.setter
    def clip_direction(self, val: __ClipDirection) -> None: ...
    @property
    def rel_rotate_angle(self) -> float: ...
    @rel_rotate_angle.setter
    def rel_rotate_angle(self, val: float) -> None: ...
    @property
    def global_rotate_angle(self) -> float: ...
    @global_rotate_angle.setter
    def global_rotate_angle(self, val: float) -> None: ...
    @property
    def rel_rotate_point(self) -> FTuple2: ...
    @rel_rotate_point.setter
    def rel_rotate_point(self, val: FTuple2) -> None: ...
    @property
    def global_rotate_point(self) -> FTuple2: ...
    @global_rotate_point.setter
    def global_rotate_point(self, val: FTuple2) -> None: ...
    @property
    def rect(self) -> Tuple[FTuple2, FTuple2, FTuple2, FTuple2]: ...
    @property
    def rect_left_top(self) -> FTuple2: ...
    @property
    def rect_right_top(self) -> FTuple2: ...
    @property
    def rect_left_bottom(self) -> FTuple2: ...
    @property
    def rect_right_bottom(self) -> FTuple2: ...
    def play_frame_anim(
        self,
        tex_path: str,
        frame_count: int,
        frame_rate: int,
        stop_frame: int = -1,
        loop: bool = False,
        callback: Optional[Callable] = None,
        args: Optional[Args] = None,
        kwargs: Optional[Kwargs] = None,
    ) -> None: ...
    def pause_frame_anim(self) -> None: ...
    def stop_frame_anim(self) -> None: ...
    PlayFrameAnim = play_frame_anim
    PauseFrameAnim = pause_frame_anim
    StopFrameAnim = stop_frame_anim
    SetSprite = ImageUIControl.SetSprite
    SetSpriteColor = ImageUIControl.SetSpriteColor
    SetSpriteGray = ImageUIControl.SetSpriteGray
    SetSpriteUV = ImageUIControl.SetSpriteUV
    SetSpriteUVSize = ImageUIControl.SetSpriteUVSize
    SetSpriteClipRatio = ImageUIControl.SetSpriteClipRatio
    SetSpritePlatformHead = ImageUIControl.SetSpritePlatformHead
    SetSpritePlatformFrame = ImageUIControl.SetSpritePlatformFrame
    SetClipDirection = ImageUIControl.SetClipDirection
    GetClipDirection = ImageUIControl.GetClipDirection
    SetImageAdaptionType = ImageUIControl.SetImageAdaptionType
    Rotate = ImageUIControl.Rotate
    RotateAround = ImageUIControl.RotateAround
    SetRotatePivot = ImageUIControl.SetRotatePivot
    GetRotatePivot = ImageUIControl.GetRotatePivot
    GetRotateAngle = ImageUIControl.GetRotateAngle
    GetGlobalRotateAngle = ImageUIControl.GetGlobalRotateAngle
    GetGlobalRotatePoint = ImageUIControl.GetGlobalRotatePoint
    GetRotateRect = ImageUIControl.GetRotateRect
