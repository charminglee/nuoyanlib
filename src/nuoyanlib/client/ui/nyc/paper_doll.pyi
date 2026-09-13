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
from ....core._types._checker import args_type_check
from ....core._types._typing import NyScreenBaseT
from .control import NyControl


class NyPaperDoll(NyControl[NyScreenBaseT]):
    _base_control: NeteasePaperDollUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBaseT,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl[NyScreenBaseT]: ...
    __div__ = __truediv__
    @property
    def model_id(self) -> int: ...
    get_model_id = GetModelId = NeteasePaperDollUIControl.GetModelId
    render_entity = RenderEntity = NeteasePaperDollUIControl.RenderEntity
    render_skeleton_model = RenderSkeletonModel = NeteasePaperDollUIControl.RenderSkeletonModel
    render_block_geometry_model = RenderBlockGeometryModel = NeteasePaperDollUIControl.RenderBlockGeometryModel
