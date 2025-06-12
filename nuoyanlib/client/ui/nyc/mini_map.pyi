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


from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyMiniMap(NyControl):
    base_control: MiniMapUIControl
    """
    | 小地图 ``MiniMapUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        mini_map_control: MiniMapUIControl,
    ) -> None: ...

