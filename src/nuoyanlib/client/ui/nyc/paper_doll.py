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


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyPaperDoll",
]


class NyPaperDoll(NyControl):
    """
    纸娃娃控件类。

    示例
    ----

    >>> self.paper_doll = nyl.NyPaperDoll(self, "/panel/paper_doll")

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该纸娃娃控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.NETEASE_PAPER_DOLL

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def model_id(self):
        """
        [只读属性]

        渲染的骨骼模型ID。

        :rtype: int
        """
        return self._base_control.GetModelId()

    # endregion

    # region Compatibility =============================================================================================

    get_model_id                = GetModelId               = lambda s, *a, **k: s._base_control.GetModelId(*a, **k)
    render_entity               = RenderEntity             = lambda s, *a, **k: s._base_control.RenderEntity(*a, **k)
    render_skeleton_model       = RenderSkeletonModel      = lambda s, *a, **k: s._base_control.RenderSkeletonModel(*a, **k)
    render_block_geometry_model = RenderBlockGeometryModel = lambda s, *a, **k: s._base_control.RenderBlockGeometryModel(*a, **k)

    # endregion





