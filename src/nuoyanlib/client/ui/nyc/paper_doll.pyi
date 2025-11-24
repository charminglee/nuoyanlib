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


from typing import Optional
from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ....core._types._checker import args_type_check


class NyPaperDoll(NyControl):
    _base_control: NeteasePaperDollUIControl
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        paper_doll_control: NeteasePaperDollUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    @property
    def model_id(self) -> int: ...
    GetModelId = NeteasePaperDollUIControl.GetModelId
    RenderEntity = NeteasePaperDollUIControl.RenderEntity
    RenderSkeletonModel = NeteasePaperDollUIControl.RenderSkeletonModel
    RenderBlockGeometryModel = NeteasePaperDollUIControl.RenderBlockGeometryModel
