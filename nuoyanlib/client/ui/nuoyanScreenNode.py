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
#   Last Modified : 2023-08-29
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
import mod.client.extraClientApi as _clientApi
from ..setting import read_setting as _read_setting, save_setting as _save_setting
from uiutils import get_parent_path as _get_parent_path
from ...config import (
    MOD_NAME as _MOD_NAME,
    CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME,
    SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME
)
from ...mctypes.client.ui.controls.buttonUIControl import ButtonUIControl as _ButtonUIControl


__all__ = [
    "NuoyanScreenNode",
    "listen",
    "notify_to_server",
]


_ENGINE_NAMESPACE = _clientApi.GetEngineNamespace()
_ENGINE_SYSTEM_NAME = _clientApi.GetEngineSystemName()
_ScreenNode = _clientApi.GetScreenNodeCls()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_PLAYER_ID = _clientApi.GetLocalPlayerId()
_LEVEL_ID = _clientApi.GetLevelId()
_LevelGameComp = _ClientCompFactory.CreateGame(_LEVEL_ID)
_LevelDeviceComp = _ClientCompFactory.CreateDevice(_LEVEL_ID)
_ViewBinder = _clientApi.GetViewBinderCls()


_lsnFuncArgs = []


def notify_to_server(func):
    """
    函数装饰器，用于按钮的回调函数。

    被装饰的按钮回调函数每触发一次，服务端的同名函数也会触发一次。

    服务端同名函数的参数与按钮回调函数的参数相同，且自带一个名为__id__的key，其value为触发按钮的玩家实体ID。

    可通过args['cancelNotify'] = False或return -1的方式取消触发服务端函数。

    若对按钮回调参数进行修改（如增加、修改或删除某个key或value），服务端得到的参数为修改后的参数，可通过该方式向服务端传递更多信息。

    -----

    :param function func: 被装饰函数

    :return: 装饰后的新函数
    :rtype: function
    """
    @_wraps(func)
    def wrapper(self, args):
        args['cancelNotify'] = False
        ret = func(self, args)
        if ('cancelNotify' in args and args['cancelNotify']) or ret == -1:
            return ret
        cs = _clientApi.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        if cs:
            args['__name__'] = func.__name__
            cs.NotifyToServer("_ButtonCallbackTriggered", args)
        return ret
    return wrapper


