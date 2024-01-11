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
#   Last Modified : 2023-12-24
#
# ====================================================


"""

nuoyanScreenNode
================

该模块为ScreenNode提供了扩展功能。

-----

使用方法：

1、将您的UI类继承NuoyanScreenNode，例如class MyUi(NuoyanScreenNode)，即可使用该模块提供的扩展功能，此后无需再继承ScreenNode。

"""


from functools import wraps as _wraps
import mod.client.extraClientApi as api
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
from ..client_system import ALL_CLIENT_ENGINE_EVENTS as _ALL_CLIENT_ENGINE_EVENTS
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


_lsnFuncArgs = []


def _add_listener(func, eventName="", namespace=_MOD_NAME, systemName=_SERVER_SYSTEM_NAME, priority=0):
    if not eventName:
        eventName = func.__name__
    _lsnFuncArgs.append((namespace, systemName, eventName, func, priority))


def ui_listener(eventName="", namespace="", systemName="", priority=0):
    """
    函数装饰器，通过对函数进行装饰即可实现监听。

    省略所有参数时，监听当前服务端传来的与被装饰函数同名的事件。

    当指定命名空间和系统名称时，可监听来自其他系统的事件。

    监听引擎事件时，只需传入该事件的名称即可，无需传入引擎命名空间和系统名称。

    -----

    【示例】

    >>> class MyUI(NuoyanScreenNode):
    ...     @ui_listener("MyCustomEvent1")  # 监听当前服务端传来的自定义事件
    ...     def eventCallback1(self, args):
    ...         pass
    ...
    ...     @ui_listener("MyCustomEvent2", "OtherNamespace", "OtherServer")  # 监听其他服务端传来的自定义事件
    ...     def eventCallback2(self, args):
    ...         pass
    ...
    ...     @ui_listener  # 监听当前服务端传来的与函数同名的事件
    ...     def SomeEvent1(self, args):
    ...         pass
    ...
    ...     @ui_listener(namespace="OtherNamespace", systemName="OtherServer")  # 监听其他服务端传来的与函数同名的事件
    ...     def SomeEvent2(self, args):
    ...         pass
    ...
    ...     @ui_listener("AddEntityClientEvent")  # 监听引擎事件
    ...     def OnAddEntity(self, args):
    ...         pass

    -----

    :param str eventName: 事件名称，默认为空字符串，表示监听与函数同名的事件
    :param str namespace: 指定命名空间，默认为空字符串，表示当前服务端的命名空间
    :param str systemName: 指定系统名称，默认为空字符串，表示当前服务端的系统名称
    :param int priority: 优先级，默认为0
    """
    if callable(eventName):
        _add_listener(eventName)
        return eventName
    else:
        if not namespace and not systemName:
            if eventName in _ALL_CLIENT_ENGINE_EVENTS:
                namespace = _CLIENT_ENGINE_NAMESPACE
                systemName = _CLIENT_ENGINE_SYSTEM_NAME
            else:
                namespace = _MOD_NAME
                systemName = _SERVER_SYSTEM_NAME
        elif not namespace:
            raise AssertionError("Missing parameter 'namespace'.")
        elif not systemName:
            raise AssertionError("Missing parameter 'systemName'.")
        def decorator(func):
            _add_listener(func, eventName, namespace, systemName, priority)
            return func
        return decorator


def notify_server(func):
    """
    函数装饰器，用于按钮的回调函数。

    被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。

    服务端同名函数的参数与按钮回调函数的参数相同，且自带一个名为__id__的key，其value为触发按钮的玩家实体ID。

    可通过args['cancelNotify'] = False或return -1的方式取消触发服务端函数。

    若对按钮回调参数进行修改（如增加、修改或删除某个key或value），服务端得到的参数为修改后的参数，可通过该方式向服务端传递更多信息。
    """
    @_wraps(func)
    def wrapper(self, args):
        args['cancelNotify'] = False
        ret = func(self, args)
        if ('cancelNotify' in args and args['cancelNotify']) or ret == -1:
            return ret
        cs = api.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        if cs:
            args['__name__'] = func.__name__
            cs.NotifyToServer("_ButtonCallbackTriggered", args)
        return ret
    return wrapper


