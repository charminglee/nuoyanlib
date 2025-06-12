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


from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyEditBox(NyControl):
    base_control: TextEditBoxUIControl
    """
    | 文本编辑框 ``TextEditBoxUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        edit_box_control: TextEditBoxUIControl,
    ) -> None: ...

