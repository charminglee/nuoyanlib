# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


if 0:
    from typing import Any
    from ..screen_node import ScreenNodeExtension


import time
from ....core.client.comp import LvComp
from ....core._types._checker import args_type_check
from ....core.listener import listen_event, unlisten_event, is_listened
from ....core._utils import kwargs_defaults
from ....utils.enum import ButtonCallbackType, ControlType, ClientEvent
from ..ui_utils import is_out_of_screen
from .control import NyControl, InteractableControl


__all__ = [
    "NyButton",
]


def _vibrate(t):
    return LvComp.Device.SetDeviceVibrate(t)


class NyButton(InteractableControl, NyControl):
    """
    按钮控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 按钮所在UI类的实例（需继承 ScreenNodeExtension）
    :param ButtonUIControl btn_control: 通过 asButton() 等方式获取的 ButtonUIControl 实例
    :param dict[str,Any]|None touch_event_params: [仅关键字参数] 按钮参数字典；默认为 None，详细说明见 AddTouchEventParams
    """

    CONTROL_TYPE = ControlType.BUTTON
    CALLBACK_TYPE = ButtonCallbackType
    DEFAULT_IMG_PATH = "/default"
    HOVER_IMG_PATH = "/hover"
    PRESSED_IMG_PATH = "/pressed"
    BTN_LABEL_PATH = "/button_label"

    @kwargs_defaults(touch_event_params=None)
    def __init__(self, screen_node_ex, btn_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, btn_control)
        InteractableControl.__init__(
            self,
            {
                ButtonCallbackType.UP           : (btn_control.SetButtonTouchUpCallback, self._on_up),
                ButtonCallbackType.DOWN         : (btn_control.SetButtonTouchDownCallback, self._on_down),
                ButtonCallbackType.CANCEL       : (btn_control.SetButtonTouchCancelCallback, self._on_cancel),
                ButtonCallbackType.MOVE         : (btn_control.SetButtonTouchMoveCallback, self._on_move),
                ButtonCallbackType.MOVE_IN      : (btn_control.SetButtonTouchMoveInCallback, self._on_move_in),
                ButtonCallbackType.MOVE_OUT     : (btn_control.SetButtonTouchMoveOutCallback, self._on_move_out),
                ButtonCallbackType.HOVER_IN     : (btn_control.SetButtonHoverInCallback, self._on_hover_in),
                ButtonCallbackType.HOVER_OUT    : (btn_control.SetButtonHoverOutCallback, self._on_hover_out),
                ButtonCallbackType.SCREEN_EXIT  : (btn_control.SetButtonScreenExitCallback, self._on_screen_exit),
                ButtonCallbackType.LONG_CLICK   : (self._register_long_click_callback, None),
                ButtonCallbackType.DOUBLE_CLICK : (self._register_double_click_callback, None),
            },
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
        self.default_img = self / NyButton.DEFAULT_IMG_PATH
        if self.default_img:
            self.default_img = self.default_img.to_image()
        self.hover_img = self / NyButton.HOVER_IMG_PATH
        if self.hover_img:
            self.hover_img = self.hover_img.to_image()
        self.pressed_img = self / NyButton.PRESSED_IMG_PATH
        if self.pressed_img:
            self.pressed_img = self.pressed_img.to_image()
        self.btn_label = self / NyButton.BTN_LABEL_PATH
        if self.btn_label:
            self.btn_label = self.btn_label.to_label()
        self._base_control.AddTouchEventParams(self.touch_event_params)
        self._base_control.AddHoverEventParams()

    def __destroy__(self):
        unlisten_event(self._OnClickScreen, ClientEvent.GetEntityByCoordReleaseClientEvent)
        if self.is_movable:
            self.cancel_movable()
        LvComp.Game.CancelTimer(self._long_click_timer)
        NyControl.__destroy__(self)
        InteractableControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def vibrate_time(self):
        """
        [可读写属性]

        长按震动反馈的时长，单位为毫秒。

        :rtype: int
        """
        return self._vibrate_time

    @vibrate_time.setter
    @args_type_check(int, is_method=True)
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

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        self.default_img.texture = tex_path

    def set_hover_texture(self, tex_path):
        """
        设置按钮悬浮（hover）贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        self.hover_img.texture = tex_path

    def set_pressed_texture(self, tex_path):
        """
        设置按钮按下（pressed）贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        self.pressed_img.texture = tex_path

    def set_text(self, text):
        """
        设置按钮文本。

        -----

        :param str text: 按钮文本

        :return: 无
        :rtype: None
        """
        self.btn_label.text = text

    SetDefaultTexture = set_default_texture
    SetHoverTexture = set_hover_texture
    SetPressedTexture = set_pressed_texture
    SetText = set_text

    # endregion

    # region Callback ==================================================================================================

    def set_callback(self, func, cb_type=ButtonCallbackType.UP):
        """
        设置按钮回调函数。

        说明
        ----

        支持对同一个按钮设置多个同类型的回调，按设置顺序依次触发。

        调用本方法后请勿再调用 ModSDK 的设置按钮回调的接口（如 ``.SetButtonTouchUpCallback()`` ），
        否则所有通过本方法设置的回调函数将无效。

        -----

        :param function func: 回调函数
        :param ButtonCallbackType cb_type: 回调类型，请使用ButtonCallbackType枚举值；默认为ButtonCallbackType.UP

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型无效
        """
        return InteractableControl.set_callback(self, func, cb_type)

    def remove_callback(self, func, cb_type=ButtonCallbackType.UP):
        """
        移除通过 ``.set_callback()`` 设置的按钮回调函数。

        -----

        :param function func: 要移除的回调函数
        :param ButtonCallbackType cb_type: 回调类型，请使用ButtonCallbackType枚举值；默认为ButtonCallbackType.UP

        :return: 是否成功
        :rtype: bool

        :raise ValueError: 回调类型无效
        """
        return InteractableControl.remove_callback(self, func, cb_type)

    def _register_long_click_callback(self, _):
        self.set_callback(self._on_touch_down_lc, ButtonCallbackType.DOWN)
        self.set_callback(self._cancel_long_click, ButtonCallbackType.MOVE)
        self.set_callback(self._cancel_long_click, ButtonCallbackType.UP)

    def _register_double_click_callback(self, _):
        self.set_callback(self._on_touch_up_dc)

    _on_up              = lambda self, *args: self._exec_callbacks(ButtonCallbackType.UP, *args)
    _on_down            = lambda self, *args: self._exec_callbacks(ButtonCallbackType.DOWN, *args)
    _on_cancel          = lambda self, *args: self._exec_callbacks(ButtonCallbackType.CANCEL, *args)
    _on_move            = lambda self, *args: self._exec_callbacks(ButtonCallbackType.MOVE, *args)
    _on_move_in         = lambda self, *args: self._exec_callbacks(ButtonCallbackType.MOVE_IN, *args)
    _on_move_out        = lambda self, *args: self._exec_callbacks(ButtonCallbackType.MOVE_OUT, *args)
    _on_double_click    = lambda self, *args: self._exec_callbacks(ButtonCallbackType.DOUBLE_CLICK, *args)
    _on_long_click      = lambda self, *args: self._exec_callbacks(ButtonCallbackType.LONG_CLICK, *args)
    _on_hover_in        = lambda self, *args: self._exec_callbacks(ButtonCallbackType.HOVER_IN, *args)
    _on_hover_out       = lambda self, *args: self._exec_callbacks(ButtonCallbackType.HOVER_OUT, *args)
    _on_screen_exit     = lambda self, *args: self._exec_callbacks(ButtonCallbackType.SCREEN_EXIT, *args)

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
        LvComp.Game.CancelTimer(self._long_click_timer)
        self._long_click_timer = None

    SetCallback = set_callback
    RemoveCallback = remove_callback

    # endregion

    # region Movable ===================================================================================================

    def set_movable(self, move_parent=False, associated_uis=None, auto_save=False):
        """
        开启按钮拖动。

        说明
        ----

        开启拖动后，如需对该按钮设置回调函数，请使用 ``.set_callback()`` ，不要使用 ModSDK 中的接口。

        -----

        :param bool move_parent: 是否同步拖动父控件；默认为False
        :param str|BaseUIControl|NyControl|list[str|BaseUIControl|NyControl]|None associated_uis: 关联拖动的其他控件，拖动该按钮时也会同步拖动这些控件，可传入控件路径或实例，如有多个控件可使用列表传入；默认为None
        :param bool auto_save: 是否自动保存位置；默认为False

        :return: 无
        :rtype: None
        """
        self._set_movable_data(True, move_parent, associated_uis, auto_save)
        self.set_callback(self._on_move_mov, ButtonCallbackType.MOVE)

    def set_movable_by_long_click(self, move_parent=False, associated_uis=None, auto_save=False):
        """
        开启按钮长按拖动（长按后才能拖动）。

        说明
        ----

        设置可拖动后，如果需要对该按钮设置回调函数，请使用 ``.set_callback()`` ，不要使用 ModSDK 中的接口。

        -----

        :param bool move_parent: 是否同步拖动父控件；默认为False
        :param str|BaseUIControl|NyControl|list[str|BaseUIControl|NyControl]|None associated_uis: 关联拖动的其他控件，拖动该按钮时也会同步拖动这些控件，可传入控件路径或实例，如有多个控件可使用列表传入；默认为None
        :param bool auto_save: 是否自动保存位置；默认为False

        :return: 无
        :rtype: None
        """
        self._set_movable_data(True, move_parent, associated_uis, auto_save)
        self.set_callback(self._on_long_click_mov, ButtonCallbackType.LONG_CLICK)
        self.set_callback(self._on_touch_down_mov, ButtonCallbackType.DOWN)

    def cancel_movable(self):
        """
        关闭按钮拖动。

        -----

        :return: 无
        :rtype: None
        """
        if not self.is_movable:
            return
        self._set_movable_data(False)
        self.remove_callback(self._on_move_mov, ButtonCallbackType.MOVE)
        self.remove_callback(self._on_long_click_mov, ButtonCallbackType.LONG_CLICK)
        self.remove_callback(self._on_touch_down_mov, ButtonCallbackType.DOWN)

    def _set_movable_data(self, movable, move_parent=False, associated_uis=None, auto_save=False):
        if movable:
            movable_controls = [self.parent if move_parent else self]
            if associated_uis:
                if isinstance(associated_uis, (list, tuple)):
                    associated_uis = map(self.ui_node._create_nyc, associated_uis)
                    movable_controls.extend(associated_uis)
                else:
                    associated_uis = self.ui_node._create_nyc(associated_uis)
                    movable_controls.append(associated_uis)
            self._movable_controls = movable_controls
            self.auto_save_pos = auto_save
            self.is_movable = True
            if not is_listened(self._OnClickScreen, ClientEvent.GetEntityByCoordReleaseClientEvent):
                listen_event(self._OnClickScreen, ClientEvent.GetEntityByCoordReleaseClientEvent)
        else:
            self._movable_controls = []
            self.auto_save_pos = False
            self.is_movable = False
            unlisten_event(self._OnClickScreen, ClientEvent.GetEntityByCoordReleaseClientEvent)

    def _OnClickScreen(self, args):
        if self.auto_save_pos:
            self.save_pos_data()
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
        self.set_callback(self._on_move_mov, ButtonCallbackType.MOVE)

    def _on_touch_down_mov(self, args):
        self.remove_callback(self._on_move_mov, ButtonCallbackType.MOVE)

    def clear_pos_data(self):
        """
        删除按钮位置数据。

        关联拖动的其他控件的位置数据也会一并删除。

        -----

        :return: 是否成功
        :rtype: bool
        """
        data = self.ui_node._get_ui_pos_data()
        if self.path in data:
            del data[self.path]
            return self.ui_node._save_ui_pos_data(data)
        return False

    def save_pos_data(self):
        """
        保存按钮位置数据。

        说明
        ----

        关联拖动的其他控件的位置数据也会一并保存，下次进入游戏（创建界面）时自动恢复位置。
        为保证安全，当控件超出屏幕边界时，将保存失败。

        -----

        :return: 是否成功
        :rtype: bool
        """
        data = self.ui_node._get_ui_pos_data()
        controls = self._movable_controls or [self]
        pos_lst = []
        for c in controls:
            if not is_out_of_screen(c):
                pos_lst.append((c.path, c.position))
            else:
                return False
        data[self.path] = pos_lst
        return self.ui_node._save_ui_pos_data(data)

    SetMovable = set_movable
    SetMovableByLongClick = set_movable_by_long_click
    CancelMovable = cancel_movable
    ClearPosData = clear_pos_data
    SavePosData = save_pos_data

    # endregion













