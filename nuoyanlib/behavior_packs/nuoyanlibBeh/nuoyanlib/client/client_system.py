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
#   Last Modified : 2024-07-03
#
# ====================================================


import mod.client.extraClientApi as _client_api
from behavior_packs.nuoyanlibBeh.nuoyanlibScripts._core._client import (
    get_lib_system as _get_lib_system,
)
from behavior_packs.nuoyanlibBeh.nuoyanlibScripts._core._client import (
    listen_custom as _listen_custom,
    listen_engine_and_lib as _listen_engine_and_lib,
)
from behavior_packs.nuoyanlibBeh.nuoyanlibScripts._core._client import (
    ClientSystem as _ClientSystem,
)


__all__ = [
    "NuoyanClientSystem",
]


class NuoyanClientSystem(_ClientSystem):
    """
    | ClientSystem扩展类。将客户端继承本类即可使用本类的全部功能。

    -----

    【注意事项】

    | 1、带有 *[event]* 标签的方法为事件，重写该方法即可使用该事件。
    | 2、带有 *[tick]* 标签的事件为帧事件，需要注意编写相关逻辑。
    | 3、事件回调参数中，参数名前面的美元符号 ``$`` 表示该参数可进行修改。
    """

    def __init__(self, namespace, system_name):
        super(NuoyanClientSystem, self).__init__(namespace, system_name)
        self.__lib_sys = _get_lib_system()
        self.__namespace = namespace
        self.__system_name = system_name
        _listen_engine_and_lib(self)
        _listen_custom(self)
        self._set_print_log()

    def Destroy(self):
        """
        *[event]*

        | 客户端系统销毁时触发。
        | 若重写该方法，请调用一次父类的同名方法。如：
        ::

            class MyClientSystem(NuoyanClientSystem):
                def Destroy(self):
                    super(MyClientSystem, self).Destroy()

        -----

        :return: 无
        :rtype: None
        """
        super(NuoyanClientSystem, self).Destroy()
        self.UnListenAllEvents()

    # Engine Event Callbacks ===========================================================================================

    def GyroSensorChangedClientEvent(self, args):
        """
        *[event]*

        | 陀螺仪传感器姿态发生变化时触发。
        | 该事件只适用于移动端。

        -----

        | 【xDiff: float】 x轴角速度，单位为弧度/s
        | 【yDiff: float】 y轴角速度，单位为弧度/s
        | 【zDiff: float】 z轴角速度，单位为弧度/s
        | 【timestamp: float】 触发时间戳，秒

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ModBlockEntityTickClientEvent(self, args):
        """
        *[event]*

        | 客户端自定义方块实体tick事件。
        | 只有 ``client_tick`` 字段为 ``true`` 的自定义方块实体才能触发该事件（见 `自定义方块实体 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93.html>`_）。
        | 目前客户端实体tick范围为硬编码，范围为玩家为中心的等腰等斜边八边形，其中斜边长度为5，非斜边长度为3。

        -----

        | 【posX: int】 自定义方块实体的位置X
        | 【posY: int】 自定义方块实体的位置Y
        | 【posZ: int】 自定义方块实体的位置Z
        | 【dimensionId: int】 维度ID
        | 【blockName: str】 方块的identifier，包含命名空间及名称

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ModBlockEntityRemoveClientEvent(self, args):
        """
        *[event]*

        | 客户端自定义方块实体卸载时触发。

        -----

        | 【posX: int】 自定义方块实体的位置X
        | 【posY: int】 自定义方块实体的位置Y
        | 【posZ: int】 自定义方块实体的位置Z
        | 【dimensionId: int】 维度ID
        | 【blockName: str】 方块的identifier，包含命名空间及名称

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def AchievementButtonMovedClientEvent(self, args):
        """
        *[event]*

        | 使用自定义成就系统的时，拖动成就入口结束时触发。

        -----

        | 【oldPosition: Tuple[float, float]】 移动前该控件相对父节点的坐标信息，第一项为横轴，第二项为纵轴
        | 【newPosition: Tuple[float, float]】 移动后该控件相对父节点的坐标信息，第一项为横轴，第二项为纵轴

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnKeyboardControllerLayoutChangeClientEvent(self, args):
        """
        *[event]*

        | 键盘按键映射改变事件。

        -----

        | 【action: str】 行为
        | 【newKey: int】 修改后的键码，详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
        | 【oldKey: int】 修改前的键码，详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnGamepadControllerLayoutChangeClientEvent(self, args):
        """
        *[event]*

        | 游戏手柄按键映射改变事件。

        -----

        | 【action: str】 行为
        | 【newKey: int】 修改后的键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        | 【oldKey: int】 修改前的键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnGamepadTriggerClientEvent(self, args):
        """
        *[event]*

        | 游戏手柄扳机事件。当扣动扳机的力度发生改变时触发。

        -----

        | 【key: int】 键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        | 【magnitude: float】 扣动扳机的力度，取值为 0 ~ 1.0

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnGamepadStickClientEvent(self, args):
        """
        *[event]*

        | 游戏手柄摇杆事件。当摇杆摇动位置发生改变时触发。

        -----

        | 【key: int】 键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        | 【x: float】摇杆水平方向的值，从左到右取值为 -1.0 ~ 1.0
        | 【y: float】摇杆竖直方向的值，从下到上取值为 -1.0 ~ 1.0

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnGamepadKeyPressClientEvent(self, args):
        """
        *[event]*

        | 游戏手柄按键事件。

        -----

        | 【screenName: str】 当前screenName
        | 【key: int】 键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        | 【isDown: str】 是否按下，按下为1，弹起为0

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ModBlockEntityLoadedClientEvent(self, args):
        """
        *[event]*

        | 客户端自定义方块实体加载完成后第一次出现在玩家视野中时触发。
        | 只有在客户端自定义方块实体加载完成后，第一次出现在玩家视野中时才会触发该事件。注意：只有添加了自定义方块实体扩展功能的自定义方块实体才能触发该事件（见 `自定义方块实体外观 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/4.1-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93%E5%A4%96%E8%A7%82.html>`_ ）；出生点是常加载区域，来回传送不会重复触发此事件。

        -----

        | 【posX: int】 自定义方块实体的位置X
        | 【posY: int】 自定义方块实体的位置Y
        | 【posZ: int】 自定义方块实体的位置Z
        | 【dimensionId: int】 维度ID
        | 【blockName: str】 方块的identifier，包含命名空间及名称

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def CloseNeteaseShopEvent(self, args):
        """
        *[event]*

        | 关闭商城界面时触发，包括脚本商城和Apollo插件商城。

        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PopScreenAfterClientEvent(self, args):
        """
        *[event]*

        | screen移除触发。
        | 与 ``PopScreenEvent`` 不同， ``PopScreenAfterClientEvent`` 触发时机是在完全把UI弹出后，返回的 ``screenName`` 是弹出后最顶层UI的Screen名。
        
        -----

        | 【screenName: str】 UI名字
        | 【screenDef: str】 包含命名空间的UI名字，格式为namespace.screenName

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def TapOrHoldReleaseClientEvent(self, args):
        """
        *[event]*

        | 玩家点击屏幕后松手时触发。
        | 仅在移动端或pc的F11模式下触发，pc的非F11模式可以使用 ``LeftClickReleaseClientEvent`` 与 ``RightClickReleaseClientEvent`` 事件监听鼠标松开。
        | 短按及长按后松手都会触发该事件。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def TapBeforeClientEvent(self, args):
        """
        *[event]*

        | 玩家点击屏幕并松手，即将响应到游戏内时触发。
        | 仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用 ``LeftClickBeforeClientEvent`` 事件监听鼠标左键。
        | 玩家点击屏幕的处理顺序为：
        | 1、玩家点击屏幕，没有进行拖动，并在短按判定时间（250毫秒）内松手；
        | 2、触发该事件；
        | 3、若事件没有cancel，则根据准心处的物体类型以及与玩家的距离，进行攻击或放置等操作。
        | 与 ``GetEntityByCoordEvent`` 事件不同的是，被ui层捕获，没有穿透到世界的点击不会触发该事件，例如：
        | 1、点击原版的移动/跳跃等按钮。
        | 2、通过 ``SetIsHud(0)`` 屏蔽了游戏操作。
        | 3、对按钮使用 ``AddTouchEventHandler`` 接口时 ``isSwallow`` 参数设置为 ``True`` 。
        
        -----

        | 【$cancel: bool】 设置为True可拦截原版的攻击或放置响应

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def RightClickReleaseClientEvent(self, args):
        """
        *[event]*

        | 玩家松开鼠标右键时触发。
        | 仅在pc的普通控制模式（即非F11模式）下触发。
        | 在F11下右键，按下会触发 ``RightClickBeforeClientEvent`` ，松开时会触发 ``TapOrHoldReleaseClientEvent`` 。
        | pc的普通控制模式下的鼠标点击流程见 ``TapOrHoldReleaseClientEvent`` 备注中的 `配图 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%8E%A7%E5%88%B6.html?key=TapOrHoldReleaseClientEvent&docindex=6&type=0>`_。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def RightClickBeforeClientEvent(self, args):
        """
        *[event]*

        | 玩家按下鼠标右键时触发。仅在pc下触发（普通控制模式及F11模式都会触发）。
        
        -----

        | 【$cancel: bool】 设置为True可拦截原版的物品使用/实体交互响应

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnMouseMiddleDownClientEvent(self, args):
        """
        *[event]*

        | 鼠标按下中键时触发。
        | 仅通过 ``PushScreen`` 创建的界面能够正常返回坐标，开启F11模式的时候，返回最后点击屏幕时的坐标。
        
        -----

        | 【isDown: str】 是否按下，按下为1，弹起为0
        | 【mousePositionX: float】 按下时的x坐标
        | 【mousePositionY: float】 按下时的y坐标

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnKeyPressInGame(self, args):
        """
        *[event]*

        | 按键按下或按键释放时触发。
        
        -----

        | 【screenName: str】 当前screenName
        | 【key: str】 键码（注：这里的int型被转成了str型，比如"1"对应的就是枚举值文档中的1），详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
        | 【isDown: str】 是否按下，按下为1，弹起为0

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnClientPlayerStopMove(self):
        """
        *[event]*

        | 移动按钮按下释放时触发事件，同时按下多个方向键，需要释放所有的方向键才会触发事件。
        
        -----

        | 无参数

        -----

        :return: 无
        :rtype: None
        """

    def OnClientPlayerStartMove(self):
        """
        *[event]*

        | 移动按钮按下触发事件，在按住一个方向键的同时，去按另外一个方向键，不会触发第二次。
        
        -----

        | 无参数

        -----

        :return: 无
        :rtype: None
        """

    def OnBackButtonReleaseClientEvent(self, args):
        """
        *[event]*

        | 返回按钮（目前特指安卓系统导航中的返回按钮）松开时触发。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def MouseWheelClientEvent(self, args):
        """
        *[event]*

        | 鼠标滚轮滚动时触发。
        
        -----

        | 【direction: int】 1为向上滚动，0为向下滚动

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def LeftClickReleaseClientEvent(self, args):
        """
        *[event]*

        | 玩家松开鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def LeftClickBeforeClientEvent(self, args):
        """
        *[event]*

        | 玩家按下鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。
        
        -----

        | 【$cancel: bool】 设置为True可拦截原版的挖方块或攻击响应

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def HoldBeforeClientEvent(self, args):
        """
        *[event]*

        | 玩家长按屏幕，即将响应到游戏内时触发。
        | 仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用 ``RightClickBeforeClientEvent`` 事件监听鼠标右键。
        | 玩家长按屏幕的处理顺序为：
        | 1、玩家点击屏幕，在长按判定时间内（默认为400毫秒，可通过 ``SetHoldTimeThreshold`` 接口修改）一直没有进行拖动或松手；
        | 2、触发该事件；
        | 3、若事件没有cancel，则根据主手上的物品，准心处的物体类型以及与玩家的距离，进行挖方块/使用物品/与实体交互等操作。
        | 即该事件只会在到达长按判定时间的瞬间触发一次，后面一直按住不会连续触发，可以使用 ``TapOrHoldReleaseClientEvent`` 监听长按后松手。
        | 与 ``TapBeforeClientEvent`` 事件类似，被ui层捕获，没有穿透到世界的点击不会触发该事件。
        
        -----

        | 【$cancel: bool】 设置为True可拦截原版的挖方块/使用物品/与实体交互响应

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def GetEntityByCoordReleaseClientEvent(self, args):
        """
        *[event]*

        | 玩家点击屏幕后松开时触发，多个手指点在屏幕上时，只有最后一个手指松开时触发。
        
        -----

        | 【x: int】 手指点击位置x坐标
        | 【y: int】 手指点击位置y坐标

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def GetEntityByCoordEvent(self, args):
        """
        *[event]*

        | 玩家点击屏幕时触发，多个手指点在屏幕上时，只有第一个会触发。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientJumpButtonReleaseEvent(self, args):
        """
        *[event]*

        | 跳跃按钮按下释放事件。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientJumpButtonPressDownEvent(self, args):
        """
        *[event]*

        | 跳跃按钮按下事件，返回值设置参数只对当次按下事件起作用。
        
        -----

        | 【$continueJump: bool】 设置是否执行跳跃逻辑

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PlaySoundClientEvent(self, args):
        """
        *[event]*

        | 播放场景音效或UI音效时触发。
        
        -----

        | 【name: str】 即资源包中sounds/sound_definitions.json中的key
        | 【pos: Tuple[float, float, float]】 音效播放的位置，UI音效为(0,0,0)
        | 【volume: float】 音量，范围为0-1
        | 【pitch: float】 播放速度，正常速度为1
        | 【$cancel: bool】 设为True可屏蔽该次音效播放

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PlayMusicClientEvent(self, args):
        """
        *[event]*

        | 播放背景音乐时触发。
        
        -----

        | 【name: str】 即资源包中sounds/music_definitions.json中的event_name，并且对应sounds/sound_definitions.json中的key
        | 【$cancel: bool】 设为True可屏蔽该次音效播放

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnMusicStopClientEvent(self, args):
        """
        *[event]*

        | 音乐停止时，当玩家调用 ``StopCustomMusic`` 来停止自定义背景音乐时，会触发该事件。
        
        -----

        | 【musicName: str】 音乐名称

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ScreenSizeChangedClientEvent(self, args):
        """
        *[event]*

        | 改变屏幕大小时会触发的事件。该事件仅支持PC。
        
        -----

        | 【beforeX: float】 屏幕大小改变前的宽度
        | 【beforeY: float】 屏幕大小改变前的高度
        | 【afterX: float】 屏幕大小改变后的宽度
        | 【afterY: float】 屏幕大小改变后的高度

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PushScreenEvent(self, args):
        """
        *[event]*

        | screen创建触发。
        
        -----

        | 【screenName: str】 UI名字
        | 【screenDef: str】 包含命名空间的UI名字，格式为namespace.screenName

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PopScreenEvent(self, args):
        """
        *[event]*

        | screen移除触发。
        | ``screenName`` 为正在弹出的Screen名，如果需要获取下一个Screen可使用 ``PopScreenAfterClientEvent`` 。
        
        -----

        | 【screenName: str】 UI名字
        | 【screenDef: str】 包含命名空间的UI名字，格式为"namespace.screenName"

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PlayerChatButtonClickClientEvent(self, args):
        """
        *[event]*

        | 玩家点击聊天按钮或回车键触发呼出聊天窗口时客户端抛出的事件。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnItemSlotButtonClickedEvent(self, args):
        """
        *[event]*

        | 点击快捷栏、背包栏、盔甲栏、副手栏的物品槽时触发。
        
        -----

        | 【slotIndex: int】 点击的物品槽的编号，编号对应位置详见 `物品栏 <https://minecraft.fandom.com/zh/wiki/%E7%89%A9%E5%93%81%E6%A0%8F>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def GridComponentSizeChangedClientEvent(self, args):
        """
        *[event]*

        | UI grid组件里格子数目发生变化时触发。
        
        -----

        | 【path: str】 grid网格所在的路径（从UI根节点算起）

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientPlayerInventoryOpenEvent(self, args):
        """
        *[event]*

        | 打开物品背包界面时触发。
        
        -----

        | 【isCreative: bool】 是否是创造模式背包界面
        | 【$cancel: bool】 是否取消打开物品背包界面。

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientPlayerInventoryCloseEvent(self, args):
        """
        *[event]*

        | 关闭物品背包界面时触发。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientChestOpenEvent(self, args):
        """
        *[event]*

        | 打开箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【x: int】 箱子x坐标
        | 【y: int】 箱子y坐标
        | 【z: int】 箱子z坐标

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientChestCloseEvent(self, args):
        """
        *[event]*

        | 关闭箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def WalkAnimEndClientEvent(self, args):
        """
        *[event]*

        | 走路动作结束时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。
        
        -----

        | 【id: str】 实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def WalkAnimBeginClientEvent(self, args):
        """
        *[event]*

        | 走路动作开始时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。
        
        -----

        | 【id: str】 实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def AttackAnimEndClientEvent(self, args):
        """
        *[event]*

        | 攻击动作结束时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。
        
        -----

        | 【id: str】 实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def AttackAnimBeginClientEvent(self, args):
        """
        *[event]*

        | 攻击动作开始时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。
        
        -----

        | 【id: str】 实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def StopUsingItemClientEvent(self, args):
        """
        *[event]*

        | 玩家停止使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【itemDict: dict】  `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def StartUsingItemClientEvent(self, args):
        """
        *[event]*

        | 玩家使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【itemDict: dict】  `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PlayerTryDropItemClientEvent(self, args):
        """
        *[event]*

        | 玩家丢弃物品时触发。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【itemDict: dict】 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【$cancel: bool】 是否取消此次操作

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnCarriedNewItemChangedClientEvent(self, args):
        """
        *[event]*

        | 手持物品发生变化时，触发该事件；数量改变不会触发。

        | *作者的tips：*
        | *该事件在进入游戏时会触发一次，且触发时机比UiInitFinished更早。*

        -----

        | 【itemDict: dict】 切换后的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ItemReleaseUsingClientEvent(self, args):
        """
        *[event]*

        | 释放正在使用的物品时触发。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【durationLeft: float】 蓄力剩余时间（当物品缺少"minecraft:maxduration"组件时，蓄力剩余时间为负数）
        | 【itemDict: dict】  `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【maxUseDuration: int】 最大蓄力时长
        | 【$cancel: bool】 设置为True可以取消，需要同时取消服务端事件ItemReleaseUsingServerEvent

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def InventoryItemChangedClientEvent(self, args):
        """
        *[event]*

        | 玩家背包物品变化时客户端抛出的事件。
        | 如果槽位变空，变化后槽位中物品为空气。
        | 触发时槽位物品仍为变化前物品。
        | 背包内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【slot: int】 背包槽位
        | 【oldItemDict: dict】 变化前槽位中的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【newItemDict: dict】 变化后槽位中的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def GrindStoneRemovedEnchantClientEvent(self, args):
        """
        *[event]*

        | 玩家点击砂轮合成得到的物品时抛出的事件。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【oldItemDict: dict】 合成前的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（砂轮内第一个物品）
        | 【additionalItemDict: dict】 作为合成材料的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（砂轮内第二个物品）
        | 【newItemDict: dict】 合成后的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【exp: int】 本次合成返还的经验

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientShapedRecipeTriggeredEvent(self, args):
        """
        *[event]*

        | 玩家合成物品时触发。
        
        -----

        | 【recipeId: str】 配方ID，对应配方json文件中的identifier字段

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientItemUseOnEvent(self, args):
        """
        *[tick]* *[event]*

        | 玩家在对方块使用物品时客户端抛出的事件。
        | 注：如果需要取消物品的使用需要同时在 ``ClientItemUseOnEvent`` 和 ``ServerItemUseOnEvent`` 中将 ``ret`` 设置为 ``True`` 才能正确取消。
        | 该事件仅在鼠标模式下为帧事件。
        
        -----

        | 【entityId: str】 玩家实体ID
        | 【itemDict: dict】  `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【x: int】 方块x坐标
        | 【y: int】 方块y坐标
        | 【z: int】 方块z坐标
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【blockAuxValue: int】 方块的附加值
        | 【face: int】 点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        | 【clickX: float】 点击点的x比例位置
        | 【clickY: float】 点击点的y比例位置
        | 【clickZ: float】 点击点的z比例位置
        | 【$ret: bool】 设为True可取消物品的使用

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientItemTryUseEvent(self, args):
        """
        *[event]*

        | 玩家点击右键尝试使用物品时客户端抛出的事件，可以通过设置 ``cancel`` 为 ``True`` 取消使用物品。
        | 注：如果需要取消物品的使用需要同时在 ``ClientItemTryUseEvent`` 和 ``ServerItemTryUseEvent`` 中将 ``cancel`` 设置为 ``True`` 才能正确取消。
        | ``ServerItemTryUseEvent`` / ``ClientItemTryUseEvent`` 不能取消对方块使用物品的行为，如使用生物蛋，使用桶倒出/收集，使用打火石点燃草等；
        | 如果想要取消这种行为，请使用 ``ClientItemUseOnEvent`` 和 ``ServerItemUseOnEvent`` 。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【itemDict: dict】  `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【$cancel: bool】 是否取消使用物品

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def AnvilCreateResultItemAfterClientEvent(self, args):
        """
        *[event]*

        | 玩家点击铁砧合成得到的物品时抛出的事件。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【itemShowName: str】 合成后的物品显示名称
        | 【itemDict: dict】 合成后的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【oldItemDict: dict】 合成前的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（铁砧内第一个物品）
        | 【materialItemDict: dict】 合成所使用材料的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（铁砧内第二个物品）

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ActorUseItemClientEvent(self, args):
        """
        *[event]*

        | 玩家使用物品时客户端抛出的事件（比较特殊不走该事件的例子：1.喝牛奶；2.染料对有水的炼药锅使用；3.盔甲架装备盔甲）。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【itemDict: dict】  `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【useMethod: int】 使用物品的方法，详见 `ItemUseMethodEnum枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemUseMethodEnum.html?key=ItemUseMethodEnum&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ActorAcquiredItemClientEvent(self, args):
        """
        *[event]*

        | 玩家获得物品时客户端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点）。
        
        -----

        | 【actor: str】 获得物品玩家实体ID
        | 【secondaryActor: str】 物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
        | 【itemDict: dict】 获取到的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        | 【acquireMethod: int】 获得物品的方法，详见 `ItemAcquisitionMethod <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemAcquisitionMethod.html?key=ItemAcquisitionMethod&docindex=1&type=0>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def StepOnBlockClientEvent(self, args):
        """
        *[event]*

        | 实体刚移动至一个新实心方块时触发。
        | 在合并微软更新之后，本事件触发时机与微软molang实验性玩法组件 ``minecraft:on_step_on`` 一致。
        | 压力板与绊线钩在过去的版本的事件是可以触发的，但在更新后这种非实心方块并不会触发，有需要的可以使用 ``OnEntityInsideBlockClientEvent`` 事件。
        | 不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStepOn`` 接口注册才能触发。
        | 原版的红石矿默认注册了，但深层红石矿没有默认注册。
        | 如果需要修改 ``cancel`` ，强烈建议配合服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        
        -----

        | 【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止触发后续原版逻辑
        | 【blockX: int】 方块x坐标
        | 【blockY: int】 方块y坐标
        | 【blockZ: int】 方块z坐标
        | 【entityId: str】 实体ID
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【dimensionId: int】 维度ID
        
        -----

        【相关接口】

        * BlockInfoComponentClient.RegisterOnStepOn(blockName: str, sendPythonEvent: bool) -> bool
        * BlockInfoComponentClient.UnRegisterOnStepOn(blockName: str) -> bool

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def StartDestroyBlockClientEvent(self, args):
        """
        *[event]*

        | 玩家开始挖方块时触发。创造模式下不触发。
        | 如果是隔着火焰挖方块，即使将该事件cancel掉，火焰也会被扑灭。如果要阻止火焰扑灭，需要配合 ``ExtinguishFireClientEvent`` 使用。
        
        -----

        | 【pos: Tuple[float, float, float]】 方块的坐标
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【auxValue: int】 方块的附加值
        | 【playerId: str】 玩家的实体ID
        | 【$cancel: bool】 修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockServerEvent一起修改。
        | 【face: int】 方块被敲击面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html>`_

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def StepOffBlockClientEvent(self, args):
        """
        *[event]*

        | 实体移动离开一个实心方块时触发。
        | 不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStepOff`` 接口注册才能触发。
        | 压力板与绊线钩这种非实心方块不会触发。
        
        -----

        | 【blockX: int】 方块位置x
        | 【blockY: int】 方块位置y
        | 【blockZ: int】 方块位置z
        | 【entityId: str】 实体ID
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【dimensionId: int】 维度ID
        
        -----

        【相关接口】

        * BlockInfoComponentClient.RegisterOnStepOff(blockName: str, sendPythonEvent: bool) -> bool
        * BlockInfoComponentClient.UnRegisterOnStepOff(blockName: str) -> bool

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ShearsDestoryBlockBeforeClientEvent(self, args):
        """
        *[event]*

        | 玩家手持剪刀破坏方块时，有剪刀特殊效果的方块会在客户端线程触发该事件。
        | 目前仅绊线会触发，需要取消剪刀效果得配合 ``ShearsDestoryBlockBeforeServerEvent`` 同时使用。
        
        -----

        | 【blockX: int】 方块位置x
        | 【blockY: int】 方块位置y
        | 【blockZ: int】 方块位置z
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【auxData: int】 方块附加值
        | 【dropName: str】 触发剪刀效果的掉落物identifier，包含命名空间及名称
        | 【dropCount: int】 触发剪刀效果的掉落物数量
        | 【playerId: str】 触发剪刀效果的玩家ID
        | 【dimensionId: int】 玩家触发时的维度ID
        | 【$cancelShears: bool】 是否取消剪刀效果

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PlayerTryDestroyBlockClientEvent(self, args):
        """
        *[event]*

        | 当玩家即将破坏方块时，客户端线程触发该事件。
        | 主要用于床，旗帜，箱子这些根据方块实体数据进行渲染的方块，一般情况下请使用 ``ServerPlayerTryDestroyBlockEvent`` 。
        
        -----

        | 【x: int】 方块x坐标
        | 【y: int】 方块y坐标
        | 【z: int】 方块z坐标
        | 【face: int】 方块被敲击的面向ID，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【auxData: int】 方块附加值
        | 【playerId: str】 试图破坏方块的玩家的实体ID
        | 【$cancel: bool】 默认为False，在脚本层设置为True就能取消该方块的破坏

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnStandOnBlockClientEvent(self, args):
        """
        *[tick]* *[event]*

        | 当实体站立到方块上时客户端持续触发。
        | 不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStandOn`` 接口注册才能触发。
        | 如果要在脚本层修改 ``motion`` / ``cancel`` ，强烈建议配合 ``OnStandOnBlockServerEvent`` 服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        | 如果要在脚本层修改 ``motion`` ，回传的一定要是浮点型，例如需要赋值0.0而不是0。
        
        -----

        | 【entityId: str】 实体ID
        | 【dimensionId: int】 实体所在维度ID
        | 【posX: float】 实体位置x
        | 【posY: float】 实体位置y
        | 【posZ: float】 实体位置z
        | 【$motionX: float】 瞬时移动x方向的力
        | 【$motionY: float】 瞬时移动y方向的力
        | 【$motionZ: float】 瞬时移动z方向的力
        | 【blockX: int】 方块位置x
        | 【blockY: int】 方块位置y
        | 【blockZ: int】 方块位置z
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【$cancel: bool】 可由脚本层回传True给引擎，阻止触发后续原版逻辑
        
        -----

        【相关接口】

        * BlockInfoComponentClient.RegisterOnStandOn(blockName: str, sendPythonEvent: bool) -> bool
        * BlockInfoComponentClient.UnRegisterOnStandOn(blockName: str) -> bool

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnModBlockNeteaseEffectCreatedClientEvent(self, args):
        """
        *[event]*

        | 自定义方块实体绑定的特效创建成功事件。
        | 以及使用接口 ``CreateFrameEffectForBlockEntity`` 或 ``CreateParticleEffectForBlockEntity`` 为自定义方块实体添加特效成功时触发。
        
        -----

        | 【effectName: str】 创建成功的特效的自定义键值名称
        | 【id: int】 该特效的ID
        | 【effectType: int】 该特效的类型，0为粒子特效，1为序列帧特效
        | 【blockPos: Tuple[float, float, float]】 该特效绑定的自定义方块实体的世界坐标

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnEntityInsideBlockClientEvent(self, args):
        """
        *[tick]* *[event]*

        | 当实体碰撞盒所在区域有方块时，客户端持续触发。
        | 不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnEntityInside`` 接口注册才能触发。
        | 如果需要修改 ``slowdownMulti`` / ``cancel`` ，强烈建议与服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        | 如果要在脚本层修改 ``slowdownMulti`` ，回传的一定要是浮点型，例如需要赋值1.0而不是1。
        | 有任意 ``slowdownMulti`` 参数被传回非0值时生效减速比例。
        | ``slowdownMulti`` 参数更像是一个Buff，并不是立刻计算，而是先保存在实体属性里延后计算、在已经有 ``slowdownMulti`` 属性的情况下会取最低的值、免疫掉落伤害等，与原版蜘蛛网逻辑基本一致。
        
        -----

        | 【entityId: str】 实体ID
        | 【dimensionId: int】 实体所在维度ID
        | 【$slowdownMultiX: float】 实体移速x方向的减速比例
        | 【$slowdownMultiY: float】 实体移速y方向的减速比例
        | 【$slowdownMultiZ: float】 实体移速z方向的减速比例
        | 【blockX: int】 方块位置x
        | 【blockY: int】 方块位置y
        | 【blockZ: int】 方块位置z
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【$cancel: bool】 可由脚本层回传True给引擎，阻止触发后续原版逻辑
        
        -----

        【相关接口】

        * BlockInfoComponentClient.RegisterOnEntityInside(blockName: str, sendPythonEvent: bool) -> bool
        * BlockInfoComponentClient.UnRegisterOnEntityInside(blockName: str) -> bool

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnAfterFallOnBlockClientEvent(self, args):
        """
        *[tick]* *[event]*

        | 当实体降落到方块后客户端触发，主要用于力的计算。
        | 不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ）。
        | 如果要在脚本层修改 ``motion`` ，回传的需要是浮点型，例如需要赋值0.0而不是0。
        | 如果需要修改实体的力，最好配合服务端事件同步修改，避免产生非预期现象。
        | 因为引擎最后一定会按照原版方块规则计算力（普通方块置0，床、粘液块等反弹），所以脚本层如果想直接修改当前力需要将 ``calculate`` 设为 ``True`` 取消原版计算，按照传回值计算。
        | 引擎在落地之后 ``OnAfterFallOnBlockClientEvent`` 会一直触发，因此请在脚本层中做对应的逻辑判断。
        
        -----

        | 【entityId: str】 实体ID
        | 【posX: float】 实体位置x
        | 【posY: float】 实体位置y
        | 【posZ: float】 实体位置z
        | 【$motionX: float】 瞬时移动x方向的力
        | 【$motionY: float】 瞬时移动y方向的力
        | 【$motionZ: float】 瞬时移动z方向的力
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【$calculate: bool】 是否按脚本层传值计算力

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def FallingBlockCauseDamageBeforeClientEvent(self, args):
        """
        *[event]*

        | 当下落的方块开始计算砸到实体的伤害时，客户端触发该事件。
        | 不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义重力方块 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/3-%E7%89%B9%E6%AE%8A%E6%96%B9%E5%9D%97/6-%E8%87%AA%E5%AE%9A%E4%B9%89%E9%87%8D%E5%8A%9B%E6%96%B9%E5%9D%97.html>`_ ）。
        | 当该事件的参数数据与服务端事件 ``FallingBlockCauseDamageBeforeServerEvent`` 数据有差异时，请以服务端事件数据为准。
        
        -----

        | 【fallingBlockId: str】 下落的方块实体ID
        | 【fallingBlockX: float】 下落的方块实体位置x
        | 【fallingBlockY: float】 下落的方块实体位置y
        | 【fallingBlockZ: float】 下落的方块实体位置z
        | 【blockName: str】 重力方块的identifier，包含命名空间及名称
        | 【dimensionId: int】 下落的方块实体维度ID
        | 【collidingEntitys: Optional[List[str]]】 当前碰撞到的实体ID列表（客户端只能获取到玩家），如果没有的话是None
        | 【fallTickAmount: int】 下落的方块实体持续下落了多少tick
        | 【fallDistance: float】 下落的方块实体持续下落了多少距离
        | 【isHarmful: bool】 客户端始终为false，因为客户端不会计算伤害值
        | 【fallDamage: int】 对实体的伤害

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ClientBlockUseEvent(self, args):
        """
        *[tick]* *[event]*

        | 玩家右键点击新版自定义方块（或者通过接口 ``AddBlockItemListenForUseEvent`` 增加监听的MC原生游戏方块）时客户端抛出该事件。
        | 有的方块是在 ``ServerBlockUseEvent`` 中设置 ``cancel`` 生效，但是有部分方块是在 ``ClientBlockUseEvent`` 中设置 ``cancel`` 才生效，如有需求建议在两个事件中同时设置 ``cancel`` 以保证生效。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【blockName: str】 方块的identifier，包含命名空间及名称
        | 【aux: int】 方块附加值
        | 【$cancel: bool】 设置为True可拦截与方块交互的逻辑
        | 【x: int】 方块x坐标
        | 【y: int】 方块y坐标
        | 【z: int】 方块z坐标

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def PerspChangeClientEvent(self, args):
        """
        *[event]*

        | 视角切换时会触发的事件。
        | 视角数字代表含义 0: 第一人称 1: 第三人称背面 2: 第三人称正面。
        
        -----

        | 【from: int】 切换前的视角
        | 【to: int】 切换后的视角

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnPlayerHitBlockClientEvent(self, args):
        """
        *[event]*

        | 通过 ``OpenPlayerHitBlockDetection`` 打开方块碰撞检测后，当玩家碰撞到方块时触发该事件。
        | 玩家着地时会触发 ``OnGroundClientEvent`` ，而不是该事件。
        | 客户端和服务端分别作碰撞检测，可能两个事件返回的结果略有差异。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【posX: int】 碰撞方块x坐标
        | 【posY: int】 碰撞方块y坐标
        | 【posZ: int】 碰撞方块z坐标
        | 【blockId: str】 碰撞方块的identifier
        | 【auxValue: int】 碰撞方块的附加值
        
        -----

        【相关接口】

        * PlayerCompClient.OpenPlayerHitBlockDetection(precision: float) -> bool
        * PlayerCompClient.ClosePlayerHitBlockDetection() -> bool

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def GameTypeChangedClientEvent(self, args):
        """
        *[event]*

        | 个人游戏模式发生变化时客户端触发。
        | 游戏模式：生存，创造，冒险分别为0~2。
        | 默认游戏模式发生变化时最后反映在个人游戏模式之上。

        -----

        | 【playerId: str】 玩家的实体ID
        | 【oldGameType: int】 切换前的游戏模式
        | 【newGameType: int】 切换后的游戏模式

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ExtinguishFireClientEvent(self, args):
        """
        *[event]*

        | 玩家扑灭火焰时触发。下雨，倒水等方式熄灭火焰不会触发。
        
        -----

        | 【pos: Tuple[float, float, float]】 火焰方块的坐标
        | 【playerId: str】 玩家的实体ID
        | 【$cancel: bool】 修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireServerEvent一起修改。

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def DimensionChangeFinishClientEvent(self, args):
        """
        *[event]*

        | 玩家维度改变完成后触发。
        | 当通过传送门从末地回到主世界时， ``toPos`` 的y值为32767，其他情况一般会比设置值高1.62。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【fromDimensionId: int】 维度改变前的维度
        | 【toDimensionId: int】 维度改变后的维度
        | 【toPos: Tuple[float, float, float]】 改变后的位置(x,y,z)，其中y值为脚底加上角色的身高值

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def DimensionChangeClientEvent(self, args):
        """
        *[event]*

        | 玩家维度改变时触发。
        | 当通过传送门从末地回到主世界时， ``toY`` 值为32767，其他情况一般会比设置值高1.62。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【fromDimensionId: int】 维度改变前的维度
        | 【toDimensionId: int】 维度改变后的维度
        | 【fromX: float】 改变前的位置x
        | 【fromY: float】 改变前的位置y
        | 【fromZ: float】 改变前的位置z
        | 【toX: float】 改变后的位置x
        | 【toY: float】 改变后的位置y
        | 【toZ: float】 改变后的位置z

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def CameraMotionStopClientEvent(self, args):
        """
        *[event]*

        | 相机运动器停止事件。相机添加运动器并开始运行后，运动器自动停止时触发。
        | 注意：该事件触发表示运动器播放顺利完成，手动调用的 ``StopCameraMotion`` 、 ``RemoveCameraMotion`` 不会触发该事件。
        
        -----

        | 【motionId: int】 运动器ID
        | 【$remove: bool】 是否移除该运动器，设置为False则保留，默认为True，即运动器停止后自动移除

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def CameraMotionStartClientEvent(self, args):
        """
        *[event]*

        | 相机运动器开始事件。相机添加运动器后，运动器开始运行时触发。
        
        -----

        | 【motionId: int】 运动器ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def LeaveEntityClientEvent(self, args):
        """
        *[event]*

        | 玩家远离生物时触发。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【entityId: str】 远离的生物的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def StartRidingClientEvent(self, args):
        """
        *[event]*

        | 一个实体即将骑乘另外一个实体时触发。
        | 如果需要修改 ``cancel`` ，请通过服务端事件 ``StartRidingServerEvent`` 修改，客户端触发该事件时，实体已经骑乘成功。
        
        -----

        | 【actorId: str】 骑乘者的实体ID
        | 【victimId: str】 被骑乘者的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnMobHitMobClientEvent(self, args):
        """
        *[event]*

        | 通过 ``OpenPlayerHitMobDetection`` 打开生物碰撞检测后，当生物间（包含玩家）碰撞时触发该事件。
        | 注：客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。
        | 本事件代替原有的 ``OnPlayerHitMobClientEvent`` 事件。
        
        -----

        | 【mobId: str】 当前生物的实体ID
        | 【hittedMobList: List[str]】 当前生物碰撞到的其他所有生物的实体ID的list
        
        -----

        【相关接口】

        * PlayerCompClient.OpenPlayerHitMobDetection() -> bool
        * PlayerCompClient.ClosePlayerHitMobDetection() -> bool

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnGroundClientEvent(self, args):
        """
        *[event]*

        | 实体着地事件。玩家，沙子，铁砧，掉落的物品，点燃的TNT掉落地面时触发，其余实体着地不触发。
        
        -----

        | 【id: str】 实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def HealthChangeClientEvent(self, args):
        """
        *[event]*

        | 生物生命值发生变化时触发。
        
        -----

        | 【entityId: str】 实体ID
        | 【from: float】 变化前的生命值
        | 【to: float】 变化后的生命值

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def EntityStopRidingEvent(self, args):
        """
        *[event]*

        | 当实体停止骑乘时触发。
        | 以下情况不允许取消：
        * 玩家传送时；
        * 坐骑死亡时；
        * 玩家睡觉时；
        * 玩家死亡时；
        * 未驯服的马；
        * 怕水的生物坐骑进入水里；
        * 切换维度；
        * ride组件 ``StopEntityRiding`` 接口。
        
        -----

        | 【id: str】 实体ID
        | 【rideId: str】 坐骑的实体ID
        | 【exitFromRider: bool】 是否下坐骑
        | 【entityIsBeingDestroyed: bool】 坐骑是否将要销毁
        | 【switchingRides: bool】 是否换乘坐骑
        | 【$cancel: bool】 设置为True可以取消（需要与服务端事件一同取消）

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def EntityModelChangedClientEvent(self, args):
        """
        *[event]*

        | 实体模型切换时触发。
        
        -----

        | 【entityId: str】 实体ID
        | 【newModel: str】 新的模型名字
        | 【oldModel: str】 旧的模型名字

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ApproachEntityClientEvent(self, args):
        """
        *[event]*

        | 玩家靠近生物时触发。
        
        -----

        | 【playerId: str】 玩家的实体ID
        | 【entityId: str】 靠近的生物的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """
    
    def UnLoadClientAddonScriptsBefore(self, args):
        """
        *[event]*

        | 客户端卸载mod之前触发。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def RemovePlayerAOIClientEvent(self, args):
        """
        *[event]*

        | 玩家离开当前玩家同一个区块时触发AOI事件。
        
        -----

        | 【playerId: str】 玩家的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def RemoveEntityClientEvent(self, args):
        """
        *[event]*

        | 客户端侧实体被移除时触发。
        | 客户端接收服务端AOI事件时触发，原事件名 ``RemoveEntityPacketEvent`` 。
        
        -----

        | 【id: str】 移除的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnLocalPlayerStopLoading(self, args):
        """
        *[event]*

        | 玩家进入存档，出生点地形加载完成时触发。该事件触发时可以进行切换维度的操作。
        
        -----

        | 【playerId: str】 玩家的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnCommandOutputClientEvent(self, args):
        """
        *[event]*

        | 当command命令有成功消息输出时触发。
        | 部分命令在返回的时候没有命令名称，命令组件需要 ``showOutput`` 参数为 ``True`` 时才会有返回。

        -----

        | 【command: str】 命令名称
        | 【message: str】 命令返回的消息

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def LoadClientAddonScriptsAfter(self, args):
        """
        *[event]*

        | 客户端加载mod完成事件。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ChunkLoadedClientEvent(self, args):
        """
        *[event]*

        | 客户端区块加载完成时触发。
        
        -----

        | 【dimension: int】 区块所在维度
        | 【chunkPosX: int】 区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
        | 【chunkPosZ: int】 区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def ChunkAcquireDiscardedClientEvent(self, args):
        """
        *[event]*

        | 客户端区块即将被卸载时触发。
        | 区块卸载：游戏只会加载玩家周围的区块，玩家移动到别的区域时，原来所在区域的区块会被卸载，参考 `区块介绍 <https://minecraft.fandom.com/zh/wiki/%E5%8C%BA%E5%9D%97>`_。
        
        -----

        | 【dimension: int】 区块所在维度
        | 【chunkPosX: int】 区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
        | 【chunkPosZ: int】 区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def AddPlayerCreatedClientEvent(self, args):
        """
        *[event]*

        | 玩家进入当前玩家所在的区块AOI后，玩家皮肤数据异步加载完成后触发的事件。
        | 由于玩家皮肤是异步加载的原因，该事件触发时机比 ``AddPlayerAOIClientEvent`` 晚，触发该事件后可以对该玩家调用相关玩家渲染接口。
        | 当前客户端每加载好一个玩家的皮肤，就会触发一次该事件，比如刚进入世界时，本地玩家加载好会触发一次，周围的所有玩家加载好后也会分别触发一次。
        
        -----

        | 【playerId: str】 玩家的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def AddPlayerAOIClientEvent(self, args):
        """
        *[event]*

        | 玩家加入游戏或者其余玩家进入当前玩家所在的区块时触发的AOI事件，替换 ``AddPlayerEvent`` 。
        | 该事件触发只表明在服务端数据中接收到了新玩家，并不能代表此时玩家在客户端中可见，若想在玩家进入AOI后立马调用玩家渲染相关接口，建议使用 ``AddPlayerCreatedClientEvent`` 。
        
        -----

        | 【playerId: str】 玩家的实体ID

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def AddEntityClientEvent(self, args):
        """
        *[event]*

        | 客户端侧创建新实体时触发。创建玩家时不会触发该事件。
        
        -----

        | 【id: str】 实体ID
        | 【posX: float】 位置x
        | 【posY: float】 位置y
        | 【posZ: float】 位置z
        | 【dimensionId: int】 实体维度
        | 【isBaby: bool】 是否为幼儿
        | 【engineTypeStr: str】 实体类型
        | 【itemName: str】 物品identifier（仅当物品实体时存在该字段）
        | 【auxValue: int】 物品附加值（仅当物品实体时存在该字段）

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnScriptTickClient(self):
        """
        *[tick]* *[event]*

        | 客户端tick事件，1秒30次。
        
        -----

        | 无参数

        -----

        :return: 无
        :rtype: None
        """

    def UiInitFinished(self, args):
        """
        *[event]*

        | UI初始化框架完成，此时可以创建UI。
        | 切换维度后会重新初始化UI并触发该事件。
        
        -----

        | 无参数

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    # Lib Event Callbacks ==============================================================================================

    # New Interfaces ===================================================================================================

    def CallServer(self, name, callback=None, *args):
        """
        | 调用服务端属性（包括变量和函数）。
        
        -----

        :param str name: 服务端属性名
        :param function callback: 回调函数，调用服务端成功后服务端会返回结果并调用该函数，该函数接受一个参数，即调用结果，具体用法请看示例
        :param Any args: 调用参数；如果调用的服务端属性为变量，则args会赋值给该变量（不写调用参数则不会进行赋值）；如果调用的服务端属性为函数，则args会作为参数传入该函数

        :return: 无
        :rtype: None
        """

    def BroadcastToAllClient(self, event_name, event_data):
        """
        | 广播事件到所有玩家的客户端。
        | 监听时使用当前客户端的命名空间和名称。
        | 若传递的数据为字典，则客户端接收到的字典会内置一个名为 ``__id__`` 的key，其value为发送广播的玩家实体ID。

        -----

        :param str event_name: 事件名称
        :param Any event_data: 数据

        :return: 是否成功
        :rtype: bool
        """
        if not self.__lib_sys:
            return False
        self.__lib_sys.NotifyToServer("_BroadcastToAllClient", {
            'event_name': event_name,
            'event_data': event_data,
            'namespace': self.__namespace,
            'sys_name': self.__system_name,
        })
        return True

    def RegisterAndCreateUI(self, namespace, ui_key, cls_path, ui_screen_def, stack=False, param=None):
        """
        | 注册并创建UI。
        | 如果UI已创建，则返回其实例。
        | 使用该接口创建的UI，其UI类 ``__init__`` 方法的 ``param`` 参数会自带一个名为 ``__cs__`` 的key，对应的值为创建UI的客户端的实例，可以方便地调用客户端的属性、方法和接口。

        -----

        :param str namespace: 命名空间，建议为mod名字
        :param str ui_key: UI唯一标识
        :param str cls_path: UI类路径
        :param str ui_screen_def: UI画布路径，格式为"namespace.scree_name"，namespace对应UI json文件中"namespace"的值，scree_name为想打开的画布的名称（一般为main）
        :param bool stack: 是否使用堆栈管理的方式创建UI，默认为False
        :param dict|None param: 创建UI的参数字典，会传到UI类__init__方法的param参数中，默认为空字典

        :return: UI类实例，注册或创建失败时返回None
        :rtype: _ScreenNode|None
        """
        node = _client_api.GetUI(namespace, ui_key)
        if node:
            return node
        if not _client_api.RegisterUI(namespace, ui_key, cls_path, ui_screen_def):
            return
        if param is None:
            param = {}
        if isinstance(param, dict):
            param['__cs__'] = self
        if stack:
            return _client_api.PushScreen(namespace, ui_key, param)
        else:
            return _client_api.CreateUI(namespace, ui_key, param)

    # Internal =========================================================================================================

    def _set_print_log(self):
        _client_api.SetMcpModLogCanPostDump(True)

















