# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ..ui_utils import _UIControlType
from .control import NyControl, InteractableControl


__all__ = [
    "NySelectionWheel",
]


class NySelectionWheel(InteractableControl, NyControl):
    """
    轮盘控件类。

    示例
    ----

    >>> self.wheel = nyl.NySelectionWheel(self, "/panel/selection_wheel")
    >>> def on_slice_click(args):
    ...     print(args)
    >>> self.wheel.set_callback(on_slice_click, nyl.NySelectionWheel.CLICK)
    >>> self.wheel.curr_slice_index = 0

    参见
    ----

    - ``NyControl.to_selection_wheel()`` -- 将通用控件实例转换为轮盘控件实例。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该轮盘控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.SELECTION_WHEEL

    CLICK = 1 << 0
    HOVER = 1 << 1

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)
        InteractableControl.__init__(
            self,
            {
                NySelectionWheel.CLICK: (self._base_control.SetTouchUpCallback, self._on_click),
                NySelectionWheel.HOVER: (self._base_control.SetHoverCallback, self._on_hover),
            }
        )

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)
        InteractableControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def slice_count(self):
        """
        [只读属性]

        轮盘切片数量。

        :rtype: int
        """
        return self._base_control.GetSliceCount()

    @property
    def curr_slice_index(self):
        """
        [可读写属性]

        轮盘当前选择的切片的索引。

        :rtype: int
        """
        return self._base_control.GetCurrentSliceIndex()

    @curr_slice_index.setter
    def curr_slice_index(self, val):
        """
        [可读写属性]

        轮盘当前选择的切片的索引。

        :type val: int
        """
        self._base_control.SetCurrentSliceIndex(val)

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func, *cb_types):
        """
        设置轮盘回调函数。

        说明
        ----

        支持同时设置多个同类型的回调，例如同时设置两个点击轮盘切片回调，按设置顺序依次触发。

        示例
        ----

        >>> def on_slice_click(args):
        ...     print(args)
        >>> self.wheel.set_callback(on_slice_click, NySelectionWheel.CLICK)

        -----

        :param function func: 回调函数
        :param int cb_types: [变长位置参数] 回调类型，请使用 NySelectionWheel 枚举值；可同时传入多个类型

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型错误时抛出
        """
        InteractableControl.set_callback(self, func, *cb_types)

    def remove_callback(self, func, *cb_types):
        """
        移除通过 ``.set_callback()`` 设置的轮盘回调函数。

        -----

        :param function func: 回调函数
        :param int cb_types: [变长位置参数] 回调类型，请使用 NySelectionWheel 枚举值；可同时传入多个类型

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型错误时抛出
        """
        InteractableControl.remove_callback(self, func, *cb_types)

    _on_click = lambda s, *a: s.exec_callbacks(NySelectionWheel.CLICK, *a)
    _on_hover = lambda s, *a: s.exec_callbacks(NySelectionWheel.HOVER, *a)

    # endregion

    # region Compatibility =============================================================================================

    get_slice_count         = GetSliceCount        = lambda s, *a, **k: s._base_control.GetSliceCount(*a, **k)
    get_current_slice_index = GetCurrentSliceIndex = lambda s, *a, **k: s._base_control.GetCurrentSliceIndex(*a, **k)
    set_current_slice_index = SetCurrentSliceIndex = lambda s, *a, **k: s._base_control.SetCurrentSliceIndex(*a, **k)
    set_touch_up_callback   = SetTouchUpCallback   = lambda s, *a, **k: s._base_control.SetTouchUpCallback(*a, **k)
    set_hover_callback      = SetHoverCallback     = lambda s, *a, **k: s._base_control.SetHoverCallback(*a, **k)

    # endregion


