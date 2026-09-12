# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ....core.client.comp import ViewBinder
from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyToggle",
]


class NyToggle(NyControl):
    """
    开关控件类。

    示例
    ----

    >>> def on_toggle_changed(args):
    ...     print(args)
    >>> self.toggle = nyl.NyToggle(self, "/panel/toggle")
    >>> self.toggle.set_callback(on_toggle_changed)
    >>> self.toggle.state = True

    参见
    ----

    - ``NyToggle.set_callback()`` -- 设置开关状态变化回调。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该开关控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.TOGGLE

    CHANGED = 1 << 0

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

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

        :type val: bool|int
        """
        if isinstance(val, int):
            val = bool(val)
        self._base_control.SetToggleState(val)

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func):
        """
        设置开关状态改变时触发的回调函数。

        说明
        ----

        由于开关回调依赖绑定，请将 UI json 中开关控件的 ``"$toggle_name"`` 字段的值设置为 ``"#<namespace>.<func_name>"`` 。
        ``<namespace>`` 为 UI json 中 ``"namespace"`` 字段的值， ``<func_name>`` 为回调函数名。

        示例
        ----

        >>> def on_toggle_changed(args):
        ...     print(args)
        >>> self.toggle.set_callback(on_toggle_changed)

        -----

        :param function func: 回调函数，参数为一个字典： {'state': bool, 'index': int}

        :return: 无
        :rtype: None
        """
        self.ny_screen_node.build_binding(func, ViewBinder.BF_ToggleChanged)

    def remove_callback(self, func):
        """
        移除通过 ``.set_callback()`` 设置的开关回调函数。

        示例
        ----

        >>> self.toggle.remove_callback(on_toggle_changed)

        -----

        :param function func: 回调函数

        :return: 无
        :rtype: None
        """
        self.ny_screen_node.unbuild_binding(func)

    # endregion

    # region Compatibility =============================================================================================

    set_toggle_state = SetToggleState = lambda s, *a, **k: s._base_control.SetToggleState(*a, **k)
    get_toggle_state = GetToggleState = lambda s, *a, **k: s._base_control.GetToggleState(*a, **k)

    # endregion





