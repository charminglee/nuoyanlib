# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-26
|
| ==============================================
"""


from typing import Optional, Callable, Any, List, TypedDict
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check


class __ToggleCallbackArgs(TypedDict):
    state: bool
__ToggleChangedCallback = Callable[[__ToggleCallbackArgs], Any]


class NyToggle(NyControl):
    _changed_cbs: List[__ToggleChangedCallback]
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
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    def set_callback(self, func: __ToggleChangedCallback) -> bool: ...
    def remove_callback(self, func: __ToggleChangedCallback) -> bool: ...
    @property
    def state(self) -> bool: ...
    @state.setter
    def state(self, val: bool) -> None: ...

    def SetToggleState(self, is_on: bool, toggle_path: str = "/this_toggle") -> None:
        """
        | 设置Toggle开关控件的值。

        -----

        :param bool is_on: 开关状态
        :param str toggle_path: 实际toggle控件相对路径，由UI编辑器生成的开关控件该参数即为默认值"/this_toggle"

        :return: 无
        :rtype: None
        """
    def GetToggleState(self, toggle_path: str = "/this_toggle") -> bool:
        """
        | 获取Toggle开关控件的状态。

        -----

        :param str toggle_path: 实际toggle控件相对路径，由UI编辑器生成的开关控件该参数即为默认值"/this_toggle"

        :return: 开关状态
        :rtype: bool
        """
