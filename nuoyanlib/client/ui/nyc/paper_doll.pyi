# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-22
|
| ==============================================
"""


from typing import Optional
from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check


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
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3

