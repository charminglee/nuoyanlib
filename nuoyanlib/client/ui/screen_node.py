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
#   Last Modified : 2025-02-21
#
# ====================================================


from types import MethodType as _MethodType
from functools import wraps as _wraps
from ..._core._client._comp import (
    CLIENT_ENGINE_NAMESPACE as _CLIENT_ENGINE_NAMESPACE,
    CLIENT_ENGINE_SYSTEM_NAME as _CLIENT_ENGINE_SYSTEM_NAME,
    LvComp as _LvComp,
    ScreenNode as _ScreenNode,
)
from ..._core._client._lib_client import (
    get_lib_system as _get_lib_system,
)
from ..._core._listener import (
    event as _event,
    quick_listen as _quick_listen,
)
from ..setting import (
    read_setting as _read_setting,
    save_setting as _save_setting,
)
from .ui_utils import (
    get_direct_children_path as _get_direct_children_path,
    get_parent_path as _get_parent_path,
    get_parent_control as _get_parent_control,
)
# from .item_fly_anim import ItemFlyAnim as _ItemFlyAnim
# from .item_tips_box import ItemTipsBox as _ItemTipsBox
# from .item_grid_manager import ItemGridManager as _ItemGridManager
from ..._core._logging import log as _log


__all__ = [
    "NuoyanScreenNode",
]


def notify_server(func):
    """
    【已废弃】

    | 函数装饰器，用于按钮的回调函数。
    | 被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。
    | 服务端同名函数的参数与按钮回调函数的参数相同，且自带一个名为 ``__id__`` 的key，其value为触发按钮的玩家实体ID。
    | 可通过 args['cancel_notify'] = True 或 return -1 的方式取消触发服务端函数。
    | 若对按钮回调参数进行修改（如增加、修改或删除某个key或value），服务端得到的参数字典同样为修改后的字典，可通过该方式向服务端传递更多信息。
    """
    @_wraps(func)
    def wrapper(self, args):
        args['cancel_notify'] = False
        ret = func(self, args)
        if args['cancel_notify'] or ret == -1:
            return ret
        del args['cancel_notify']
        _get_lib_system().NotifyToServer("_ButtonCallbackTrigger", {'name': func.__name__, 'args': args})
        return ret
    return wrapper


def _set_touch_up_callback(self, func):
    path = self.GetPath()
    self._nuoyan_screen_node._btn_touch_up_data[path] = func


def _set_touch_down_callback(self, func):
    path = self.GetPath()
    self._nuoyan_screen_node._btn_touch_down_data[path] = func


def _set_touch_move_callback(self, func):
    path = self.GetPath()
    self._nuoyan_screen_node._btn_touch_move_data[path] = func


