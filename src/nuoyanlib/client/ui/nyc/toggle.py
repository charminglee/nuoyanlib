# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


if 0:
    from ..screen_node import ScreenNodeExtension


from ....core.client.comp import ViewBinder
from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyToggle",
]


class NyToggle(NyControl):
    """
    开关控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 开关所在UI类的实例（需继承ScreenNodeExtension）
    :param SwitchToggleUIControl toggle_control: 通过asSwitchToggle()等方式获取的SwitchToggleUIControl实例
    """

    CONTROL_TYPE = ControlType.TOGGLE

    def __init__(self, screen_node_ex, toggle_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, toggle_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def state(self):
        """
        [可读写属性]

        开关状态。

        :rtype: bool
        """
        return self._base_control.GetToggleState()

    @state.setter
    def state(self, val):
        """
        [可读写属性]

        开关状态。

        :type val: bool
        """
        if isinstance(val, int):
            val = bool(val)
        self._base_control.SetToggleState(val)

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func):
        """
        设置开关状态改变时触发的回调函数。

        需要将UI json中开关的 ``"$toggle_name"`` 字段的值设置为 ``"#<namespace>.<func_name>"`` 方可生效，
        ``<namespace>`` 即为UI json中 ``"namespace"`` 对应的值， ``<func_name>`` 为回调函数名。

        -----

        :param function func: 回调函数，参数为一个字典：{'state': bool, 'index': int}

        :return: 是否成功
        :rtype: bool
        """
        return self.ui_node.build_binding(func, ViewBinder.BF_ToggleChanged)

    def remove_callback(self, func):
        """
        移除通过 ``.set_callback()`` 设置的开关回调函数。

        -----

        :param function func: 回调函数

        :return: 是否成功
        :rtype: bool
        """
        return self.ui_node.unbuild_binding(func)

    SetCallback = set_callback
    RemoveCallback = remove_callback

    # endregion










