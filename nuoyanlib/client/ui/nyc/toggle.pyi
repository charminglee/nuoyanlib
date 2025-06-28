# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-22
|
| ==============================================
"""


from typing import Optional
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._utils import args_type_check


class NyToggle(NyControl):
    base_control: SwitchToggleUIControl
    """
    | 开关 ``SwitchToggleUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        toggle_control: SwitchToggleUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3

