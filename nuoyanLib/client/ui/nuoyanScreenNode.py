# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-02-26
#
# ====================================================


from collections import Callable as _Callable
from ..setting import read_setting as _read_setting, save_setting as _save_setting
from utils import get_parent_path as _get_parent_path
from ..._config import CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME, MOD_NAME as _MOD_NAME, \
    SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME
from ...mctypes.client.ui.controls.buttonUIControl import ButtonUIControl
try:
    import mod.client.extraClientApi as _clientApi
except:
    pass


__all__ = [
    "NuoyanScreenNode",
]


try:
    _ENGINE_NAMESPACE = _clientApi.GetEngineNamespace()
    _ENGINE_SYSTEM_NAME = _clientApi.GetEngineSystemName()
    _ScreenNode = _clientApi.GetScreenNodeCls()
    _ClientCompFactory = _clientApi.GetEngineCompFactory()
    _PLAYER_ID = _clientApi.GetLocalPlayerId()
    _LEVEL_ID = _clientApi.GetLevelId()
    _LevelGameComp = _ClientCompFactory.CreateGame(_LEVEL_ID)
    _LevelDeviceComp = _ClientCompFactory.CreateDevice(_LEVEL_ID)
except:
    from ...mctypes.client.ui.screenNode import ScreenNode
    _ScreenNode = ScreenNode  # type: type[ScreenNode]
    _ENGINE_NAMESPACE = ""
    _ENGINE_SYSTEM_NAME = ""


_lsnFuncArgs = []


