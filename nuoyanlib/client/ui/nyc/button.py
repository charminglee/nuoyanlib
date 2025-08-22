# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-22
|
| ==============================================
"""


from time import time
from ..ui_utils import (
    to_control, is_ui_out_of_screen,
    get_ui_pos_data, save_ui_pos_data, get_parent_control,
)
from ...._core._client.comp import LvComp
from ...._core._types._checker import args_type_check
from ...._core.event.listener import listen_event, unlisten_event
from .control import NyControl
from ....utils.enum import Enum, ButtonCallbackType, ControlType


__all__ = [
    "NyButton",
]


class NyButton(NyControl):
    """
    | 创建 ``NyButton`` 按钮实例。
    | 兼容ModSDK ``ButtonUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNodeExtension screen_node_ex: 按钮所在UI类的实例
    :param ButtonUIControl btn_control: 通过asButton()获取的按钮实例
    :param dict[str,Any]|None touch_event_params: [仅关键字参数] 按钮参数字典，默认为None，详细说明见AddTouchEventParams
    """

    _CONTROL_TYPE = ControlType.BUTTON
    _CALLBACK_API_MAP = {
        ButtonCallbackType.UP           : "SetButtonTouchUpCallback",
        ButtonCallbackType.DOWN         : "SetButtonTouchDownCallback",
        ButtonCallbackType.CANCEL       : "SetButtonTouchCancelCallback",
        ButtonCallbackType.MOVE         : "SetButtonTouchMoveCallback",
        ButtonCallbackType.MOVE_IN      : "SetButtonTouchMoveInCallback",
        ButtonCallbackType.MOVE_OUT     : "SetButtonTouchMoveOutCallback",
        ButtonCallbackType.HOVER_IN     : "SetButtonHoverInCallback",
        ButtonCallbackType.HOVER_OUT    : "SetButtonHoverOutCallback",
        ButtonCallbackType.SCREEN_EXIT  : "SetButtonScreenExitCallback",
    }

    class CommonChildPath(Enum[str]):
        """
        | 按钮通用子控件路径枚举。
        """

        default = Enum.auto()
        """
        | 默认图片控件。
        """

        hover = Enum.auto()
        """
        | 悬浮图片控件。
        """

        pressed = Enum.auto()
        """
        | 按下图片控件。
        """

        button_label = Enum.auto()
        """
        | 文本控件。
        """

    def __init__(self, screen_node_ex, btn_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, btn_control)
        self.__vibrate_time = 100
        self._btn_callbacks = {}
        self._enabled_double_click = False
        self._double_click_time = 0
        self._enabled_long_click = False
        self._long_click_timer = None
        self._movable_controls = []
        self._finger_pos = None
        self._ui_pos_data_key = screen_node_ex._ui_pos_data_key
        self.is_movable = False
        self.auto_save_pos = False
        self.has_long_clicked = False
        self.touch_event_params = kwargs.get('touch_event_params')
        self.base_control.AddTouchEventParams(self.touch_event_params)
        self.base_control.AddHoverEventParams()
        listen_event(self.GetEntityByCoordReleaseClientEvent)

    def __destroy__(self):
        unlisten_event(self.GetEntityByCoordReleaseClientEvent)
        if self.is_movable:
            self.cancel_movable()
        LvComp.Game.CancelTimer(self._long_click_timer)
        self._btn_callbacks.clear()
        NyControl.__destroy__(self)

    def GetEntityByCoordReleaseClientEvent(self, args):
        if self.auto_save_pos:
            self.save_pos_data()
        self._finger_pos = None

    # region API =======================================================================================================

    def set_default_texture(self, tex_path):
        """
        | 设置按钮默认（default）贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        (self / NyButton.CommonChildPath.default).to_image().SetSprite(tex_path)

    def set_hover_texture(self, tex_path):
        """
        | 设置按钮悬浮（hover）贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        (self / NyButton.CommonChildPath.hover).to_image().SetSprite(tex_path)

    def set_pressed_texture(self, tex_path):
        """
        | 设置按钮按下（pressed）贴图。

        -----

        :param str tex_path: 贴图路径

        :return: 无
        :rtype: None
        """
        (self / NyButton.CommonChildPath.pressed).to_image().SetSprite(tex_path)

    def set_text(self, text):
        """
        | 设置按钮文本。

        -----

        :param str text: 按钮文本

        :return: 无
        :rtype: None
        """
        (self / NyButton.CommonChildPath.button_label).to_label().text = text

    @property
    def vibrate_time(self):
        """
        [可读写属性]

        | 长按震动反馈的时长，单位为毫秒。

        :rtype: int
        """
        return self.__vibrate_time

    @vibrate_time.setter
    @args_type_check(int, is_method=True)
    def vibrate_time(self, val):
        """
        [可读写属性]

        | 长按震动反馈的时长，单位为毫秒。

        :type val: int
        """
        self.__vibrate_time = val

    def set_callback(self, callback_type, func):
        """
        | 添加按钮回调函数，支持对同一个按钮添加多个同类型的回调，按添加顺序依次触发。
        | 注意：调用本方法后请勿再调用ModSDK的设置按钮回调的接口（如 ``.SetButtonTouchUpCallback()``），否则所有通过本方法添加的回调函数将无效。

        -----

        :param int callback_type: 回调类型，请使用ButtonCallbackType枚举值
        :param function func: 回调函数

        :return: 是否成功
        :rtype: bool
        """
        if callback_type not in ButtonCallbackType:
            return False
        callback_lst = self._btn_callbacks.setdefault(callback_type, [])
        if func not in callback_lst:
            callback_lst.append(func)
        else:
            return False
        if callback_type == ButtonCallbackType.DOUBLE_CLICK:
            if not self._enabled_double_click:
                self._enabled_double_click = True
                self.set_callback(ButtonCallbackType.UP, self._on_touch_up_dc)
        elif callback_type == ButtonCallbackType.LONG_CLICK:
            if not self._enabled_long_click:
                self._enabled_long_click = True
                self.set_callback(ButtonCallbackType.DOWN, self._on_touch_down_lc)
                self.set_callback(ButtonCallbackType.MOVE, self._cancel_long_click)
                self.set_callback(ButtonCallbackType.UP, self._cancel_long_click)
        else:
            def proxy(args):
                self._exec_callbacks(callback_type, args)
            set_callback_api = getattr(self.base_control, NyButton._CALLBACK_API_MAP[callback_type])
            set_callback_api(proxy)
        return True
    
    SetCallback = set_callback

    def remove_callback(self, callback_type, func):
        """
        | 移除通过 ``.set_callback()`` 添加的按钮回调函数。

        -----

        :param int callback_type: 回调类型，请使用ButtonCallbackType枚举值
        :param function func: 要移除的回调函数

        :return: 是否成功
        :rtype: bool
        """
        if callback_type in self._btn_callbacks and func in self._btn_callbacks[callback_type]:
            callback_lst = self._btn_callbacks[callback_type]
            callback_lst.remove(func)
        else:
            return False
        if not callback_lst:
            if callback_type == ButtonCallbackType.DOUBLE_CLICK:
                if self._enabled_double_click:
                    self._enabled_double_click = False
                    self.remove_callback(ButtonCallbackType.UP, self._on_touch_up_dc)
            elif callback_type == ButtonCallbackType.LONG_CLICK:
                if self._enabled_long_click:
                    self._enabled_long_click = False
                    self.remove_callback(ButtonCallbackType.DOWN, self._on_touch_down_lc)
                    self.remove_callback(ButtonCallbackType.MOVE, self._cancel_long_click)
                    self.remove_callback(ButtonCallbackType.UP, self._cancel_long_click)
        return True

    RemoveCallback = remove_callback

    def set_movable(self, move_parent=False, associated_uis=None, auto_save=False):
        """
        | 设置按钮可拖动（随时拖动）。
        | 注意：设置可拖动后，如果需要对该按钮设置回调函数，请使用 ``.set_callback()`` ，不要使用ModSDK中的接口。
        | 请勿同时设置 ``.set_movable()`` 和 ``.set_movable_by_long_click()`` 。

        -----

        :param bool move_parent: 是否同步拖动父控件，默认为False
        :param str|BaseUIControl|list[str|BaseUIControl]|None associated_uis: 关联拖动的其他控件，拖动该按钮时也会同步拖动这些控件，可传入控件路径或实例，如有多个控件可使用列表传入；默认为None
        :param bool auto_save: 是否自动保存位置；默认为False

        :return: 无
        :rtype: None
        """
        self._set_movable_data(True, move_parent, associated_uis, auto_save)
        self.set_callback(ButtonCallbackType.MOVE, self._on_move)

    SetMovable = set_movable

    def set_movable_by_long_click(self, move_parent=False, associated_uis=None, auto_save=False):
        """
        | 设置按钮长按拖动（长按后才能拖动）。
        | 注意：设置可拖动后，如果需要对该按钮设置回调函数，请使用 ``.set_callback()`` ，不要使用ModSDK中的接口。
        | 请勿同时设置 ``.set_movable()`` 和 ``.set_movable_by_long_click()`` 。

        -----

        :param bool move_parent: 是否同步拖动父控件，默认为False
        :param str|BaseUIControl|list[str|BaseUIControl]|None associated_uis: 关联拖动的其他控件，拖动该按钮时也会同步拖动这些控件，可传入控件路径或实例，如有多个控件可使用列表传入；默认为None
        :param bool auto_save: 是否自动保存位置；默认为False

        :return: 无
        :rtype: None
        """
        self._set_movable_data(True, move_parent, associated_uis, auto_save)
        self.set_callback(ButtonCallbackType.LONG_CLICK, self._on_long_click_mov)
        self.set_callback(ButtonCallbackType.DOWN, self._on_touch_down_mov)

    SetMovableByLongClick = set_movable_by_long_click

    def cancel_movable(self):
        """
        | 取消按钮可拖动。

        -----

        :return: 无
        :rtype: None
        """
        self._set_movable_data(False)
        self.remove_callback(ButtonCallbackType.MOVE, self._on_move)
        self.remove_callback(ButtonCallbackType.LONG_CLICK, self._on_long_click_mov)
        self.remove_callback(ButtonCallbackType.DOWN, self._on_touch_down_mov)

    CancelMovable = cancel_movable

    def clear_pos_data(self):
        """
        | 删除按钮位置数据，关联拖动的其他控件的位置数据也会一并删除。

        -----

        :return: 是否成功
        :rtype: bool
        """
        data = get_ui_pos_data(self._ui_pos_data_key)
        if self.path in data:
            del data[self.path]
            return save_ui_pos_data(self._ui_pos_data_key, data)
        return False

    ClearPosData = clear_pos_data

    def save_pos_data(self):
        """
        | 保存按钮位置数据，关联拖动的其他控件的位置数据也会一并保存，下次进入游戏时会自动恢复位置。
        | 为保证安全，当控件超出屏幕边界时，将保存失败。

        -----

        :return: 是否成功
        :rtype: bool
        """
        data = get_ui_pos_data(self._ui_pos_data_key)
        controls = self._movable_controls or [self.base_control]
        this_data = []
        for c in controls:
            if not is_ui_out_of_screen(c):
                this_data.append((c.GetPath(), c.GetPosition()))
            else:
                return False
        data[self.path] = this_data
        return save_ui_pos_data(self._ui_pos_data_key, data)

    SavePosData = save_pos_data

    # endregion

    # region Internal ==================================================================================================

    def _set_movable_data(self, movable, move_parent=False, associated_uis=None, auto_save=False):
        if movable:
            movable_controls = []
            if move_parent:
                movable_controls.append(get_parent_control(self.base_control, self._screen_node))
            else:
                movable_controls.append(self.base_control)
            if associated_uis:
                if isinstance(associated_uis, (list, tuple)):
                    movable_controls.extend(associated_uis)
                else:
                    movable_controls.append(associated_uis)
            self._movable_controls = movable_controls
            self.auto_save_pos = auto_save
            self.is_movable = True
        else:
            self._movable_controls = []
            self.auto_save_pos = False
            self.is_movable = False

    def _exec_callbacks(self, callback_type, args):
        for cb in self._btn_callbacks[callback_type]:
            cb(args)

    def _on_touch_up_dc(self, args):
        if self.has_long_clicked:
            return
        if time() - self._double_click_time <= 0.3:
            self._double_click_time = 0
            self._exec_callbacks(ButtonCallbackType.DOUBLE_CLICK, args)
        else:
            self._double_click_time = time()

    def _on_touch_down_lc(self, args):
        threshold = LvComp.Operation.GetHoldTimeThresholdInMs() / 1000.0
        self.has_long_clicked = False
        def on_long_click():
            self._vibrate()
            self._exec_callbacks(ButtonCallbackType.LONG_CLICK, args)
            self.has_long_clicked = True
        self._long_click_timer = LvComp.Game.AddTimer(threshold, on_long_click)

    def _cancel_long_click(self, args):
        LvComp.Game.CancelTimer(self._long_click_timer)
        self._long_click_timer = None

    def _on_move(self, args):
        x = args['TouchPosX']
        y = args['TouchPosY']
        if not self._finger_pos:
            self._finger_pos = (x, y)
        offset = (x - self._finger_pos[0], y - self._finger_pos[1])
        self._finger_pos = (x, y)
        for c in self._movable_controls:
            self._set_offset(c, offset)

    def _on_long_click_mov(self, args):
        self.set_callback(ButtonCallbackType.MOVE, self._on_move)

    def _on_touch_down_mov(self, args):
        self.remove_callback(ButtonCallbackType.MOVE, self._on_move)

    def _vibrate(self):
        LvComp.Device.SetDeviceVibrate(self.__vibrate_time)

    def _set_offset(self, control, offset):
        control = to_control(self._screen_node, control)
        orig_pos = control.GetPosition()
        new_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])
        control.SetPosition(new_pos)
        if is_ui_out_of_screen(control):
            control.SetPosition(orig_pos)

    # endregion













