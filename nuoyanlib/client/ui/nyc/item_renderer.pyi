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


from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyItemRenderer(NyControl):
    base_control: ItemRendererUIControl
    """
    | 物品渲染器 ``ItemRendererUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        item_renderer_control: ItemRendererUIControl,
    ) -> None: ...