def listen(eventName, t=0, namespace="", systemName="", priority=0):
    # type: (str, int, str, str, int) -> ...
    """
    函数装饰器，通过对函数进行装饰即可实现监听。
    示例：
    class MyUI(ScreenNode):
        # 监听服务端传来的自定义事件
        @listen("MyCustomEvent")
        def eventCallback(self, args):
            pass

        # 监听AddEntityClientEvent事件
        @listen("AddEntityClientEvent", 1)
        def OnAddEntity(self, args):
            pass
    -----------------------------------------------------------
    【eventName: str】 事件名称
    【t: int = 0】 0表示监听服务端传来的自定义事件，1表示监听客户端引擎事件，2表示监听其他Mod的事件
    【namespace: str = ""】 其他Mod的命名空间
    【systemName: str = ""】 其他Mod的系统名称
    【priority: int = 0】 优先级
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


class NuoyanScreenNode(_ScreenNode):  # type:
    """
    ScreenNode扩展类。将自定义UI类继承本类即可使用本类的全部功能。
    -----------------------------------------------------------
    【基础功能】
    -----------------------------------------------------------
    【新增接口】
    1. SetButtonDoubleClickCallback：设置按钮双击监听
    2. SetButtonMovable：设置按钮可拖动
    3. CancelButtonMovable：取消按钮可拖动
    4. SetButtonLongClickCallback：设置按钮长按监听
    5. RemoveButtonLongClickCallback：移除按钮长按监听
    6. SetLongClickVibrateTime：设置长按后震动反馈的时长
    7. HasLongClicked：用于判断按钮在当次按下中是否已经触发了长按
    8. SetButtonMovableAfterLongClick：设置按钮长按拖动
    -----------------------------------------------------------
    【新增事件】
    -----------------------------------------------------------
    【新增属性】
    1. cs：客户端系统实例，可直接使用该属性在UI类中调用客户端的接口、方法、属性等，如self.cs.NotifyToServer(...)、self.cs.xxx = ...
    2. screenSize: 屏幕尺寸元组，(宽度, 高度)；屏幕尺寸改变时，该属性也会跟着改变
    -----------------------------------------------------------
    【注意事项】
    1. 重写Create和Update方法时请调用一次父类的同名方法，如：super(MyUI, self).Create()或NuoyanScreenNode.Create(self)；
    2. 带有*tick*标签的事件为帧事件，需要注意编写相关逻辑。
    """

    def __init__(self, namespace, name, param):
        super(NuoyanScreenNode, self).__init__(namespace, name, param)
        self.cs = _clientApi.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        self.screenSize = _LevelGameComp.GetScreenSize()
        self._doubleClickTick = 0
        self._btnDoubleClickData = {}
        self._doubleClickBtnPath = ""
        self._doubleClickArgs = None
        self._fingerPos = None
        self._isMoving = False
        self._vibrateTime = 100
        self._btnLongClickData = {}
        self._btnTouchData = {}
        self._touchingButtonPath = ""
        self._touchingButtonArgs = {}
        self._tick = 0
        self._btnMovableData = {}
        self._btnTouchUpCallbackData = {}
        self._moveAfterLCData = {}
        self._savePosUis = []
        self._uiPosKey = self.__class__.__name__ + "_ui_pos_data"
        self._listen()

    def _listen(self):
        global _lsnFuncArgs
        for eventName, funcName, t, namespace, systemName, priority in _lsnFuncArgs:
            self.cs.ListenForEvent(namespace, systemName, eventName, self, getattr(self, funcName), priority)
        _lsnFuncArgs = []

    def Create(self):
        """
        UI生命周期函数，当UI创建成功时调用。
        若重写该方法，请调用一次NuoyanScreenNode的同名方法，否则部分功能将不可用。如：
        def Create(self):
            super(MyUI, self).Create()
            # 或者：NuoyanScreenNode.Create(self)
        """
        uiPosData = _read_setting(self._uiPosKey, False)
        if uiPosData:
            for bp, pos in uiPosData.items():
                self.GetBaseUIControl(bp).SetPosition(tuple(pos))

    def Update(self):
        """
        *tick*
        客户端每帧调用，1秒有30帧。
        若重写该方法，请调用一次NuoyanScreenNode的同名方法，否则部分功能将不可用。如：
        def Update(self):
            super(MyUI, self).Update()  # 或者：NuoyanScreenNode.Update(self)
        """
        if self._doubleClickTick:
            self._doubleClickTick += 1
            if self._doubleClickTick == 11:
                self._doubleClickTick = 0
        if 1 <= self._tick <= 20:
            self._tick += 1
            if self._tick == 21 and self._touchingButtonPath in self._btnLongClickData:
                btnData = self._btnLongClickData[self._touchingButtonPath]
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

    # todo:==================================== Custom Event Callback ==================================================

    # todo:======================================= Basic Function ======================================================

    def SetButtonDoubleClickCallback(self, buttonPath, doubleClickCallback, touchUpCallback=None):
        # type: (str, _Callable[[dict], None], _Callable[[dict], None] | None) -> None
        """
        设置按钮双击监听。
        -----------------------------------------------------------
        【buttonPath: str】 按钮路径
        【doubleClickCallback: (dict) -> None】 DoubleClick回调函数
        【touchUpCallback: Optional[(dict) -> None] = None】 TouchUp回调函数
        -----------------------------------------------------------
        NoReturn
        """
        self._btnDoubleClickData[buttonPath] = {
            'doubleClickCallback': doubleClickCallback,
            'touchUpCallback': touchUpCallback
        }
        btnCtrl = self.GetBaseUIControl(buttonPath).asButton()
        btnCtrl.AddTouchEventParams()
        btnCtrl.SetButtonTouchUpCallback(self._runTouchUpList)
        if buttonPath not in self._btnTouchUpCallbackData:
            self._btnTouchUpCallbackData[buttonPath] = []
        if touchUpCallback and touchUpCallback not in self._btnTouchUpCallbackData[buttonPath]:
            self._btnTouchUpCallbackData[buttonPath].append(touchUpCallback)
        self._btnTouchUpCallbackData[buttonPath].append(self._onBtnTouchUp)

    def SetButtonMovable(self, btnPath, moveParent=False, associatedWidgetPath=(), touchMoveCallback=None):
        # type: (str, bool, str | tuple[str, ...], _Callable[[dict], None] | None) -> None
        """
        设置按钮可拖动。
        -----------------------------------------------------------
        【btnPath: str】 按钮路径
        【moveParent: bool = False】 是否同时拖动父控件
        【associatedWidgetPath: Union[str, Tuple[str, ...]] = ()】 关联拖动的其他控件的路径，多个控件请使用元组
        【touchMoveCallback: Optional[(dict) -> None] = None】 TouchMove回调函数
        -----------------------------------------------------------
        NoReturn
        """
        self._isMoving = False
        self._fingerPos = None
        if isinstance(associatedWidgetPath, str):
            associatedWidgetPath = (associatedWidgetPath,)
        self._btnMovableData[btnPath] = {
            'moveParent': moveParent,
            'associatedWidgetPath': associatedWidgetPath,
            'touchMoveCallback': touchMoveCallback
        }
        btn = self.GetBaseUIControl(btnPath).asButton()
        btn.AddTouchEventParams()
        btn.SetButtonTouchMoveCallback(self._onMove)

    def CancelButtonMovable(self, btnPath):
        # type: (str) -> None
        """
        取消按钮可拖动。
        -----------------------------------------------------------
        【btnPath: str】 按钮路径
        -----------------------------------------------------------
        NoReturn
        """
        if btnPath in self._btnMovableData:
            del self._btnMovableData[btnPath]
        self.GetBaseUIControl(btnPath).asButton().SetButtonTouchMoveCallback(None)

    def SetButtonMovableAfterLongClick(self, btnPath, moveParent=False, associatedWidgetPath=(), touchUpFunc=None,
                                       longClickFunc=None, touchMoveCallback=None, touchMoveOutFunc=None,
                                       touchDownFunc=None, touchCancelFunc=None):
        # type: (str, bool, str | tuple[str, ...], _Callable[[dict], None] | None, _Callable[[dict], None] | None, _Callable[[dict], None] | None, _Callable[[dict], None] | None, _Callable[[dict], None] | None, _Callable[[dict], None] | None) -> ButtonUIControl
        """
        设置按钮长按拖动。
        该方法设置的按钮拖动会自动保存位置，下次启动游戏时按钮会恢复到上次游戏时的位置。
        -----------------------------------------------------------
        【btnPath: str】 按钮路径
        【moveParent: bool = False】 是否同时拖动父控件
        【associatedWidgetPath: Union[str, Tuple[str, ...]] = ()】 关联拖动的其他控件的路径，多个控件请使用元组
        【touchUpFunc: Optional[(dict) -> None] = None】 TouchUp回调函数
        【longClickFunc: Optional[(dict) -> None] = None】 LongClick回调函数
        【touchMoveCallback: Optional[(dict) -> None] = None】 TouchMove回调函数
        【touchMoveOutFunc: Optional[(dict) -> None] = None】 TouchMoveOut回调函数
        【touchDownFunc: Optional[(dict) -> None] = None】 TouchDown回调函数
        【touchCancelFunc: Optional[(dict) -> None] = None】 TouchCancel回调函数
        -----------------------------------------------------------
        return: ButtonUIControl -> 按钮的ButtonUIControl实例
        """
        if isinstance(associatedWidgetPath, str):
            associatedWidgetPath = (associatedWidgetPath,)
        btn = self.SetButtonLongClickCallback(
            btnPath, self._onLongClick, touchUpFunc, touchMoveOutFunc, self._onDown, touchCancelFunc
        )
        self._moveAfterLCData[btnPath] = {
            'moveParent': moveParent,
            'associatedWidgetPath': associatedWidgetPath,
            'touchMoveCallback': touchMoveCallback,
            'longClickFunc': longClickFunc,
            'touchDownFunc': touchDownFunc
        }
        self._savePosUis.extend(associatedWidgetPath)
        if moveParent:
            self._savePosUis.append(_get_parent_path(btnPath))
        else:
            self._savePosUis.append(btnPath)
        return btn

    def SetButtonLongClickCallback(self, btnPath, longClickFunc, touchUpFunc=None, touchMoveOutFunc=None,
                                   touchDownFunc=None, touchCancelFunc=None):
        # type: (str, _Callable[[dict], None], _Callable[[dict], None] | None, _Callable[[dict], None] | None, _Callable[[dict], None] | None, _Callable[[dict], None] | None) -> ButtonUIControl
        """
        设置按钮长按监听。
        -----------------------------------------------------------
        【btnPath：str】 按钮路径
        【longClickFunc：(dict) -> None】 LongClick回调函数
        【touchUpFunc：Optional[(dict) -> None] = None】 TouchUp回调函数
        【touchMoveOutFunc：Optional[(dict) -> None] = None】 TouchMoveOut回调函数
        【touchDownFunc：Optional[(dict) -> None] = None】 TouchDown回调函数
        【touchCancelFunc：Optional[(dict) -> None] = None】 TouchCancel回调函数
        -----------------------------------------------------------
        return: ButtonUIControl -> 按钮的ButtonUIControl实例
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
        btn.AddTouchEventParams()
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
        # type: (str) -> None
        """
        移除按钮长按监听。
        -----------------------------------------------------------
        【btnPath: str】 按钮路径
        -----------------------------------------------------------
        NoReturn
        """
        if btnPath in self._btnLongClickData:
            del self._btnLongClickData[btnPath]

    def SetLongClickVibrateTime(self, time):
        # type: (int) -> None
        """
        设置长按后震动反馈的时长。
        -----------------------------------------------------------
        【time: int】 毫秒
        -----------------------------------------------------------
        NoReturn
        """
        self._vibrateTime = time

    def HasLongClicked(self, bp):
        # type: (str) -> bool
        """
        用于判断按钮在当次按下中是否已经触发了长按。
        -----------------------------------------------------------
        【bp: str】 按钮路径
        -----------------------------------------------------------
        return: bool -> 从按钮按下到触发长按前，该方法返回False；从触发长按到下次按钮按下前，该方法返回True
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

    def _saveUiPosition(self):
        data = {}
        for bp in self._savePosUis:
            pos = self.GetBaseUIControl(bp).GetPosition()
            if pos[0] < 0 or pos[1] < 0:
                continue
            data[bp] = pos
        _save_setting(self._uiPosKey, data, False)

    def _onBtnTouchUp(self, args):
        bp = args['ButtonPath']
        if bp in self._btnDoubleClickData:
            if self._doubleClickTick and bp == self._doubleClickBtnPath:
                self._btnDoubleClickData[bp]['doubleClickCallback'](args)
                self._doubleClickTick = 0
                self._doubleClickBtnPath = ""
                self._doubleClickArgs = None
            else:
                self._doubleClickTick = 1
                self._doubleClickBtnPath = bp
                self._doubleClickArgs = args

    def _onTouchUp(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._tick = 0

    def _onTouchCancel(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._tick = 0
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchCancelFunc']:
                touchData['touchCancelFunc'](args)

    def _onTouchMoveOut(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._tick = 0
        if btnPath in self._btnTouchData:
            touchData = self._btnTouchData[btnPath]
            if touchData['touchMoveOutFunc']:
                touchData['touchMoveOutFunc'](args)

    def _onTouchDown(self, args):
        btnPath = args['ButtonPath']
        if btnPath in self._btnLongClickData:
            self._touchingButtonArgs = args
            self._touchingButtonPath = btnPath
            self._tick = 1
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
        arg2 = data['associatedWidgetPath']
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

    def _setWidgetPosition(self, widgetControl, offset, widgetSize):
        origPos = widgetControl.GetPosition()
        newPos = [origPos[0] + offset[0], origPos[1] + offset[1]]
        self._testPosIsOut(newPos, widgetSize)
        widgetControl.SetPosition(tuple(newPos))

    def _onMove(self, args):
        touchX = args['TouchPosX']
        touchY = args['TouchPosY']
        buttonPath = args['ButtonPath']
        if buttonPath not in self._btnMovableData:
            return
        moveParent = self._btnMovableData[buttonPath]['moveParent']
        associatedWidgetPath = self._btnMovableData[buttonPath]['associatedWidgetPath']
        touchMoveCallback = self._btnMovableData[buttonPath]['touchMoveCallback']
        self._isMoving = True
        if not self._fingerPos:
            self._fingerPos = (touchX, touchY)
        offset = (touchX - self._fingerPos[0], touchY - self._fingerPos[1])
        self._fingerPos = (touchX, touchY)
        if not moveParent:
            buttonControl = self.GetBaseUIControl(buttonPath)
            buttonSize = buttonControl.GetSize()
            self._setWidgetPosition(buttonControl, offset, buttonSize)
        else:
            buttonName = buttonPath.split("/")[-1]
            parentPath = buttonPath.split("/" + buttonName)[0]
            parentControl = self.GetBaseUIControl(parentPath)
            parentSize = parentControl.GetSize()
            self._setWidgetPosition(parentControl, offset, parentSize)
        for path in associatedWidgetPath:
            associatedWidgetControl = self.GetBaseUIControl(path)
            associatedWidgetSize = associatedWidgetControl.GetSize()
            self._setWidgetPosition(associatedWidgetControl, offset, associatedWidgetSize)
        if touchMoveCallback:
            touchMoveCallback(args)

    @listen("ScreenSizeChangedClientEvent", 1)
    def _OnScreenSizeChanged(self, args):
        self.screenSize = args['afterX'], args['afterY']


def _test():
    pass




















