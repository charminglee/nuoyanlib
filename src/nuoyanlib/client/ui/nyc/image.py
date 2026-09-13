# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


if bool(0):
    from typing import Any
    from ..screen_node import NyScreenNode, NyScreenProxy


from ....core import error
from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyImage",
]


class NyImage(NyControl):
    """
    图片控件类。

    示例
    ----

    >>> self.image = nyl.NyImage(self, "/panel/image")
    >>> self.image.texture = "textures/ui/my_icon"
    >>> self.image.color = (1.0, 1.0, 1.0)

    参见
    ----

    - ``NyControl.to_image()`` -- 将通用控件实例转换为图片控件实例。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该图片控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.IMAGE

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def texture(self):
        """
        [只写属性]

        图片路径。

        :rtype: None
        """
        raise error.GetPropertyError("texture")

    @texture.setter
    def texture(self, val):
        """
        [只写属性]

        图片路径。

        :type val: str
        """
        self._base_control.SetSprite(val)

    @property
    def color(self):
        """
        [只写属性]

        图片颜色 rgb，取值 [0, 1]。

        :rtype: None
        """
        raise error.GetPropertyError("color")

    @color.setter
    def color(self, val):
        """
        [只写属性]

        图片颜色 rgb，取值 [0, 1]。

        :type val: tuple[float,float,float]
        """
        self._base_control.SetSpriteColor(val)

    @property
    def gray(self):
        """
        [只写属性]

        图片置灰。

        :rtype: None
        """
        raise error.GetPropertyError("gray")

    @gray.setter
    def gray(self, val):
        """
        [只写属性]

        图片置灰。

        :type val: bool
        """
        self._base_control.SetSpriteGray(val)

    @property
    def uv(self):
        """
        [只写属性]

        图片的起始 uv。

        与 json 中的 ``"uv"`` 属性作用一致。

        :rtype: None
        """
        raise error.GetPropertyError("uv")

    @uv.setter
    def uv(self, val):
        """
        [只写属性]

        图片的起始 uv。

        与 json 中的 ``"uv"`` 属性作用一致。

        :type val: tuple[float,float]
        """
        self._base_control.SetSpriteUV(val)

    @property
    def uv_size(self):
        """
        [只写属性]

        图片的 uv 大小。

        与 json 中的 ``"uv_size"`` 属性作用一致。

        :rtype: None
        """
        raise error.GetPropertyError("uv_size")

    @uv_size.setter
    def uv_size(self, val):
        """
        [只写属性]

        图片的 uv 大小。

        与 json 中的 ``"uv_size"`` 属性作用一致。

        :type val: tuple[float,float]
        """
        self._base_control.SetSpriteUVSize(val)

    @property
    def clip_ratio(self):
        """
        [只写属性]

        图片的裁剪区域比例（不改变控件尺寸）。

        :rtype: None
        """
        raise error.GetPropertyError("clip_ratio")

    @clip_ratio.setter
    def clip_ratio(self, val):
        """
        [只写属性]

        图片的裁剪区域比例（不改变控件尺寸）。

        :type val: float
        """
        self._base_control.SetSpriteClipRatio(val)

    @property
    def clip_direction(self):
        """
        [可读写属性]

        图片控件的裁剪方向。

        可选值：

        - ``"fromLeftToRight"`` -- 从左到右
        - ``"fromRightToLeft"`` -- 从右到左
        - ``"fromOutsideToInside"`` -- 从外到内
        - ``"fromTopToBottom"`` -- 从上到下
        - ``"fromBottomToTop"`` -- 从下到上

        :rtype: str
        """
        return self._base_control.GetClipDirection()

    @clip_direction.setter
    def clip_direction(self, val):
        """
        [可读写属性]

        图片控件的裁剪方向。

        可选值：

        - ``"fromLeftToRight"`` -- 从左到右
        - ``"fromRightToLeft"`` -- 从右到左
        - ``"fromOutsideToInside"`` -- 从外到内
        - ``"fromTopToBottom"`` -- 从上到下
        - ``"fromBottomToTop"`` -- 从下到上

        :type val: str
        """
        self._base_control.SetClipDirection(val)

    @property
    def rel_rotate_angle(self):
        """
        [可读写属性]

        图片控件相对自身的旋转锚点的旋转角度。

        :rtype: float
        """
        return self._base_control.GetRotateAngle()

    @rel_rotate_angle.setter
    def rel_rotate_angle(self, val):
        """
        [可读写属性]

        图片控件相对自身的旋转锚点的旋转角度。

        :type val: float
        """
        self._base_control.Rotate(val)

    @property
    def global_rotate_angle(self):
        """
        [可读写属性]

        图片控件相对于全局旋转锚点的旋转角度。

        :rtype: float
        """
        return self._base_control.GetGlobalRotateAngle()

    @global_rotate_angle.setter
    def global_rotate_angle(self, val):
        """
        [可读写属性]

        图片控件相对于全局旋转锚点的旋转角度。

        :type val: float
        """
        self._base_control.RotateAround(self.global_rotate_point, val)

    @property
    def rel_rotate_point(self):
        """
        [可读写属性]

        图片控件相对自身的旋转锚点。

        说明
        ----

        自身的旋转锚点是一个相对坐标，它是根据图片当前所在位置和大小进行计算的，所以一旦设置后，就会每帧都进行位置的计算。
        如果不调用该函数，默认状态下图片的旋转锚点是 ``(0.5,0.5)`` 。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetRotatePivot()

    @rel_rotate_point.setter
    def rel_rotate_point(self, val):
        """
        [可读写属性]

        图片控件相对自身的旋转锚点。

        说明
        ----

        自身的旋转锚点是一个相对坐标，它是根据图片当前所在位置和大小进行计算的，所以一旦设置后，就会每帧都进行位置的计算。
        如果不调用该函数，默认状态下图片的旋转锚点是 ``(0.5,0.5)`` 。

        :type val: tuple[float,float]
        """
        self._base_control.SetRotatePivot(val)

    @property
    def global_rotate_point(self):
        """
        [可读写属性]

        图片控件在全局坐标系中的旋转锚点。

        :rtype: tuple[float,float]
        """
        return self._base_control.GetGlobalRotatePoint()

    @global_rotate_point.setter
    def global_rotate_point(self, val):
        """
        [可读写属性]

        图片控件在全局坐标系中的旋转锚点。

        :type val: tuple[float,float]
        """
        self._base_control.RotateAround(val, self.global_rotate_angle)

    @property
    def rect(self):
        """
        [只读属性]

        图片四个边角点坐标。

        分别为左上、右上、右下、左下。

        :rtype: tuple[tuple[float,float],tuple[float,float],tuple[float,float],tuple[float,float]]
        """
        return self._base_control.GetRotateRect()

    @property
    def rect_left_top(self):
        """
        [只读属性]

        图片左上边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.rect[0]

    @property
    def rect_right_top(self):
        """
        [只读属性]

        图片右上边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.rect[1]

    @property
    def rect_left_bottom(self):
        """
        [只读属性]

        图片左下边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.rect[3]

    @property
    def rect_right_bottom(self):
        """
        [只读属性]

        图片右下边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.rect[2]

    # endregion

    # region Common ====================================================================================================

    def play_frame_anim(
            self,
            tex_path,
            frame_count,
            frame_rate,
            stop_frame=-1,
            loop=False,
            callback=None,
            args=None,
            kwargs=None,
    ):
        """
        播放由多张图片组成的序列帧动画。

        示例
        ----

        >>> self.image.play_frame_anim(
        ...     "textures/ui/skill_%d",
        ...     frame_count=8,
        ...     frame_rate=12,
        ... )

        参见
        ----

        - ``NyImage.pause_frame_anim()`` -- 暂停当前序列帧动画。
        - ``NyImage.stop_frame_anim()`` -- 停止当前序列帧动画。

        -----

        :param str tex_path: 序列帧贴图路径，请使用%d作为数字占位符，该接口将会按顺序播放 tex_path % 0 到 tex_path % (frame_count - 1) 的贴图
        :param int frame_count: 帧数（一共有多少帧）
        :param int frame_rate: 帧率（每秒播放多少帧）
        :param int stop_frame: 播放结束后停留在哪一帧，仅 loop 参数设为 False 时有效；0 为第一帧，1 为第二帧，-1 为最后一帧，以此类推；默认为 -1
        :param bool loop: 是否循环播放；默认为 False
        :param function|None callback: 播放结束后触发的回调函数，仅 loop 参数设为 False 时有效；默认为 None
        :param tuple|None args: 回调函数位置参数元组；默认为 None
        :param dict[str,Any]|None kwargs: 回调函数关键字参数字典；默认为 None

        :return: 无
        :rtype: None

        :raise ValueError: 参数错误
        """
        if tex_path.count("%d") != 1:
            raise ValueError("'tex_path' must contain exactly one '%d' placeholder")
        if frame_count <= 0:
            raise ValueError("'frame_count' must be greater than 0")
        if frame_rate <= 0:
            raise ValueError("'frame_rate' must be greater than 0")
        if not (-frame_count <= stop_frame < frame_count):
            raise ValueError("'stop_frame' must satisfy: -frame_count <= stop_frame < frame_count")
        self.ny_screen_node._play_frame_anim(
            self, tex_path, frame_count, frame_rate, stop_frame, loop, callback, args, kwargs
        )

    def pause_frame_anim(self):
        """
        暂停当前正在播放的序列帧动画。

        -----

        :return: 无
        :rtype: None
        """
        self.ny_screen_node._pause_frame_anim(self)

    def stop_frame_anim(self):
        """
        停止当前正在播放的序列帧动画。

        -----

        :return: 无
        :rtype: None
        """
        self.ny_screen_node._stop_frame_anim(self)

    # endregion

    # region Compatibility =============================================================================================

    set_sprite                = SetSprite              = lambda s, *a, **k: s._base_control.SetSprite(*a, **k)
    set_sprite_color          = SetSpriteColor         = lambda s, *a, **k: s._base_control.SetSpriteColor(*a, **k)
    set_sprite_gray           = SetSpriteGray          = lambda s, *a, **k: s._base_control.SetSpriteGray(*a, **k)
    set_sprite_uv             = SetSpriteUV            = lambda s, *a, **k: s._base_control.SetSpriteUV(*a, **k)
    set_sprite_uvsize         = SetSpriteUVSize        = lambda s, *a, **k: s._base_control.SetSpriteUVSize(*a, **k)
    set_sprite_clip_ratio     = SetSpriteClipRatio     = lambda s, *a, **k: s._base_control.SetSpriteClipRatio(*a, **k)
    set_sprite_platform_head  = SetSpritePlatformHead  = lambda s, *a, **k: s._base_control.SetSpritePlatformHead(*a, **k)
    set_sprite_platform_frame = SetSpritePlatformFrame = lambda s, *a, **k: s._base_control.SetSpritePlatformFrame(*a, **k)
    set_clip_direction        = SetClipDirection       = lambda s, *a, **k: s._base_control.SetClipDirection(*a, **k)
    get_clip_direction        = GetClipDirection       = lambda s, *a, **k: s._base_control.GetClipDirection(*a, **k)
    set_image_adaption_type   = SetImageAdaptionType   = lambda s, *a, **k: s._base_control.SetImageAdaptionType(*a, **k)
    rotate                    = Rotate                 = lambda s, *a, **k: s._base_control.Rotate(*a, **k)
    rotate_around             = RotateAround           = lambda s, *a, **k: s._base_control.RotateAround(*a, **k)
    set_rotate_pivot          = SetRotatePivot         = lambda s, *a, **k: s._base_control.SetRotatePivot(*a, **k)
    get_rotate_pivot          = GetRotatePivot         = lambda s, *a, **k: s._base_control.GetRotatePivot(*a, **k)
    get_rotate_angle          = GetRotateAngle         = lambda s, *a, **k: s._base_control.GetRotateAngle(*a, **k)
    get_global_rotate_angle   = GetGlobalRotateAngle   = lambda s, *a, **k: s._base_control.GetGlobalRotateAngle(*a, **k)
    get_global_rotate_point   = GetGlobalRotatePoint   = lambda s, *a, **k: s._base_control.GetGlobalRotatePoint(*a, **k)
    get_rotate_rect           = GetRotateRect          = lambda s, *a, **k: s._base_control.GetRotateRect(*a, **k)

    # endregion


