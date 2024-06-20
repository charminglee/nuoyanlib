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
#   Last Modified : 2024-06-19
#
# ====================================================


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
from ..._core._client._listener import (
    listen_custom as _listen_custom,
    event as _event,
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
from .item_fly_anim import ItemFlyAnim as _ItemFlyAnim
from .item_tips_box import ItemTipsBox as _ItemTipsBox
from .item_grid_manager import ItemGridManager as _ItemGridManager


__all__ = [
    "notify_server",
    "NuoyanScreenNode",
]


def notify_server(func):
    """
    | 函数装饰器，用于按钮的回调函数。
    | 被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。
    | 服务端同名函数的参数与按钮回调函数的参数相同，且自带一个名为 ``__id__`` 的key，其value为触发按钮的玩家实体ID。
    | 可通过 args['cancel_notify'] = False 或 return -1 的方式取消触发服务端函数。
    | 若对按钮回调参数进行修改（如增加、修改或删除某个key或value），服务端得到的参数为修改后的参数，可通过该方式向服务端传递更多信息。
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
        if param is None:
            param = {}
        # 功能组合
        self.__lib_sys = _get_lib_system()
        self.__screen_node = param.get('screen_node', self)
        enable_ifa = param.get('enable_item_fly_anim', False)
        enable_itb = param.get('enable_item_tips_box', False)
        enable_igm = param.get('enable_item_grid', False)
        self.__ifa_ins = _ItemFlyAnim(self.__screen_node) if enable_ifa or enable_igm else None
        self.__itb_ins = _ItemTipsBox(self.__screen_node) if enable_itb or enable_igm else None
        self.__igm_ins = _ItemGridManager(self, self.__ifa_ins, self.__itb_ins) if enable_igm else None
        self.__compose_ins = (self.__ifa_ins, self.__itb_ins, self.__igm_ins)
        # 私有属性
        self.__btn_double_click_data = {}
        self.__double_click_args = None
        self._vibrate_time = 100
        self.__btn_long_click_data = {}
        self.__btn_touch_data = {}
        self.__touching_button_args = {}
        self.__btn_movable_data = {}
        self.__btn_touch_up_data = {}
        self.__move_after_lc_data = {}
        self.__save_pos_uis = set()
        self.__double_click_tick = 0
        self.__double_click_btn_path = ""
        self.__finger_pos = None
        self.__is_moving = False
        self.__touching_btn_path = ""
        self.__tick = 0
        self.__ui_pos_key = self.__class__.__name__ + "_ui_pos_data"
        # 公共属性
        self.cs = param.get('__cs__')
        self.screen_size = _LvComp.Game.GetScreenSize()
        _listen_custom(self)

    def __getattr__(self, name):
        for ins in self.__compose_ins:
            if ins and hasattr(ins, name):
                return getattr(ins, name)
        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

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
        super(NuoyanScreenNode, self).Create()
        self._super("Create")
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
        self._super("Update")
        if self.__double_click_tick:
            self.__double_click_tick += 1
            if self.__double_click_tick == 11:
                self.__double_click_tick = 0
        if 1 <= self.__tick <= 20:
            self.__tick += 1
            if self.__tick == 21 and self.__touching_btn_path in self.__btn_long_click_data:
                btn_data = self.__btn_long_click_data[self.__touching_btn_path]
                btn_data['on_long_click'](self.__touching_button_args)
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
        self._super("Destroy")
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

    # New Interfaces ===================================================================================================

    def GetDirectChildrenPath(self, control):
        """
        | 获取控件的所有一级子控件的路径。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，图片为面板的二级子控件，以此类推。

        -----

        :param str|BaseUIControl control: 控件路径或控件实例

        :return: 控件所有一级子控件的路径的列表，获取不到返回空列表
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
        self.__btn_double_click_data[btn_path] = {
            'on_double_click': on_double_click,
            'on_touch_up': on_touch_up,
        }
        btn_ctrl = self.__screen_node.GetBaseUIControl(btn_path).asButton()
        btn_ctrl.SetButtonTouchUpCallback(self._run_touch_up_list)
        if btn_path not in self.__btn_touch_up_data:
            self.__btn_touch_up_data[btn_path] = []
        if on_touch_up and on_touch_up not in self.__btn_touch_up_data[btn_path]:
            self.__btn_touch_up_data[btn_path].append(on_touch_up)
        self.__btn_touch_up_data[btn_path].append(self._on_btn_touch_up)

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
        self.__btn_movable_data[btn_path] = {
            'move_parent': move_parent,
            'associated_path': associated_path,
            'on_touch_move': on_touch_move
        }
        btn = self.__screen_node.GetBaseUIControl(btn_path).asButton()
        btn.SetButtonTouchMoveCallback(self._on_move)
        self.__save_pos_uis.update(associated_path)
        if move_parent:
            self.__save_pos_uis.add(_get_parent_path(btn_path))
        else:
            self.__save_pos_uis.add(btn_path)

    def CancelButtonMovable(self, btn_path):
        """
        | 取消按钮可拖动。

        -----

        :param str btn_path: 按钮路径

        :return: 无
        :rtype: None
        """
        if btn_path in self.__btn_movable_data:
            orig_callback = self.__btn_movable_data[btn_path]['on_touch_move']
            self.__screen_node.GetBaseUIControl(btn_path).asButton().SetButtonTouchMoveCallback(orig_callback)
            del self.__btn_movable_data[btn_path]

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
        self.__move_after_lc_data[btn_path] = {
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
        self.__btn_long_click_data[btn_path] = {
            'on_long_click': on_long_click,
            'hasLongClicked': False
        }
        self.__btn_touch_data[btn_path] = {
            'on_touch_move_out': on_touch_move_out,
            'on_touch_down': on_touch_down,
            'on_touch_cancel': on_touch_cancel
        }
        btn = self.__screen_node.GetBaseUIControl(btn_path).asButton()
        btn.SetButtonTouchMoveOutCallback(self._on_touch_move_out)
        btn.SetButtonTouchDownCallback(self._on_touch_down)
        btn.SetButtonTouchCancelCallback(self._on_touch_cancel)
        btn.SetButtonTouchUpCallback(self._run_touch_up_list)
        if btn_path not in self.__btn_touch_up_data:
            self.__btn_touch_up_data[btn_path] = []
        self.__btn_touch_up_data[btn_path].append(self._on_touch_up)
        if on_touch_up and on_touch_up not in self.__btn_touch_up_data[btn_path]:
            self.__btn_touch_up_data[btn_path].append(on_touch_up)
        return btn

    def RemoveButtonLongClickCallback(self, btn_path):
        """
        | 移除按钮长按监听。

        -----

        :param str btn_path: 按钮路径

        :return: 无
        :rtype: None
        """
        if btn_path in self.__btn_long_click_data:
            del self.__btn_long_click_data[btn_path]

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
        if bp in self.__btn_long_click_data:
            return self.__btn_long_click_data[bp]['hasLongClicked']
        return False

    # Internal =========================================================================================================

    def _super(self, name):
        for ins in self.__compose_ins:
            if ins and hasattr(ins, name):
                getattr(ins, name)()

    def _run_touch_up_list(self, args):
        bp = args['ButtonPath']
        if bp in self.__btn_touch_up_data:
            for func in self.__btn_touch_up_data[bp]:
                func(args)

    def _on_btn_touch_up(self, args):
        bp = args['ButtonPath']
        if bp in self.__btn_double_click_data:
            if self.__double_click_tick and bp == self.__double_click_btn_path:
                self.__btn_double_click_data[bp]['on_double_click'](args)
                self.__double_click_tick = 0
                self.__double_click_btn_path = ""
                self.__double_click_args = None
            else:
                self.__double_click_tick = 1
                self.__double_click_btn_path = bp
                self.__double_click_args = args

    def _on_touch_up(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self.__btn_long_click_data:
            self.__tick = 0

    def _on_touch_cancel(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self.__btn_long_click_data:
            self.__tick = 0
        if btn_path in self.__btn_touch_data:
            data = self.__btn_touch_data[btn_path]
            if data['on_touch_cancel']:
                data['on_touch_cancel'](args)

    def _on_touch_move_out(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self.__btn_long_click_data:
            self.__tick = 0
        if btn_path in self.__btn_touch_data:
            data = self.__btn_touch_data[btn_path]
            if data['on_touch_move_out']:
                data['on_touch_move_out'](args)

    def _on_touch_down(self, args):
        btn_path = args['ButtonPath']
        if btn_path in self.__btn_long_click_data:
            self.__touching_button_args = args
            self.__touching_btn_path = btn_path
            self.__tick = 1
            self.__btn_long_click_data[btn_path]['hasLongClicked'] = False
        if btn_path in self.__btn_touch_data:
            data = self.__btn_touch_data[btn_path]
            if data['on_touch_down']:
                data['on_touch_down'](args)

    def _on_long_click(self, args):
        bp = args['ButtonPath']
        if bp not in self.__move_after_lc_data:
            return
        data = self.__move_after_lc_data[bp]
        arg1 = data['move_parent']
        arg2 = data['associated_path']
        arg3 = data['on_touch_move']
        self.SetButtonMovable(bp, arg1, arg2, arg3)
        if data['on_long_click']:
            data['on_long_click'](args)

    def _on_down(self, args):
        bp = args['ButtonPath']
        if bp not in self.__move_after_lc_data:
            return
        self.CancelButtonMovable(bp)
        data = self.__move_after_lc_data[bp]
        if data['on_touch_down']:
            data['on_touch_down'](args)

    def _on_move(self, args):
        touch_x = args['TouchPosX']
        touch_y = args['TouchPosY']
        btn_path = args['ButtonPath']
        if btn_path not in self.__btn_movable_data:
            return
        data = self.__btn_movable_data[btn_path]
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
        for bp in self.__save_pos_uis:
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





















