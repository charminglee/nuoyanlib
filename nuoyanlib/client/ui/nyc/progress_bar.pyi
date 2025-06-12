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


from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension


class NyProgressBar(NyControl):
    base_control: ProgressBarUIControl
    """
    | 进度条 ``ProgressBarUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        progress_bar_control: ProgressBarUIControl,
    ) -> None: ...

