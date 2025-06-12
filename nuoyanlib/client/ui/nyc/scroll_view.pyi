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


from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyScrollView(NyControl):
    base_control: ScrollViewUIControl
    """
    | 滚动视图 ``ScrollViewUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        scroll_view_control: ScrollViewUIControl,
    ) -> None: ...

