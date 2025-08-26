# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-27
|
| ==============================================
"""


from ...._core._utils import get_func
from ...._core._client.comp import ScreenNode
from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyToggle",
]


class NyToggle(NyControl):
    """
    | 创建 ``NyToggle`` 开关实例。
    | 兼容ModSDK ``SwitchToggleUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 开关所在UI类的实例（需继承ScreenNodeExtension）
    :param SwitchToggleUIControl toggle_control: 通过asSwitchToggle()等方式获取的SwitchToggleUIControl实例
    """

    __set_callback = staticmethod(get_func(
        ScreenNode,
        (103, 117, 105),
        (114, 101, 103, 105, 115, 116, 101, 114, 95, 116, 111, 103, 103, 108, 101, 95, 99, 104, 97, 110, 103, 101, 100, 95, 104, 97, 110, 100, 108, 101, 114)
    ))
    __remove_callback = staticmethod(get_func(
        ScreenNode,
        (103, 117, 105),
        (117, 110, 114, 101, 103, 105, 115, 116, 101, 114, 95, 116, 111, 103, 103, 108, 101, 95, 99, 104, 97, 110, 103, 101, 100, 95, 104, 97, 110, 100, 108, 101, 114)
    ))
    _CONTROL_TYPE = ControlType.TOGGLE

    def __init__(self, screen_node_ex, toggle_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, toggle_control)
        self._changed_cbs = []

    def __destroy__(self):
        NyControl.__destroy__(self)
        while self._changed_cbs:
            cb = self._changed_cbs.pop()
            self.remove_callback(cb)

    # region API =======================================================================================================

    def set_callback(self, func):
        """
        | 设置开关状态改变时触发的回调函数。
        | 需要将UI json中开关的 ``"$toggle_name"`` 字段的值设置为 ``"#namespace.func_name"`` ，其中，``namespace`` 与UI json中的 ``"namespace"`` 字段相同， ``func_name`` 为回调函数名。

        -----

        :param function func: 回调函数，参数为一个字典：{'state': bool}

        :return: 是否成功
        :rtype: bool
        """
        if func in self._changed_cbs:
            return False
        screen_name = self._screen_node.screen_name # NOQA
        binding_name = "#%s.%s" % (self._screen_node.namespace, func.__name__) # NOQA
        NyToggle.__set_callback(screen_name, binding_name, self._screen_node, func)
        self._changed_cbs.append(func)
        return True

    def remove_callback(self, func):
        """
        | 移除开关状态改变时触发的回调函数。

        -----

        :param function func: 回调函数

        :return: 是否成功
        :rtype: bool
        """
        if func not in self._changed_cbs:
            return False
        screen_name = self._screen_node.screen_name # NOQA
        binding_name = "#%s.%s" % (self._screen_node.namespace, func.__name__) # NOQA
        NyToggle.__remove_callback(screen_name, binding_name)
        self._changed_cbs.remove(func)
        return True

    # endregion

    # region Properties ================================================================================================

    @property
    def state(self):
        """
        [可读写属性]

        | 开关状态。

        :rtype: bool
        """
        return self.base_control.GetToggleState()

    @state.setter
    def state(self, val):
        """
        [可读写属性]

        | 开关状态。

        :type val: bool
        """
        if isinstance(val, int):
            val = bool(val)
        self.base_control.SetToggleState(val)

    # endregion