def listen(eventName, t=0, namespace="", systemName="", priority=0):
    """
    带参数的函数装饰器，用于UI类，通过对函数进行装饰即可实现监听。

    -----

    示例：

    >>> class MyUI(ScreenNode):
    ...     @listen("MyCustomEvent")  # 监听服务端传来的自定义事件
    ...     def eventCallback(self, args):
    ...         pass
    ...
    ...     @listen("AddEntityClientEvent", 1)  # 监听AddEntityClientEvent事件
    ...     def OnAddEntity(self, args):
    ...         pass

    -----

    :param str eventName: 事件名称
    :param int t: 0表示监听服务端传来的自定义事件，1表示监听客户端引擎事件，2表示监听其他Mod的事件，默认为0
    :param str namespace: 指定命名空间，默认为空字符串
    :param str systemName: 指定系统名称，默认为空字符串
    :param int priority: 优先级，默认为0

    :return: 装饰器函数
    :rtype: (function)->function
    """
    if t == 0:
        _namespace = _MOD_NAME
        _systemName = _SERVER_SYSTEM_NAME
    elif t == 1:
        _namespace = _ENGINE_NAMESPACE
        _systemName = _ENGINE_SYSTEM_NAME
    else:
        _namespace = namespace
        _systemName = systemName
    def decorator(func):
        _lsnFuncArgs.append([eventName, func.__name__, t, _namespace, _systemName, priority])
        return func
    return decorator


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

    2、带有 *[tick]* 标签的事件为帧事件，需要注意相关逻辑的编写。
    """

    def __init__(self, namespace, name, param):
        super(NuoyanScreenNode, self).__init__(namespace, name, param)
        self.cs = _clientApi.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        self.screenSize = _LevelGameComp.GetScreenSize()
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

    def __listen(self):
        global _lsnFuncArgs
        for eventName, funcName, t, namespace, systemName, priority in _lsnFuncArgs:
            self.cs.ListenForEvent(namespace, systemName, eventName, self, getattr(self, funcName), priority)
        _lsnFuncArgs = []

    def Create(self):
        """
        UI生命周期函数，当UI创建成功时调用。

        若重写该方法，请调用一次NuoyanScreenNode的同名方法，否则部分功能将不可用。如：

        >>> def Create(self):
        ...     super(MyUI, self).Create()  # 或者：NuoyanScreenNode.Create(self)
        """
        uiPosData = _read_setting(self.__uiPosKey, False)
        if uiPosData:
            for bp, pos in uiPosData.items():
                ui = self.GetBaseUIControl(bp)
                if ui:
                    ui.SetPosition(tuple(pos))

    def Update(self):
        """
        *[tick]*

        客户端每帧调用，1秒有30帧。
        若重写该方法，请调用一次NuoyanScreenNode的同名方法，否则部分功能将不可用。如：

        >>> def Update(self):
        ...     super(MyUI, self).Update()  # 或者：NuoyanScreenNode.Update(self)
        """
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

    def Destroy(self):
        """
        UI生命周期函数，当UI销毁时调用。
        """

    def OnDeactive(self):
        """
        UI生命周期函数，当栈顶UI有其他UI入栈时调用。

        不建议使用在OnDeactive函数中调用SetScreenVisible(False)，在OnActive函数中调用SetScreenVisible(True)的方式实现打开新界面时隐藏原界面，新界面关闭时自动显示原界面的功能，由于隐藏接口不会改动UI栈，多Mod容易形成冲突。推荐使用PushScreen，PopScreen接口实现。
        """

    def OnActive(self):
        """
        UI生命周期函数，当UI重新回到栈顶时调用。

        不建议使用在OnDeactive函数中调用SetScreenVisible(False)，在OnActive函数中调用SetScreenVisible(True)的方式实现打开新界面时隐藏原界面，新界面关闭时自动显示原界面的功能，由于隐藏接口不会改动UI栈，多Mod容易形成冲突。推荐使用PushScreen，PopScreen接口实现。
        """

    # ========================================== Basic Function ========================================================

    def SetButtonDoubleClickCallback(self, buttonPath, doubleClickCallback, touchUpCallback=None):
        """
        设置按钮双击监听。

        -----

        :param str buttonPath: 按钮路径
        :param (dict)->Any doubleClickCallback: DoubleClick回调函数
        :param ((dict)->Any)|None touchUpCallback: TouchUp回调函数，默认为None

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
        :param ((dict)->Any)|None touchMoveCallback: TouchMove回调函数，默认为None

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
        :param ((dict)->Any)|None touchUpFunc: TouchUp回调函数，默认为None
        :param ((dict)->Any)|None longClickFunc: LongClick回调函数，默认为None
        :param ((dict)->Any)|None touchMoveCallback: TouchMove回调函数，默认为None
        :param ((dict)->Any)|None touchMoveOutFunc: TouchMoveOut回调函数，默认为None
        :param ((dict)->Any)|None touchDownFunc: TouchDown回调函数，默认为None
        :param ((dict)->Any)|None touchCancelFunc: TouchCancel回调函数，默认为None

        :return: 按钮的ButtonUIControl实例
        :rtype: _ButtonUIControl
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
            'touchDownFunc': touchDownFunc
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
        :param (dict)->Any longClickFunc: LongClick回调函数
        :param ((dict)->Any)|None touchUpFunc: TouchUp回调函数，默认为None
        :param ((dict)->Any)|None touchMoveOutFunc: TouchMoveOut回调函数，默认为None
        :param ((dict)->Any)|None touchDownFunc: TouchDown回调函数，默认为None
        :param ((dict)->Any)|None touchCancelFunc: TouchCancel回调函数，默认为None

        :return: 按钮的ButtonUIControl实例
        :rtype: _ButtonUIControl
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
        btn.SetButtonTouchMoveOutCallback(self._onTouchCancel)
        btn.SetButtonTouchDownCallback(self._onTouchDown)
        btn.SetButtonTouchCancelCallback(self._onTouchMoveOut)
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

    # todo:====================================== Internal Method ======================================================

    def _runTouchUpList(self, args):
        bp = args['ButtonPath']
        if bp in self._btnTouchUpCallbackData:
            for func in self._btnTouchUpCallbackData[bp]:
                func(args)

    @listen("GetEntityByCoordReleaseClientEvent", 1)
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
        _LevelDeviceComp.SetDeviceVibrate(self._vibrateTime)

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

    @listen("ScreenSizeChangedClientEvent", 1)
    def _OnScreenSizeChanged(self, args):
        self.screenSize = args['afterX'], args['afterY']






















