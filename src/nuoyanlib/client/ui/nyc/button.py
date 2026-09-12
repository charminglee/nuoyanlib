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
    from typing import Any
    from ..screen_node import NyScreenNode, NyScreenProxy
    from . import NyImage, NyLabel


import time
from ....core.client.comp import LvComp
from ....core.listener import listen_event, unlisten_event, is_listened
from ....core._utils import kwargs_defaults, cached_property
from ..ui_utils import is_out_of_screen, _UIControlType
from .control import NyControl, InteractableControl


__all__ = [
    "NyButton",
]


def _vibrate(t):
    return LvComp.Device.SetDeviceVibrate(t)


class NyButton(InteractableControl, NyControl):
    """
    按钮控件类。

    说明
    ----

    按钮控件通常包含 ``/default`` ``/hover`` ``/pressed`` 和 ``/button_label`` 四个子控件，分别对应默认、悬浮、按下状态的图片以及按钮文本。
    可通过 ``.default_image`` ``.hover_image`` ``.pressed_image`` ``.button_label`` 属性访问这些子控件，若控件不存在则返回 ``None`` 。

    示例
    ----

    >>> self.button = nyl.NyButton(self, "/panel/button", touch_event_params={'isSwallow': True})
    >>> self.button.set_default_texture("textures/ui/button_default")
    >>> self.button.set_text("确定")
    >>> def on_button_up(args):
    ...     print("按钮点击")
    >>> self.button.set_callback(on_button_up, nyl.NyButton.UP)

    参见
    ----

    - ``NyControl.to_button()`` -- 将通用控件实例转换为按钮控件实例。
    - ``@NyScreenBase.button_callback`` -- 通过装饰器的方式注册按钮回调。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该按钮控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    :param dict[str,Any]|None touch_event_params: [仅关键字参数] 按钮参数字典；默认为 None，详细说明见 `AddTouchEventParams() <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E8%87%AA%E5%AE%9A%E4%B9%89UI/UI%E6%8E%A7%E4%BB%B6.html?key=AddTouchEventParams&docindex=1&type=0>`_

    :raise TypeError: 传入的 ny_screen_node 没有继承 NyScreenNode 或 NyScreenProxy 时抛出
    :raise ControlNotFoundError: 找不到指定路径的控件时抛出
    :raise ControlTypeNotMatchedError: 指定路径的控件非按钮类型时抛出
    """

    CONTROL_TYPE = _UIControlType.BUTTON

    UP           = 1 << 0
    DOWN         = 1 << 1
    CANCEL       = 1 << 2
    MOVE         = 1 << 3
    MOVE_IN      = 1 << 4
    MOVE_OUT     = 1 << 5
    DOUBLE_CLICK = 1 << 6
    LONG_CLICK   = 1 << 7
    HOVER_IN     = 1 << 8
    HOVER_OUT    = 1 << 9
    SCREEN_EXIT  = 1 << 10

    DEFAULT_IMAGE_PATH = "/default"
    HOVER_IMAGE_PATH = "/hover"
    PRESSED_IMAGE_PATH = "/pressed"
    BUTTON_LABEL_PATH = "/button_label"

    @kwargs_defaults(touch_event_params=None)
    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)
        InteractableControl.__init__(
            self,
            {
                NyButton.UP           : (self._base_control.SetButtonTouchUpCallback, self._on_up),
                NyButton.DOWN         : (self._base_control.SetButtonTouchDownCallback, self._on_down),
                NyButton.CANCEL       : (self._base_control.SetButtonTouchCancelCallback, self._on_cancel),
                NyButton.MOVE         : (self._base_control.SetButtonTouchMoveCallback, self._on_move),
                NyButton.MOVE_IN      : (self._base_control.SetButtonTouchMoveInCallback, self._on_move_in),
                NyButton.MOVE_OUT     : (self._base_control.SetButtonTouchMoveOutCallback, self._on_move_out),
                NyButton.HOVER_IN     : (self._base_control.SetButtonHoverInCallback, self._on_hover_in),
                NyButton.HOVER_OUT    : (self._base_control.SetButtonHoverOutCallback, self._on_hover_out),
                NyButton.SCREEN_EXIT  : (self._base_control.SetButtonScreenExitCallback, self._on_screen_exit),
                NyButton.LONG_CLICK   : self._register_long_click_callback,
                NyButton.DOUBLE_CLICK : self._register_double_click_callback,
            }
        )
        
        self._vibrate_time = 100
        self._double_click_time = 0
        self._long_click_timer = None
        self._movable_controls = []
        self._finger_pos = None
        self.is_movable = False
        self.auto_save_pos = False
        self.has_long_clicked = False
        self.touch_event_params = kwargs['touch_event_params']
        
        self._base_control.AddTouchEventParams(self.touch_event_params)
        self._base_control.AddHoverEventParams()

    def __ui_destroy__(self):
        unlisten_event(self.GetEntityByCoordReleaseClientEvent)
        if self.is_movable:
            self.cancel_movable()
        if self._long_click_timer:
            LvComp.Game.CancelTimer(self._long_click_timer)
        NyControl.__ui_destroy__(self)
        InteractableControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @cached_property
    def default_image(self):
        """
        [只读属性]

        按钮默认图片控件（default）的 ``NyImage`` 实例。

        :rtype: NyImage|None
        """
        return self.get_child(NyButton.DEFAULT_IMAGE_PATH)

    @cached_property
    def hover_image(self):
        """
        [只读属性]

        按钮悬浮图片控件（hover）的 ``NyImage`` 实例。

        :rtype: NyImage|None
        """
        return self.get_child(NyButton.HOVER_IMAGE_PATH)

    @cached_property
    def pressed_image(self):
        """
        [只读属性]

        按钮按下图片控件（pressed）的 ``NyImage`` 实例。

        :rtype: NyImage|None
        """
        return self.get_child(NyButton.PRESSED_IMAGE_PATH)

    @cached_property
    def button_label(self):
        """
        [只读属性]

        按钮文本控件（button_label）的 ``NyLabel`` 实例。

        :rtype: NyLabel|None
        """
        return self.get_child(NyButton.BUTTON_LABEL_PATH)

    @property
    def vibrate_time(self):
        """
        [可读写属性]

        长按震动反馈的时长，单位为毫秒。

        :rtype: int
        """
        return self._vibrate_time

    @vibrate_time.setter
    def vibrate_time(self, val):
        """
        [可读写属性]

        长按震动反馈的时长，单位为毫秒。

        :type val: int
        """
        self._vibrate_time = val

    # endregion

    # region Common ====================================================================================================

    def set_default_texture(self, tex_path):
        """
        设置按钮默认（default）贴图。

        说明
        ----

        如果按钮不存在 ``/default`` 子控件则无法通过该接口设置。

        示例
        ----

        >>> self.button.set_default_texture("textures/ui/button_default")

        参见
        ----

        - ``NyButton.default_image`` -- 获取默认图片控件。
        - ``NyButton.set_hover_texture()`` -- 设置按钮悬浮贴图。
        - ``NyButton.set_pressed_texture()`` -- 设置按钮按下贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        self.default_image.texture = tex_path

    def set_hover_texture(self, tex_path):
        """
        设置按钮悬浮（hover）贴图。

        说明
        ----

        如果按钮不存在 ``/hover`` 子控件则无法通过该接口设置。

        示例
        ----

        >>> self.button.set_hover_texture("textures/ui/button_hover")

        参见
        ----

        - ``NyButton.hover_image`` -- 获取悬浮图片控件。
        - ``NyButton.set_default_texture()`` -- 设置按钮默认贴图。
        - ``NyButton.set_pressed_texture()`` -- 设置按钮按下贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        self.hover_image.texture = tex_path

    def set_pressed_texture(self, tex_path):
        """
        设置按钮按下（pressed）贴图。

        说明
        ----

        如果按钮不存在 ``/pressed`` 子控件则无法通过该接口设置。

        示例
        ----

        >>> self.button.set_pressed_texture("textures/ui/button_pressed")

        参见
        ----

        - ``NyButton.pressed_image`` -- 获取按下图片控件。
        - ``NyButton.set_default_texture()`` -- 设置按钮默认贴图。
        - ``NyButton.set_hover_texture()`` -- 设置按钮悬浮贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        self.pressed_image.texture = tex_path

    def set_text(self, text):
        """
        设置按钮文本。

        说明
        ----

        如果按钮不存在 ``/button_label`` 子控件则无法通过该接口设置。

        示例
        ----

        >>> self.button.set_text("开始游戏")

        参见
        ----

        - ``NyButton.button_label`` -- 获取按钮文本控件。

        -----

        :param str text: 按钮文本

        :return: 无
        :rtype: None
        """
        self.button_label.text = text

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func, *cb_types):
        """
        设置按钮回调函数。

        说明
        ----

        支持同时设置多个同类型的回调，例如同时设置两个按钮抬起回调，按设置顺序依次触发。

        示例
        ----

        >>> def on_button_up(args):
        ...     print("按钮抬起")
        >>> self.button.set_callback(on_button_up, nyl.NyButton.UP, nyl.NyButton.CANCEL)

        参见
        ----

        - ``NyButton.remove_callback()`` -- 移除回调函数。
        - ``@NyScreenBase.button_callback`` -- 通过装饰器的方式注册按钮回调。

        -----

        :param function func: 回调函数
        :param int cb_types: [变长位置参数] 回调类型，请使用 NyButton 枚举值；可同时传入多个类型

        :return: 无
        :rtype: None

        :raise ValueError: 回调类型错误时抛出
        """
        InteractableControl.set_callback(self, func, *cb_types)

    def remove_callback(self, func, *cb_types):
        """
        移除通过 ``.set_callback()`` 设置的按钮回调函数。

        示例
        ----

        >>> self.button.remove_callback(on_button_up, nyl.NyButton.UP, nyl.NyButton.CANCEL)

        参见
        ----

        - ``NyButton.set_callback()`` -- 设置按钮回调函数。

        -----

        :param function func: 要移除的回调函数
        :param int cb_types: [变长位置参数] 回调类型，请使用 NyButton 枚举值；可同时传入多个类型

        :return: 无
        :rtype: None

        :raise ValueError: 回调类型错误时抛出
        """
        InteractableControl.remove_callback(self, func, *cb_types)

    def _register_long_click_callback(self):
        self.set_callback(self._on_touch_down_lc, NyButton.DOWN)
        self.set_callback(self._cancel_long_click, NyButton.MOVE)
        self.set_callback(self._cancel_long_click, NyButton.UP)

    def _register_double_click_callback(self):
        self.set_callback(self._on_touch_up_dc, NyButton.UP)

    _on_up              = lambda s, *a: s.exec_callbacks(NyButton.UP, *a)
    _on_down            = lambda s, *a: s.exec_callbacks(NyButton.DOWN, *a)
    _on_cancel          = lambda s, *a: s.exec_callbacks(NyButton.CANCEL, *a)
    _on_move            = lambda s, *a: s.exec_callbacks(NyButton.MOVE, *a)
    _on_move_in         = lambda s, *a: s.exec_callbacks(NyButton.MOVE_IN, *a)
    _on_move_out        = lambda s, *a: s.exec_callbacks(NyButton.MOVE_OUT, *a)
    _on_double_click    = lambda s, *a: s.exec_callbacks(NyButton.DOUBLE_CLICK, *a)
    _on_long_click      = lambda s, *a: s.exec_callbacks(NyButton.LONG_CLICK, *a)
    _on_hover_in        = lambda s, *a: s.exec_callbacks(NyButton.HOVER_IN, *a)
    _on_hover_out       = lambda s, *a: s.exec_callbacks(NyButton.HOVER_OUT, *a)
    _on_screen_exit     = lambda s, *a: s.exec_callbacks(NyButton.SCREEN_EXIT, *a)

    def _on_touch_up_dc(self, args):
        if self.has_long_clicked:
            return
        if time.time() - self._double_click_time <= 0.3:
            # 触发双击
            self._double_click_time = 0
            self._on_double_click(args)
        else:
            self._double_click_time = time.time()

    def _on_touch_down_lc(self, args):
        threshold = LvComp.Operation.GetHoldTimeThresholdInMs() / 1000.0
        self.has_long_clicked = False
        def on_long_click():
            # 触发长按
            self.has_long_clicked = True
            _vibrate(self._vibrate_time)
            self._on_long_click(args)
        self._long_click_timer = LvComp.Game.AddTimer(threshold, on_long_click)

    def _cancel_long_click(self, args):
        if self._long_click_timer:
            LvComp.Game.CancelTimer(self._long_click_timer)
            self._long_click_timer = None

    # endregion

    # region Movable ===================================================================================================

    def set_movable(
            self,
            move_parent=False,
            associated=None,
            auto_save=False,
            by_long_click=False,
    ):
        """
        开启按钮拖动。

        说明
        ----

        开启后如需对该按钮设置回调函数，请使用按钮的 ``.set_callback()`` 方法，不要使用 ModSDK 的原生接口。

        示例
        ----

        >>> self.button.set_movable(auto_save=True, by_long_click=True)

        参见
        ----

        - ``NyButton.cancel_movable()`` -- 关闭按钮拖动。
        - ``NyButton.save_pos()`` -- 手动保存当前位置。

        -----

        :param bool move_parent: 是否同步拖动父控件；默认为 False
        :param str|NyControl|list[str|NyControl]|None associated: 关联拖动的其他控件的路径或实例，拖动该按钮时也会同步拖动这些控件，如有多个控件可使用列表传入；默认为 None
        :param bool auto_save: 是否自动保存位置；默认为 False
        :param bool by_long_click: 是否长按按钮（不松开手指）后才能拖动；默认为 False

        :return: 无
        :rtype: None
        """
        if self.is_movable:
            return

        self.is_movable = True
        movable_controls = [self.parent if move_parent else self]
        if isinstance(associated, (list, tuple)):
            for i in associated:
                movable_controls.append(
                    NyControl(self.ny_screen_node, i) if isinstance(i, str) else i
                )
        elif isinstance(associated, NyControl):
            movable_controls.append(associated)
        self._movable_controls = movable_controls
        self.auto_save_pos = auto_save
        if not is_listened(self.GetEntityByCoordReleaseClientEvent):
            listen_event(self.GetEntityByCoordReleaseClientEvent)

        if by_long_click:
            self.set_callback(self._on_long_click_mov, NyButton.LONG_CLICK)
            self.set_callback(self._on_touch_down_mov, NyButton.DOWN)
        else:
            self.set_callback(self._on_move_mov, NyButton.MOVE)

    def cancel_movable(self):
        """
        关闭按钮拖动。

        说明
        ----

        本方法只关闭当前实例的拖动行为，不会删除已经保存的位置数据。

        示例
        ----

        >>> self.button.cancel_movable()

        参见
        ----

        - ``NyButton.set_movable()`` -- 开启按钮拖动。
        - ``NyButton.clear_pos_data()`` -- 删除已保存的位置数据。

        -----

        :return: 无
        :rtype: None
        """
        if not self.is_movable:
            return

        self.is_movable = False
        self._movable_controls = []
        self.auto_save_pos = False
        unlisten_event(self.GetEntityByCoordReleaseClientEvent)

        self.remove_callback(self._on_long_click_mov, NyButton.LONG_CLICK)
        self.remove_callback(self._on_touch_down_mov, NyButton.DOWN)
        self.remove_callback(self._on_move_mov, NyButton.MOVE)

    def GetEntityByCoordReleaseClientEvent(self, args):
        if self.auto_save_pos:
            self.save_pos()
        self._finger_pos = None

    def _on_move_mov(self, args):
        x = args['TouchPosX']
        y = args['TouchPosY']
        if not self._finger_pos:
            self._finger_pos = (x, y)
            return
        offset = (x - self._finger_pos[0], y - self._finger_pos[1])
        self._finger_pos = (x, y)
        for c in self._movable_controls:
            org_pos = c.position
            new_pos = (org_pos[0] + offset[0], org_pos[1] + offset[1])
            c.position = new_pos
            if is_out_of_screen(c):
                c.position = org_pos

    def _on_long_click_mov(self, args):
        self.set_callback(self._on_move_mov, NyButton.MOVE)

    def _on_touch_down_mov(self, args):
        self.remove_callback(self._on_move_mov, NyButton.MOVE)

    def clear_pos_data(self, with_associated=True):
        """
        删除按钮位置数据。

        删除后下次创建UI时将不会恢复位置。

        示例
        ----

        >>> self.button.clear_pos_data()
        True

        参见
        ----

        - ``NyButton.save_pos()`` -- 保存按钮当前位置。
        - ``NyButton.reset_pos()`` -- 将按钮恢复到默认位置。
        - ``NyButton.cancel_movable()`` -- 关闭拖动。

        -----

        :param bool with_associated: 是否同时删除与此按钮关联的其他控件的位置数据；默认为 True

        :return: 是否成功
        :rtype: bool
        """
        NyControl.clear_pos_data(self)
        if with_associated and self._movable_controls:
            for c in self._movable_controls:
                if c is not self:
                    c.clear_pos_data()
        return True

    def save_pos(self, with_associated=True):
        """
        保存按钮位置数据。

        保存后下次创建UI时将自动恢复位置。

        说明
        ----

        为保证安全，当存在超出屏幕边界的控件时，将跳过本次保存并返回 ``False`` 。

        示例
        ----

        >>> self.button.save_pos()
        True

        参见
        ----

        - ``NyButton.set_movable()`` -- 开启按钮拖动。
        - ``NyButton.reset_pos()`` -- 将按钮恢复到默认位置。
        - ``NyButton.clear_pos_data()`` -- 删除按钮位置数据。

        -----

        :param bool with_associated: 是否同时保存与此按钮关联的其他控件的位置数据；默认为 True

        :return: 是否成功
        :rtype: bool
        """
        NyControl.save_pos(self)
        if with_associated and self._movable_controls:
            for c in self._movable_controls:
                if c is not self:
                    c.save_pos()
        return True

    def reset_pos(self, with_associated=True):
        """
        将按钮恢复到默认位置。

        说明
        ----

        默认位置指的是 UI json 中保存的原始位置。

        示例
        ----

        >>> self.button.reset_pos()
        True

        参见
        ----

        - ``NyButton.set_movable()`` -- 开启按钮拖动。
        - ``NyButton.save_pos()`` -- 保存按钮当前位置。
        - ``NyButton.clear_pos_data()`` -- 删除按钮位置数据。

        -----

        :param bool with_associated: 是否同时重置与此按钮关联的其他控件的位置数据；默认为 True

        :return: 是否成功
        :rtype: bool
        """
        NyControl.reset_pos(self)
        if with_associated and self._movable_controls:
            for c in self._movable_controls:
                if c is not self:
                    c.reset_pos()
        return True

    # endregion

    # region Compatibility =============================================================================================

    add_touch_event_params             = AddTouchEventParams           = lambda s, *a, **k: s._base_control.AddTouchEventParams(*a, **k)
    add_hover_event_params             = AddHoverEventParams           = lambda s, *a, **k: s._base_control.AddHoverEventParams(*a, **k)
    set_button_touch_down_callback     = SetButtonTouchDownCallback    = lambda s, *a, **k: s._base_control.SetButtonTouchDownCallback(*a, **k)
    set_button_hover_in_callback       = SetButtonHoverInCallback      = lambda s, *a, **k: s._base_control.SetButtonHoverInCallback(*a, **k)
    set_button_hover_out_callback      = SetButtonHoverOutCallback     = lambda s, *a, **k: s._base_control.SetButtonHoverOutCallback(*a, **k)
    set_button_touch_up_callback       = SetButtonTouchUpCallback      = lambda s, *a, **k: s._base_control.SetButtonTouchUpCallback(*a, **k)
    set_button_touch_cancel_callback   = SetButtonTouchCancelCallback  = lambda s, *a, **k: s._base_control.SetButtonTouchCancelCallback(*a, **k)
    set_button_touch_move_callback     = SetButtonTouchMoveCallback    = lambda s, *a, **k: s._base_control.SetButtonTouchMoveCallback(*a, **k)
    set_button_touch_move_in_callback  = SetButtonTouchMoveInCallback  = lambda s, *a, **k: s._base_control.SetButtonTouchMoveInCallback(*a, **k)
    set_button_touch_move_out_callback = SetButtonTouchMoveOutCallback = lambda s, *a, **k: s._base_control.SetButtonTouchMoveOutCallback(*a, **k)
    set_button_screen_exit_callback    = SetButtonScreenExitCallback   = lambda s, *a, **k: s._base_control.SetButtonScreenExitCallback(*a, **k)

    # endregion




