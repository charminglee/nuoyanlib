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
#   Last Modified : 2024-04-28
#
# ====================================================


from functools import wraps as _wraps
import mod.client.extraClientApi as _api
from ...config import SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME
from ..setting import (
    read_setting as _read_setting,
    save_setting as _save_setting,
)
from ui_utils import get_parent_path as _get_parent_path
from ...config import (
    MOD_NAME as _MOD_NAME,
    CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME,
)
from ...utils._error import ClientNotFoundError as _ClientNotFoundError
from ..client_system import _ALL_CLIENT_ENGINE_EVENTS
from ..comp import (
    CLIENT_ENGINE_NAMESPACE as _CLIENT_ENGINE_NAMESPACE,
    CLIENT_ENGINE_SYSTEM_NAME as _CLIENT_ENGINE_SYSTEM_NAME,
    LvComp as _LvComp,
    ScreenNode as _ScreenNode,
)


__all__ = [
    "ui_listener",
    "notify_server",
    "NuoyanScreenNode",
]


_lsn_func_args = []


def ui_listener(event_name="", namespace="", system_name="", priority=0):
    """
    | 函数装饰器，通过对函数进行装饰即可实现监听。
    | 省略所有参数时，监听当前服务端传来的与被装饰函数同名的事件。
    | 当指定命名空间和系统名称时，可监听来自其他系统的事件。
    | 监听引擎事件时，只需传入该事件的名称即可，无需传入引擎命名空间和系统名称。

    -----

    【示例】
    ::

        class MyUI(NuoyanScreenNode):
            # 监听当前服务端传来的自定义事件
            @ui_listener("MyCustomEvent1")
            def eventCallback1(self, args):
                pass

            # 监听其他服务端传来的自定义事件
            @ui_listener("MyCustomEvent2", "OtherNamespace", "OtherServer")
            def eventCallback2(self, args):
                pass

            # 监听当前服务端传来的与函数同名的事件
            @ui_listener
            def SomeEvent1(self, args):
                pass

            # 监听其他服务端传来的与函数同名的事件
            @ui_listener(namespace="OtherNamespace", system_name="OtherServer")
            def SomeEvent2(self, args):
                pass

            # 监听引擎事件
            @ui_listener("AddEntityClientEvent")
            def OnAddEntity(self, args):
                pass

    -----

    :param str event_name: 事件名称，默认为空字符串，表示监听与函数同名的事件
    :param str namespace: 指定命名空间，默认为空字符串，表示当前服务端的命名空间
    :param str system_name: 指定系统名称，默认为空字符串，表示当前服务端的系统名称
    :param int priority: 优先级，默认为0
    """
    # todo: 新增功能：UI类Destroy时自动反监听由该装饰器注册的事件
    if callable(event_name):
        _add_listener(event_name)
        return event_name
    else:
        if not namespace and not system_name:
            if event_name in _ALL_CLIENT_ENGINE_EVENTS:
                namespace = _CLIENT_ENGINE_NAMESPACE
                system_name = _CLIENT_ENGINE_SYSTEM_NAME
            else:
                namespace = _MOD_NAME
                system_name = _SERVER_SYSTEM_NAME
        elif not namespace:
            raise AssertionError("Missing parameter 'namespace'.")
        elif not system_name:
            raise AssertionError("Missing parameter 'system_name'.")
        def decorator(func):
            _add_listener(func, event_name, namespace, system_name, priority)
            return func
        return decorator


def _add_listener(func, event_name="", namespace=_MOD_NAME, system_name=_SERVER_SYSTEM_NAME, priority=0):
    if not event_name:
        event_name = func.__name__
    _lsn_func_args.append((namespace, system_name, event_name, func, priority))


def _listen(self):
    for args in _lsn_func_args:
        func = args[3]
        method = getattr(self, func.__name__, None)
        if method and method.__func__ is func:
            self.cs.ListenForEvent(args[0], args[1], args[2], self, method, args[4])


def notify_server(func):
    """
    | 函数装饰器，用于按钮的回调函数。
    | 被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。
    | 服务端同名函数的参数与按钮回调函数的参数相同，且自带一个名为 ``__id__`` 的key，其value为触发按钮的玩家实体ID。
    | 可通过 args['cancelNotify'] = False 或 return -1 的方式取消触发服务端函数。
    | 若对按钮回调参数进行修改（如增加、修改或删除某个key或value），服务端得到的参数为修改后的参数，可通过该方式向服务端传递更多信息。
    """
    @_wraps(func)
    def wrapper(self, args):
        args['cancelNotify'] = False
        ret = func(self, args)
        if ('cancelNotify' in args and args['cancelNotify']) or ret == -1:
            return ret
        cs = _api.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        if cs:
            args['__name__'] = func.__name__
            cs.NotifyToServer("_ButtonCallbackTriggered", args)
        return ret
    return wrapper


