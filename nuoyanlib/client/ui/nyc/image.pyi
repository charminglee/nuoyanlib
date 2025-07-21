# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-22
|
| ==============================================
"""


from typing import Callable, Optional, Tuple, NoReturn
from mod.client.ui.controls.imageUIControl import ImageUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check
from ...._core._types._typing import FTuple2, FTuple3, FTuple4, ClipDirectionType, ImageAdaptionType, Args, Kwargs


class NyImage(NyControl):
    base_control: ImageUIControl
    """
    | 图片 ``ImageUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        image_control: ImageUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3
    @args_type_check(str, int, int, int, bool, is_method=True)
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
    def clip_direction(self) -> ClipDirectionType: ...
    @clip_direction.setter
    def clip_direction(self, val: ClipDirectionType) -> None: ...
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

    def SetSprite(self, texture_path: str) -> None:
        """
        | 给图片控件换指定贴图。

        -----

        :param str texture_path: 贴图路径

        :return: 无
        :rtype: None
        """
    def SetSpriteColor(self, color: FTuple3) -> None:
        """
        | 设置图片颜色。

        -----
        :param tuple[float,float,float] color: 图片颜色rgb，取值[0, 1]

        :return: 无
        :rtype: None
        """
    def SetSpriteGray(self, gray: bool) -> None:
        """
        | 给图片控件置灰，比直接 ``SetSprite`` 一张灰图片效率要高。

        -----

        :param bool gray: 是否置灰

        :return: 无
        :rtype: None
        """
    def SetSpriteUV(self, uv: FTuple2) -> None:
        """
        | 设置图片的起始uv，与json中的 ``"uv"`` 属性作用一致。

        -----

        :param tuple[float,float] uv: 图片的左上角为(0, 0)，向右为x轴，向下为y轴

        :return: 无
        :rtype: None
        """
    def SetSpriteUVSize(self, uv_size: FTuple2) -> None:
        """
        | 设置图片的uv大小，与json中的 ``"uv_size"`` 属性作用一致。

        -----

        :param tuple[float,float] uv_size: uv大小

        :return: 无
        :rtype: None
        """
    def SetSpriteClipRatio(self, clip_ratio: float) -> None:
        """
        | 设置图片的裁剪区域比例（不改变控件尺寸）。可以配合image控件的 ``clip_ratio`` 属性控制方向。

        -----

        :param float clip_ratio: 图片的裁剪比例（范围0到1），裁剪精度与图片分辨率相关

        :return: 无
        :rtype: None
        """
    def SetSpritePlatformHead(self) -> None:
        """
        | 设置图片为我的世界移动端启动器当前帐号的头像。
        | 该接口仅支持移动端调用，其他平台该接口无效。

        -----

        :return: 无
        :rtype: None
        """
    def SetSpritePlatformFrame(self) -> None:
        """
        | 设置图片为我的世界移动端启动器当前帐号的头像框。
        | 该接口仅支持移动端调用，其他平台该接口无效。

        -----

        :return: 无
        :rtype: None
        """
    def SetClipDirection(self, clip_direction: ClipDirectionType) -> bool:
        """
        | 设置图片控件的裁剪方向。
        | 可选值：
        - ``"fromLeftToRight"`` -- 从左到右
        - ``"fromRightToLeft"`` -- 从右到左
        - ``"fromOutsideToInside"`` -- 从外到内
        - ``"fromTopToBottom"`` -- 从上到下
        - ``"fromBottomToTop"`` -- 从下到上

        -----

        :param str clip_direction: 裁剪方向

        :return: 设置是否成功
        :rtype: bool
        """
    def GetClipDirection(self) -> ClipDirectionType:
        """
        | 获取图片控件的裁剪方向。

        -----

        :return: 裁剪方向，详见SetClipDirection接口
        :rtype: str
        """
    def SetImageAdaptionType(
        self,
        image_adaption_type: ImageAdaptionType,
        image_adaption_data: Optional[FTuple4] = None,
    ) -> bool:
        """
        | 设置图片控件的图片适配方式以及信息。
        | ``image_adaption_type`` 可选的值如下：
        - ``"normal"`` -- 普通适配，不开启九宫并保持宽高比
        - ``"filled"`` -- 填充适配，不开启九宫并保持宽高比
        - ``"oldNineSlice"`` -- 旧版九宫格适配
        - ``"originNineSlice"`` -- 原版九宫格适配

        -----

        :param str image_adaption_type: 图片适配方式
        :param tuple[float,float,float,float]|None image_adaption_data: 如果图片不是九宫适配方式，无需传该值，否则需要设置，tuple的每个值分别代表九宫格切割的四个参数：左，右，上，下

        :return: 设置是否成功
        :rtype: bool
        """
    def Rotate(self, angle: float) -> None:
        """
        | 图片相对自身的旋转锚点进行旋转。

        -----

        :param float angle: 旋转角度

        :return: 无
        :rtype: None
        """
    def RotateAround(self, point: FTuple2, angle: float) -> None:
        """
        | 图片相对全局坐标系中某个固定的点进行旋转。

        -----

        :param tuple[float,float] point: 全局坐标点
        :param float angle: 旋转角度

        :return: 无
        :rtype: None
        """
    def SetRotatePivot(self, pivot: FTuple2) -> None:
        """
        | 设置图片自身旋转锚点，该点并不是固定的点，而是相对于自身位置的点。
        | 自身的旋转锚点是一个相对坐标，它是根据图片当前所在位置和大小进行计算的，所以一旦设置后，就会每帧都进行位置的计算。如果不调用该函数，默认状态下图片的旋转锚点是 ``(0.5,0.5)`` 。

        -----

        :param tuple[float,float] pivot: 相对于自身位置的锚点，第一项为横轴x，第二项为纵轴y，锚点实际坐标=图片的position + anchor * (width, height)

        :return: 无
        :rtype: None
        """
    def GetRotatePivot(self) -> FTuple2:
        """
        | 获取图片相对自身的旋转锚点。

        -----

        :return: 图片相对自身的旋转锚点，第一项为横轴，第二项为纵轴
        :rtype: tuple[float,float]
        """
    def GetRotateAngle(self) -> float:
        """
        | 获取图片相对自身的旋转锚点旋转的角度。

        -----

        :return: 旋转角度
        :rtype: float
        """
    def GetGlobalRotateAngle(self) -> float:
        """
        | 获取图片通过 ``RotateAround`` 函数设置进去的角度值。

        -----

        :return: 角度
        :rtype: float
        """
    def GetGlobalRotatePoint(self) -> FTuple2:
        """
        | 获取图片通过 ``RotateAround`` 函数设置进去的 ``point`` 值。

        -----

        :return: 全局坐标点
        :rtype: tuple[float,float]
        """
    def GetRotateRect(self) -> Tuple[FTuple2, FTuple2, FTuple2, FTuple2]:
        """
        | 获取图片当前的四个边角点。

        -----

        :return: 图片四个边角坐标
        :rtype: tuple[tuple[float,float],tuple[float,float],tuple[float,float],tuple[float,float]]
        """
