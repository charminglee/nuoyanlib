# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


from typing import Callable, Optional, Tuple, NoReturn, Literal
from mod.client.ui.controls.imageUIControl import ImageUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
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
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
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
    def gray(self) -> NoReturn: ...
    @gray.setter
    def gray(self, val: bool) -> None: ...
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
    set_sprite = SetSprite = ImageUIControl.SetSprite
    set_sprite_color = SetSpriteColor = ImageUIControl.SetSpriteColor
    set_sprite_gray = SetSpriteGray = ImageUIControl.SetSpriteGray
    set_sprite_uv = SetSpriteUV = ImageUIControl.SetSpriteUV
    set_sprite_uvsize = SetSpriteUVSize = ImageUIControl.SetSpriteUVSize
    set_sprite_clip_ratio = SetSpriteClipRatio = ImageUIControl.SetSpriteClipRatio
    set_sprite_platform_head = SetSpritePlatformHead = ImageUIControl.SetSpritePlatformHead
    set_sprite_platform_frame = SetSpritePlatformFrame = ImageUIControl.SetSpritePlatformFrame
    set_clip_direction = SetClipDirection = ImageUIControl.SetClipDirection
    get_clip_direction = GetClipDirection = ImageUIControl.GetClipDirection
    set_image_adaption_type = SetImageAdaptionType = ImageUIControl.SetImageAdaptionType
    rotate = Rotate = ImageUIControl.Rotate
    rotate_around = RotateAround = ImageUIControl.RotateAround
    set_rotate_pivot = SetRotatePivot = ImageUIControl.SetRotatePivot
    get_rotate_pivot = GetRotatePivot = ImageUIControl.GetRotatePivot
    get_rotate_angle = GetRotateAngle = ImageUIControl.GetRotateAngle
    get_global_rotate_angle = GetGlobalRotateAngle = ImageUIControl.GetGlobalRotateAngle
    get_global_rotate_point = GetGlobalRotatePoint = ImageUIControl.GetGlobalRotatePoint
    get_rotate_rect = GetRotateRect = ImageUIControl.GetRotateRect
