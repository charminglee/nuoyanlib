# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-11
|
| ==============================================
"""


from ...._core._utils import args_type_check
from ...._core import _error
from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyImage",
]


class NyImage(NyControl):
    """
    | 创建 ``NyImage`` 图片实例。
    | 兼容ModSDK ``ImageUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 图片所在UI类的实例
    :param ImageUIControl image_control: 通过asImage()获取的图片实例
    """

    _CONTROL_TYPE = ControlType.image

    def __init__(self, screen_node_ex, image_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, image_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API =======================================================================================================

    @args_type_check(str, int, int, int, bool, is_method=True)
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
        | 播放由多张图片组成的序列帧动画。

        -----

        :param str tex_path: 序列帧贴图路径，请使用%d作为数字占位符，该接口将会按顺序播放 tex_path % 0 到 tex_path % (frame_count - 1) 的贴图
        :param int frame_count: 帧数（一共有多少帧）
        :param int frame_rate: 帧率（每秒播放多少帧）
        :param int stop_frame: 播放结束后停留在哪一帧，仅loop参数设为False时有效；0为第一帧，-1为最后一帧，-2为倒数第二帧，以此类推；默认为-1
        :param bool loop: 是否循环播放，默认为False
        :param function|None callback: 播放结束后触发的回调函数，仅loop参数设为False时有效；默认为None
        :param tuple|None args: 回调函数位置参数元组；默认为None
        :param dict[str,Any]|None kwargs: 回调函数关键字参数字典；默认为None

        :return: 无
        :rtype: None
        """
        if tex_path.count("%d") != 1:
            raise ValueError("'tex_path' must contain exactly one '%d' placeholder")
        if frame_count <= 0:
            raise ValueError("'frame_count' must be greater than 0")
        if frame_rate <= 0:
            raise ValueError("'frame_rate' must be greater than 0")
        if not (-frame_count <= stop_frame < frame_count):
            raise ValueError("'stop_frame' must satisfy: -'frame_count' <= 'stop_frame' < 'frame_count'")
        self.ui_node._play_frame_anim(
            self, tex_path, frame_count, frame_rate, stop_frame, loop, callback, args, kwargs
        )

    def pause_frame_anim(self):
        """
        | 暂停当前正在播放的序列帧动画。

        -----

        :return: 无
        :rtype: None
        """
        self.ui_node._pause_frame_anim(self)

    def stop_frame_anim(self):
        """
        | 停止当前正在播放的序列帧动画。

        -----

        :return: 无
        :rtype: None
        """
        self.ui_node._stop_frame_anim(self)

    # endregion

    # region property proxy ============================================================================================

    @property
    def texture(self):
        """
        [只写属性]

        | 贴图路径。

        :rtype: None
        """
        raise _error.GetPropertyError("texture")

    @texture.setter
    def texture(self, val):
        """
        [只写属性]

        | 贴图路径。

        :type val: str
        """
        self.base_control.SetSprite(val)

    @property
    def color(self):
        """
        [只写属性]

        | 图片颜色rgb，取值[0, 1]。

        :rtype: None
        """
        raise _error.GetPropertyError("color")

    @color.setter
    def color(self, val):
        """
        [只写属性]

        | 图片颜色rgb，取值[0, 1]。

        :type val: tuple[float,float,float]
        """
        self.base_control.SetSpriteColor(tuple(val))

    @property
    def uv(self):
        """
        [只写属性]

        | 图片的起始uv，与json中的 ``"uv"`` 属性作用一致。

        :rtype: None
        """
        raise _error.GetPropertyError("uv")

    @uv.setter
    def uv(self, val):
        """
        [只写属性]

        | 图片的起始uv，与json中的 ``"uv"`` 属性作用一致。

        :type val: tuple[float,float]
        """
        self.base_control.SetSpriteUV(tuple(val))

    @property
    def uv_size(self):
        """
        [只写属性]

        | 图片的uv大小，与json中的 ``"uv_size"`` 属性作用一致。

        :rtype: None
        """
        raise _error.GetPropertyError("uv_size")

    @uv_size.setter
    def uv_size(self, val):
        """
        [只写属性]

        | 图片的uv大小，与json中的 ``"uv_size"`` 属性作用一致。

        :type val: tuple[float,float]
        """
        self.base_control.SetSpriteUVSize(tuple(val))

    @property
    def clip_ratio(self):
        """
        [只写属性]

        | 图片的裁剪区域比例（不改变控件尺寸）。

        :rtype: None
        """
        raise _error.GetPropertyError("clip_ratio")

    @clip_ratio.setter
    def clip_ratio(self, val):
        """
        [只写属性]

        | 图片的裁剪区域比例（不改变控件尺寸）。

        :type val: float
        """
        self.base_control.SetSpriteClipRatio(val)

    @property
    def clip_direction(self):
        """
        [可读写属性]

        | 图片控件的裁剪方向。
        | 可选值：
        - ``"fromLeftToRight"`` -- 从左到右
        - ``"fromRightToLeft"`` -- 从右到左
        - ``"fromOutsideToInside"`` -- 从外到内
        - ``"fromTopToBottom"`` -- 从上到下
        - ``"fromBottomToTop"`` -- 从下到上

        :rtype: str
        """
        return self.base_control.GetClipDirection()

    @clip_direction.setter
    def clip_direction(self, val):
        """
        [可读写属性]

        | 图片控件的裁剪方向。
        | 可选值：
        - ``"fromLeftToRight"`` -- 从左到右
        - ``"fromRightToLeft"`` -- 从右到左
        - ``"fromOutsideToInside"`` -- 从外到内
        - ``"fromTopToBottom"`` -- 从上到下
        - ``"fromBottomToTop"`` -- 从下到上

        :type val: str
        """
        self.base_control.SetClipDirection(val)

    @property
    def rel_rotate_angle(self):
        """
        [可读写属性]

        | 图片控件相对自身的旋转锚点的旋转角度。

        :rtype: float
        """
        return self.base_control.GetRotateAngle()

    @rel_rotate_angle.setter
    def rel_rotate_angle(self, val):
        """
        [可读写属性]

        | 图片控件相对自身的旋转锚点的旋转角度。

        :type val: float
        """
        self.base_control.Rotate(val)

    @property
    def global_rotate_angle(self):
        """
        [可读写属性]

        | 图片控件相对于全局旋转锚点的旋转角度。

        :rtype: float
        """
        return self.base_control.GetGlobalRotateAngle()

    @global_rotate_angle.setter
    def global_rotate_angle(self, val):
        """
        [可读写属性]

        | 图片控件相对于全局旋转锚点的旋转角度。

        :type val: float
        """
        self.base_control.RotateAround(self.global_rotate_point, val)

    @property
    def rel_rotate_point(self):
        """
        [可读写属性]

        | 图片控件相对自身的旋转锚点。
        | 自身的旋转锚点是一个相对坐标，它是根据图片当前所在位置和大小进行计算的，所以一旦设置后，就会每帧都进行位置的计算。如果不调用该函数，默认状态下图片的旋转锚点是 ``(0.5,0.5)`` 。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetRotatePivot()

    @rel_rotate_point.setter
    def rel_rotate_point(self, val):
        """
        [可读写属性]

        | 图片控件相对自身的旋转锚点。
        | 自身的旋转锚点是一个相对坐标，它是根据图片当前所在位置和大小进行计算的，所以一旦设置后，就会每帧都进行位置的计算。如果不调用该函数，默认状态下图片的旋转锚点是 ``(0.5,0.5)`` 。

        :type val: tuple[float,float]
        """
        self.base_control.SetRotatePivot(tuple(val))

    @property
    def global_rotate_point(self):
        """
        [可读写属性]

        | 图片控件在全局坐标系中的旋转锚点。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetGlobalRotatePoint()

    @global_rotate_point.setter
    def global_rotate_point(self, val):
        """
        [可读写属性]

        | 图片控件在全局坐标系中的旋转锚点。

        :type val: tuple[float,float]
        """
        self.base_control.RotateAround(tuple(val), self.global_rotate_angle)

    @property
    def rect(self):
        """
        [只读属性]

        | 图片四个边角点坐标，分别为左上、右上、右下、左下。

        :rtype: tuple[tuple[float,float],tuple[float,float],tuple[float,float],tuple[float,float]]
        """
        return self.base_control.GetRotateRect()

    @property
    def rect_left_top(self):
        """
        [只读属性]

        | 图片左上边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetRotateRect()[0]

    @property
    def rect_right_top(self):
        """
        [只读属性]

        | 图片右上边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetRotateRect()[1]

    @property
    def rect_left_bottom(self):
        """
        [只读属性]

        | 图片左下边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetRotateRect()[3]

    @property
    def rect_right_bottom(self):
        """
        [只读属性]

        | 图片右下边角点坐标。

        :rtype: tuple[float,float]
        """
        return self.base_control.GetRotateRect()[2]

    # endregion











