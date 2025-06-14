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


from mod.client.ui.controls.inputPanelUIControl import InputPanelUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyInputPanel(NyControl):
    base_control: InputPanelUIControl
    """
    | 输入面板 ``InputPanelUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        input_panel_control: InputPanelUIControl,
    ) -> None: ...

