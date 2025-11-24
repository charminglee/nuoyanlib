# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-30
|
| ====================================================
"""


from typing import Optional, NoReturn
from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check


class NyMiniMap(NyControl):
    _base_control: MiniMapUIControl
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        mini_map_control: MiniMapUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def highest_y(self) -> NoReturn: ...
    @highest_y.setter
    def highest_y(self, val: int) -> None: ...
    ZoomIn = MiniMapUIControl.ZoomIn
    ZoomOut = MiniMapUIControl.ZoomOut
    ZoomReset = MiniMapUIControl.ZoomReset
    SetHighestY = MiniMapUIControl.SetHighestY
    AddEntityMarker = MiniMapUIControl.AddEntityMarker
    AddEntityTextMarker = MiniMapUIControl.AddEntityTextMarker
    AddStaticMarker = MiniMapUIControl.AddStaticMarker
    AddStaticTextMarker = MiniMapUIControl.AddStaticTextMarker
    RemoveEntityMarker = MiniMapUIControl.RemoveEntityMarker
    RemoveEntityTextMarker = MiniMapUIControl.RemoveEntityTextMarker
    RemoveStaticMarker = MiniMapUIControl.RemoveStaticMarker
    RemoveStaticTextMarker = MiniMapUIControl.RemoveStaticTextMarker
    RepaintMiniMap = MiniMapUIControl.RepaintMiniMap