class NuoyanScreenNode(_ScreenNode):
    """
    ScreenNode扩展类。将自定义UI类继承本类即可使用本类的全部功能。

    -----

    接口一览：

    1、SetButtonDoubleClickCallback：设置按钮双击监听。

    2、SetButtonMovable：设置按钮可拖动。

    3、CancelButtonMovable：取消按钮可拖动。

    4、SetButtonLongClickCallback：设置按钮长按监听。

    5、RemoveButtonLongClickCallback：移除按钮长按监听。

    6、SetLongClickVibrateTime：设置长按后震动反馈的时长。

    7、HasLongClicked：用于判断按钮在当次按下中是否已经触发了长按。

    8、SetButtonMovableAfterLongClick：设置按钮长按拖动。

    -----

    属性一览：

    1、cs：客户端系统实例，可直接使用该属性在UI类中调用客户端的接口、方法、属性等，如self.cs.NotifyToServer(...)、self.cs.xxx = ...。

    2、screenSize: 屏幕尺寸元组，(宽度, 高度)；屏幕尺寸改变时，该属性也会跟着改变。

    -----

    注意事项：

    1、重写Create或Update方法时请调用一次父类的同名方法，如：super(MyUI, self).Create()或NuoyanScreenNode.Create(self)。

    2、带有 *[event]* 标签的方法为事件，重写该方法即可使用该事件。

    3、带有 *[tick]* 标签的事件为帧事件，需要注意相关逻辑的编写。
    """

    def __init__(self, namespace, name, param):
        # noinspection PySuperArguments
        super(NuoyanScreenNode, self).__init__(namespace, name, param)
        self.cs = api.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        if not self.cs:
            raise _ClientNotFoundError
        self.screenSize = _LvComp.Game.GetScreenSize()
        self._btnDoubleClickData = {}
        self._doubleClickArgs = None
        self._vibrateTime = 100
        self._btnLongClickData = {}
        self._btnTouchData = {}
        self._touchingButtonArgs = {}
        self._btnMovableData = {}
        self._btnTouchUpCallbackData = {}
        self._moveAfterLCData = {}
        self._savePosUis = set()
        self.__doubleClickTick = 0
        self.__doubleClickBtnPath = ""
        self.__fingerPos = None
        self.__isMoving = False
        self.__touchingButtonPath = ""
        self.__tick = 0
        self.__uiPosKey = self.__class__.__name__ + "_ui_pos_data"
        self.__listen()

    def Create(self):
        """
        *[event]*

        UI生命周期函数，当UI创建成功时调用。

        若重写该方法，请调用一次NuoyanScreenNode的同名方法，否则部分功能将不可用。如：

        >>> class MyUI(NuoyanScreenNode):
        ...     def __init__(self, namespace, name, param):
        ...         pass
        ...     def Create(self):
        ...         super(MyUI, self).Create()  # 或者：NuoyanScreenNode.Create(self)

        -----

        :return: 无
        :rtype: None
        """
        uiPosData = _read_setting(self.__uiPosKey, False)
        if uiPosData:
            for bp, pos in uiPosData.items():
                ui = self.GetBaseUIControl(bp)
                if ui:
                    ui.SetPosition(tuple(pos))

    @ui_listener("OnScriptTickClient")
    def _onTick(self):
        if self.__doubleClickTick:
            self.__doubleClickTick += 1
            if self.__doubleClickTick == 11:
                self.__doubleClickTick = 0
        if 1 <= self.__tick <= 20:
            self.__tick += 1
            if self.__tick == 21 and self.__touchingButtonPath in self._btnLongClickData:
                btnData = self._btnLongClickData[self.__touchingButtonPath]
                btnData['longClickFunc'](self._touchingButtonArgs)
                btnData['hasLongClicked'] = True
                self._vibrate()
        self.OnTick()

    def OnTick(self):
        """
        *[tick]* *[event]*

        客户端每帧调用，1秒有30帧。

        -----

        :return: 无
        :rtype: None
        """

    def Update(self):
        """
        *[tick]* *[event]*

        客户端每帧调用。

        注意：在2.10及以上版本中，该方法的触发频率与游戏实时帧率同步。在2.10以下版本中，触发频率为固定的每秒钟30次。

        -----

        :return: 无
        :rtype: None
        """

    def Destroy(self):
        """
        *[event]*

        UI生命周期函数，当UI销毁时调用。

        -----

        :return: 无
        :rtype: None
        """

    def OnDeactive(self):
        """
        *[event]*

        UI生命周期函数，当栈顶UI有其他UI入栈时调用。

        不建议使用在OnDeactive函数中调用SetScreenVisible(False)，在OnActive函数中调用SetScreenVisible(True)的方式实现打开新界面时隐藏原界面，新界面关闭时自动显示原界面的功能，由于隐藏接口不会改动UI栈，多Mod容易形成冲突。推荐使用PushScreen，PopScreen接口实现。

        -----

        :return: 无
        :rtype: None
        """

    def OnActive(self):
        """
        *[event]*

        UI生命周期函数，当UI重新回到栈顶时调用。

        不建议使用在OnDeactive函数中调用SetScreenVisible(False)，在OnActive函数中调用SetScreenVisible(True)的方式实现打开新界面时隐藏原界面，新界面关闭时自动显示原界面的功能，由于隐藏接口不会改动UI栈，多Mod容易形成冲突。推荐使用PushScreen，PopScreen接口实现。

        -----

        :return: 无
        :rtype: None
        """

    # ========================================== Basic Function ==============================================

    def SetButtonDoubleClickCallback(self, buttonPath, doubleClickCallback, touchUpCallback=None):
        """
        设置按钮双击监听。

        -----

        :param str buttonPath: 按钮路径
        :param function doubleClickCallback: DoubleClick回调函数
        :param function|None touchUpCallback: TouchUp回调函数，默认为None

        :return: 无
        :rtype: None
        """
        self._btnDoubleClickData[buttonPath] = {
            'doubleClickCallback': doubleClickCallback,
            'touchUpCallback': touchUpCallback
        }
        btnCtrl = self.GetBaseUIControl(buttonPath).asButton()
        btnCtrl.SetButtonTouchUpCallback(self._runTouchUpList)
        if buttonPath not in self._btnTouchUpCallbackData:
            self._btnTouchUpCallbackData[buttonPath] = []
        if touchUpCallback and touchUpCallback not in self._btnTouchUpCallbackData[buttonPath]:
            self._btnTouchUpCallbackData[buttonPath].append(touchUpCallback)
        self._btnTouchUpCallbackData[buttonPath].append(self._onBtnTouchUp)

    def SetButtonMovable(self, btnPath, moveParent=False, associatedPath=None, touchMoveCallback=None):
        """
        设置按钮可拖动。

        -----

        :param str btnPath: 按钮路径
        :param bool moveParent: 是否同时拖动父控件，默认为False
        :param str|tuple[str]|None associatedPath: 关联拖动的其他控件的路径，多个控件请使用元组，默认为None
        :param function|None touchMoveCallback: TouchMove回调函数，默认为None

        :return: 无
        :rtype: None
        """
        self.__isMoving = False
        self.__fingerPos = None
        if not associatedPath:
            associatedPath = ()
        elif isinstance(associatedPath, str):
            associatedPath = (associatedPath,)
        self._btnMovableData[btnPath] = {
            'moveParent': moveParent,
            'associatedPath': associatedPath,
            'touchMoveCallback': touchMoveCallback
        }
        btn = self.GetBaseUIControl(btnPath).asButton()
        btn.SetButtonTouchMoveCallback(self._onMove)
        self._savePosUis.update(associatedPath)
        if moveParent:
            self._savePosUis.add(_get_parent_path(btnPath))
        else:
            self._savePosUis.add(btnPath)

    def CancelButtonMovable(self, btnPath):
        """
        取消按钮可拖动。

        :param str btnPath: 按钮路径

        :return: 无
        :rtype: None
        """
        if btnPath in self._btnMovableData:
            origCallback = self._btnMovableData[btnPath]['touchMoveCallback']
            self.GetBaseUIControl(btnPath).asButton().SetButtonTouchMoveCallback(origCallback)
            del self._btnMovableData[btnPath]

    def SetButtonMovableAfterLongClick(
            self,
            btnPath,
            moveParent=False,
            associatedPath=None,
            touchUpFunc=None,
            longClickFunc=None,
            touchMoveCallback=None,
            touchMoveOutFunc=None,
            touchDownFunc=None,
            touchCancelFunc=None,
    ):
        """
        设置按钮长按拖动。该方法设置的按钮拖动会自动保存位置，下次启动游戏时按钮会恢复到上次游戏时的位置。

        -----

        :param str btnPath: 按钮路径
        :param bool moveParent: 是否同时拖动父控件，默认为False
        :param str|tuple[str]|None associatedPath: 关联拖动的其他控件的路径，多个控件请使用元组，默认为None
        :param function|None touchUpFunc: TouchUp回调函数，默认为None
        :param function|None longClickFunc: LongClick回调函数，默认为None
        :param function|None touchMoveCallback: TouchMove回调函数，默认为None
        :param function|None touchMoveOutFunc: TouchMoveOut回调函数，默认为None
        :param function|None touchDownFunc: TouchDown回调函数，默认为None
        :param function|None touchCancelFunc: TouchCancel回调函数，默认为None

        :return: 按钮的ButtonUIControl实例，设置失败时返回None
        :rtype: ButtonUIControl|None
        """
        if not associatedPath:
            associatedPath = ()
        elif isinstance(associatedPath, str):
            associatedPath = (associatedPath,)
        btn = self.SetButtonLongClickCallback(
            btnPath, self._onLongClick, touchUpFunc, touchMoveOutFunc, self._onDown, touchCancelFunc
        )
        self._moveAfterLCData[btnPath] = {
            'moveParent': moveParent,
            'associatedPath': associatedPath,
            'touchMoveCallback': touchMoveCallback,
            'longClickFunc': longClickFunc,
            'touchDownFunc': touchDownFunc,
        }
        return btn

    def SetButtonLongClickCallback(
            self,
            btnPath,
            longClickFunc,
            touchUpFunc=None,
            touchMoveOutFunc=None,
            touchDownFunc=None,
            touchCancelFunc=None,
    ):
        """
        设置按钮长按监听。

        -----

        :param str btnPath: 按钮路径
        :param function longClickFunc: LongClick回调函数
        :param function|None touchUpFunc: TouchUp回调函数，默认为None
        :param function|None touchMoveOutFunc: TouchMoveOut回调函数，默认为None
        :param function|None touchDownFunc: TouchDown回调函数，默认为None
        :param function|None touchCancelFunc: TouchCancel回调函数，默认为None

        :return: 按钮的ButtonUIControl实例，设置失败时返回None
        :rtype: ButtonUIControl|None
        """
        self._btnLongClickData[btnPath] = {
            'longClickFunc': longClickFunc,
            'hasLongClicked': False
        }
        self._btnTouchData[btnPath] = {
            'touchMoveOutFunc': touchMoveOutFunc,
            'touchDownFunc': touchDownFunc,
            'touchCancelFunc': touchCancelFunc
        }
        btn = self.GetBaseUIControl(btnPath).asButton()
        btn.SetButtonTouchMoveOutCallback(self._onTouchMoveOut)
        btn.SetButtonTouchDownCallback(self._onTouchDown)
        btn.SetButtonTouchCancelCallback(self._onTouchCancel)
        btn.SetButtonTouchUpCallback(self._runTouchUpList)
        if btnPath not in self._btnTouchUpCallbackData:
            self._btnTouchUpCallbackData[btnPath] = []
        self._btnTouchUpCallbackData[btnPath].append(self._onTouchUp)
        if touchUpFunc and touchUpFunc not in self._btnTouchUpCallbackData[btnPath]:
            self._btnTouchUpCallbackData[btnPath].append(touchUpFunc)
        return btn

    def RemoveButtonLongClickCallback(self, btnPath):
        """
        移除按钮长按监听。

        -----

        :param str btnPath: 按钮路径

        :return: 无
        :rtype: None
        """
        if btnPath in self._btnLongClickData:
            del self._btnLongClickData[btnPath]

    def SetLongClickVibrateTime(self, time):
        """
        设置长按后震动反馈的时长。

        -----

        :param int time: 毫秒

        :return: 无
        :rtype: None
        """
        self._vibrateTime = time

    def HasLongClicked(self, bp):
        """
        用于判断按钮在当次按下中是否已经触发了长按。

        -----

        :param str bp: 按钮路径

        :return: 从按钮按下到触发长按前，该方法返回False；从触发长按到下次按钮按下前，该方法返回True
        :rtype: bool
        """
        if bp in self._btnLongClickData:
            return self._btnLongClickData[bp]['hasLongClicked']
        return False

    # ====================================== Internal Method =================================================

    def __listen(self):
        for args in _lsnFuncArgs:
            func = args[3]
            method = getattr(self, func.__name__, None)
            if method and method.__func__ is func:
                self.cs.ListenForEvent(args[0], args[1], args[2], self, method, args[4])

    def _runTouchUpList(self, args):
        bp = args['ButtonPath']
        if bp in self._btnTouchUpCallbackData:
            for func in self._btnTouchUpCallbackData[bp]:
                func(args)

    @ui_listener("GetEntityByCoordReleaseClientEvent")
    def _OnCoordRelease(self, args):
        self._saveUiPosition()
        self.__fingerPos = None

    def _saveUiPosition(self):
        data = {}
        for bp in self._savePosUis:
            pos = self.GetBaseUIControl(bp).GetPosition()
            if pos[0] < 0 or pos[1] < 0:
                continue
            data[bp] = pos
        _save_setting(self.__uiPosKey, data, False)

    def _onBtnTouchUp(self, args):
        bp = args['ButtonPath']
        if bp in self._btnDoubleClickData:
            if self.__doubleClickTick and bp == self.__doubleClickBtnPath:
                self._btnDoubleClickData[bp]['doubleClickCallback'](args)
                self.__doubleClickTick = 0
                self.__doubleClickBtnPath = ""
                self._doubleClickArgs = None
            else:
                self.__doubleClickTick = 1
                self.__doubleClickBtnPath = bp
                self._doubleClickArgs = args

    def _onTouchUp(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self.__tick = 0

    def _onTouchCancel(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self.__tick = 0
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchCancelFunc']:
                touchData['touchCancelFunc'](args)

    def _onTouchMoveOut(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self.__tick = 0
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchMoveOutFunc']:
                touchData['touchMoveOutFunc'](args)

    def _onTouchDown(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._touchingButtonArgs = args
            self.__touchingButtonPath = btnPath
            self.__tick = 1
            self._btnLongClickData[btnPath]['hasLongClicked'] = False
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchDownFunc']:
                touchData['touchDownFunc'](args)

    def _vibrate(self):
        _LvComp.Device.SetDeviceVibrate(self._vibrateTime)

    def _onLongClick(self, args):
        bp = args['ButtonPath']
        if bp not in self._moveAfterLCData:
            return
        data = self._moveAfterLCData[bp]
        arg1 = data['moveParent']
        arg2 = data['associatedPath']
        arg3 = data['touchMoveCallback']
        self.SetButtonMovable(bp, arg1, arg2, arg3)
        if data['longClickFunc']:
            data['longClickFunc'](args)

    def _onDown(self, args):
        bp = args['ButtonPath']
        if bp not in self._moveAfterLCData:
            return
        self.CancelButtonMovable(bp)
        data = self._moveAfterLCData[bp]
        if data['touchDownFunc']:
            data['touchDownFunc'](args)

    def _testPosIsOut(self, pos, buttonSize):
        if pos[1] < 0:
            pos[1] = 0
        if pos[0] < 0:
            pos[0] = 0
        if pos[1] + buttonSize[1] > self.screenSize[1]:
            pos[1] = self.screenSize[1] - buttonSize[1]
        if pos[0] + buttonSize[0] > self.screenSize[0]:
            pos[0] = self.screenSize[0] - buttonSize[0]

    def _setWidgetPosition(self, widgetControl, offset):
        origPos = widgetControl.GetPosition()
        newPos = [origPos[0] + offset[0], origPos[1] + offset[1]]
        self._testPosIsOut(newPos, widgetControl.GetSize())
        widgetControl.SetPosition(tuple(newPos))

    def _onMove(self, args):
        touchX = args['TouchPosX']
        touchY = args['TouchPosY']
        buttonPath = args['ButtonPath']
        if buttonPath not in self._btnMovableData:
            return
        data = self._btnMovableData[buttonPath]
        moveParent = data['moveParent']
        associatedPath = data['associatedPath']
        touchMoveCallback = data['touchMoveCallback']
        self.__isMoving = True
        if not self.__fingerPos:
            self.__fingerPos = (touchX, touchY)
        offset = (touchX - self.__fingerPos[0], touchY - self.__fingerPos[1])
        self.__fingerPos = (touchX, touchY)
        if not moveParent:
            buttonControl = self.GetBaseUIControl(buttonPath)
            self._setWidgetPosition(buttonControl, offset)
        else:
            parentPath = _get_parent_path(buttonPath)
            parentControl = self.GetBaseUIControl(parentPath)
            self._setWidgetPosition(parentControl, offset)
        for path in associatedPath:
            associatedWidgetControl = self.GetBaseUIControl(path)
            self._setWidgetPosition(associatedWidgetControl, offset)
        if touchMoveCallback:
            touchMoveCallback(args)

    @ui_listener("ScreenSizeChangedClientEvent")
    def _OnScreenSizeChanged(self, args):
        self.screenSize = args['afterX'], args['afterY']






















