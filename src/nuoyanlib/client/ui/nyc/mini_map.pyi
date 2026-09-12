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


from typing import NoReturn
from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check


class NyMiniMap(NyControl):
    _base_control: MiniMapUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def highest_y(self) -> NoReturn: ...
    @highest_y.setter
    def highest_y(self, val: int) -> None: ...
    zoom_in = ZoomIn = MiniMapUIControl.ZoomIn
    zoom_out = ZoomOut = MiniMapUIControl.ZoomOut
    zoom_reset = ZoomReset = MiniMapUIControl.ZoomReset
    set_highest_y = SetHighestY = MiniMapUIControl.SetHighestY
    add_entity_marker = AddEntityMarker = MiniMapUIControl.AddEntityMarker
    add_entity_text_marker = AddEntityTextMarker = MiniMapUIControl.AddEntityTextMarker
    add_static_marker = AddStaticMarker = MiniMapUIControl.AddStaticMarker
    add_static_text_marker = AddStaticTextMarker = MiniMapUIControl.AddStaticTextMarker
    remove_entity_marker = RemoveEntityMarker = MiniMapUIControl.RemoveEntityMarker
    remove_entity_text_marker = RemoveEntityTextMarker = MiniMapUIControl.RemoveEntityTextMarker
    remove_static_marker = RemoveStaticMarker = MiniMapUIControl.RemoveStaticMarker
    remove_static_text_marker = RemoveStaticTextMarker = MiniMapUIControl.RemoveStaticTextMarker
    repaint_mini_map = RepaintMiniMap = MiniMapUIControl.RepaintMiniMap