class NuoyanScreenNode(_ScreenNode):
    """
    | ScreenNode扩展类，将自定义UI类继承本类即可使用本类的全部功能。

    -----

    | 注意事项：
    | 1、重写 ``Create`` 或 ``Update`` 方法时请调用一次父类的同名方法，如： ``super(MyUI, self).Create()`` 或 ``NuoyanScreenNode.Create(self)`` 。
    | 2、带有 *[event]* 标签的方法为事件，重写该方法即可使用该事件。
    | 3、带有 *[tick]* 标签的事件为帧事件，需要注意相关逻辑的编写。
    """

    def __init__(self, namespace, name, param):
        super(NuoyanScreenNode, self).__init__(namespace, name, param)
        if param and '__cs__' in param:
            self.cs = param['__cs__']
        else:
            self.cs = _api.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        if not self.cs:
            raise _ClientNotFoundError
        self.__screen_node = param['_screen_node'] if param and '_screen_node' in param else self
        self.screen_size = _LvComp.Game.GetScreenSize()
        self._btn_double_click_data = {}
        self._double_click_args = None
        self._vibrate_time = 100
        self._btn_long_click_data = {}
        self._btn_touch_data = {}
        self._touching_button_args = {}
        self._btn_movable_data = {}
        self._btn_touch_up_data = {}
        self._move_after_lc_data = {}
        self._save_pos_uis = set()
        self.__double_click_tick = 0
        self.__double_click_btn_path = ""
        self.__finger_pos = None
        self.__is_moving = False
        self.__touching_btn_path = ""
        self.__tick = 0
        self.__ui_pos_key = self.__class__.__name__ + "_ui_pos_data"
        _listen(self)

    def Create(self):
        """
        *[event]*

        | UI生命周期函数，当UI创建成功时调用。
        | 若重写了该方法，请调用一次父类的同名方法，否则部分功能将不可用。如：
        ::

            class MyUI(NuoyanScreenNode):
                def Create(self):
                    super(MyUI, self).Create()

        -----

        :return: 无
        :rtype: None
        """
        super(NuoyanScreenNode, self).Create()
        data = _read_setting(self.__ui_pos_key, False)
        if data:
            for bp, pos in data.items():
                ui = self.__screen_node.GetBaseUIControl(bp)
                if ui:
                    ui.SetPosition(tuple(pos))

    def Update(self):
        """
        *[tick]* *[event]*

        | 客户端每帧调用。
        | 若重写了该方法，请调用一次父类的同名方法。如：
        ::

            class MyUI(NuoyanScreenNode):
                def Update(self):
                    super(MyUI, self).Update()

        -----

        :return: 无
        :rtype: None
        """
        super(NuoyanScreenNode, self).Update()
        if self.__double_click_tick:
            self.__double_click_tick += 1
            if self.__double_click_tick == 11:
                self.__double_click_tick = 0
        if 1 <= self.__tick <= 20:
            self.__tick += 1
            if self.__tick == 21 and self.__touching_btn_path in self._btn_long_click_data:
                btn_data = self._btn_long_click_data[self.__touching_btn_path]
                btn_data['on_long_click'](self._touching_button_args)
                btn_data['hasLongClicked'] = True
                self._vibrate()

    def Destroy(self):
        """
        *[event]*

        | UI生命周期函数，当UI销毁时调用。
        | 若重写了该方法，请调用一次父类的同名方法。如：
        ::

            class MyUI(NuoyanScreenNode):
                def Destroy(self):
                    super(MyUI, self).Destroy()

        -----

        :return: 无
        :rtype: None
        """
        super(NuoyanScreenNode, self).Destroy()
        self.cs.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "GetEntityByCoordReleaseClientEvent",
            self, self._GetEntityByCoordReleaseClientEvent
        )
        self.cs.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "ScreenSizeChangedClientEvent",
            self, self._ScreenSizeChangedClientEvent
        )

    def OnDeactive(self):
        """
        *[event]*

        | UI生命周期函数，当栈顶UI有其他UI入栈时调用。
        | 不建议使用在 ``OnDeactive`` 函数中调用 ``SetScreenVisible(False)`` ，在 ``OnActive`` 函数中调用 ``SetScreenVisible(True)`` 的方式实现打开新界面时隐藏原界面，新界面关闭时自动显示原界面的功能，由于隐藏接口不会改动UI栈，多Mod容易形成冲突。推荐使用 ``PushScreen`` ， ``PopScreen`` 接口实现。
        | 若重写了该方法，请调用一次父类的同名方法。如：
        ::

            class MyUI(NuoyanScreenNode):
                def OnDeactive(self):
                    super(MyUI, self).OnDeactive()

        -----

        :return: 无
        :rtype: None
        """
        super(NuoyanScreenNode, self).OnDeactive()

    def OnActive(self):
        """
        *[event]*

        | UI生命周期函数，当UI重新回到栈顶时调用。
        | 不建议使用在 ``OnDeactive`` 函数中调用 ``SetScreenVisible(False)`` ，在 ``OnActive`` 函数中调用 ``SetScreenVisible(True)`` 的方式实现打开新界面时隐藏原界面，新界面关闭时自动显示原界面的功能，由于隐藏接口不会改动UI栈，多Mod容易形成冲突。推荐使用 ``PushScreen`` ， ``PopScreen`` 接口实现。
        | 若重写了该方法，请调用一次父类的同名方法。如：
        ::

            class MyUI(NuoyanScreenNode):
                def OnActive(self):
                    super(MyUI, self).OnActive()

        -----

        :return: 无
        :rtype: None
        """
        super(NuoyanScreenNode, self).OnActive()

    # ================================================ New Interface ===================================================

    def SetButtonDoubleClickCallback(self, btn_path, on_double_click, on_touch_up=None):
        """
        | 设置按钮双击监听。

        -----

        :param str btn_path: 按钮路径
        :param function on_double_click: DoubleClick回调函数
        :param function|None on_touch_up: TouchUp回调函数，默认为None

        :return: 无
        :rtype: None
        """
        self._btn_double_click_data[btn_path] = {
            'on_double_click': on_double_click,
            'on_touch_up': on_touch_up,
        }
        btn_ctrl = self.__screen_node.GetBaseUIControl(btn_path).asButton()
        btn_ctrl.SetButtonTouchUpCallback(self._run_touch_up_list)
        if btn_path not in self._btn_touch_up_data:
            self._btn_touch_up_data[btn_path] = []
        if on_touch_up and on_touch_up not in self._btn_touch_up_data[btn_path]:
            self._btn_touch_up_data[btn_path].append(on_touch_up)
        self._btn_touch_up_data[btn_path].append(self._on_btn_touch_up)

    def SetButtonMovable(self, btn_path, move_parent=False, associated_path=None, on_touch_move=None):
        """
        | 设置按钮可拖动。

        -----

        :param str btn_path: 按钮路径
        :param bool move_parent: 是否同时拖动父控件，默认为False
        :param str|tuple[str]|None associated_path: 关联拖动的其他控件的路径，多个控件请使用元组，默认为None
        :param function|None on_touch_move: TouchMove回调函数，默认为None

        :return: 无
        :rtype: None
        """
        self.__is_moving = False
        self.__finger_pos = None
        if not associated_path:
            associated_path = ()
        elif isinstance(associated_path, str):
            associated_path = (associated_path,)
        self._btn_movable_data[btn_path] = {
            'move_parent': move_parent,
            'associated_path': associated_path,
            'on_touch_move': on_touch_move
        }
        btn = self.__screen_node.GetBaseUIControl(btn_path).asButton()
        btn.SetButtonTouchMoveCallback(self._on_move)
        self._save_pos_uis.update(associated_path)
        if move_parent:
            self._save_pos_uis.add(_get_parent_path(btn_path))
        else:
            self._save_pos_uis.add(btn_path)

    def CancelButtonMovable(self, btn_path):
        """
        | 取消按钮可拖动。

        -----

        :param str btn_path: 按钮路径

        :return: 无
        :rtype: None
        """
        if btn_path in self._btn_movable_data:
            orig_callback = self._btn_movable_data[btn_path]['on_touch_move']
            self.__screen_node.GetBaseUIControl(btn_path).asButton().SetButtonTouchMoveCallback(orig_callback)
            del self._btn_movable_data[btn_path]

    def SetButtonMovableAfterLongClick(
            self,
            btn_path,
            move_parent=False,
            associated_path=None,
            on_touch_up=None,
            on_long_click=None,
            on_touch_move=None,
            on_touch_move_out=None,
            on_touch_down=None,
            on_touch_cancel=None,
    ):
        """
        | 设置按钮长按拖动。该方法设置的按钮拖动会自动保存位置，下次启动游戏时按钮会恢复到上次游戏时的位置。

        -----

        :param str btn_path: 按钮路径
        :param bool move_parent: 是否同时拖动父控件，默认为False
        :param str|tuple[str]|None associated_path: 关联拖动的其他控件的路径，多个控件请使用元组，默认为None
        :param function|None on_touch_up: TouchUp回调函数，默认为None
        :param function|None on_long_click: LongClick回调函数，默认为None
        :param function|None on_touch_move: TouchMove回调函数，默认为None
        :param function|None on_touch_move_out: TouchMoveOut回调函数，默认为None
        :param function|None on_touch_down: TouchDown回调函数，默认为None
        :param function|None on_touch_cancel: TouchCancel回调函数，默认为None

        :return: 按钮的ButtonUIControl实例，设置失败时返回None
        :rtype: ButtonUIControl|None
        """
        if not associated_path:
            associated_path = ()
        elif isinstance(associated_path, str):
            associated_path = (associated_path,)
        btn = self.SetButtonLongClickCallback(
            btn_path, self._on_long_click, on_touch_up, on_touch_move_out, self._on_down, on_touch_cancel
        )
        self._move_after_lc_data[btn_path] = {
            'move_parent': move_parent,
            'associated_path': associated_path,
            'on_touch_move': on_touch_move,
            'on_long_click': on_long_click,
            'on_touch_down': on_touch_down,
        }
        return btn

    def SetButtonLongClickCallback(
            self,
            btn_path,
            on_long_click,
            on_touch_up=None,
            on_touch_move_out=None,
            on_touch_down=None,
            on_touch_cancel=None,
    ):
        """
        | 设置按钮长按监听。

        -----

        :param str btn_path: 按钮路径
        :param function on_long_click: LongClick回调函数
        :param function|None on_touch_up: TouchUp回调函数，默认为None
        :param function|None on_touch_move_out: TouchMoveOut回调函数，默认为None
        :param function|None on_touch_down: TouchDown回调函数，默认为None
        :param function|None on_touch_cancel: TouchCancel回调函数，默认为None

        :return: 按钮的ButtonUIControl实例，设置失败时返回None
        :rtype: ButtonUIControl|None
        """
        self._btn_long_click_data[btn_path] = {
            'on_long_click': on_long_click,
            'hasLongClicked': False
        }
        self._btn_touch_data[btn_path] = {
            'on_touch_move_out': on_touch_move_out,
            'on_touch_down': on_touch_down,
            'on_touch_cancel': on_touch_cancel
        }
        btn = self.__screen_node.GetBaseUIControl(btn_path).asButton()
        btn.SetButtonTouchMoveOutCallback(self._on_touch_move_out)
        btn.SetButtonTouchDownCallback(self._on_touch_down)
        btn.SetButtonTouchCancelCallback(self._on_touch_cancel)
        btn.SetButtonTouchUpCallback(self._run_touch_up_list)
        if btn_path not in self._btn_touch_up_data:
            self._btn_touch_up_data[btn_path] = []
        self._btn_touch_up_data[btn_path].append(self._on_touch_up)
        if on_touch_up and on_touch_up not in self._btn_touch_up_data[btn_path]:
            self._btn_touch_up_data[btn_path].append(on_touch_up)
        return btn

    def RemoveButtonLongClickCallback(self, btn_path):
        """
        | 移除按钮长按监听。

        -----

        :param str btn_path: 按钮路径

        :return: 无
        :rtype: None
        """
        if btn_path in self._btn_long_click_data:
            del self._btn_long_click_data[btn_path]

    def SetLongClickVibrateTime(self, time):
        """
        | 设置长按后震动反馈的时长。

        -----

        :param int time: 毫秒

        :return: 无
        :rtype: None
        """
        self._vibrate_time = time

    def HasLongClicked(self, bp):
        """
        | 用于判断按钮在当次按下中是否已经触发了长按。

        -----

        :param str bp: 按钮路径

        :return: 从按钮按下到触发长按前，该方法返回False；从触发长按到下次按钮按下前，该方法返回True
        :rtype: bool
        """
        if bp in self._btn_long_click_data:
            return self._btn_long_click_data[bp]['hasLongClicked']
        return False

    # =========================================== Internal Method ======================================================

    @ui_listener("ScreenSizeChangedClientEvent")
    def _ScreenSizeChangedClientEvent(self, args):
        self.screen_size = args['afterX'], args['afterY']

    @ui_listener("GetEntityByCoordReleaseClientEvent")
    def _GetEntityByCoordReleaseClientEvent(self, args):
        self._save_ui_pos()
        self.__finger_pos = None

    def _run_touch_up_list(self, args):
        bp = args['ButtonPath']
        if bp in self._btn_touch_up_data:
            for func in self._btn_touch_up_data[bp]:
                func(args)

    def _on_btn_touch_up(self, args):
        bp = args['ButtonPath']
        if bp in self._btn_double_click_data:
            if self.__double_click_tick and bp == self.__double_click_btn_path:
                self._btn_double_click_data[bp]['on_double_click'](args)
                self.__double_click_tick = 0
                self.__double_click_btn_path = ""
                self._double_click_args = None
            else:
                self.__double_click_tick = 1
                self.__double_click_btn_path = bp
                self._double_click_args = args

    def _on_touch_up(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self._btn_long_click_data:
            self.__tick = 0

    def _on_touch_cancel(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self._btn_long_click_data:
            self.__tick = 0
        if btn_path in self._btn_touch_data:
            data = self._btn_touch_data[btn_path]
            if data['on_touch_cancel']:
                data['on_touch_cancel'](args)

    def _on_touch_move_out(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self._btn_long_click_data:
            self.__tick = 0
        if btn_path in self._btn_touch_data:
            data = self._btn_touch_data[btn_path]
            if data['on_touch_move_out']:
                data['on_touch_move_out'](args)

    def _on_touch_down(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self._btn_long_click_data:
            self._touching_button_args = args
            self.__touching_btn_path = btn_path
            self.__tick = 1
            self._btn_long_click_data[btn_path]['hasLongClicked'] = False
        if btn_path in self._btn_touch_data:
            data = self._btn_touch_data[btn_path]
            if data['on_touch_down']:
                data['on_touch_down'](args)

    def _on_long_click(self, args):
        bp = args['ButtonPath']
        if bp not in self._move_after_lc_data:
            return
        data = self._move_after_lc_data[bp]
        arg1 = data['move_parent']
        arg2 = data['associated_path']
        arg3 = data['on_touch_move']
        self.SetButtonMovable(bp, arg1, arg2, arg3)
        if data['on_long_click']:
            data['on_long_click'](args)

    def _on_down(self, args):
        bp = args['ButtonPath']
        if bp not in self._move_after_lc_data:
            return
        self.CancelButtonMovable(bp)
        data = self._move_after_lc_data[bp]
        if data['on_touch_down']:
            data['on_touch_down'](args)

    def _on_move(self, args):
        touch_x = args['TouchPosX']
        touch_y = args['TouchPosY']
        btn_path = args['ButtonPath']
        if btn_path not in self._btn_movable_data:
            return
        data = self._btn_movable_data[btn_path]
        move_parent = data['move_parent']
        associated_path = data['associated_path']
        on_touch_move = data['on_touch_move']
        self.__is_moving = True
        if not self.__finger_pos:
            self.__finger_pos = (touch_x, touch_y)
        offset = (touch_x - self.__finger_pos[0], touch_y - self.__finger_pos[1])
        self.__finger_pos = (touch_x, touch_y)
        if not move_parent:
            btn = self.__screen_node.GetBaseUIControl(btn_path)
            self._set_widget_pos(btn, offset)
        else:
            parent_path = _get_parent_path(btn_path)
            ctrl = self.__screen_node.GetBaseUIControl(parent_path)
            self._set_widget_pos(ctrl, offset)
        for path in associated_path:
            ctrl = self.__screen_node.GetBaseUIControl(path)
            self._set_widget_pos(ctrl, offset)
        if on_touch_move:
            on_touch_move(args)

    def _save_ui_pos(self):
        data = {}
        for bp in self._save_pos_uis:
            pos = self.__screen_node.GetBaseUIControl(bp).GetPosition()
            if pos[0] < 0 or pos[1] < 0:
                continue
            data[bp] = pos
        _save_setting(self.__ui_pos_key, data, False)

    def _vibrate(self):
        _LvComp.Device.SetDeviceVibrate(self._vibrate_time)

    def _test_pos_is_out(self, pos, button_size):
        if pos[1] < 0:
            pos[1] = 0
        if pos[0] < 0:
            pos[0] = 0
        if pos[1] + button_size[1] > self.screen_size[1]:
            pos[1] = self.screen_size[1] - button_size[1]
        if pos[0] + button_size[0] > self.screen_size[0]:
            pos[0] = self.screen_size[0] - button_size[0]

    def _set_widget_pos(self, widget_ctrl, offset):
        orig_pos = widget_ctrl.GetPosition()
        new_pos = [orig_pos[0] + offset[0], orig_pos[1] + offset[1]]
        self._test_pos_is_out(new_pos, widget_ctrl.GetSize())
        widget_ctrl.SetPosition(tuple(new_pos))






