@_quick_listen
class NuoyanScreenNode(_ScreenNode):
    """
    | ScreenNode扩展类，将自定义UI类继承本类即可使用其全部功能。
    | ``NuoyanScreenNode`` 已启用快捷监听功能，继承 ``NuoyanScreenNode`` 后无需再使用 ``quick_listen`` 装饰器。

    -----

    【注意事项】

    | 1、重写 ``Create`` 、 ``Update`` 或 ``Destroy`` 方法时请调用一次父类的同名方法，如：``super(MyUI,self).Create()``。
    | 2、带有 *[event]* 标签的方法为事件，重写该方法即可使用该事件。
    | 3、带有 *[tick]* 标签的事件为帧事件，需要注意相关逻辑的编写。
    """

    def __init__(self, namespace, name, param):
        super(NuoyanScreenNode, self).__init__(namespace, name, param)
        if param is None:
            param = {}
        # 功能组合
        self.__lib_sys = _get_lib_system()
        self.__screen_node = param.get('screen_node', self) # 兼容UI代理
        # enable_ifa = param.get('enable_item_fly_anim', False)
        # enable_itb = param.get('enable_item_tips_box', False)
        # enable_igm = param.get('enable_item_grid', False)
        # self.__ifa_ins = _ItemFlyAnim(self.__screen_node) if enable_ifa or enable_igm else None
        # self.__itb_ins = _ItemTipsBox(self.__screen_node) if enable_itb or enable_igm else None
        # self.__igm_ins = _ItemGridManager(self, self.__ifa_ins, self.__itb_ins) if enable_igm else None
        # self.__compose_ins = (self.__ifa_ins, self.__itb_ins, self.__igm_ins)
        # 私有属性
        self._btn_double_click_data = {}
        self.__double_click_tick = 0
        self.__double_click_btn_path = ""
        self.__double_click_args = None
        self._btn_long_click_data = {}
        self.__long_click_tick = 0
        self.__long_click_btn_path = ""
        self.__long_click_args = {}
        self.__long_click_threshold = 0
        self._btn_touch_down_data = {}
        self.__btn_movable_data = {}
        self._btn_touch_up_data = {}
        self.__movable_by_lc_data = {}
        self._btn_touch_move_data = {}
        self._vibrate_time = 100
        self.__finger_pos = None
        self.__is_moving = False
        self.__save_pos_uis = set()
        self.__ui_pos_key = self.__class__.__name__ + "_ui_pos_data"
        # 公共属性
        self.cs = param.get('__cs__')
        _log("cs of %s: %s" % (self.__class__.__name__, self.cs), NuoyanScreenNode)
        self.screen_size = _LvComp.Game.GetScreenSize()
        _log("Inited: %s" % self.__class__.__module__, NuoyanScreenNode)

    # def __getattr__(self, name):
    #     for ins in self.__compose_ins:
    #         if ins and hasattr(ins, name):
    #             return getattr(ins, name)
    #     raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    # System Event Callbacks ===========================================================================================

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
        self.__super("Create")
        self._recover_ui_pos()

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
        self.__super("Update")
        # double click
        if self.__double_click_tick:
            self.__double_click_tick += 1
            if self.__double_click_tick >= 11:
                self.__double_click_tick = 0
                self._btn_touch_up_data[self.__double_click_btn_path](self.__double_click_args)
        # long click
        if self.__long_click_tick:
            self.__long_click_tick += 1
            if self.__long_click_tick >= self.__long_click_threshold:
                data = self._btn_long_click_data[self.__long_click_btn_path]
                self.__long_click_tick = 0
                data['on_long_click'](self.__long_click_args)
                data['has_long_clicked'] = True
                self.__vibrate()

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
        self.__super("Destroy")
        self.__lib_sys.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "GetEntityByCoordReleaseClientEvent",
            self, self._on_get_entity_by_coord_release
        )
        self.__lib_sys.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "ScreenSizeChangedClientEvent",
            self, self._on_screen_size_changed
        )

    @_event("ScreenSizeChangedClientEvent")
    def _on_screen_size_changed(self, args):
        self.screen_size = (args['afterX'], args['afterY'])

    @_event("GetEntityByCoordReleaseClientEvent")
    def _on_get_entity_by_coord_release(self, args):
        self._save_ui_pos()
        self.__finger_pos = None

    # Interfaces =======================================================================================================

    def DelUiPosData(self, btn=None):
        """
        | 删除通过 ``SetButtonMovable`` 或 ``SetButtonMovableByLongClick`` 保存的UI位置数据。

        -----

        :param str btn: 要删除数据的按钮路径或ButtonUIControl实例，默认为None，表示删除所有数据

        :return: 无
        :rtype: None
        """
        if btn:
            path = self._get_path(btn)
            data = self._get_ui_pos_data()
            if data and path in data:
                del data[path]
        else:
            data = {}
        _save_setting(self.__ui_pos_key, data, False)

    def GetDirectChildrenPath(self, control):
        """
        | 获取控件的所有直接子控件的路径。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的直接子控件，图片为面板的间接子控件、按钮的直接子控件，以此类推。

        -----

        :param str|BaseUIControl control: 控件路径或控件实例

        :return: 控件所有直接子控件的路径列表，获取不到返回空列表
        :rtype: list[str]
        """
        return _get_direct_children_path(control, self.__screen_node)

    def GetParentPath(self, control):
        """
        | 获取控件的父控件路径。

        -----

        :param str|BaseUIControl control: 控件路径或控件实例

        :return: 父控件路径，获取不到返回None
        :rtype: str|None
        """
        return _get_parent_path(control)

    def GetParentControl(self, control):
        """
        | 获取控件的父控件实例。

        -----

        :param str|BaseUIControl control: 控件路径或控件实例

        :return: 父控件实例（BaseUIControl），获取不到返回None
        :rtype: BaseUIControl|None
        """
        return _get_parent_control(control, self.__screen_node)

    def SetButtonDoubleClickCallback(self, btn, on_double_click):
        """
        | 设置按钮双击监听。
        | 注意：如果按钮还需要设置其他监听（如 ``SetButtonTouchUpCallback`` ，长按监听除外），请在设置了双击监听之后再设置，否则将会失效。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例
        :param function on_double_click: DoubleClick回调函数

        :return: 无
        :rtype: None
        """
        control, path = self._get_control(btn).asButton(), self._get_path(btn)
        self._btn_double_click_data[path] = on_double_click
        self.__override_method(
            control, "SetButtonTouchUpCallback", _set_touch_up_callback, self.__on_touch_up
        )

    def RemoveButtonDoubleClickCallback(self, btn):
        """
        | 移除按钮双击监听。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例

        :return: 无
        :rtype: None
        """
        path = self._get_path(btn)
        if path in self._btn_double_click_data:
            del self._btn_double_click_data[path]

    def SetButtonLongClickCallback(self, btn, on_long_click):
        """
        | 设置按钮长按监听。
        | 注意：如果按钮还需要设置其他监听（如 ``SetButtonTouchUpCallback`` ，双击监听除外），请在设置了长按监听之后再设置，否则将会失效。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例
        :param function on_long_click: LongClick回调函数

        :return: 无
        :rtype: None
        """
        control, path = self._get_control(btn).asButton(), self._get_path(btn)
        self._btn_long_click_data[path] = {
            'on_long_click': on_long_click,
            'has_long_clicked': False,
        }
        self.__override_method(
            control, "SetButtonTouchUpCallback", _set_touch_up_callback, self.__on_touch_up
        )
        self.__override_method(
            control, "SetButtonTouchDownCallback", _set_touch_down_callback, self.__on_touch_down
        )
        self.__override_method(
            control, "SetButtonTouchMoveCallback", _set_touch_move_callback, self.__on_move
        )

    def RemoveButtonLongClickCallback(self, btn):
        """
        | 移除按钮长按监听。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例

        :return: 无
        :rtype: None
        """
        path = self._get_path(btn)
        if path in self._btn_long_click_data:
            del self._btn_long_click_data[path]

    def SetLongClickVibrateTime(self, time):
        """
        | 设置长按后震动反馈的时长。

        -----

        :param int time: 毫秒

        :return: 无
        :rtype: None
        """
        self._vibrate_time = time

    def HasLongClicked(self, btn):
        """
        | 用于判断按钮在当次按下中是否已经触发了长按。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例

        :return: 从按钮按下到触发长按前，该方法返回False；从触发长按到下次按钮按下前，该方法返回True
        :rtype: bool
        """
        path = self._get_path(btn)
        if path in self._btn_long_click_data:
            return self._btn_long_click_data[path]['has_long_clicked']
        return False

    def SetButtonMovable(self, btn, move_parent=False, associated_uis=None, save=True):
        """
        | 设置按钮可拖动（随时拖动）。
        | 注意：如果按钮还需要设置其他监听（如 ``SetButtonTouchUpCallback`` ，双击和长按监听除外），请在调用该接口之后再设置，否则将会失效。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例
        :param bool move_parent: 是否同时拖动父控件，默认为False
        :param str|list[str]|None associated_uis: 关联拖动的其他控件的路径，拖动当前按钮的同时也会同步拖动这些关联控件，可使用列表表示多个路径，默认为None
        :param bool save: 是否保存位置，设为True后下次进入游戏时按钮会恢复到上次位置，默认为True

        :return: 无
        :rtype: None
        """
        control, path = self._get_control(btn).asButton(), self._get_path(btn)
        self.__is_moving = False
        self.__finger_pos = None
        if not associated_uis:
            associated_uis = []
        elif isinstance(associated_uis, str):
            associated_uis = [associated_uis]
        self.__btn_movable_data[path] = {
            'move_parent': move_parent,
            'associated_uis': associated_uis,
        }
        self.__override_method(
            control, "SetButtonTouchMoveCallback", _set_touch_move_callback, self.__on_move
        )
        if save:
            self.__save_pos_uis.update(associated_uis)
            if move_parent:
                self.__save_pos_uis.add(_get_parent_path(path))
            else:
                self.__save_pos_uis.add(path)

    def CancelButtonMovable(self, btn):
        """
        | 取消按钮可拖动。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例

        :return: 无
        :rtype: None
        """
        control, path = self._get_control(btn).asButton(), self._get_path(btn)
        if path in self.__btn_movable_data:
            del self.__btn_movable_data[path]

    def SetButtonMovableByLongClick(self, btn, move_parent=False, associated_uis=None, save=True):
        """
        | 设置按钮长按拖动（长按后才能拖动）。
        | 注意：
        | 1、如果按钮还需要设置其他监听（如 ``SetButtonTouchUpCallback`` ，双击监听除外），请在调用该接口之后再设置，否则将会失效。
        | 2、设置长按拖动后不可再设置长按监听。

        -----

        :param str btn: 按钮路径或ButtonUIControl实例
        :param bool move_parent: 是否同时拖动父控件，默认为False
        :param str|list[str]|None associated_uis: 关联拖动的其他控件的路径，拖动当前按钮的同时也会同步拖动这些关联控件，可使用列表表示多个路径，默认为None
        :param bool save: 是否保存位置，设为True后下次进入游戏时按钮会恢复到上次位置，默认为True

        :return: 无
        :rtype: None
        """
        control, path = self._get_control(btn).asButton(), self._get_path(btn)
        if not associated_uis:
            associated_uis = []
        elif isinstance(associated_uis, str):
            associated_uis = [associated_uis]
        self.__movable_by_lc_data[path] = {
            'move_parent': move_parent,
            'associated_uis': associated_uis,
            'save': save,
        }
        self.SetButtonLongClickCallback(control, self.__on_movable_long_click)

    # Internal =========================================================================================================

    def __super(self, name):
        if NuoyanScreenNode:
            getattr(super(NuoyanScreenNode, self), name)()
        # for ins in self.__compose_ins:
        #     if ins and hasattr(ins, name):
        #         getattr(ins, name)()

    def __override_method(self, control, method_name, func, set_callback):
        method = getattr(control, method_name)
        if method.__func__ is not func:
            control._nuoyan_screen_node = self
            method(set_callback)
            setattr(control, method_name, _MethodType(func, control))

    def _get_control(self, path):
        if isinstance(path, str):
            return self.__screen_node.GetBaseUIControl(path)
        else:
            return path

    def _get_path(self, control):
        if isinstance(control, str):
            return control
        else:
            return control.GetPath()

    def __on_touch_up(self, args):
        bp = args['ButtonPath']
        if bp in self._btn_long_click_data:
            self.__long_click_tick = 0
            if self._btn_long_click_data[bp]['has_long_clicked']:
                return
        if bp in self._btn_double_click_data:
            if self.__double_click_tick and bp == self.__double_click_btn_path:
                self._btn_double_click_data[bp](args)
                self.__double_click_tick = 0
                self.__double_click_btn_path = ""
                self.__double_click_args = None
            else:
                self.__double_click_tick = 1
                self.__double_click_btn_path = bp
                self.__double_click_args = args
            return
        if bp in self._btn_touch_up_data:
            self._btn_touch_up_data[bp](args)

    def __on_touch_down(self, args):
        bp = args['ButtonPath']
        if bp in self._btn_long_click_data:
            self.__long_click_threshold = int(_LvComp.Operation.GetHoldTimeThresholdInMs() / 1000.0 * 30)
            self.__long_click_args = args
            self.__long_click_btn_path = bp
            self.__long_click_tick = 1
            self._btn_long_click_data[bp]['has_long_clicked'] = False
        if bp in self.__movable_by_lc_data:
            self.CancelButtonMovable(bp)
        if bp in self._btn_touch_down_data:
            self._btn_touch_down_data[bp](args)

    def __on_move(self, args):
        touch_x = args['TouchPosX']
        touch_y = args['TouchPosY']
        bp = args['ButtonPath']
        if bp in self.__btn_movable_data:
            data = self.__btn_movable_data[bp]
            move_parent = data['move_parent']
            associated_uis = data['associated_uis']
            self.__is_moving = True
            if not self.__finger_pos:
                self.__finger_pos = (touch_x, touch_y)
            offset = (touch_x - self.__finger_pos[0], touch_y - self.__finger_pos[1])
            self.__finger_pos = (touch_x, touch_y)
            path = _get_parent_path(bp) if move_parent else bp
            self.__set_widget_pos(path, offset)
            for path in associated_uis:
                self.__set_widget_pos(path, offset)
        if bp in self._btn_long_click_data:
            self.__long_click_tick = 0
        if bp in self._btn_touch_move_data:
            self._btn_touch_move_data[bp](args)

    def __on_movable_long_click(self, args):
        bp = args['ButtonPath']
        if bp in self.__movable_by_lc_data:
            args = self.__movable_by_lc_data[bp]
            self.SetButtonMovable(bp, **args)

    def _save_ui_pos(self):
        data = {}
        for bp in self.__save_pos_uis:
            pos = self._get_control(bp).GetPosition()
            if pos[0] < 0 or pos[1] < 0:
                continue
            data[bp] = pos
        _save_setting(self.__ui_pos_key, data, False)

    def _get_ui_pos_data(self):
        return _read_setting(self.__ui_pos_key, False)

    def _recover_ui_pos(self):
        data = self._get_ui_pos_data()
        if data:
            for bp, pos in data.items():
                ui = self._get_control(bp)
                if ui:
                    ui.SetPosition(tuple(pos))
        _log("Ui position data: %s" % data, self.__class__)

    def __vibrate(self):
        _LvComp.Device.SetDeviceVibrate(self._vibrate_time)

    def __set_widget_pos(self, path, offset):
        ctrl = self._get_control(path)
        orig_pos = ctrl.GetPosition()
        new_pos = [orig_pos[0] + offset[0], orig_pos[1] + offset[1]]
        size = ctrl.GetSize()
        # 边界检测
        if new_pos[1] < 0:
            new_pos[1] = 0
        if new_pos[0] < 0:
            new_pos[0] = 0
        if new_pos[1] + size[1] > self.screen_size[1]:
            new_pos[1] = self.screen_size[1] - size[1]
        if new_pos[0] + size[0] > self.screen_size[0]:
            new_pos[0] = self.screen_size[0] - size[0]
        ctrl.SetPosition(tuple(new_pos))





















