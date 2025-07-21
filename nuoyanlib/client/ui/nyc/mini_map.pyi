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


from typing import Optional
from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check


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
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3

