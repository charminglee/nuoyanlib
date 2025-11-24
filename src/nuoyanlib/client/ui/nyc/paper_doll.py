# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyPaperDoll",
]


class NyPaperDoll(NyControl):
    """
    纸娃娃控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 纸娃娃所在UI类的实例（需继承ScreenNodeExtension）
    :param NeteasePaperDollUIControl paper_doll_control: 通过asNeteasePaperDoll()等方式获取的NeteasePaperDollUIControl实例
    """

    CONTROL_TYPE = ControlType.NETEASE_PAPER_DOLL

    def __init__(self, screen_node_ex, paper_doll_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, paper_doll_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

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











