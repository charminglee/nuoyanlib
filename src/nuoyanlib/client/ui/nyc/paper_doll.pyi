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


from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check


class NyPaperDoll(NyControl):
    _base_control: NeteasePaperDollUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def model_id(self) -> int: ...
    get_model_id = GetModelId = NeteasePaperDollUIControl.GetModelId
    render_entity = RenderEntity = NeteasePaperDollUIControl.RenderEntity
    render_skeleton_model = RenderSkeletonModel = NeteasePaperDollUIControl.RenderSkeletonModel
    render_block_geometry_model = RenderBlockGeometryModel = NeteasePaperDollUIControl.RenderBlockGeometryModel
