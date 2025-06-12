# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-12
|
| ==============================================
"""


from mod.client.ui.controls.labelUIControl import LabelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyLabel(NyControl):
    base_control: LabelUIControl
    """
    | 文本 ``LabelUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        label_control: LabelUIControl,
    ) -> None: ...

