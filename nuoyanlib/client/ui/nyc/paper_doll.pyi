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


from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyPaperDoll(NyControl):
    base_control: NeteasePaperDollUIControl
    """
    | 纸娃娃 ``NeteasePaperDollUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        paper_doll_control: NeteasePaperDollUIControl,
    ) -> None: ...

