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

    # region API ===================================================================================

    # endregion

    # region property proxy ===================================================================================

    # endregion











