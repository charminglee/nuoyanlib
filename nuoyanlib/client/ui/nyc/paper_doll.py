# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from ..ui_utils import ControlType
from .control import NyControl


__all__ = [
    "NyPaperDoll",
]


class NyPaperDoll(NyControl):
    """
    | 创建 ``NyPaperDoll`` 纸娃娃实例。
    | 兼容ModSDK ``NeteasePaperDollUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 纸娃娃所在UI类的实例
    :param NeteasePaperDollUIControl paper_doll_control: 通过asNeteasePaperDoll()获取的纸娃娃实例
    """

    _CONTROL_TYPE = ControlType.netease_paper_doll

    def __init__(self, screen_node_ex, paper_doll_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, paper_doll_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region API ===================================================================================

    # endregion

    # region property proxy ===================================================================================

    # endregion











