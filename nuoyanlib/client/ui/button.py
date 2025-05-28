# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-05-21
#
# ====================================================


from time import time as _time
from . import ui_utils as _ui_utils
from .ui_utils import ButtonCallback as _ButtonCallback
from ..._core._client._comp import LvComp as _LvComp
from ..._core._client import _lib_client
from ..._core import _utils
from .control import NyControl as _NyControl


_CALLBACK_API_MAP = {
    _ButtonCallback.touch_up: "SetButtonTouchUpCallback",
    _ButtonCallback.touch_down: "SetButtonTouchDownCallback",
    _ButtonCallback.touch_cancel: "SetButtonTouchCancelCallback",
    _ButtonCallback.touch_move: "SetButtonTouchMoveCallback",
    _ButtonCallback.touch_move_in: "SetButtonTouchMoveInCallback",
    _ButtonCallback.touch_move_out: "SetButtonTouchMoveOutCallback",
    _ButtonCallback.hover_in: "SetButtonHoverInCallback",
    _ButtonCallback.hover_out: "SetButtonHoverOutCallback",
    _ButtonCallback.screen_exit: "SetButtonScreenExitCallback",
}


# todo
class NyButton(_NyControl):
    """
    | 创建NyButton按钮实例。
    | 兼容ModSDK ``ButtonUIControl`` 和 ``BaseUIControl`` 的相关接口。

    -----

    :param ScreenNode screen_node: 按钮所在UI类的实例
    :param ButtonUIControl btn_control: 通过asButton()获取的按钮实例
    """

    def __init__(self, screen_node, btn_control):
        super(NyButton, self).__init__(screen_node, btn_control)
        self._lib_sys = _lib_client.instance()
        self._btn_callbacks = {}
        self._enabled_double_click = False
        self._double_click_time = 0
        self._enabled_long_click = False
        self._long_click_timer = None
        self._movable_controls = []
        self._finger_pos = None
        # noinspection PyUnresolvedReferences
        self._ui_pos_data_key = "nyl_ui_pos_data_%s_%s" % (screen_node.namespace, screen_node.name)
        self.__vibrate_time = 100
        self.is_movable = False
        self.auto_save_pos = False
        self.has_long_clicked = False
        self._lib_sys.add_event_callback(
            "GetEntityByCoordReleaseClientEvent", self._GetEntityByCoordReleaseClientEvent
        )

    def Destroy(self):
        self._lib_sys.remove_event_callback(
            "GetEntityByCoordReleaseClientEvent", self._GetEntityByCoordReleaseClientEvent
        )

    def _GetEntityByCoordReleaseClientEvent(self, args):
        if self.auto_save_pos:
            self.SavePosData()
        self._finger_pos = None

    @property
    def vibrate_time(self):
        """
        长按震动反馈的时长，单位为毫秒。
        """
        return self.__vibrate_time

    @vibrate_time.setter
    @_utils.param_type_check(int)
    def vibrate_time(self, val):
        """
        长按震动反馈的时长，单位为毫秒。
        """
        self.__vibrate_time = val

    def SetCallback(self, callback_type, func):
        """
        | 添加按钮回调函数，支持对同一个按钮添加多个同类型的回调，按添加顺序依次触发。
        | 注意：调用本方法后请勿再调用ModSDK的设置按钮回调的接口（如 ``SetButtonTouchUpCallback``），否则所有通过本方法添加的回调函数将无效。

        -----

        :param int callback_type: 回调类型，请使用ButtonCallback枚举值
        :param function func: 回调函数

        :return: 是否成功
        :rtype: bool
        """
        if callback_type not in _ButtonCallback:
            return False
        callback_lst = self._btn_callbacks.setdefault(callback_type, [])
        if func not in callback_lst:
            callback_lst.append(func)
        else:
            return False
        if callback_type == _ButtonCallback.double_click:
            if not self._enabled_double_click:
                self._enabled_double_click = True
                self.SetCallback(_ButtonCallback.touch_up, self._on_touch_up_dc)
        elif callback_type == _ButtonCallback.long_click:
            if not self._enabled_long_click:
                self._enabled_long_click = True
                self.SetCallback(_ButtonCallback.touch_down, self._on_touch_down_lc)
                self.SetCallback(_ButtonCallback.touch_move, self._cancel_long_click)
                self.SetCallback(_ButtonCallback.touch_up, self._cancel_long_click)
        else:
            def callback_proxy(args):
                self._exec_callbacks(callback_type, args)
            set_callback_api = getattr(self.control, _CALLBACK_API_MAP[callback_type])
            set_callback_api(callback_proxy)
        return True

    def RemoveCallback(self, callback_type, func):
        """
        | 移除通过 ``SetCallback`` 添加的按钮回调函数。

        -----

        :param int callback_type: 回调类型，请使用ButtonCallback枚举值
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
            if callback_type == _ButtonCallback.double_click:
                if self._enabled_double_click:
                    self._enabled_double_click = False
                    self.RemoveCallback(_ButtonCallback.touch_up, self._on_touch_up_dc)
            elif callback_type == _ButtonCallback.long_click:
                if self._enabled_long_click:
                    self._enabled_long_click = False
                    self.RemoveCallback(_ButtonCallback.touch_down, self._on_touch_down_lc)
                    self.RemoveCallback(_ButtonCallback.touch_move, self._cancel_long_click)
                    self.RemoveCallback(_ButtonCallback.touch_up, self._cancel_long_click)
        return True

    def SetMovable(self, move_parent=False, associated_uis=None, auto_save=False):
        """
        | 设置按钮可拖动（随时拖动）。
        | 注意：设置可拖动后，如果需要对该按钮设置回调函数，请使用 ``SetCallback`` ，不要使用ModSDK中的接口。
        | 请勿同时设置 ``SetMovable`` 和 ``SetMovableByLongClick`` 。

        -----

        :param bool move_parent: 是否同步拖动父控件，默认为False
        :param str|BaseUIControl|list[str|BaseUIControl]|None associated_uis: 关联拖动的其他控件，拖动该按钮时也会同步拖动这些控件，可传入控件路径或实例，如有多个控件可使用列表传入；默认为None
        :param bool auto_save: 是否自动保存位置；默认为False

        :return: 无
        :rtype: None
        """
        self._set_movable_data(True, move_parent, associated_uis, auto_save)
        self.SetCallback(_ButtonCallback.touch_move, self._on_move)

    def SetMovableByLongClick(self, move_parent=False, associated_uis=None, auto_save=False):
        """
        | 设置按钮长按拖动（长按后才能拖动）。
        | 注意：设置可拖动后，如果需要对该按钮设置回调函数，请使用 ``SetCallback`` ，不要使用ModSDK中的接口。
        | 请勿同时设置 ``SetMovable`` 和 ``SetMovableByLongClick`` 。

        -----

        :param bool move_parent: 是否同步拖动父控件，默认为False
        :param str|BaseUIControl|list[str|BaseUIControl]|None associated_uis: 关联拖动的其他控件，拖动该按钮时也会同步拖动这些控件，可传入控件路径或实例，如有多个控件可使用列表传入；默认为None
        :param bool auto_save: 是否自动保存位置；默认为False

        :return: 无
        :rtype: None
        """
        self._set_movable_data(True, move_parent, associated_uis, auto_save)
        self.SetCallback(_ButtonCallback.long_click, self._on_long_click_mov)
        self.SetCallback(_ButtonCallback.touch_down, self._on_touch_down_mov)

    def CancelMovable(self):
        """
        | 取消按钮可拖动。

        -----

        :return: 无
        :rtype: None
        """
        self._set_movable_data(False)
        self.RemoveCallback(_ButtonCallback.touch_move, self._on_move)
        self.RemoveCallback(_ButtonCallback.long_click, self._on_long_click_mov)
        self.RemoveCallback(_ButtonCallback.touch_down, self._on_touch_down_mov)

    def ClearPosData(self):
        """
        | 删除按钮位置数据，关联拖动的其他控件的位置数据也会一并删除。

        -----

        :return: 是否成功
        :rtype: bool
        """
        data = _ui_utils.get_ui_pos_data(self._ui_pos_data_key)
        if self.path in data:
            del data[self.path]
            return _ui_utils.save_ui_pos_data(self._ui_pos_data_key, data)
        return False

    def SavePosData(self):
        """
        | 保存按钮位置数据，关联拖动的其他控件的位置数据也会一并保存，下次进入游戏时会自动恢复位置。
        | 为保证安全，当控件超出屏幕边界时，将保存失败。

        -----

        :return: 是否成功
        :rtype: bool
        """
        data = _ui_utils.get_ui_pos_data(self._ui_pos_data_key)
        controls = self._movable_controls or [self.control]
        this_data = []
        for c in controls:
            if not _ui_utils.is_ui_out_of_screen(c):
                this_data.append((c.GetPath(), c.GetPosition()))
            else:
                return False
        data[self.path] = this_data
        return _ui_utils.save_ui_pos_data(self._ui_pos_data_key, data)

    def _set_movable_data(self, movable, move_parent=False, associated_uis=None, auto_save=False):
        if movable:
            movable_controls = []
            if move_parent:
                movable_controls.append(_ui_utils.get_parent_control(self.control, self.screen_node))
            else:
                movable_controls.append(self.control)
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
        if _time() - self._double_click_time <= 0.3:
            self._double_click_time = 0
            self._exec_callbacks(_ButtonCallback.double_click, args)
        else:
            self._double_click_time = _time()

    def _on_touch_down_lc(self, args):
        threshold = _LvComp.Operation.GetHoldTimeThresholdInMs() / 1000.0
        self.has_long_clicked = False
        def on_long_click():
            self._vibrate()
            self._exec_callbacks(_ButtonCallback.long_click, args)
            self.has_long_clicked = True
        self._long_click_timer = _LvComp.Game.AddTimer(threshold, on_long_click)

    def _cancel_long_click(self, args):
        _LvComp.Game.CancelTimer(self._long_click_timer)
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
        self.SetCallback(_ButtonCallback.touch_move, self._on_move)

    def _on_touch_down_mov(self, args):
        self.RemoveCallback(_ButtonCallback.touch_move, self._on_move)

    def _vibrate(self):
        _LvComp.Device.SetDeviceVibrate(self.__vibrate_time)

    def _set_offset(self, control, offset):
        control = _ui_utils.to_control(self.screen_node, control)
        orig_pos = control.GetPosition()
        new_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])
        control.SetPosition(new_pos)
        if _ui_utils.is_ui_out_of_screen(control):
            control.SetPosition(orig_pos)














