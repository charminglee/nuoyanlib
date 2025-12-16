# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


class ClientEvent:
    def UIDefReloadSceneStackAfter(self, args):
        """
        [事件]

        UI热重载（Ctrl+R）完成后触发。

        -----

        【事件参数】

        无
        """
    def UpdatePlayerSkinClientEvent(self, args):
        """
        [事件]

        玩家加入游戏或通过更衣室局内换肤后，同步皮肤信息至客户端后触发。

        -----

        【注意】

        此事件配合 ``IsOfficialSkin`` ``IsHighLevelOfficialSkin`` ``IsHighLevelMultiJointOfficialSkin`` 接口，用于获取玩家的皮肤信息。

        -----

        【事件参数】

        - ``playerId`` -- str，更换皮肤的玩家实体ID
        """
    def PlayerTryRemoveCustomContainerItemClientEvent(self, args):
        """
        [事件]

        玩家尝试从自定义容器中移除物品时触发该事件。

        -----

        【注意】

        该事件在关闭容器物品自动返回背包时也会触发，此时如果取消操作物品将会被留在容器中，容器被破坏物品也不会掉落（因为实际存储于玩家身上），当再次打开netease_ui_container容器时会显示。
        容器内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        cancel取消本次操作后不会触发对应服务端事件。

        -----

        【事件参数】

        - ``itemDict`` -- dict，尝试移除物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，目标容器名称，对应容器json中"custom_description"字段
        - ``collectionType`` -- str，目标容器类型，目前仅支持netease_container和netease_ui_container
        - ``collectionIndex`` -- int，目标容器索引
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        - ``cancel`` -- bool，是否取消该操作，默认为False，事件中改为True时拒绝此次操作
        """
    def PlayerTryAddCustomContainerItemClientEvent(self, args):
        """
        [事件]

        玩家尝试将物品添加到自定义容器时触发该事件。

        -----

        【注意】

        容器内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        cancel取消本次操作后不会触发对应服务端事件。

        -----

        【事件参数】

        - ``itemDict`` -- dict，尝试添加物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，目标容器名称，对应容器json中"custom_description"字段
        - ``collectionType`` -- str，目标容器类型，目前仅支持netease_container和netease_ui_container
        - ``collectionIndex`` -- int，目标容器索引
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        - ``cancel`` -- bool，是否取消该操作，默认为False，事件中改为True时拒绝此次添加到自定义容器的操作
        """
    def PlayerTryPutCustomContainerItemClientEvent(self, args):
        """
        [事件]

        玩家尝试将物品放入自定义容器时触发该事件。

        -----

        【注意】

        该事件只有目标槽位为空或交换物品时触发，如果目标槽位有相同物品时只会触发 ``PlayerTryAddCustomContainerItemServerEvent`` 事件。
        PC存在shift键移动全部物品，放入同种物品时，可能会触发tryadd和tryput，请开发者注意适配。
        容器内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        cancel取消本次操作后不会触发对应服务端事件。

        -----

        【事件参数】

        - ``itemDict`` -- dict，尝试放入物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，放入容器名称，对应容器json中"custom_description"字段
        - ``collectionType`` -- str，放入容器类型，目前仅支持netease_container和netease_ui_container
        - ``collectionIndex`` -- int，放入容器索引
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        - ``cancel`` -- bool，是否取消该操作，默认为False，事件中改为True时拒绝此次放入自定义容器的操作
        """
    def PlayerPermissionChangeClientEvent(self, args):
        """
        [事件]

        玩家权限变更事件。

        具体权限说明：

        - ``build`` -- bool，放置方块
        - ``mine`` -- bool，采集方块
        - ``doorsandswitches`` -- bool，使用门和开关
        - ``opencontainers`` -- bool，打开容器
        - ``attackplayers`` -- bool，攻击玩家
        - ``attackmobs`` -- bool，攻击生物
        - ``op`` -- bool，操作员命令
        - ``teleport`` -- bool，使用传送

        -----

        【注意】

        当 ``PlayerPermissionChangeServerEvent`` 事件返回 ``cancel`` 为 ``True`` 时，权限变动被取消，该事件不会触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家实体ID
        - ``oldPermission`` -- dict，变化前的权限字典
        - ``newPermission`` -- dict，变化后的权限字典
        - ``changeCause`` -- int，变化原因，详见Minecraft枚举值文档的 `PermissionChangeCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PermissionChangeCause.html>`_
        """
    def HudButtonChangedClientEvent(self, args):
        """
        [事件]

        当原生HUD按钮位置或大小发生改变时触发，例如玩家使用了自定义控件功能会触发，可在该事件中修改mod按钮的位置防止重叠。

        修改后的按钮列表中，每个按钮的字段如下：

        - ``areaEnum`` -- str，`HUD原生UI枚举值 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/OriginGUIName.html>`_
        - ``beforeSize`` -- tuple[float, float, float, float]，(xMin, yMin, xMax, yMax)，修改前原生UI的Area
        - ``afterSize`` -- tuple[float, float, float, float]，(xMin, yMin, xMax, yMax)，修改后原生UI的Area

        -----

        【事件参数】

        - ``changedList`` -- tuple[dict]，修改后的按钮列表
        """
    def BlockAnimateRandomTickEvent(self, args):
        """
        [事件]

        以摄像机为中心，随机选取周围的方块触发Tick，触发的数量取决于设备性能。

        只有添加了 ``netease:block_animate_random_tick`` 的自定义方块才会触发此事件。

        -----

        【事件参数】

        - ``blockPos`` -- tuple[float, float, float]，方块坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- int，方块附加值
        """
    def PlayerAttackEntityEvent(self, args):
        """
        [事件]

        当本地玩家攻击时触发该事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``victimId`` -- str，受击者的实体ID
        - ``damage`` -- float，客户端收到的是真实伤害值，且修改无效
        - ``isCrit`` -- bool，本次攻击是否产生暴击，不支持修改
        """
    def OnLocalPlayerActionClientEvent(self, args):
        """
        [事件]

        玩家动作事件，当本地玩家开始/停止某些动作时触发该事件。

        -----

        【事件参数】

        - ``actionType`` -- int，动作事件枚举，详见Minecraft枚举值文档的 `PlayerActionType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PlayerActionType.html>`_
        """
    def OnLocalPlayerStartJumpClientEvent(self, args):
        """
        [事件]

        本地玩家开始跳跃时触发。

        -----

        【事件参数】

        无
        """
    def GameRenderTickEvent(self, args):
        """
        [事件]

        客户端渲染帧开始时触发该事件，一秒触发次数为当前的帧数。

        -----

        【事件参数】

        无
        """
    def GyroSensorChangedClientEvent(self, args):
        """
        [事件]

        陀螺仪传感器姿态发生变化时触发。

        -----

        【注意】

        该事件只适用于移动端。

        -----

        【事件参数】

        - ``xDiff`` -- float，x轴角速度，单位为弧度/s
        - ``yDiff`` -- float，y轴角速度，单位为弧度/s
        - ``zDiff`` -- float，z轴角速度，单位为弧度/s
        - ``orientation`` -- int，当前屏幕朝向，0竖屏正向，1横屏向左，2竖屏倒置，3横屏向右
        - ``timestamp`` -- float，触发时间戳，秒
        """
    def ModBlockEntityTickClientEvent(self, args):
        """
        [事件]

        客户端自定义方块实体tick事件。

        -----

        【注意】

        只有 ``client_tick`` 字段为 ``true`` 的自定义方块实体才能触发该事件（见 `自定义方块实体 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/4-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93.html>`_）。
        目前客户端实体tick范围为硬编码，范围为玩家为中心的等腰等斜边八边形，其中斜边长度为5，非斜边长度为3。

        -----

        【事件参数】

        - ``posX`` -- int，自定义方块实体的位置X
        - ``posY`` -- int，自定义方块实体的位置Y
        - ``posZ`` -- int，自定义方块实体的位置Z
        - ``dimensionId`` -- int，维度ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        """
    def ModBlockEntityRemoveClientEvent(self, args):
        """
        [事件]

        客户端自定义方块实体卸载时触发。

        -----

        【事件参数】

        - ``posX`` -- int，自定义方块实体的位置X
        - ``posY`` -- int，自定义方块实体的位置Y
        - ``posZ`` -- int，自定义方块实体的位置Z
        - ``dimensionId`` -- int，维度ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        """
    def AchievementButtonMovedClientEvent(self, args):
        """
        [事件]

        使用自定义成就系统的时，拖动成就入口结束时触发。

        -----

        【事件参数】

        - ``oldPosition`` -- tuple[float, float]，移动前该控件相对父节点的坐标信息，第一项为横轴，第二项为纵轴
        - ``newPosition`` -- tuple[float, float]，移动后该控件相对父节点的坐标信息，第一项为横轴，第二项为纵轴
        """
    def OnKeyboardControllerLayoutChangeClientEvent(self, args):
        """
        [事件]

        键盘按键映射改变事件。

        -----

        【事件参数】

        - ``action`` -- str，行为
        - ``newKey`` -- int，修改后的键码，详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
        - ``oldKey`` -- int，修改前的键码，详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
        """
    def OnGamepadControllerLayoutChangeClientEvent(self, args):
        """
        [事件]

        游戏手柄按键映射改变事件。

        -----

        【事件参数】

        - ``action`` -- str，行为
        - ``newKey`` -- int，修改后的键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        - ``oldKey`` -- int，修改前的键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        """
    def OnGamepadTriggerClientEvent(self, args):
        """
        [事件]

        游戏手柄扳机事件。当扣动扳机的力度发生改变时触发。

        -----

        【事件参数】

        - ``key`` -- int，键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        - ``magnitude`` -- float，扣动扳机的力度，取值为 0 ~ 1.0
        """
    def OnGamepadStickClientEvent(self, args):
        """
        [事件]

        游戏手柄摇杆事件。当摇杆摇动位置发生改变时触发。

        -----

        【事件参数】

        - ``key`` -- int，键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        - ``x`` -- float，摇杆水平方向的值，从左到右取值为 -1.0 ~ 1.0
        - ``y`` -- float，摇杆竖直方向的值，从下到上取值为 -1.0 ~ 1.0
        """
    def OnGamepadKeyPressClientEvent(self, args):
        """
        [事件]

        游戏手柄按键事件。

        -----

        【事件参数】

        - ``screenName`` -- str，当前screenName
        - ``key`` -- int，键码，详见 `GamepadKeyType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/GamepadKeyType.html?key=GamepadKeyType&docindex=1&type=0>`_
        - ``isDown`` -- str，是否按下，按下为1，弹起为0
        """
    def ModBlockEntityLoadedClientEvent(self, args):
        """
        [事件]

        客户端自定义方块实体加载完成后第一次出现在玩家视野中时触发。

        -----

        【注意】

        只有在客户端自定义方块实体加载完成后，第一次出现在玩家视野中时才会触发该事件。注意：只有添加了自定义方块实体扩展功能的自定义方块实体才能触发该事件（见 `自定义方块实体外观 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/4.1-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93%E5%A4%96%E8%A7%82.html>`_ ）；出生点是常加载区域，来回传送不会重复触发此事件。

        -----

        【事件参数】

        - ``posX`` -- int，自定义方块实体的位置X
        - ``posY`` -- int，自定义方块实体的位置Y
        - ``posZ`` -- int，自定义方块实体的位置Z
        - ``dimensionId`` -- int，维度ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        """
    def CloseNeteaseShopEvent(self, args):
        """
        [事件]

        关闭商城界面时触发，包括脚本商城和Apollo插件商城。

        -----

        【事件参数】

        无
        """
    def PopScreenAfterClientEvent(self, args):
        """
        [事件]

        screen移除触发。

        -----

        【注意】

        与 ``PopScreenEvent`` 不同， ``PopScreenAfterClientEvent`` 触发时机是在完全把UI弹出后，返回的 ``screenName`` 是弹出后最顶层UI的Screen名。

        -----

        【事件参数】

        - ``screenName`` -- str，UI名字
        - ``screenDef`` -- str，包含命名空间的UI名字，格式为namespace.screenName
        """
    def TapOrHoldReleaseClientEvent(self, args):
        """
        [事件]

        玩家点击屏幕后松手时触发。

        -----

        【注意】

        仅在移动端或pc的F11模式下触发，pc的非F11模式可以使用 ``LeftClickReleaseClientEvent`` 与 ``RightClickReleaseClientEvent`` 事件监听鼠标松开。
        短按及长按后松手都会触发该事件。

        -----

        【事件参数】

        无
        """
    def TapBeforeClientEvent(self, args):
        """
        [事件]

        玩家点击屏幕并松手，即将响应到游戏内时触发。

        -----

        【注意】

        仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用 ``LeftClickBeforeClientEvent`` 事件监听鼠标左键。
        玩家点击屏幕的处理顺序为：

        | 1、玩家点击屏幕，没有进行拖动，并在短按判定时间（250毫秒）内松手；
        | 2、触发该事件；
        | 3、若事件没有cancel，则根据准心处的物体类型以及与玩家的距离，进行攻击或放置等操作。

        与 ``GetEntityByCoordEvent`` 事件不同的是，被ui层捕获，没有穿透到世界的点击不会触发该事件，例如：

        | 1、点击原版的移动/跳跃等按钮。
        | 2、通过 ``SetIsHud(0)`` 屏蔽了游戏操作。
        | 3、对按钮使用 ``AddTouchEventHandler`` 接口时 ``isSwallow`` 参数设置为 ``True`` 。

        -----

        【事件参数】

        - ``cancel`` -- bool，设置为True可拦截原版的攻击或放置响应
        """
    def RightClickReleaseClientEvent(self, args):
        """
        [事件]

        玩家松开鼠标右键时触发。

        -----

        【注意】

        仅在pc的普通控制模式（即非F11模式）下触发。
        在F11下右键，按下会触发 ``RightClickBeforeClientEvent`` ，松开时会触发 ``TapOrHoldReleaseClientEvent`` 。
        pc的普通控制模式下的鼠标点击流程见 ``TapOrHoldReleaseClientEvent`` 备注中的 `配图 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%8E%A7%E5%88%B6.html?key=TapOrHoldReleaseClientEvent&docindex=6&type=0>`_。

        -----

        【事件参数】

        无
        """
    def RightClickBeforeClientEvent(self, args):
        """
        [事件]

        玩家按下鼠标右键时触发。仅在pc下触发（普通控制模式及F11模式都会触发）。

        -----

        【事件参数】

        - ``cancel`` -- bool，设置为True可拦截原版的物品使用/实体交互响应
        """
    def OnMouseMiddleDownClientEvent(self, args):
        """
        [事件]

        鼠标按下中键时触发。

        -----

        【注意】

        仅通过 ``PushScreen`` 创建的界面能够正常返回坐标，开启F11模式的时候，返回最后点击屏幕时的坐标。

        -----

        【事件参数】

        - ``isDown`` -- str，是否按下，按下为1，弹起为0
        - ``mousePositionX`` -- float，按下时的x坐标
        - ``mousePositionY`` -- float，按下时的y坐标
        """
    def OnKeyPressInGame(self, args):
        """
        [事件]

        按键按下或按键释放时触发。

        -----

        【事件参数】

        - ``screenName`` -- str，当前screenName
        - ``key`` -- str，键码（注：这里的int型被转成了str型，比如"1"对应的就是枚举值文档中的1），详见 `KeyBoardType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/KeyBoardType.html?key=KeyBoardType&docindex=1&type=0>`_
        - ``isDown`` -- str，是否按下，按下为1，弹起为0
        """
    def OnClientPlayerStopMove(self, args):
        """
        [事件]

        移动按钮按下释放时触发事件，同时按下多个方向键，需要释放所有的方向键才会触发事件。

        -----

        【事件参数】

        无
        """
    def OnClientPlayerStartMove(self, args):
        """
        [事件]

        移动按钮按下触发事件，在按住一个方向键的同时，去按另外一个方向键，不会触发第二次。

        -----

        【事件参数】

        无
        """
    def OnBackButtonReleaseClientEvent(self, args):
        """
        [事件]

        返回按钮（目前特指安卓系统导航中的返回按钮）松开时触发。

        -----

        【事件参数】

        无
        """
    def MouseWheelClientEvent(self, args):
        """
        [事件]

        鼠标滚轮滚动时触发。

        -----

        【事件参数】

        - ``direction`` -- int，1为向上滚动，0为向下滚动
        """
    def LeftClickReleaseClientEvent(self, args):
        """
        [事件]

        玩家松开鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。

        -----

        【事件参数】

        无
        """
    def LeftClickBeforeClientEvent(self, args):
        """
        [事件]

        玩家按下鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。

        -----

        【事件参数】

        - ``cancel`` -- bool，设置为True可拦截原版的挖方块或攻击响应
        """
    def HoldBeforeClientEvent(self, args):
        """
        [事件]

        玩家长按屏幕，即将响应到游戏内时触发。

        -----

        【注意】

        仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用 ``RightClickBeforeClientEvent`` 事件监听鼠标右键。
        玩家长按屏幕的处理顺序为：

        | 1、玩家点击屏幕，在长按判定时间内（默认为400毫秒，可通过 ``SetHoldTimeThreshold`` 接口修改）一直没有进行拖动或松手；
        | 2、触发该事件；
        | 3、若事件没有cancel，则根据主手上的物品，准心处的物体类型以及与玩家的距离，进行挖方块/使用物品/与实体交互等操作。

        即该事件只会在到达长按判定时间的瞬间触发一次，后面一直按住不会连续触发，可以使用 ``TapOrHoldReleaseClientEvent`` 监听长按后松手。
        与 ``TapBeforeClientEvent`` 事件类似，被ui层捕获，没有穿透到世界的点击不会触发该事件。

        -----

        【事件参数】

        - ``cancel`` -- bool，设置为True可拦截原版的挖方块/使用物品/与实体交互响应
        """
    def GetEntityByCoordReleaseClientEvent(self, args):
        """
        [事件]

        玩家点击屏幕后松开时触发，多个手指点在屏幕上时，只有最后一个手指松开时触发。

        -----

        【事件参数】

        - ``x`` -- int，手指点击位置x坐标
        - ``y`` -- int，手指点击位置y坐标
        """
    def GetEntityByCoordEvent(self, args):
        """
        [事件]

        玩家点击屏幕时触发，多个手指点在屏幕上时，只有第一个会触发。

        -----

        【事件参数】

        无
        """
    def ClientJumpButtonReleaseEvent(self, args):
        """
        [事件]

        跳跃按钮按下释放事件。

        -----

        【事件参数】

        无
        """
    def ClientJumpButtonPressDownEvent(self, args):
        """
        [事件]

        跳跃按钮按下事件，返回值设置参数只对当次按下事件起作用。

        -----

        【事件参数】

        - ``continueJump`` -- bool，设置是否执行跳跃逻辑
        """
    def PlaySoundClientEvent(self, args):
        """
        [事件]

        播放场景音效或UI音效时触发。

        -----

        【事件参数】

        - ``name`` -- str，即资源包中sounds/sound_definitions.json中的key
        - ``pos`` -- tuple[float, float, float]，音效播放的位置，UI音效为(0,0,0)
        - ``volume`` -- float，音量，范围为0-1
        - ``pitch`` -- float，播放速度，正常速度为1
        - ``cancel`` -- bool，设为True可屏蔽该次音效播放
        """
    def PlayMusicClientEvent(self, args):
        """
        [事件]

        播放背景音乐时触发。

        -----

        【事件参数】

        - ``name`` -- str，即资源包中sounds/music_definitions.json中的event_name，并且对应sounds/sound_definitions.json中的key
        - ``cancel`` -- bool，设为True可屏蔽该次音效播放
        """
    def OnMusicStopClientEvent(self, args):
        """
        [事件]

        音乐停止时，当玩家调用 ``StopCustomMusic`` 来停止自定义背景音乐时，会触发该事件。

        -----

        【事件参数】

        - ``musicName`` -- str，音乐名称
        """
    def ScreenSizeChangedClientEvent(self, args):
        """
        [事件]

        改变屏幕大小时会触发的事件。该事件仅支持PC。

        -----

        【事件参数】

        - ``beforeX`` -- float，屏幕大小改变前的宽度
        - ``beforeY`` -- float，屏幕大小改变前的高度
        - ``afterX`` -- float，屏幕大小改变后的宽度
        - ``afterY`` -- float，屏幕大小改变后的高度
        """
    def PushScreenEvent(self, args):
        """
        [事件]

        screen创建触发。

        -----

        【事件参数】

        - ``screenName`` -- str，UI名字
        - ``screenDef`` -- str，包含命名空间的UI名字，格式为namespace.screenName
        """
    def PopScreenEvent(self, args):
        """
        [事件]

        screen移除触发。

        -----

        【注意】

        ``screenName`` 为正在弹出的Screen名，如果需要获取下一个Screen可使用 ``PopScreenAfterClientEvent`` 。

        -----

        【事件参数】

        - ``screenName`` -- str，UI名字
        - ``screenDef`` -- str，包含命名空间的UI名字，格式为"namespace.screenName"
        """
    def PlayerChatButtonClickClientEvent(self, args):
        """
        [事件]

        玩家点击聊天按钮或回车键触发呼出聊天窗口时客户端抛出的事件。

        -----

        【事件参数】

        无
        """
    def OnItemSlotButtonClickedEvent(self, args):
        """
        [事件]

        点击快捷栏、背包栏、盔甲栏、副手栏的物品槽时触发。

        -----

        【事件参数】

        - ``slotIndex`` -- int，点击的物品槽的编号，编号对应位置详见 `物品栏 <https://minecraft.fandom.com/zh/wiki/%E7%89%A9%E5%93%81%E6%A0%8F>`_
        """
    def GridComponentSizeChangedClientEvent(self, args):
        """
        [事件]

        UI grid组件里格子数目发生变化时触发。

        -----

        【事件参数】

        - ``path`` -- str，grid网格所在的路径（从UI根节点算起）
        """
    def ClientPlayerInventoryOpenEvent(self, args):
        """
        [事件]

        打开物品背包界面时触发。

        -----

        【事件参数】

        - ``isCreative`` -- bool，是否是创造模式背包界面
        - ``cancel`` -- bool，是否取消打开物品背包界面。
        """
    def ClientPlayerInventoryCloseEvent(self, args):
        """
        [事件]

        关闭物品背包界面时触发。

        -----

        【事件参数】

        无
        """
    def ClientChestOpenEvent(self, args):
        """
        [事件]

        打开箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``x`` -- int，箱子x坐标
        - ``y`` -- int，箱子y坐标
        - ``z`` -- int，箱子z坐标
        """
    def ClientChestCloseEvent(self, args):
        """
        [事件]

        关闭箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子。

        -----

        【事件参数】

        无
        """
    def WalkAnimEndClientEvent(self, args):
        """
        [事件]

        走路动作结束时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def WalkAnimBeginClientEvent(self, args):
        """
        [事件]

        走路动作开始时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def AttackAnimEndClientEvent(self, args):
        """
        [事件]

        攻击动作结束时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def AttackAnimBeginClientEvent(self, args):
        """
        [事件]

        攻击动作开始时触发。使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def StopUsingItemClientEvent(self, args):
        """
        [事件]

        玩家停止使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def StartUsingItemClientEvent(self, args):
        """
        [事件]

        玩家使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def PlayerTryDropItemClientEvent(self, args):
        """
        [事件]

        玩家丢弃物品时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict，`物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``cancel`` -- bool，是否取消此次操作
        """
    def OnCarriedNewItemChangedClientEvent(self, args):
        """
        [事件]

        手持物品发生变化时，触发该事件；数量改变不会触发。

        -----

        【注意】

        该事件在进入游戏时会触发一次，且触发时机比UiInitFinished更早。

        -----

        【事件参数】

        - ``itemDict`` -- dict | None，切换后的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def ItemReleaseUsingClientEvent(self, args):
        """
        [事件]

        释放正在使用的物品时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``durationLeft`` -- float，蓄力剩余时间（当物品缺少"minecraft:maxduration"组件时，蓄力剩余时间为负数）
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``maxUseDuration`` -- int，最大蓄力时长
        - ``cancel`` -- bool，设置为True可以取消，需要同时取消服务端事件ItemReleaseUsingServerEvent
        """
    def InventoryItemChangedClientEvent(self, args):
        """
        [事件]

        玩家背包物品变化时客户端抛出的事件。

        -----

        【注意】

        如果槽位变空，变化后槽位中物品为空气。
        触发时槽位物品仍为变化前物品。
        背包内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``slot`` -- int，背包槽位
        - ``oldItemDict`` -- dict | None，变化前槽位中的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``newItemDict`` -- dict | None，变化后槽位中的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def GrindStoneRemovedEnchantClientEvent(self, args):
        """
        [事件]

        玩家点击砂轮合成得到的物品时抛出的事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``oldItemDict`` -- dict，合成前的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（砂轮内第一个物品）
        - ``additionalItemDict`` -- dict，作为合成材料的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（砂轮内第二个物品）
        - ``newItemDict`` -- dict，合成后的物品 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``exp`` -- int，本次合成返还的经验
        """
    def ClientShapedRecipeTriggeredEvent(self, args):
        """
        [事件]

        玩家合成物品时触发。

        -----

        【事件参数】

        - ``recipeId`` -- str，配方ID，对应配方json文件中的identifier字段
        """
    def ClientItemUseOnEvent(self, args):
        """
        [事件] [tick]

        玩家在对方块使用物品时客户端抛出的事件。

        -----

        【注意】

        如果需要取消物品的使用需要同时在 ``ClientItemUseOnEvent`` 和 ``ServerItemUseOnEvent`` 中将 ``ret`` 设置为 ``True`` 才能正确取消。
        该事件仅在鼠标模式下为帧事件。

        -----

        【事件参数】

        - ``entityId`` -- str，玩家实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``blockAuxValue`` -- int，方块的附加值
        - ``face`` -- int，点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``clickX`` -- float，点击点的x比例位置
        - ``clickY`` -- float，点击点的y比例位置
        - ``clickZ`` -- float，点击点的z比例位置
        - ``ret`` -- bool，设为True可取消物品的使用
        """
    def ClientItemTryUseEvent(self, args):
        """
        [事件]

        玩家点击右键尝试使用物品时客户端抛出的事件，可以通过设置 ``cancel`` 为 ``True`` 取消使用物品。

        -----

        【注意】

        如果需要取消物品的使用需要同时在 ``ClientItemTryUseEvent`` 和 ``ServerItemTryUseEvent`` 中将 ``cancel`` 设置为 ``True`` 才能正确取消。
        ``ServerItemTryUseEvent`` / ``ClientItemTryUseEvent`` 不能取消对方块使用物品的行为，如使用生物蛋，使用桶倒出/收集，使用打火石点燃草等；
        如果想要取消这种行为，请使用 ``ClientItemUseOnEvent`` 和 ``ServerItemUseOnEvent`` 。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``cancel`` -- bool，是否取消使用物品
        """
    def AnvilCreateResultItemAfterClientEvent(self, args):
        """
        [事件]

        玩家点击铁砧合成得到的物品时抛出的事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemShowName`` -- str，合成后的物品显示名称
        - ``itemDict`` -- dict，合成后的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``oldItemDict`` -- dict，合成前的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（铁砧内第一个物品）
        - ``materialItemDict`` -- dict，合成所使用材料的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_（铁砧内第二个物品）
        """
    def ActorUseItemClientEvent(self, args):
        """
        [事件]

        玩家使用物品时客户端抛出的事件（比较特殊不走该事件的例子：1.喝牛奶；2.染料对有水的炼药锅使用；3.盔甲架装备盔甲）。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``useMethod`` -- int，使用物品的方法，详见 `ItemUseMethodEnum枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemUseMethodEnum.html?key=ItemUseMethodEnum&docindex=1&type=0>`_
        """
    def ActorAcquiredItemClientEvent(self, args):
        """
        [事件]

        玩家获得物品时客户端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点）。

        -----

        【事件参数】

        - ``actor`` -- str，获得物品玩家实体ID
        - ``secondaryActor`` -- str，物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
        - ``itemDict`` -- dict，获取到的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``acquireMethod`` -- int，获得物品的方法，详见 `ItemAcquisitionMethod <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemAcquisitionMethod.html?key=ItemAcquisitionMethod&docindex=1&type=0>`_
        """
    def StepOnBlockClientEvent(self, args):
        """
        [事件]

        实体刚移动至一个新实心方块时触发。

        -----

        【注意】

        在合并微软更新之后，本事件触发时机与微软molang实验性玩法组件 ``minecraft:on_step_on`` 一致。
        压力板与绊线钩在过去的版本的事件是可以触发的，但在更新后这种非实心方块并不会触发，有需要的可以使用 ``OnEntityInsideBlockClientEvent`` 事件。
        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStepOn`` 接口注册才能触发。
        原版的红石矿默认注册了，但深层红石矿没有默认注册。
        如果需要修改 ``cancel`` ，强烈建议配合服务端事件同步修改，避免出现被服务端矫正等非预期现象。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否允许触发，默认为False，若设为True，可阻止触发后续原版逻辑
        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``entityId`` -- str，实体ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID

        -----

        【相关接口】

        - `RegisterOnStepOn <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=RegisterOnStepOn&docindex=2&type=0>`_
        - `UnRegisterOnStepOn <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=UnRegisterOnStepOn&docindex=1&type=0>`_
        """
    def StartDestroyBlockClientEvent(self, args):
        """
        [事件]

        玩家开始挖方块时触发。创造模式下不触发。

        -----

        【注意】

        如果是隔着火焰挖方块，即使将该事件cancel掉，火焰也会被扑灭。如果要阻止火焰扑灭，需要配合 ``ExtinguishFireClientEvent`` 使用。

        -----

        【事件参数】

        - ``pos`` -- tuple[float, float, float]，方块的坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxValue`` -- int，方块的附加值
        - ``playerId`` -- str，玩家的实体ID
        - ``cancel`` -- bool，修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockServerEvent一起修改。
        - ``face`` -- int，方块被敲击面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html>`_
        """
    def StepOffBlockClientEvent(self, args):
        """
        [事件]

        实体移动离开一个实心方块时触发。

        -----

        【注意】

        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStepOff`` 接口注册才能触发。
        压力板与绊线钩这种非实心方块不会触发。

        -----

        【事件参数】

        - ``blockX`` -- int，方块位置x
        - ``blockY`` -- int，方块位置y
        - ``blockZ`` -- int，方块位置z
        - ``entityId`` -- str，实体ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID

        -----

        【相关接口】

        - `RegisterOnStepOff <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=RegisterOnStepOff&docindex=2&type=0>`_
        - `UnRegisterOnStepOff <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=UnRegisterOnStepOff&docindex=2&type=0>`_
        """
    def ShearsDestoryBlockBeforeClientEvent(self, args):
        """
        [事件]

        玩家手持剪刀破坏方块时，有剪刀特殊效果的方块会在客户端线程触发该事件。

        -----

        【注意】

        目前仅绊线会触发，需要取消剪刀效果得配合 ``ShearsDestoryBlockBeforeServerEvent`` 同时使用。

        -----

        【事件参数】

        - ``blockX`` -- int，方块位置x
        - ``blockY`` -- int，方块位置y
        - ``blockZ`` -- int，方块位置z
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- int，方块附加值
        - ``dropName`` -- str，触发剪刀效果的掉落物identifier，包含命名空间及名称
        - ``dropCount`` -- int，触发剪刀效果的掉落物数量
        - ``playerId`` -- str，触发剪刀效果的玩家实体ID
        - ``dimensionId`` -- int，玩家触发时的维度ID
        - ``cancelShears`` -- bool，是否取消剪刀效果
        """
    def PlayerTryDestroyBlockClientEvent(self, args):
        """
        [事件]

        当玩家即将破坏方块时，客户端线程触发该事件。

        -----

        【注意】

        主要用于床，旗帜，箱子这些根据方块实体数据进行渲染的方块，一般情况下请使用 ``ServerPlayerTryDestroyBlockEvent`` 。

        -----

        【事件参数】

        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``face`` -- int，方块被敲击的面向ID，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- int，方块附加值
        - ``playerId`` -- str，试图破坏方块的玩家的实体ID
        - ``cancel`` -- bool，默认为False，在脚本层设置为True就能取消该方块的破坏
        """
    def OnStandOnBlockClientEvent(self, args):
        """
        [事件] [tick]

        当实体站立到方块上时客户端持续触发。

        -----

        【注意】

        不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStandOn`` 接口注册才能触发。
        如果要在脚本层修改 ``motion`` / ``cancel`` ，强烈建议配合 ``OnStandOnBlockServerEvent`` 服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        如果要在脚本层修改 ``motion`` ，回传的一定要是浮点型，例如需要赋值0.0而不是0。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``dimensionId`` -- int，实体所在维度ID
        - ``posX`` -- float，实体位置x
        - ``posY`` -- float，实体位置y
        - ``posZ`` -- float，实体位置z
        - ``motionX`` -- float，瞬时移动x方向的力
        - ``motionY`` -- float，瞬时移动y方向的力
        - ``motionZ`` -- float，瞬时移动z方向的力
        - ``blockX`` -- int，方块位置x
        - ``blockY`` -- int，方块位置y
        - ``blockZ`` -- int，方块位置z
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``cancel`` -- bool，可由脚本层回传True给引擎，阻止触发后续原版逻辑

        -----

        【相关接口】

        - `RegisterOnStandOn <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=RegisterOnStandOn&docindex=2&type=0>`_
        - `UnRegisterOnStandOn <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=UnRegisterOnStandOn&docindex=2&type=0>`_
        """
    def OnModBlockNeteaseEffectCreatedClientEvent(self, args):
        """
        [事件]

        自定义方块实体绑定的特效创建成功事件。

        -----

        【注意】

        以及使用接口 ``CreateFrameEffectForBlockEntity`` 或 ``CreateParticleEffectForBlockEntity`` 为自定义方块实体添加特效成功时触发。

        -----

        【事件参数】

        - ``effectName`` -- str，创建成功的特效的自定义键值名称
        - ``id`` -- int，该特效的ID
        - ``effectType`` -- int，该特效的类型，0为粒子特效，1为序列帧特效
        - ``blockPos`` -- tuple[float, float, float]，该特效绑定的自定义方块实体的世界坐标
        """
    def OnEntityInsideBlockClientEvent(self, args):
        """
        [事件] [tick]

        当实体碰撞盒所在区域有方块时，客户端持续触发。

        -----

        【注意】

        不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnEntityInside`` 接口注册才能触发。
        如果需要修改 ``slowdownMulti`` / ``cancel`` ，强烈建议与服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        如果要在脚本层修改 ``slowdownMulti`` ，回传的一定要是浮点型，例如需要赋值1.0而不是1。
        有任意 ``slowdownMulti`` 参数被传回非0值时生效减速比例。
        ``slowdownMulti`` 参数更像是一个Buff，并不是立刻计算，而是先保存在实体属性里延后计算、在已经有 ``slowdownMulti`` 属性的情况下会取最低的值、免疫掉落伤害等，与原版蜘蛛网逻辑基本一致。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``dimensionId`` -- int，实体所在维度ID
        - ``slowdownMultiX`` -- float，实体移速x方向的减速比例
        - ``slowdownMultiY`` -- float，实体移速y方向的减速比例
        - ``slowdownMultiZ`` -- float，实体移速z方向的减速比例
        - ``blockX`` -- int，方块位置x
        - ``blockY`` -- int，方块位置y
        - ``blockZ`` -- int，方块位置z
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``cancel`` -- bool，可由脚本层回传True给引擎，阻止触发后续原版逻辑

        -----

        【相关接口】

        - `RegisterOnEntityInside <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=RegisterOnEntityInside&docindex=2&type=0>`_
        - `UnRegisterOnEntityInside <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=UnRegisterOnEntityInside&docindex=2&type=0>`_
        """
    def OnAfterFallOnBlockClientEvent(self, args):
        """
        [事件] [tick]

        当实体降落到方块后客户端触发，主要用于力的计算。

        -----

        【注意】

        不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ）。
        如果要在脚本层修改 ``motion`` ，回传的需要是浮点型，例如需要赋值0.0而不是0。
        如果需要修改实体的力，最好配合服务端事件同步修改，避免产生非预期现象。
        因为引擎最后一定会按照原版方块规则计算力（普通方块置0，床、粘液块等反弹），所以脚本层如果想直接修改当前力需要将 ``calculate`` 设为 ``True`` 取消原版计算，按照传回值计算。
        引擎在落地之后 ``OnAfterFallOnBlockClientEvent`` 会一直触发，因此请在脚本层中做对应的逻辑判断。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``posX`` -- float，实体位置x
        - ``posY`` -- float，实体位置y
        - ``posZ`` -- float，实体位置z
        - ``motionX`` -- float，瞬时移动x方向的力
        - ``motionY`` -- float，瞬时移动y方向的力
        - ``motionZ`` -- float，瞬时移动z方向的力
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``calculate`` -- bool，是否按脚本层传值计算力
        """
    def FallingBlockCauseDamageBeforeClientEvent(self, args):
        """
        [事件]

        当下落的方块开始计算砸到实体的伤害时，客户端触发该事件。

        -----

        【注意】

        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义重力方块 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/3-%E7%89%B9%E6%AE%8A%E6%96%B9%E5%9D%97/6-%E8%87%AA%E5%AE%9A%E4%B9%89%E9%87%8D%E5%8A%9B%E6%96%B9%E5%9D%97.html>`_ ）。
        当该事件的参数数据与服务端事件 ``FallingBlockCauseDamageBeforeServerEvent`` 数据有差异时，请以服务端事件数据为准。

        -----

        【事件参数】

        - ``fallingBlockId`` -- str，下落的方块实体ID
        - ``fallingBlockX`` -- float，下落的方块实体位置x
        - ``fallingBlockY`` -- float，下落的方块实体位置y
        - ``fallingBlockZ`` -- float，下落的方块实体位置z
        - ``blockName`` -- str，重力方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，下落的方块实体维度ID
        - ``collidingEntitys`` -- list[str] | None，当前碰撞到的实体ID列表（客户端只能获取到玩家），如果没有的话是None
        - ``fallTickAmount`` -- int，下落的方块实体持续下落了多少tick
        - ``fallDistance`` -- float，下落的方块实体持续下落了多少距离
        - ``isHarmful`` -- bool，客户端始终为false，因为客户端不会计算伤害值
        - ``fallDamage`` -- int，对实体的伤害
        """
    def ClientBlockUseEvent(self, args):
        """
        [事件] [tick]

        玩家右键点击新版自定义方块（或者通过接口 ``AddBlockItemListenForUseEvent`` 增加监听的MC原生游戏方块）时客户端抛出该事件。

        -----

        【注意】

        有的方块是在 ``ServerBlockUseEvent`` 中设置 ``cancel`` 生效，但是有部分方块是在 ``ClientBlockUseEvent`` 中设置 ``cancel`` 才生效，如有需求建议在两个事件中同时设置 ``cancel`` 以保证生效。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``aux`` -- int，方块附加值
        - ``cancel`` -- bool，设置为True可拦截与方块交互的逻辑
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``clickX`` -- float，点击点的x比例位置
        - ``clickY`` -- float，点击点的y比例位置
        - ``clickZ`` -- float，点击点的z比例位置
        """
    def PerspChangeClientEvent(self, args):
        """
        [事件]

        视角切换时会触发的事件。

        -----

        【注意】

        视角数字代表含义 0`` -- 第一人称 1`` -- 第三人称背面 2`` -- 第三人称正面。

        -----

        【事件参数】

        - ``from`` -- int，切换前的视角（请使用event['from']获取该参数）
        - ``to`` -- int，切换后的视角
        """
    def OnPlayerHitBlockClientEvent(self, args):
        """
        [事件]

        通过 ``OpenPlayerHitBlockDetection`` 打开方块碰撞检测后，当玩家碰撞到方块时触发该事件。

        -----

        【注意】

        玩家着地时会触发 ``OnGroundClientEvent`` ，而不是该事件。
        客户端和服务端分别作碰撞检测，可能两个事件返回的结果略有差异。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``posX`` -- int，碰撞方块x坐标
        - ``posY`` -- int，碰撞方块y坐标
        - ``posZ`` -- int，碰撞方块z坐标
        - ``blockId`` -- str，碰撞方块的identifier
        - ``auxValue`` -- int，碰撞方块的附加值

        -----

        【相关接口】

        - `OpenPlayerHitBlockDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E7%8E%A9%E5%AE%B6.html?key=OpenPlayerHitBlockDetection&docindex=4&type=0>`_
        - `ClosePlayerHitBlockDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E7%8E%A9%E5%AE%B6.html?key=ClosePlayerHitBlockDetection&docindex=1&type=0>`_
        """
    def GameTypeChangedClientEvent(self, args):
        """
        [事件]

        个人游戏模式发生变化时客户端触发。

        -----

        【注意】

        游戏模式：生存，创造，冒险分别为0~2。
        默认游戏模式发生变化时最后反映在个人游戏模式之上。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``oldGameType`` -- int，切换前的游戏模式
        - ``newGameType`` -- int，切换后的游戏模式
        """
    def ExtinguishFireClientEvent(self, args):
        """
        [事件]

        玩家扑灭火焰时触发。下雨，倒水等方式熄灭火焰不会触发。

        -----

        【事件参数】

        - ``pos`` -- tuple[float, float, float]，火焰方块的坐标
        - ``playerId`` -- str，玩家的实体ID
        - ``cancel`` -- bool，修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireServerEvent一起修改。
        """
    def DimensionChangeFinishClientEvent(self, args):
        """
        [事件]

        玩家维度改变完成后触发。

        -----

        【注意】

        当通过传送门从末地回到主世界时， ``toPos`` 的y值为32767，其他情况一般会比设置值高1.62。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``fromDimensionId`` -- int，维度改变前的维度
        - ``toDimensionId`` -- int，维度改变后的维度
        - ``toPos`` -- tuple[float, float, float]，改变后的位置(x,y,z)，其中y值为脚底加上角色的身高值
        """
    def DimensionChangeClientEvent(self, args):
        """
        [事件]

        玩家维度改变时触发。

        -----

        【注意】

        当通过传送门从末地回到主世界时， ``toY`` 值为32767，其他情况一般会比设置值高1.62。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``fromDimensionId`` -- int，维度改变前的维度
        - ``toDimensionId`` -- int，维度改变后的维度
        - ``fromX`` -- float，改变前的位置x
        - ``fromY`` -- float，改变前的位置y
        - ``fromZ`` -- float，改变前的位置z
        - ``toX`` -- float，改变后的位置x
        - ``toY`` -- float，改变后的位置y
        - ``toZ`` -- float，改变后的位置z
        """
    def CameraMotionStopClientEvent(self, args):
        """
        [事件]

        相机运动器停止事件。相机添加运动器并开始运行后，运动器自动停止时触发。

        -----

        【注意】

        该事件触发表示运动器播放顺利完成，手动调用的 ``StopCameraMotion`` 、 ``RemoveCameraMotion`` 不会触发该事件。

        -----

        【事件参数】

        - ``motionId`` -- int，运动器ID
        - ``remove`` -- bool，是否移除该运动器，设置为False则保留，默认为True，即运动器停止后自动移除
        """
    def CameraMotionStartClientEvent(self, args):
        """
        [事件]

        相机运动器开始事件。相机添加运动器后，运动器开始运行时触发。

        -----

        【事件参数】

        - ``motionId`` -- int，运动器ID
        """
    def LeaveEntityClientEvent(self, args):
        """
        [事件]

        玩家远离生物时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``entityId`` -- str，远离的生物的实体ID
        """
    def StartRidingClientEvent(self, args):
        """
        [事件]

        一个实体即将骑乘另外一个实体时触发。

        -----

        【注意】

        如果需要修改 ``cancel`` ，请通过服务端事件 ``StartRidingServerEvent`` 修改，客户端触发该事件时，实体已经骑乘成功。

        -----

        【事件参数】

        - ``actorId`` -- str，骑乘者的实体ID
        - ``victimId`` -- str，被骑乘者的实体ID
        """
    def OnMobHitMobClientEvent(self, args):
        """
        [事件]

        通过 ``OpenPlayerHitMobDetection`` 打开生物碰撞检测后，当生物间（包含玩家）碰撞时触发该事件。

        -----

        【注意】

        客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。
        本事件代替原有的 ``OnPlayerHitMobClientEvent`` 事件。

        -----

        【事件参数】

        - ``mobId`` -- str，当前生物的实体ID
        - ``hittedMobList`` -- list[str]，当前生物碰撞到的其他所有生物的实体ID的list

        -----

        【相关接口】

        - `OpenPlayerHitMobDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=OpenPlayerHitMobDetection&docindex=4&type=0>`_
        - `ClosePlayerHitMobDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=ClosePlayerHitMobDetection&docindex=1&type=0>`_
        """
    def OnGroundClientEvent(self, args):
        """
        [事件]

        实体着地事件。玩家，沙子，铁砧，掉落的物品，点燃的TNT掉落地面时触发，其余实体着地不触发。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def HealthChangeClientEvent(self, args):
        """
        [事件]

        生物生命值发生变化时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``from`` -- float，变化前的生命值（请使用event['from']获取该参数）
        - ``to`` -- float，变化后的生命值
        """
    def EntityStopRidingEvent(self, args):
        """
        [事件]

        当实体停止骑乘时触发。

        -----

        【注意】

        以下情况不允许取消：

        - 玩家传送时；
        - 坐骑死亡时；
        - 玩家睡觉时；
        - 玩家死亡时；
        - 未驯服的马；
        - 怕水的生物坐骑进入水里；
        - 切换维度；
        - ride组件 ``StopEntityRiding`` 接口。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        - ``rideId`` -- str，坐骑的实体ID
        - ``exitFromRider`` -- bool，是否下坐骑
        - ``entityIsBeingDestroyed`` -- bool，坐骑是否将要销毁
        - ``switchingRides`` -- bool，是否换乘坐骑
        - ``cancel`` -- bool，设置为True可以取消（需要与服务端事件一同取消）
        """
    def EntityModelChangedClientEvent(self, args):
        """
        [事件]

        实体模型切换时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``newModel`` -- str，新的模型名字
        - ``oldModel`` -- str，旧的模型名字
        """
    def ApproachEntityClientEvent(self, args):
        """
        [事件]

        玩家靠近生物时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``entityId`` -- str，靠近的生物的实体ID
        """
    def UnLoadClientAddonScriptsBefore(self, args):
        """
        [事件]

        客户端卸载mod之前触发。

        -----

        【事件参数】

        无
        """
    def RemovePlayerAOIClientEvent(self, args):
        """
        [事件]

        玩家离开当前玩家同一个区块时触发AOI事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def RemoveEntityClientEvent(self, args):
        """
        [事件]

        客户端侧实体被移除时触发。

        -----

        【注意】

        客户端接收服务端AOI事件时触发，原事件名 ``RemoveEntityPacketEvent`` 。

        -----

        【事件参数】

        - ``id`` -- str，移除的实体ID
        """
    def OnLocalPlayerStopLoading(self, args):
        """
        [事件]

        玩家进入存档，出生点地形加载完成时触发。该事件触发时可以进行切换维度的操作。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def OnCommandOutputClientEvent(self, args):
        """
        [事件]

        当command命令有成功消息输出时触发。

        -----

        【注意】

        部分命令在返回的时候没有命令名称，命令组件需要 ``showOutput`` 参数为 ``True`` 时才会有返回。

        -----

        【事件参数】

        - ``command`` -- str，命令名称
        - ``message`` -- str，命令返回的消息
        """
    def LoadClientAddonScriptsAfter(self, args):
        """
        [事件]

        客户端加载mod完成事件。

        -----

        【事件参数】

        无
        """
    def ChunkLoadedClientEvent(self, args):
        """
        [事件]

        客户端区块加载完成时触发。

        -----

        【事件参数】

        - ``dimension`` -- int，区块所在维度
        - ``chunkPosX`` -- int，区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
        - ``chunkPosZ`` -- int，区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]
        """
    def ChunkAcquireDiscardedClientEvent(self, args):
        """
        [事件]

        客户端区块即将被卸载时触发。

        -----

        【注意】

        区块卸载：游戏只会加载玩家周围的区块，玩家移动到别的区域时，原来所在区域的区块会被卸载，参考 `区块介绍 <https://minecraft.fandom.com/zh/wiki/%E5%8C%BA%E5%9D%97>`_。

        -----

        【事件参数】

        - ``dimension`` -- int，区块所在维度
        - ``chunkPosX`` -- int，区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
        - ``chunkPosZ`` -- int，区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]
        """
    def AddPlayerCreatedClientEvent(self, args):
        """
        [事件]

        玩家进入当前玩家所在的区块AOI后，玩家皮肤数据异步加载完成后触发的事件。

        -----

        【注意】

        由于玩家皮肤是异步加载的原因，该事件触发时机比 ``AddPlayerAOIClientEvent`` 晚，触发该事件后可以对该玩家调用相关玩家渲染接口。
        当前客户端每加载好一个玩家的皮肤，就会触发一次该事件，比如刚进入世界时，本地玩家加载好会触发一次，周围的所有玩家加载好后也会分别触发一次。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def AddPlayerAOIClientEvent(self, args):
        """
        [事件]

        玩家加入游戏或者其余玩家进入当前玩家所在的区块时触发的AOI事件，替换 ``AddPlayerEvent`` 。

        -----

        【注意】

        该事件触发只表明在服务端数据中接收到了新玩家，并不能代表此时玩家在客户端中可见，若想在玩家进入AOI后立马调用玩家渲染相关接口，建议使用 ``AddPlayerCreatedClientEvent`` 。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def AddEntityClientEvent(self, args):
        """
        [事件]

        客户端侧创建新实体时触发。创建玩家时不会触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        - ``posX`` -- float，位置x
        - ``posY`` -- float，位置y
        - ``posZ`` -- float，位置z
        - ``dimensionId`` -- int，实体维度
        - ``isBaby`` -- bool，是否为幼儿
        - ``engineTypeStr`` -- str，实体类型
        - ``itemName`` -- str，物品identifier（仅当物品实体时存在该字段）
        - ``auxValue`` -- int，物品附加值（仅当物品实体时存在该字段）
        """
    def OnScriptTickClient(self, args):
        """
        [事件] [tick]

        客户端tick事件，1秒30次。

        -----

        【事件参数】

        无
        """
    def UiInitFinished(self, args):
        """
        [事件]

        UI初始化框架完成，此时可以创建UI。

        -----

        【注意】

        切换维度后会重新初始化UI并触发该事件。

        -----

        【事件参数】

        无
        """


class ServerEvent:
    def ItemPullOutCustomContainerServerEvent(self, args):
        """
        [事件]

        漏出物品到漏斗时触发该事件。

        -----

        【事件参数】

        - ``itemDict`` -- dict，漏斗漏出物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，漏出物品的容器名称，目前仅支持netease_container
        - ``collectionIndex`` -- int，漏出物品的容器索引
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        - ``cancel`` -- bool，是否取消该操作，默认为False，事件中改为True时拒绝此次漏出物品的操作
        """
    def ItemPushInCustomContainerServerEvent(self, args):
        """
        [事件]

        漏斗漏入物品时触发该事件。

        -----

        【事件参数】

        - ``itemDict`` -- dict，漏斗漏入物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，目标容器名称，目前仅支持netease_container
        - ``collectionIndex`` -- int，目标容器索引
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        - ``cancel`` -- bool，是否取消该操作，默认为False，事件中改为True时拒绝此次漏入物品的操作
        """
    def PlayerPermissionChangeServerEvent(self, args):
        """
        [事件]

        玩家权限变更事件。

        具体权限说明：

        - ``build`` -- bool，放置方块
        - ``mine`` -- bool，采集方块
        - ``doorsandswitches`` -- bool，使用门和开关
        - ``opencontainers`` -- bool，打开容器
        - ``attackplayers`` -- bool，攻击玩家
        - ``attackmobs`` -- bool，攻击生物
        - ``op`` -- bool，操作员命令
        - ``teleport`` -- bool，使用传送

        -----

        【事件参数】

        - ``playerId`` -- str，玩家实体ID
        - ``oldPermission`` -- dict，变化前的权限字典
        - ``newPermission`` -- dict，变化后的权限字典
        - ``changeCause`` -- int，变化原因，详见Minecraft枚举值文档的 `PermissionChangeCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PermissionChangeCause.html>`_
        - ``cancel`` -- bool，为True时，取消本次权限变更
        """
    def PlayerTryRemoveCustomContainerItemServerEvent(self, args):
        """
        [事件]

        玩家尝试从自定义容器中移除物品时触发该事件。

        -----

        【注意】

        容器内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。

        -----

        【事件参数】

        - ``itemDict`` -- dict，尝试移除物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，目标容器名称，对应容器json中"custom_description"字段
        - ``collectionType`` -- str，目标容器类型，目前仅支持netease_container和netease_ui_container
        - ``collectionIndex`` -- int，目标容器索引
        - ``playerId`` -- str，玩家实体ID
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        """
    def PlayerTryAddCustomContainerItemServerEvent(self, args):
        """
        [事件]

        玩家尝试将物品添加到自定义容器时触发该事件。

        -----

        【注意】

        容器内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        PC存在shift键移动全部物品，放入同种物品时，可能会触发tryadd和tryput，请开发者注意适配。

        -----

        【事件参数】

        - ``itemDict`` -- dict，尝试添加物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，目标容器名称，对应容器json中"custom_description"字段
        - ``collectionType`` -- str，目标容器类型，目前仅支持netease_container和netease_ui_container
        - ``collectionIndex`` -- int，目标容器索引
        - ``playerId`` -- str，玩家实体ID
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        """
    def PlayerTryPutCustomContainerItemServerEvent(self, args):
        """
        [事件]

        玩家尝试将物品放入自定义容器时触发该事件。

        -----

        【注意】

        容器内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        PC存在shift键移动全部物品，放入同种物品时，可能会触发tryadd和tryput，请开发者注意适配。

        -----

        【事件参数】

        - ``itemDict`` -- dict，尝试放入物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``collectionName`` -- str，放入容器名称，对应容器json中"custom_description"字段
        - ``collectionType`` -- str，放入容器类型，目前仅支持netease_container和netease_ui_container
        - ``collectionIndex`` -- int，放入容器索引
        - ``playerId`` -- str，玩家实体ID
        - ``x`` -- int，容器方块x坐标
        - ``y`` -- int，容器方块y坐标
        - ``z`` -- int，容器方块z坐标
        - ``cancel`` -- bool，是否取消该操作，默认为False，事件中改为True时拒绝此次放入自定义容器的操作
        """
    def MountTamingEvent(self, args):
        """
        [事件]

        玩家通过骑乘驯服生物后触发该事件。

        -----

        【注意】

        该事件是检测 ``minecraft:tamemount`` 行为包组件，即玩家通过不断骑乘生物，使其冒出爱心时触发。

        -----

        【事件参数】

        - ``eid`` -- str，生物实体ID
        - ``pid`` -- str，玩家实体ID
        """
    def OnPlayerActionServerEvent(self, args):
        """
        [事件]

        玩家动作事件，当玩家开始/停止某些动作时触发该事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家实体ID
        - ``actionType`` -- int，动作事件枚举，详见Minecraft枚举值文档的 `PlayerActionType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PlayerActionType.html>`_
        """
    def CustomCommandTriggerServerEvent(self, args):
        """
        [事件]

        自定义命令触发事件。

        -----

        【注意】

        ``args`` 中的某个dict参数说明如下：

        - ``name`` -- str，参数名称，对应json中的name字段
        - ``type`` -- str，参数类型，对应json中的type字段
        - ``value`` -- 参数的值，若玩家没传，则采用json中填写的default的值，但会转为python变量格式。如null转为None，array转为tuple

        当 ``type`` 为 ``"pos"`` 、 ``"entity"`` 、 ``"item"`` 时， ``value`` 的格式如下：

        - ``pos`` -- tuple，一个含有三个float的坐标，如(-0.93, 81.25, -5.67)
        - ``entity`` -- dict，一个含有entityType的字典，如 {'entityType': 'minecraft:cow'}
        - ``item`` -- dict，一个含有itemName的字典，如 {'itemName': 'minecraft:apple'}

        ``origin`` 参数说明如下：

        - ``entityId`` -- str，触发指令的实体ID，若由命令方块触发，则不会含有此字段
        - ``dimension`` -- int，指令触发的维度ID，0-主世界; 1-下界; 2-末地; 或其他自定义维度
        - ``blockPos`` -- tuple，触发指令的实体或命令方块的整数坐标

        -----

        【事件参数】

        - ``command`` -- str，自定义命令名称，对应json中的name字段
        - ``args`` -- list[dict]，自定义命令参数，详情见上方
        - ``variant`` -- int，表示是哪条变体，范围[0, 9]，对应json中args键中的数字，未配置变体则为0
        - ``origin`` -- dict，触发源的信息，详情见上方
        - ``return_failed`` -- bool，设置自定义命令是否执行失败，默认为False，如果执行失败，返回信息以红色字体显示
        - ``return_msg_key`` -- str，设置返回给玩家或命令方块的信息，支持在语言文件（.lang）中定义，默认值为commands.custom.success（自定义命令执行成功）
        """
    def GlobalCommandServerEvent(self, args):
        """
        [事件]

        服务端全局命令事件。包括聊天输入指令、 ``SetCommand`` 接口、命令方块、命令方块矿车执行指令时触发、行为包动画执行指令。

        -----

        【事件参数】

        - ``entityId`` -- str，执行命令的实体ID，命令方块执行时没有该参数
        - ``command`` -- str，命令
        - ``blockPos`` -- tuple[int, int, int]，执行命令的实体或方块的方块坐标
        - ``dimension`` -- int，执行命令的实体或方块所在维度ID
        - ``cancel`` -- bool，设置为True可以取消命令执行
        """
    def PlayerPickupArrowServerEvent(self, args):
        """
        [事件]

        玩家即将捡起抛射物时触发，包括使用 ``netease:pick_up`` 的自定义抛射物。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家实体ID
        - ``arrowId`` -- str，抛射物实体ID
        - ``itemDict`` -- dict，触碰的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``cancel`` -- bool，设置为True时将取消本次拾取
        - ``pickupDelay`` -- int，取消拾取后重新设置该物品的拾取cd，小于15帧将视作15帧，大于等于97813帧将视作无法拾取，每秒30帧
        """
    def EntityDieLoottableAfterServerEvent(self, args):
        """
        [事件]

        生物死亡掉落物品之后触发。

        -----

        【注意】

        该事件为生物死亡掉落物品生成后触发，可以得到掉落物的id列表，如果需要更改掉落物，请使用 ``EntityDieLoottableServerEvent`` 。
        该事件在生物死亡后会触发，无论是否掉落物品，因此掉落物品列表可能存在为空的情况。
        掉落物不包含玩家或生物携带以及背包内的物品，若要获取死亡后由背包扔出的物品请参考 ``EntityDroppedItemServerEvent`` 事件。

        -----

        【事件参数】

        - ``dieEntityId`` -- str，死亡实体ID
        - ``attacker`` -- str，伤害来源实体ID
        - ``itemList`` -- list[dict]，掉落物品列表，每个元素为一个itemDict，格式可参考 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``itemEntityIdList`` -- list[str]，掉落物品的实体ID列表
        """
    def PlayerHungerChangeServerEvent(self, args):
        """
        [事件]

        玩家饥饿度变化时触发该事件。

        -----

        【注意】

        当通过 ``SetPlayerHunger`` 接口设置饥饿度时，不会触发服务端对应的事件。
        当通过 ``/hunger`` 等指令设置饥饿度设置时， ``hunger`` 字段值可能会超过最大饥饿度。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家实体ID
        - ``hungerBefore`` -- float，变化前的饥饿度
        - ``hunger`` -- float，变化后的饥饿度
        - ``cancel`` -- bool，是否取消饥饿度变化
        """
    def ItemDurabilityChangedServerEvent(self, args):
        """
        [事件]

        物品耐久度变化事件。

        -----

        【注意】

        目前只有存在耐久的物品，并且有物主的物品才会触发该事件，存在发射器中发射导致的物品耐久变化不会触发该事件。
        目前铁砧修复、经验修补魔咒、 ``SetItemDurability`` 接口触发的耐久度变化中 ``canChange`` 为 ``False`` ，并且不支持修改变化后耐久度。

        -----

        【事件参数】

        - ``entityId`` -- str，物品拥有者的实体ID
        - ``itemDict`` -- dict，物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``durabilityBefore`` -- int，变化前耐久度
        - ``durability`` -- int，变化后耐久度，支持修改。但是请注意修改范围，支持范围为[-32768,32767)
        - ``canChange`` -- bool，是否支持修改，为True时支持通过durability修改，为False时不支持
        """
    def PlaceNeteaseLargeFeatureServerEvent(self, args):
        """
        [事件]

        网易版大型结构即将生成时服务端抛出该事件。

        -----

        【事件参数】

        - ``dimensionId`` -- int，维度ID
        - ``pos`` -- tuple[int, int]，中心结构放置坐标(x, z)
        - ``rot`` -- int，中心结构顺时针旋转角度
        - ``depth`` -- int，大型结构递归深度
        - ``centerPool`` -- str，中心池的identifier
        - ``ignoreFitInContext`` -- bool，是否允许生成过结构的地方继续生成结构
        - ``cancel`` -- bool，设置为True时可阻止该大型结构的放置
        """
    def PlayerNamedEntityServerEvent(self, args):
        """
        [事件]

        玩家用命名牌重命名实体时触发，例如玩家手持命名牌对羊修改名字、玩家手持命名牌对盔甲架修改名字。

        -----

        【事件参数】

        - ``playerId`` -- str，主动命名生物的玩家的实体ID
        - ``entityId`` -- str，被命名生物的实体ID
        - ``preName`` -- str，实体当前的名字
        - ``afterName`` -- str，实体重命名后的名字
        - ``cancel`` -- bool，是否取消触发，默认为False，若设为True，可阻止触发后续的实体命名逻辑
        """
    def PlayerFeedEntityServerEvent(self, args):
        """
        [事件]

        玩家喂养生物时触发，例如玩家手持小麦喂养牛、玩家手持胡萝卜喂养幼年猪。

        -----

        【注意】

        对于幼年生物，用对应的物品喂养后就可以触发事件，例如用小麦喂养幼年牛、用生鲑鱼喂养幼年猫；对于成年生物，用对应的物品喂养后，该生物要进入“求爱模式”（持续散发红心粒子），才可以触发事件。
        特殊的成年生物列举如下：
        - 可骑乘生物，例如马，玩家要驯服马后，再给它喂养食物（例如金苹果、金萝卜），才可以触发事件；已驯服的马受伤后，用金苹果喂养时会治疗马，不触发事件，马的血量回满时，再喂养金苹果，才会触发事件；
        - 可驯服生物，例如狼，玩家要用骨头驯服狼后，再给它喂养肉类物品（例如熟猪排），才可以触发事件；
        - 需要在特定环境下才能繁殖的生物，例如熊猫，玩家用竹子喂养熊猫时，熊猫的5格内至少要有8根竹子，喂养后才可以触发事件。
        该事件中如需调用使用手持物相关的接口，如 ``PlayerUseItemToEntity`` 或其他设置物品数量的接口，会导致接口正常调用但是物品数量计算异常，建议通过timer延迟调用。

        -----

        【事件参数】

        - ``playerId`` -- str，主动喂养生物的玩家的实体ID
        - ``entityId`` -- str，被喂养生物的实体ID
        - ``itemDict`` -- dict，当前玩家手持物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``cancel`` -- bool，是否取消触发，默认为False，若设为True，可阻止触发后续的生物喂养逻辑
        """
    def lobbyGoodBuySucServerEvent(self, args):
        """
        [事件]

        玩家登录联机大厅服务器，或者联机大厅游戏内购买商品时触发。如果是玩家登录，触发时玩家客户端已经触发了 ``UiInitFinished`` 事件。

        -----

        【事件参数】

        - ``eid`` -- str，玩家的实体ID
        - ``buyItem`` -- bool，玩家登录时为False，玩家购买了商品时为True
        """
    def UrgeShipEvent(self, args):
        """
        [事件]

        玩家点击商城催促发货按钮时触发该事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def PlayerInventoryOpenScriptServerEvent(self, args):
        """
        [事件]

        某个客户端打开物品背包界面时触发。可以监听此事件判定客户端是否打开了创造背包。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``isCreative`` -- str，是否是创造模式背包界面
        """
    def WalkAnimEndServerEvent(self, args):
        """
        [事件]

        当走路动作结束时触发。

        -----

        【注意】

        使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def WalkAnimBeginServerEvent(self, args):
        """
        [事件]

        当走路动作开始时触发。

        -----

        【注意】

        使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def JumpAnimBeginServerEvent(self, args):
        """
        [事件]

        当跳跃动作开始时触发。

        -----

        【注意】

        使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def AttackAnimEndServerEvent(self, args):
        """
        [事件]

        当攻击动作结束时触发。

        -----

        【注意】

        使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def AttackAnimBeginServerEvent(self, args):
        """
        [事件]

        当攻击动作开始时触发。

        -----

        【注意】

        使用 ``SetModel`` 替换骨骼模型后，该事件才生效。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def UIContainerItemChangedServerEvent(self, args):
        """
        [事件]

        合成容器物品发生变化时触发。

        -----

        【注意】

        合成容器包括工作台、铁砧、附魔台、织布机、砂轮、切石机、制图台、锻造台，输入物品发生变化时会触发本事件。
        可通过容器槽位区分不同的生成容器类型。
        合成容器的生成槽位生成物品时不触发本事件，生成物品可通过 ``CraftItemOutputChangeServerEvent`` 监听。
        储物容器（箱子，潜影箱），熔炉，酿造台，发射器，投掷器，漏斗，炼药锅，唱片机，高炉，烟熏炉中物品发生变化不会触发此事件，此类容器可通过 ``ContainerItemChangedServerEvent`` 监听。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``slot`` -- int，容器槽位，含义见： `PlayerUISlot枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/PlayerUISlot.html?key=PlayerUISlot&docindex=1&type=0>`_
        - ``oldItemDict`` -- dict，旧 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``newItemDict`` -- dict，生成的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def ShearsUseToBlockBeforeServerEvent(self, args):
        """
        [事件] [tick]

        实体手持剪刀对方块使用时，有剪刀特殊效果的方块会在服务端线程触发该事件。

        -----

        【注意】

        目前会触发该事件的方块：南瓜、蜂巢。
        该事件触发在 ``ServerItemUseOnEvent`` 之后，如果 ``ServerItemUseOnEvent`` 中取消了物品使用，该事件无法被触发。
        和 ``ServerItemUseOnEvent`` 一样该事件判定在tick执行，意味着如果取消剪刀效果该事件可能会多次触发（取决于玩家按下使用键时长）。

        -----

        【事件参数】

        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- str，方块附加值
        - ``dropName`` -- str，触发剪刀效果的掉落物identifier，包含命名空间及名称
        - ``dropCount`` -- str，触发剪刀效果的掉落物数量
        - ``entityId`` -- str，触发剪刀效果的实体ID，目前仅玩家会触发
        - ``dimensionId`` -- int，维度ID
        - ``cancelShears`` -- int，是否取消剪刀效果
        """
    def ServerPlayerTryTouchEvent(self, args):
        """
        [事件]

        玩家即将捡起物品时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``entityId`` -- str，物品的实体ID
        - ``itemDict`` -- dict，`物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``cancel`` -- bool，设置为True时将取消本次拾取
        - ``pickupDelay`` -- int，取消拾取后重新设置该物品的拾取cd，小于15帧将视作15帧，大于等于97813帧将视作无法拾取
        """
    def ServerItemTryUseEvent(self, args):
        """
        [事件]

        玩家点击右键尝试使用物品时服务端抛出的事件。

        -----

        【注意】

        如果需要取消物品的使用需要同时在 ``ClientItemTryUseEvent`` 和 ``ServerItemTryUseEvent`` 中将 ``cancel`` 设置为 ``True`` 才能正确取消。
         ``ServerItemTryUseEvent`` / ``ClientItemTryUseEvent`` 不能取消对方块使用物品的行为，如使用生物蛋，使用桶倒出/收集，使用打火石点燃草等；如果想要取消这种行为，请使用 ``ClientItemUseOnEvent`` 和 ``ServerItemUseOnEvent`` 。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``cancel`` -- bool，设为True可取消物品的使用
        """
    def PlayerDropItemServerEvent(self, args):
        """
        [事件]

        玩家丢弃物品时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemEntityId`` -- str，物品的实体ID
        """
    def OnPlayerBlockedByShieldBeforeServerEvent(self, args):
        """
        [事件]

        玩家使用盾牌抵挡伤害之前触发。

        -----

        【注意】

        盾牌抵挡了所有伤害时，才会触发事件；部分抛射物造成的伤害无法全部抵挡，无法触发事件，例如带有穿透魔咒的弩。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``sourceId`` -- str，伤害来源实体ID，没有实体返回"-1"
        - ``itemDict`` -- dict，盾牌 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``damage`` -- float，抵挡的伤害数值
        """
    def OnPlayerBlockedByShieldAfterServerEvent(self, args):
        """
        [事件]

        玩家使用盾牌抵挡伤害之后触发.

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``sourceId`` -- str，伤害来源实体ID，没有实体返回"-1"
        - ``itemDict`` -- dict，盾牌 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``damage`` -- float，抵挡的伤害数值
        """
    def OnPlayerActiveShieldServerEvent(self, args):
        """
        [事件]

        玩家激活/取消激活盾牌触发的事件。包括玩家持盾进入潜行状态，以及在潜行状态切换盾牌（切换耐久度不同的相同盾牌不会触发）。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``isActive`` -- str，True:尝试激活，False:尝试取消激活
        - ``itemDict`` -- dict，盾牌 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``cancelable`` -- bool，是否可以取消。如果玩家在潜行状态切换盾牌，则无法取消
        - ``cancel`` -- bool，是否取消这次激活
        """
    def OnOffhandItemChangedServerEvent(self, args):
        """
        [事件]

        玩家切换副手物品时触发该事件。

        -----

        【注意】

        当原有的物品槽内容为空时， ``oldItemName`` 值为 ``"minecraft:air"`` ，且 ``oldItem`` 其余字段不存在。
        当切换原有物品，且新物品为空时，参数值同理。

        -----

        【事件参数】

        - ``oldArmorDict`` -- dict | None，旧物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当旧物品为空时，此项属性为None
        - ``newArmorDict`` -- dict | None，新物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当新物品为空时，此项属性为None
        - ``playerId`` -- str，玩家的实体ID
        """
    def OnNewArmorExchangeServerEvent(self, args):
        """
        [事件]

        玩家切换盔甲时触发该事件。

        -----

        【注意】

        当玩家登录时，每个盔甲槽位会触发两次该事件，第一次为 ``None`` 切换到身上的装备，第二次的 ``oldArmorDict`` 和 ``newArmorDict`` 都为身上装备。如果槽位为空，则是触发两次从 ``None`` 切换到 ``None`` 的事件。
        注意：避免在该事件回调中对玩家修改盔甲栏装备，如 `SetEntityItem <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%83%8C%E5%8C%85.html?key=SetEntityItem&docindex=1&type=0>`_ 接口，会导致事件循环触发造成堆栈溢出。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``slot`` -- int，槽位ID
        - ``oldArmorDict`` -- dict | None，旧装备的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当旧装备为空时，此项属性为None
        - ``newArmorDict`` -- dict | None，新装备的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当新装备为空时，此项属性为None
        """
    def OnItemPutInEnchantingModelServerEvent(self, args):
        """
        [事件]

        玩家将可附魔物品放到附魔台上时触发。

        -----

        【注意】

        ``options`` 为包含三个 ``dict`` 的 ``list`` ，单个 ``dict`` 的格式如下：
        ::

            {
              'cost': 1,
              'enchantData': [(1, 1)],
              'modEnchantData': [("custom_enchant", 1)],
            }

        其中 ``cost`` 为解锁该选项所需的玩家等级， ``enchantData`` 为该附魔选项包含的原版附魔数据， ``modEnchantData`` 为该选项包含的自定义附魔数据。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``slotType`` -- int，玩家放入物品的EnchantSlotType
        - ``options`` -- list[dict]，附魔台选项
        - ``change`` -- bool，传入True时，附魔台选项会被新传入的options覆盖
        """
    def ItemUseOnAfterServerEvent(self, args):
        """
        [事件]

        玩家在对方块使用物品之后服务端抛出的事件。

        -----

        【注意】

        在 ``ServerItemUseOnEvent`` 和原版物品使用事件（例如 ``StartUsingItemClientEvent`` ）之后触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``face`` -- int，点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``clickX`` -- float，点击点的x比例位置
        - ``clickY`` -- float，点击点的y比例位置
        - ``clickZ`` -- float，点击点的z比例位置
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``blockAuxValue`` -- int，方块的附加值
        - ``dimensionId`` -- int，维度ID
        """
    def ItemUseAfterServerEvent(self, args):
        """
        [事件]

        玩家在使用物品之后服务端抛出的事件。

        -----

        【注意】

        做出使用物品这个动作之后触发，一些需要蓄力的物品使用事件（ ``ActorUseItemServerEvent`` ）会在之后触发。如投掷三叉戟，先触发本事件，投出去之后再触发 ``ActorUseItemServerEvent`` 。

        -----

        【事件参数】

        - ``entityId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def ItemReleaseUsingServerEvent(self, args):
        """
        [事件]

        释放正在使用的物品时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``durationLeft`` -- float，蓄力剩余时间(当物品缺少"minecraft:maxduration"组件时,蓄力剩余时间为负数)
        - ``itemDict`` -- dict，使用的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``maxUseDuration`` -- int，最大蓄力时长
        - ``cancel`` -- bool，设置为True可以取消，需要同时取消客户端事件ItemReleaseUsingClientEvent
        - ``changeItem`` -- bool，如果要在该事件的回调中修改当前使用槽位的物品，需设置这个参数为True，否则将修改物品失败，例如修改耐久度或者替换成新物品
        """
    def InventoryItemChangedServerEvent(self, args):
        """
        [事件]

        玩家背包物品变化时服务端抛出的事件。

        -----

        【注意】

        如果槽位变空，变化后槽位中物品为空气。
        触发时槽位物品仍为变化前物品。
        玩家进入游戏时，身上的物品会触发该事件。
        背包内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``slot`` -- int，背包槽位
        - ``oldItemDict`` -- dict | None，变化前的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``newItemDict`` -- dict | None，变化后的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def FurnaceBurnFinishedServerEvent(self, args):
        """
        [事件]

        服务端熔炉烧制触发事件。熔炉、高炉、烟熏炉烧出物品时触发。

        -----

        【事件参数】

        - ``dimensionId`` -- int，维度ID
        - ``posX`` -- float，位置x
        - ``posY`` -- float，位置y
        - ``posZ`` -- float，位置z
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def CraftItemOutputChangeServerEvent(self, args):
        """
        [事件]

        玩家从容器拿出生成物品时触发。
        支持工作台，铁砧，砂轮等工作方块。

        -----

        【注意】

        当 ``screenContainerType`` 为 ``ContainerType.INVENTORY`` 时，表示从创造模式物品栏中拿出物品，或者从合成栏中拿出合成物品。
        通过 ``cancel`` 参数取消生成物品，可用于禁止外挂刷物品。
        ``cancel=True`` 时无法从创造模式物品栏拿物品。
        ``cancel=True`` 时铁砧无法修复或重命名物品，但仍会扣除经验值。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict，`物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``screenContainerType`` -- int，当前界面类型，类型含义见： `ContainerType枚举枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ContainerType.html?key=ContainerType&docindex=1&type=0>`_
        - ``cancel`` -- bool，是否取消生成物品
        """
    def ContainerItemChangedServerEvent(self, args):
        """
        [事件]

        容器物品变化事件。
        储物容器（箱子，潜影箱），熔炉，酿造台，发射器，投掷器，漏斗，炼药锅，唱片机，高炉，烟熏炉中物品发生变化会触发此事件。

        -----

        【注意】

        工作台、铁砧、附魔台、织布机、砂轮、切石机、制图台、锻造台为合成容器，不会触发此事件，此类容器可通过 ``UIContainerItemChangedServerEvent`` 监听具体生成容器物品变化。
        炼药锅只在使用染料时触发本事件，且 ``slot`` 为2。
        唱片机只在从漏斗放入唱片触发此事件。

        -----

        【事件参数】

        - ``pos`` -- tuple[int, int, int]，容器坐标
        - ``containerType`` -- int，容器类型，类型含义见： `ContainerType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ContainerType.html?key=ContainerType&docindex=1&type=0>`_
        - ``slot`` -- int，容器槽位
        - ``dimensionId`` -- int，维度ID
        - ``oldItemDict`` -- dict | None，旧 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``newItemDict`` -- dict | None，新 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        """
    def StepOnBlockServerEvent(self, args):
        """
        [事件]

        实体刚移动至一个新实心方块时触发。

        -----

        【注意】

        在合并微软更新之后，本事件触发时机与微软molang实验性玩法组件 ``"minecraft:on_step_on"`` 一致。
        压力板与绊线钩在过去的版本的事件是可以触发的，但在更新后这种非实心方块并不会触发，有需要的可以使用 ``OnEntityInsideBlockServerEvent`` 事件。
        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStepOn`` 接口注册才能触发。原版的红石矿默认注册了，但深层红石矿没有默认注册。
        如果需要修改 ``cancel`` ，强烈建议配合客户端事件同步修改，避免出现客户端表现不一致等非预期现象。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``entityId`` -- str，实体ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID
        """
    def StepOffBlockServerEvent(self, args):
        """
        [事件]

        实体移动离开一个实心方块时触发。

        -----

        【注意】

        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStepOff`` 接口注册才能触发。
        压力板与绊线钩这种非实心方块不会触发。

        -----

        【事件参数】

        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``entityId`` -- str，实体ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID

        -----

        【相关接口】

        - `RegisterOnStepOff <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=RegisterOnStepOff&docindex=2&type=0>`_
        - `UnRegisterOnStepOff <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=UnRegisterOnStepOff&docindex=2&type=0>`_
        """
    def StartDestroyBlockServerEvent(self, args):
        """
        [事件]

        玩家开始挖方块时触发。创造模式下不触发。

        -----

        【注意】

        如果是隔着火焰挖方块，即使将该事件 ``cancel`` 掉，火焰也会被扑灭。如果要阻止火焰扑灭，需要配合 ``ExtinguishFireServerEvent`` 使用。
        该服务端事件触发于服务端收到玩家破坏操作时，当方块为秒破方块时（破坏方块所需时间为0或未设置破坏时间）， ``ServerPlayerTryDestroyBlockEvent`` 事件触发在本事件之前；当方块为非秒破方块时， ``ServerPlayerTryDestroyBlockEvent`` 事件触发在本事件之后。
        秒破方块在本事件触发前已经被服务端删除，此时本事件获取到的 ``blockName`` 为 ``"minecraft:air"`` ，且无法通过本事件进行取消操作，以下是两个解决方法：

        | 1、用 ``ServerPlayerTryDestroyBlockEvent`` 获取到正确的方块信息或取消操作。
        | 2、通过 `minecraft:destroy_time <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html#minecraft_destroy_time>`_ 方块组件来修改方块的破坏时间。

        -----

        【事件参数】

        - ``pos`` -- tuple[float, float, float]，方块坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxValue`` -- int，方块的附加值
        - ``playerId`` -- str，玩家的实体ID
        - ``dimensionId`` -- int，维度ID
        - ``cancel`` -- bool，修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockClientEvent一起修改
        - ``face`` -- int，方块被敲击面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html>`_
        """
    def ShearsDestoryBlockBeforeServerEvent(self, args):
        """
        [事件]

        玩家手持剪刀破坏方块时，有剪刀特殊效果的方块会在服务端线程触发该事件。

        -----

        【注意】

        该事件触发在 ``ServerPlayerTryDestroyBlockEvent`` 之后，如果在 ``ServerPlayerTryDestroyBlockEvent`` 事件中设置了取消Destroy或取消掉落物会导致该事件不触发。
        取消剪刀效果后不掉落任何东西的方块类型：蜘蛛网、枯萎的灌木、草丛、下界苗、树叶、海草、藤蔓。
        绊线取消剪刀效果需要配合 ``ShearsDestoryBlockBeforeClientEvent`` 同时使用，否则在表现上可能展现出来的还是剪刀剪断后的效果。绊线取消剪刀效果后依然会掉落成线。

        -----

        【事件参数】

        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- int，方块附加值
        - ``dropName`` -- str，触发剪刀效果的掉落物identifier，包含命名空间及名称
        - ``dropCount`` -- int，触发剪刀效果的掉落物数量
        - ``playerId`` -- str，玩家的实体ID
        - ``dimensionId`` -- int，维度ID
        - ``cancelShears`` -- bool，是否取消剪刀效果
        """
    def ServerPlayerTryDestroyBlockEvent(self, args):
        """
        [事件]

        当玩家即将破坏方块时，服务端线程触发该事件。

        -----

        【注意】

        若需要禁止某些特殊方块的破坏，需要配合 ``PlayerTryDestroyBlockClientEvent`` 一起使用，例如床，旗帜，箱子这些根据方块实体数据进行渲染的方块。

        -----

        【事件参数】

        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``face`` -- int，方块被敲击的面向id，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``fullName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- int，方块附加值
        - ``playerId`` -- str，试图破坏方块的玩家的实体ID
        - ``dimensionId`` -- int，维度ID
        - ``cancel`` -- bool，默认为False，在脚本层设置为True就能取消该方块的破坏
        - ``spawnResources`` -- bool，是否生成掉落物，默认为True，在脚本层设置为False就能取消生成掉落物
        """
    def ServerPlaceBlockEntityEvent(self, args):
        """
        [事件]

        手动放置或通过接口创建含自定义方块实体的方块时触发，此时可向该方块实体中存放数据。

        -----

        【事件参数】

        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimension`` -- int，维度ID
        - ``posX`` -- int，方块x坐标
        - ``posY`` -- int，方块y坐标
        - ``posZ`` -- int，方块z坐标
        """
    def ServerEntityTryPlaceBlockEvent(self, args):
        """
        [事件]

        当生物试图放置方块时触发该事件。

        -----

        【注意】

        部分放置后会产生实体的方块、可操作的方块、带有特殊逻辑的方块，不会触发该事件，包括但不限于床、门、告示牌、花盆、红石中继器、船、炼药锅、头部模型、蛋糕、酿造台、盔甲架等。
        修改放置方块信息只对一般方块有效，对一些特殊方块无效，会导致放置取消，特殊方块包括：钟、蜡烛、管珊瑚扇、台阶、青蛙卵、脚手架、海泡菜、顶层雪、睡莲。

        -----

        【事件参数】

        - ``x`` -- int，方块x坐标，支持修改
        - ``y`` -- int，方块y坐标，支持修改
        - ``z`` -- int，方块z坐标，支持修改
        - ``fullName`` -- str，方块的identifier，包含命名空间及名称，支持修改
        - ``auxData`` -- int，方块附加值，支持修改
        - ``entityId`` -- str，试图放置方块的生物的实体ID
        - ``dimensionId`` -- int，维度ID
        - ``face`` -- int，点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``cancel`` -- bool，默认为False，在脚本层设置为True就能取消该方块的放置
        - ``clickX`` -- float，点击点的x比例位置
        - ``clickY`` -- float，点击点的y比例位置
        - ``clickZ`` -- float，点击点的z比例位置
        """
    def ServerBlockEntityTickEvent(self, args):
        """
        [事件] [tick]

        自定义方块配置了 ``"netease:block_entity"`` 组件并设 ``tick`` 为 ``true`` ，方块在玩家的模拟距离（新建存档时可以设置，默认为4个区块）内，或者在tickingarea内的时候触发。

        -----

        【注意】

        方块实体的tick事件频率为每秒钟20次。
        触发本事件时，若正在退出游戏，将无法获取到抛出本事件的方块实体数据（ ``GetBlockEntityData`` 函数返回 ``None`` ），也无法对其进行操作。

        -----

        【事件参数】

        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimension`` -- int，维度ID
        - ``posX`` -- int，方块x坐标
        - ``posY`` -- int，方块y坐标
        - ``posZ`` -- int，方块z坐标
        """
    def PistonActionServerEvent(self, args):
        """
        [事件]

        活塞或者粘性活塞推送/缩回影响附近方块时触发。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否允许触发，默认为False，若设为True，可阻止触发后续的事件
        - ``action`` -- str，推送时=expanding；缩回时=retracting
        - ``pistonFacing`` -- int，活塞的朝向，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``pistonMoveFacing`` -- int，活塞的运动方向，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``dimensionId`` -- int，维度ID
        - ``pistonX`` -- int，活塞方块的x坐标
        - ``pistonY`` -- int，活塞方块的y坐标
        - ``pistonZ`` -- int，活塞方块的z坐标
        - ``blockList`` -- list[tuple[int, int, int]]，活塞运动影响到产生被移动效果的方块坐标(x,y,z)，均为int类型
        - ``breakBlockList`` -- list[tuple[int, int, int]]，活塞运动影响到产生被破坏效果的方块坐标(x,y,z)，均为int类型
        - ``entityList`` -- list[str]，活塞运动影响到产生被移动或被破坏效果的实体ID列表
        """
    def OnStandOnBlockServerEvent(self, args):
        """
        [事件] [tick]

        当实体站立到方块上时服务端持续触发。

        -----

        【注意】

        不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnStandOn`` 接口注册才能触发。
        如果需要修改 ``motion`` / ``cancel`` ，强烈建议配合客户端事件同步修改，避免出现客户端表现不一致等现象。
        如果要在脚本层修改 ``motion`` ，回传的一定要是浮点型，例如需要赋值0.0而不是0。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``dimensionId`` -- int，维度ID
        - ``posX`` -- float，实体位置x
        - ``posY`` -- float，实体位置y
        - ``posZ`` -- float，实体位置z
        - ``motionX`` -- float，瞬时移动x方向的力
        - ``motionY`` -- float，瞬时移动y方向的力
        - ``motionZ`` -- float，瞬时移动z方向的力
        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``cancel`` -- bool，可由脚本层回传True给引擎，阻止触发后续原版逻辑
        """
    def OnBeforeFallOnBlockServerEvent(self, args):
        """
        [事件]

        当实体刚降落到方块上时服务端触发，主要用于伤害计算。

        -----

        【注意】

        不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ）。
        如果要在脚本层修改 ``fallDistance`` ，回传的一定要是浮点型，例如需要赋值0.0而不是0。
        可能会因为轻微的反弹触发多次，可在脚本层针对 ``fallDistance`` 的值进行判断。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``fallDistance`` -- float，实体下降距离，可在脚本层传给引擎
        - ``cancel`` -- bool，是否取消引擎对实体下降伤害的计算
        """
    def OnAfterFallOnBlockServerEvent(self, args):
        """
        [事件] [tick]

        当实体降落到方块后服务端触发，主要用于力的计算。

        -----

        【注意】

        不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ）。
        如果要在脚本层修改 ``motion`` ，回传的需要是浮点型，例如需要赋值0.0而不是0。
        如果需要修改实体的力，最好配合客户端事件同步修改，避免产生非预期现象。
        因为引擎最后一定会按照原版方块规则计算力（普通方块置0，床、粘液块等反弹），所以脚本层如果想直接修改当前力需要将 ``calculate`` 设为 ``True`` 取消原版计算，按照传回值计算。
        引擎在落地之后， ``OnAfterFallOnBlockServerEvent`` 会一直触发，因此请在脚本层中做对应的逻辑判断。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``posX`` -- float，实体位置x
        - ``posY`` -- float，实体位置y
        - ``posZ`` -- float，实体位置z
        - ``motionX`` -- float，瞬时移动x方向的力
        - ``motionY`` -- float，瞬时移动y方向的力
        - ``motionZ`` -- float，瞬时移动z方向的力
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``calculate`` -- bool，是否按脚本层传值计算力
        """
    def HopperTryPullOutServerEvent(self, args):
        """
        [事件]

        当漏斗以毗邻的方式连接容器时，即从旁边连接容器时，漏斗向容器开始输出物品时触发，事件仅触发一次。

        -----

        【事件参数】

        - ``x`` -- int，漏斗x坐标
        - ``y`` -- int，漏斗y坐标
        - ``z`` -- int，漏斗z坐标
        - ``attachedPosX`` -- int，交互的容器的x坐标
        - ``attachedPosY`` -- int，交互的容器的y坐标
        - ``attachedPosZ`` -- int，交互的容器的z坐标
        - ``dimensionId`` -- int，维度ID
        - ``canHopper`` -- bool，是否允许容器往漏斗加东西(要关闭此交互，需先监听此事件再放置容器)
        """
    def HopperTryPullInServerEvent(self, args):
        """
        [事件]

        当漏斗上方连接容器后，容器往漏斗开始输入物品时触发，事件仅触发一次。

        -----

        【事件参数】

        - ``x`` -- int，漏斗x坐标
        - ``y`` -- int，漏斗y坐标
        - ``z`` -- int，漏斗z坐标
        - ``abovePosX`` -- int，交互的容器位置x
        - ``abovePosY`` -- int，交互的容器位置y
        - ``abovePosZ`` -- int，交互的容器位置z
        - ``dimensionId`` -- int，维度ID
        - ``canHopper`` -- bool，是否允许容器往漏斗加东西(要关闭此交互，需先监听此事件再放置容器)
        """
    def HeavyBlockStartFallingServerEvent(self, args):
        """
        [事件]

        当重力方块变为下落的方块实体后，服务端触发该事件。

        -----

        【注意】

        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义重力方块 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/3-%E7%89%B9%E6%AE%8A%E6%96%B9%E5%9D%97/6-%E8%87%AA%E5%AE%9A%E4%B9%89%E9%87%8D%E5%8A%9B%E6%96%B9%E5%9D%97.html>`_ ）。

        -----

        【事件参数】

        - ``fallingBlockId`` -- str，下落的方块实体ID
        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID
        """
    def GrassBlockToDirtBlockServerEvent(self, args):
        """
        [事件]

        草方块变成泥土方块时触发。

        -----

        【注意】

        指令或者接口的设置不会触发该事件。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        """
    def FarmBlockToDirtBlockServerEvent(self, args):
        """
        [事件]

        耕地退化为泥土时触发。

        -----

        【注意】

        指令或者接口的设置不会触发该事件。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``setBlockType`` -- int，耕地退化为泥土的原因，参考 `SetBlockType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/SetBlockType.html?key=SetBlockType&docindex=1&type=0>`_
        """
    def FallingBlockReturnHeavyBlockServerEvent(self, args):
        """
        [事件]

        当下落的方块实体变回普通重力方块时，服务端触发该事件。

        -----

        【注意】

        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义重力方块 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/3-%E7%89%B9%E6%AE%8A%E6%96%B9%E5%9D%97/6-%E8%87%AA%E5%AE%9A%E4%B9%89%E9%87%8D%E5%8A%9B%E6%96%B9%E5%9D%97.html>`_ ）。

        -----

        【事件参数】

        - ``fallingBlockId`` -- str，下落的方块实体ID
        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``heavyBlockName`` -- int，重力方块的identifier，包含命名空间及名称
        - ``prevHereBlockName`` -- int，变回重力方块时，原本方块位置的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID
        - ``fallTickAmount`` -- int，下落的方块实体持续下落了多少tick
        """
    def FallingBlockCauseDamageBeforeServerEvent(self, args):
        """
        [事件]

        当下落的方块开始计算砸到实体的伤害时，服务端触发该事件。

        -----

        【注意】

        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义重力方块 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/3-%E7%89%B9%E6%AE%8A%E6%96%B9%E5%9D%97/6-%E8%87%AA%E5%AE%9A%E4%B9%89%E9%87%8D%E5%8A%9B%E6%96%B9%E5%9D%97.html>`_ ）。
        服务端通常触发在客户端之后，而且有时会相差一个tick，这就意味着可能发生以下现象：服务端 ``fallTickAmount`` 比配置强制破坏时间多1tick，下落的距离、下落的伤害计算出来比客户端时间多1tick的误差。

        -----

        【事件参数】

        - ``fallingBlockId`` -- str，下落的方块实体ID
        - ``fallingBlockX`` -- float，下落的方块实体位置x
        - ``fallingBlockY`` -- float，下落的方块实体位置y
        - ``fallingBlockZ`` -- float，下落的方块实体位置z
        - ``blockName`` -- str，重力方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID
        - ``collidingEntitys`` -- list[str] | None，当前碰撞到的实体ID的列表，如果没有的话是None
        - ``fallTickAmount`` -- int，下落的方块实体持续下落了多少tick
        - ``fallDistance`` -- float，下落的方块实体持续下落了多少距离
        - ``isHarmful`` -- bool，是否计算对实体的伤害，引擎传来的值由json配置和伤害是否大于0决定，可在脚本层修改传回引擎
        - ``fallDamage`` -- int，对实体的伤害，引擎传来的值距离和json配置决定，可在脚本层修改传回引擎
        """
    def FallingBlockBreakServerEvent(self, args):
        """
        [事件]

        当下落的方块实体被破坏时，服务端触发该事件。

        -----

        【注意】

        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义重力方块 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/3-%E7%89%B9%E6%AE%8A%E6%96%B9%E5%9D%97/6-%E8%87%AA%E5%AE%9A%E4%B9%89%E9%87%8D%E5%8A%9B%E6%96%B9%E5%9D%97.html>`_ ）。

        -----

        【事件参数】

        - ``fallingBlockId`` -- str，下落的方块实体ID
        - ``fallingBlockX`` -- float，下落的方块实体位置x
        - ``fallingBlockY`` -- float，下落的方块实体位置y
        - ``fallingBlockZ`` -- float，下落的方块实体位置z
        - ``blockName`` -- str，重力方块的identifier，包含命名空间及名称
        - ``fallTickAmount`` -- int，下落的方块实体持续下落了多少tick
        - ``dimensionId`` -- int，维度ID
        - ``cancelDrop`` -- bool，是否取消方块物品掉落，可以在脚本层中设置
        """
    def EntityPlaceBlockAfterServerEvent(self, args):
        """
        [事件]

        当生物成功放置方块后触发。

        -----

        【注意】

        部分放置后会产生实体的方块、可操作的方块、带有特殊逻辑的方块，不会触发该事件，包括但不限于床、门、告示牌、花盆、红石中继器、船、炼药锅、头部模型、蛋糕、酿造台、盔甲架等。

        -----

        【事件参数】

        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``fullName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- int，方块附加值
        - ``entityId`` -- str，实体ID
        - ``dimensionId`` -- int，维度ID
        - ``face`` -- int，点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        """
    def DirtBlockToGrassBlockServerEvent(self, args):
        """
        [事件]

        泥土方块变成草方块时触发。

        -----

        【注意】

        指令或者接口的设置不会触发该事件。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        """
    def CommandBlockUpdateEvent(self, args):
        """
        [事件]

        玩家尝试修改命令方块的内置命令时。

        -----

        【注意】

        当修改的目标为命令方块矿车时（此时 ``isBlock`` 为 ``False`` ），设置 ``cancel`` 为 ``True`` ，依旧可以阻止修改命令方块矿车的内部指令，但是从客户端能够看到命令方块矿车的内部指令变化了，不过这仅仅是假象，重新登录或者其他客户端打开命令方块矿车的设置界面，就会发现其实内部指令没有变化。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``playerUid`` -- long，玩家的uid
        - ``command`` -- str，企图修改的命令方块中的命令内容字符串
        - ``isBlock`` -- bool，是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义
        - ``blockX`` -- int，命令方块位置x，当isBlock为True时有效
        - ``blockY`` -- int，命令方块位置y，当isBlock为True时有效
        - ``blockZ`` -- int，命令方块位置z，当isBlock为True时有效
        - ``victimId`` -- str，命令方块对应的逻辑实体的实体ID，当isBlock为False时有效
        - ``cancel`` -- bool，修改为True时，可以阻止玩家修改命令方块的内置命令
        """
    def CommandBlockContainerOpenEvent(self, args):
        """
        [事件]

        玩家点击命令方块，尝试打开命令方块的设置界面。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``isBlock`` -- bool，是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义
        - ``blockX`` -- int，命令方块位置x，当isBlock为True时有效
        - ``blockY`` -- int，命令方块位置y，当isBlock为True时有效
        - ``blockZ`` -- int，命令方块位置z，当isBlock为True时有效
        - ``victimId`` -- str，命令方块对应的逻辑实体的实体ID，当isBlock为False时有效
        - ``cancel`` -- bool，修改为True时，可以阻止玩家打开命令方块的设置界面
        """
    def ChestBlockTryPairWithServerEvent(self, args):
        """
        [事件]

        两个并排的小箱子方块准备组合为一个大箱子方块时触发。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否允许触发，默认为False，若设为True，可阻止小箱子组合成为一个大箱子
        - ``blockX`` -- int，小箱子方块x坐标
        - ``blockY`` -- int，小箱子方块y坐标
        - ``blockZ`` -- int，小箱子方块z坐标
        - ``otherBlockX`` -- int，将要与之组合的另外一个小箱子方块x坐标
        - ``otherBlockY`` -- int，将要与之组合的另外一个小箱子方块y坐标
        - ``otherBlockZ`` -- int，将要与之组合的另外一个小箱子方块z坐标
        - ``dimensionId`` -- int，维度ID
        """
    def BlockStrengthChangedServerEvent(self, args):
        """
        [事件]

        自定义机械元件方块红石信号量发生变化时触发。

        -----

        【事件参数】

        - ``posX`` -- int，方块x坐标
        - ``posY`` -- int，方块y坐标
        - ``posZ`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxValue`` -- int，方块的附加值
        - ``newStrength`` -- int，变化后的红石信号量
        - ``oldStrength`` -- int，变化前的红石信号量
        - ``dimensionId`` -- int，维度ID
        """
    def BlockSnowStateChangeServerEvent(self, args):
        """
        [事件]

        方块转为含雪或者脱离含雪前触发。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``turnSnow`` -- bool，是否转为含雪，true则转为含雪，false则脱离含雪
        - ``setBlockType`` -- int，方块进入脱离含雪的原因，参考 `SetBlockType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/SetBlockType.html?key=SetBlockType&docindex=1&type=0>`_
        """
    def BlockSnowStateChangeAfterServerEvent(self, args):
        """
        [事件]

        方块转为含雪或者脱离含雪后触发。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``turnSnow`` -- bool，是否转为含雪，true则转为含雪，false则脱离含雪
        - ``setBlockType`` -- int，方块进入脱离含雪的原因，参考 `SetBlockType枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/SetBlockType.html?key=SetBlockType&docindex=1&type=0>`_
        """
    def BlockRemoveServerEvent(self, args):
        """
        [事件]

        监听该事件的方块在销毁时触发，可以通过 `ListenOnBlockRemoveEvent <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=ListenOnBlockRemoveEvent&docindex=3&type=0>`_ 方法进行监听，或者通过json组件 `netease:listen_block_remove <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html#netease-listen-block-remove>`_ 进行配置。

        -----

        【事件参数】

        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``fullName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxValue`` -- int，方块的附加值
        - ``dimension`` -- int，维度ID

        -----

        【相关接口】

        - `ListenOnBlockRemoveEvent <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=ListenOnBlockRemoveEvent&docindex=3&type=0>`_
        """
    def BlockRandomTickServerEvent(self, args):
        """
        [事件]

        自定义方块配置 ``"netease:random_tick"`` 随机tick时触发。

        -----

        【事件参数】

        - ``dimensionId`` -- int，维度ID
        - ``posX`` -- int，方块x坐标
        - ``posY`` -- int，方块y坐标
        - ``posZ`` -- int，方块z坐标
        - ``blockName`` -- str，方块名称
        - ``fullName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxValue`` -- int，方块的附加值
        """
    def BlockNeighborChangedServerEvent(self, args):
        """
        [事件]

        自定义方块周围的方块发生变化时，需要配置 ``"netease:neighborchanged_sendto_script"`` 。

        -----

        【事件参数】

        - ``dimensionId`` -- int，维度ID
        - ``posX`` -- int，方块x坐标
        - ``posY`` -- int，方块y坐标
        - ``posZ`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``neighborPosX`` -- int，变化方块x坐标
        - ``neighborPosY`` -- int，变化方块y坐标
        - ``neighborPosZ`` -- int，变化方块z坐标
        - ``fromBlockName`` -- str，方块变化前的identifier，包含命名空间及名称
        - ``fromBlockAuxValue`` -- int，方块变化前附加值
        - ``toBlockName`` -- str，方块变化后的identifier，包含命名空间及名称
        - ``toAuxValue`` -- int，方块变化后附加值
        """
    def BlockLiquidStateChangeServerEvent(self, args):
        """
        [事件]

        方块转为含水或者脱离含水(流体)前触发。

        -----

        【事件参数】

        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxValue`` -- int，方块的附加值
        - ``dimension`` -- int，维度ID
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``turnLiquid`` -- bool，是否转为含水，True则转为含水，False则脱离含水
        """
    def BlockLiquidStateChangeAfterServerEvent(self, args):
        """
        [事件]

        方块转为含水或者脱离含水(流体)后触发。

        -----

        【事件参数】

        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxValue`` -- int，方块的附加值
        - ``dimension`` -- int，维度ID
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``turnLiquid`` -- bool，是否转为含水，True则转为含水，False则脱离含水
        """
    def BlockDestroyByLiquidServerEvent(self, args):
        """
        [事件]

        方块被水流破坏的事件。

        -----

        【注意】

        指令或者接口的设置不会触发该事件。

        -----

        【事件参数】

        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``liquidName`` -- str，流体方块identifier
        - ``blockName`` -- str，方块的identifier
        - ``auxValue`` -- int，方块的附加值
        - ``dimensionId`` -- int，方块所在维度ID
        """
    def StoreBuySuccServerEvent(self, args):
        """
        [事件]

        玩家游戏内购买商品时服务端抛出的事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def ServerPlayerGetExperienceOrbEvent(self, args):
        """
        [事件]

        玩家获取经验球时触发的事件。

        -----

        【注意】

        ``cancel`` 值设为 ``True`` 时，捡起的经验球不会增加经验值，但是经验球一样会消失。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``experienceValue`` -- int，经验球经验值
        - ``cancel`` -- bool，是否取消
        """
    def PlayerTrySleepServerEvent(self, args):
        """
        [事件]

        玩家尝试使用床睡觉时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``cancel`` -- bool，是否取消
        """
    def PlayerTeleportEvent(self, args):
        """
        [事件]

        当玩家传送时触发该事件，如：玩家使用末影珍珠或tp指令时。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        """
    def PlayerStopSleepServerEvent(self, args):
        """
        [事件]

        玩家停止睡觉时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def PlayerSleepServerEvent(self, args):
        """
        [事件]

        玩家使用床睡觉成功时触发。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def PlayerRespawnFinishServerEvent(self, args):
        """
        [事件]

        玩家复活完毕时触发。

        -----

        【注意】

        该事件触发时玩家已重生完毕，可以安全使用切维度等操作。
        通过末地传送门回到主世界时也算重生，同样也会触发该事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def PlayerRespawnEvent(self, args):
        """
        [事件]

        玩家复活时触发该事件。

        -----

        【注意】

        该事件为玩家点击重生按钮时触发，但是触发时玩家可能尚未完成复活，此时请勿对玩家进行切维度或设置生命值等操作，一般情况下推荐使用 ``PlayerRespawnFinishServerEvent`` 。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        """
    def PlayerHurtEvent(self, args):
        """
        [事件]

        当玩家受伤害前触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``attacker`` -- str，伤害来源实体ID，若没有实体攻击，例如高空坠落，该值为"-1"
        - ``cause`` -- str，伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
        - ``customTag`` -- str，使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
        """
    def PlayerEatFoodServerEvent(self, args):
        """
        [事件]

        玩家吃下食物时触发。

        -----

        【注意】

        由于牛奶本身并没有饱食度的概念，因此，当喝牛奶触发该事件时，饥饿度、营养价值字段无效并始终为0。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict，食物的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``hunger`` -- int，食物增加的饥饿值，可修改
        - ``nutrition`` -- float，食物的营养价值，回复饱和度 = 食物增加的饥饿值 * 食物的营养价值 * 2，饱和度最大不超过当前饥饿值，可修改
        """
    def PlayerDieEvent(self, args):
        """
        [事件]

        当玩家死亡时触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``attacker`` -- str，伤害来源的实体ID
        - ``cause`` -- str，伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
        - ``customTag`` -- str，使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
        """
    def OnPlayerHitBlockServerEvent(self, args):
        """
        [事件]

        通过 ``OpenPlayerHitBlockDetection`` 打开方块碰撞检测后，当玩家碰撞到方块时触发该事件。

        -----

        【注意】

        监听玩家着地请使用客户端的 ``OnGroundClientEvent`` 。
        客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``posX`` -- int，碰撞方块x坐标
        - ``posY`` -- int，碰撞方块y坐标
        - ``posY`` -- int，碰撞方块z坐标
        - ``blockId`` -- float，碰撞方块的identifier
        - ``auxValue`` -- int，碰撞方块的附加值
        - ``dimensionId`` -- int，维度ID

        -----

        【相关接口】

        - `OpenPlayerHitBlockDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E7%8E%A9%E5%AE%B6.html?key=OpenPlayerHitBlockDetection&docindex=4&type=0>`_
        - `ClosePlayerHitBlockDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E7%8E%A9%E5%AE%B6.html?key=ClosePlayerHitBlockDetection&docindex=1&type=0>`_
        """
    def GameTypeChangedServerEvent(self, args):
        """
        [事件]

        个人游戏模式发生变化时服务端触发。

        游戏模式：生存、创造、冒险分别为0、1、2。

        -----

        【注意】

        默认游戏模式发生变化时最后反映在个人游戏模式之上。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID， `SetDefaultGameType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E4%B8%96%E7%95%8C/%E6%B8%B8%E6%88%8F%E8%A7%84%E5%88%99.html?key=SetDefaultGameType&docindex=2&type=0>`_ 接口改变游戏模式时该参数为空字符串
        - ``oldGameType`` -- int，切换前的游戏模式
        - ``newGameType`` -- int，切换后的游戏模式
        """
    def ExtinguishFireServerEvent(self, args):
        """
        [事件]

        玩家扑灭火焰时触发。

        -----

        【注意】

        下雨，倒水等方式熄灭火焰不会触发。

        -----

        【事件参数】

        - ``pos`` -- tuple[float, float, float]，火焰方块的坐标
        - ``playerId`` -- str，玩家的实体ID
        - ``cancel`` -- bool，修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireClientEvent一起修改
        """
    def DimensionChangeServerEvent(self, args):
        """
        [事件]

        玩家维度改变时服务端抛出。

        -----

        【注意】

        当通过传送门从末地回到主世界时， ``toY`` 值为32767，其他情况一般会比设置值高1.62。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``fromDimensionId`` -- int，维度改变前的维度ID
        - ``toDimensionId`` -- int，维度改变前的维度ID
        - ``fromX`` -- float，改变前的位置x
        - ``fromY`` -- float，改变前的位置y
        - ``fromZ`` -- float，改变前的位置z
        - ``toX`` -- float，改变后的位置x
        - ``toY`` -- float，改变后的位置y
        - ``toZ`` -- float，改变后的位置z
        """
    def ChangeLevelUpCostServerEvent(self, args):
        """
        [事件]

        获取玩家下一个等级升级经验时触发，用于重载玩家的升级经验，每个等级在重置之前都只会触发一次。

        -----

        【事件参数】

        - ``level`` -- int，玩家当前等级
        - ``levelUpCostExp`` -- int，当前等级升级到下个等级需要的经验值，当设置升级经验小于1时会被强制调整到1
        - ``changed`` -- bool，设置为True，重载玩家升级经验才会生效

        -----

        【相关接口】

        - `ClearDefinedLevelUpCost <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E7%8E%A9%E5%AE%B6.html?key=ClearDefinedLevelUpCost&docindex=1&type=0>`_
        """
    def AddLevelEvent(self, args):
        """
        [事件]

        当玩家升级时触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``addLevel`` -- int，增加的等级值
        - ``newLevel`` -- int，新的等级
        """
    def AddExpEvent(self, args):
        """
        [事件]

        当玩家增加经验时触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``addExp`` -- int，增加的经验值
        """
    def WillTeleportToServerEvent(self, args):
        """
        [事件]

        实体即将传送或切换维度时触发。

        -----

        【注意】

        假如目标维度尚未在内存中创建（即服务器启动之后，到传送之前，没有玩家进入过这个维度），那么此时事件中返回的目标地点坐标是算法生成的，不能保证正确。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否允许触发，默认为False，若设为True，可阻止触发后续的传送
        - ``entityId`` -- str，实体ID
        - ``fromDimensionId`` -- int，传送前所在的维度
        - ``toDimensionId`` -- int，传送后的目标维度
        - ``fromX`` -- float，传送前的位置x
        - ``fromY`` -- float，传送前的位置y
        - ``fromZ`` -- float，传送前的位置z
        - ``toX`` -- float，传送后的位置x
        - ``toY`` -- float，传送后的位置y
        - ``toZ`` -- float，传送后的位置z
        - ``cause`` -- str，传送理由，详情见EntityTeleportCause枚举
        """
    def WillAddEffectServerEvent(self, args):
        """
        [事件]

        实体即将获得状态效果前触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``effectName`` -- str，状态效果的名字
        - ``effectDuration`` -- int，状态效果的持续时间，单位秒
        - ``effectAmplifier`` -- int，状态效果等级
        - ``cancel`` -- bool，设置为True可以取消
        - ``damage`` -- float，状态将会造成的伤害值，如药水；需要注意，该值不一定是最终的伤害值，例如被伤害吸收效果扣除。只有持续时间为0时有用
        """
    def StartRidingServerEvent(self, args):
        """
        [事件]

        一个实体即将骑乘另外一个实体时触发。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否允许触发，默认为False，若设为True，可阻止触发后续的实体交互事件
        - ``actorId`` -- str，骑乘者的实体ID
        - ``victimId`` -- str，被骑乘的实体ID
        """
    def RemoveEffectServerEvent(self, args):
        """
        [事件]

        实体身上状态效果被移除时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``effectName`` -- str，被移除状态效果的名字
        - ``effectDuration`` -- int，被移除状态效果的剩余持续时间，单位秒
        - ``effectAmplifier`` -- int，被移除状态效果等级
        """
    def RefreshEffectServerEvent(self, args):
        """
        [事件]

        实体身上状态效果更新时触发，更新条件1、新增状态等级较高，更新状态等级及时间；2、新增状态等级不变，时间较长，更新状态持续时间。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``effectName`` -- str，更新状态效果的名字
        - ``effectDuration`` -- int，更新后状态效果剩余持续时间，单位秒
        - ``effectAmplifier`` -- int，更新后的状态效果放大倍数
        - ``damage`` -- float，状态造成的伤害值，如药水
        """
    def ProjectileCritHitEvent(self, args):
        """
        [事件]

        当抛射物与头部碰撞时触发该事件。

        -----

        【注意】

        需调用 ``OpenPlayerCritBox`` 开启玩家爆头后才能触发。

        -----

        【事件参数】

        - ``id`` -- str，抛射物的实体ID
        - ``targetId`` -- str，碰撞目标的实体ID

        -----

        【相关接口】

        - `OpenPlayerCritBox <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=OpenPlayerCritBox&docindex=3&type=0>`_
        - `ClosePlayerCritBox <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=ClosePlayerCritBox&docindex=1&type=0>`_
        """
    def OnMobHitMobServerEvent(self, args):
        """
        [事件]

        通过 ``OpenPlayerHitMobDetection`` 打开生物碰撞检测后，当生物间（包含玩家）碰撞时触发该事件。

        -----

        【注意】

        客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。
        本事件代替原有的 ``OnPlayerHitMobServerEvent`` 事件。

        -----

        【事件参数】

        - ``mobId`` -- str，当前生物的实体ID
        - ``hittedMobList`` -- list[str]，当前生物碰撞到的其他所有生物实体ID的list

        -----

        【相关接口】

        - `OpenPlayerHitMobDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=OpenPlayerHitMobDetection&docindex=4&type=0>`_
        - `ClosePlayerHitMobDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=ClosePlayerHitMobDetection&docindex=1&type=0>`_
        """
    def OnKnockBackServerEvent(self, args):
        """
        [事件]

        实体被击退时触发。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def OnFireHurtEvent(self, args):
        """
        [事件]

        生物受到火焰伤害时触发。

        -----

        【事件参数】

        - ``victim`` -- str，受伤实体ID
        - ``src`` -- str，火焰创建者的实体ID
        - ``fireTime`` -- float，着火时间，单位秒，不支持修改
        - ``cancel`` -- bool，是否取消此处火焰伤害
        - ``cancelIgnite`` -- bool，是否取消点燃效果
        """
    def MobGriefingBlockServerEvent(self, args):
        """
        [事件]

        环境生物改变方块时触发，触发的时机与 ``mobgriefing`` 游戏规则影响的行为相同。

        -----

        【注意】

        触发的时机包括：生物踩踏耕地、破坏单个方块、破门、火矢点燃方块、凋灵boss破坏方块、末影龙破坏方块、末影人捡起方块、蠹虫破坏被虫蚀的方块、蠹虫把方块变成被虫蚀的方块、凋零杀死生物生成凋零玫瑰、生物踩坏海龟蛋。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
        - ``blockX`` -- int，方块x坐标
        - ``blockY`` -- int，方块y坐标
        - ``blockZ`` -- int，方块z坐标
        - ``entityId`` -- str，实体ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``dimensionId`` -- int，维度ID
        """
    def HealthChangeServerEvent(self, args):
        """
        [事件]

        生物生命值发生变化时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``from`` -- str，变化前的生命值（请使用event['from']获取该参数）
        - ``to`` -- str，变化后的生命值
        - ``byScript`` -- str，是否通过SetAttrValue或SetAttrMaxValue调用产生的变化
        """
    def EntityTickServerEvent(self, args):
        """
        [事件] [tick]

        实体tick时触发。该事件为20帧每秒。需要使用 ``AddEntityTickEventWhiteList`` 添加触发该事件的实体类型白名单。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``identifier`` -- str，实体identifier

        -----

        【相关接口】

        - `AddEntityTickEventWhiteList <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=AddEntityTickEventWhiteList&docindex=3&type=0>`_
        """
    def EntityPickupItemServerEvent(self, args):
        """
        [事件]

        有 ``"minecraft:behavior.pickup_items"`` 行为的生物拾取物品时触发该事件，例如村民拾取面包、猪灵拾取金锭。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``secondaryActor`` -- str，物品给予者的实体ID（一般是玩家），如果不存在给予者的话，这里为空字符串
        """
    def EntityMotionStopServerEvent(self, args):
        """
        [事件]

        实体运动器停止事件。实体（包含玩家）添加运动器并开始运行后，运动器自动停止时触发。

        -----

        【注意】

        该事件触发表示运动器播放顺利完成，手动调用的 ``StopEntityMotion`` 、 ``RemoveEntityMotion`` 以及实体被销毁导致的运动器停止不会触发该事件。

        -----

        【事件参数】

        - ``motionId`` -- int，运动器ID
        - ``entityId`` -- str，实体ID
        - ``remove`` -- bool，是否移除该运动器，设置为False则保留，默认为True，即运动器停止后自动移除，该参数设置只对非玩家实体有效
        """
    def EntityMotionStartServerEvent(self, args):
        """
        [事件]

        实体运动器开始事件。实体（包含玩家）添加运动器后，运动器开始运行时触发。

        -----

        【事件参数】

        - ``motionId`` -- int，运动器ID
        - ``entityId`` -- str，实体ID
        """
    def EntityLoadScriptEvent(self, args):
        """
        [事件]

        数据库加载实体自定义数据时触发。

        -----

        【注意】

        只有使用过extraData组件的 ``SetExtraData`` 接口的实体才有此事件，触发时可以通过extraData组件的 ``GetExtraData`` 或 ``GetWholeExtraData`` 接口获取该实体的自定义数据。

        -----

        【事件参数】

        - ``args`` -- list，该事件的参数为长度为2的list，而非dict，其中list的第一个元素为实体ID
        """
    def EntityEffectDamageServerEvent(self, args):
        """
        [事件]

        生物受到状态伤害/回复事件。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``damage`` -- float，伤害值（伤害吸收后实际扣血量），负数表示生命回复量
        - ``attributeBuffType`` -- int，状态类型，参考 `AttributeBuffType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/AttributeBuffType.html?key=AttributeBuffType&docindex=1&type=0>`_
        - ``duration`` -- float，状态持续时间，单位秒
        - ``lifeTimer`` -- float，状态生命时间，单位秒
        - ``isInstantaneous`` -- bool，是否为立即生效状态
        - ``cause`` -- str，伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
        """
    def EntityDroppedItemServerEvent(self, args):
        """
        [事件]

        生物扔出物品时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，生物的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``itemEntityId`` -- str，物品的实体ID
        """
    def EntityChangeDimensionServerEvent(self, args):
        """
        [事件]

        实体维度改变时服务端抛出。

        -----

        【注意】

        实体转移维度时，如果对应维度的对应位置的区块尚未加载，实体会缓存在维度自身的缓冲区中，直到对应区块被加载时才会创建对应的实体，此事件的抛出只代表实体从原维度消失，不代表必定会在对应维度出现。
        玩家维度改变时不触发该事件，而是会触发 ``DimensionChangeServerEvent`` 事件。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``fromDimensionId`` -- int，维度改变前的维度ID
        - ``toDimensionId`` -- int，维度改变后的维度ID
        - ``fromX`` -- float，改变前的位置x
        - ``fromY`` -- float，改变前的位置y
        - ``fromZ`` -- float，改变前的位置z
        - ``toX`` -- float，改变后的位置x
        - ``toY`` -- float，改变后的位置y
        - ``toZ`` -- float，改变后的位置z
        """
    def ChangeSwimStateServerEvent(self, args):
        """
        [事件]

        实体开始或者结束游泳时触发。

        -----

        【注意】

        当实体的状态没有变化时，不会触发此事件，即 ``formState`` 和 ``toState`` 必定一真一假。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``formState`` -- bool，事件触发前，实体是否在游泳状态
        - ``toState`` -- bool，事件触发后，实体是否在游泳状态
        """
    def AddEffectServerEvent(self, args):
        """
        [事件]

        实体获得状态效果时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``effectName`` -- str，实体获得状态效果的名字
        - ``effectDuration`` -- int，状态效果的持续时间，单位秒
        - ``effectAmplifier`` -- int，状态效果的等级
        - ``damage`` -- float，状态造成的伤害值（真实扣除生命值的量）。只有持续时间为0时有用
        """
    def ActorHurtServerEvent(self, args):
        """
        [事件]

        生物（包括玩家）受伤时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``cause`` -- str，伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_
        - ``damage`` -- float，伤害值（被伤害吸收后的值），不可修改
        - ``absorbedDamage`` -- int，被伤害吸收效果吸收的伤害值
        - ``customTag`` -- str，使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
        """
    def ServerSpawnMobEvent(self, args):
        """
        [事件]

        游戏内自动生成生物，以及使用api生成生物时触发。

        -----

        【注意】

        如果通过MOD API生成， ``identifier`` 命名空间为 ``custom`` 。
        如果需要屏蔽原版的生物生成，可以判断 ``identifier`` 命名空间不为 ``custom`` 时设置 ``cancel`` 为 ``True`` 。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``identifier`` -- str，生成实体的命名空间
        - ``type`` -- str，生成实体的类型，参考 `EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_
        - ``baby`` -- str，生成怪物是否是幼年怪
        - ``x`` -- str，生成实体坐标x
        - ``y`` -- str，生成实体坐标y
        - ``z`` -- str，生成实体坐标z
        - ``dimensionId`` -- int，生成实体的维度ID，默认值为0（0为主世界，1为地狱，2为末地）
        - ``realIdentifier`` -- int，生成实体的命名空间，通过MOD API生成的生物在这个参数也能获取到真正的命名空间，而不是以custom开头的
        - ``cancel`` -- bool，是否取消生成该实体
        """
    def ServerPreBlockPatternEvent(self, args):
        """
        [事件]

        用方块组合生成生物，在放置最后一个组成方块时触发该事件。

        -----

        【事件参数】

        - ``enable`` -- bool，是否允许继续生成。若设为False，可阻止生成生物
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``dimensionId`` -- int，维度ID
        - ``entityWillBeGenerated`` -- str，即将生成生物的名字，如"minecraft:pig"
        """
    def ServerPostBlockPatternEvent(self, args):
        """
        [事件]

        用方块组合生成生物，生成生物之后触发该事件。

        -----

        【事件参数】

        - ``entityId`` -- str，生成生物的实体ID
        - ``entityGenerated`` -- str，生成生物的名字，如"minecraft:pig"
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``dimensionId`` -- int，维度ID
        """
    def ServerChatEvent(self, args):
        """
        [事件]

        玩家发送聊天信息时触发。

        -----

        【事件参数】

        - ``username`` -- str，玩家名称
        - ``playerId`` -- str，玩家的实体ID
        - ``message`` -- str，玩家发送的聊天消息内容
        - ``cancel`` -- bool，是否取消这个聊天事件，若取消可以设置为True
        - ``bChatById`` -- bool，是否把聊天消息发送给指定在线玩家，而不是广播给所有在线玩家，若只发送某些玩家可以设置为True
        - ``bForbid`` -- bool，是否禁言，仅apollo可用。True：被禁言，玩家聊天会提示“你已被管理员禁言”
        - ``toPlayerIds`` -- list[str]，接收聊天消息的玩家实体ID的列表，bChatById为True时生效
        - ``gameChatPrefix`` -- str，设置当前玩家在网易聊天界面中的前缀，字数限制4，从字符串头部开始取。前缀文本输入非字符串格式时会被置为空。若cancel为True，会取消掉本次的前缀修改
        - ``gameChatPrefixColorR`` -- float，设置当前玩家在网易聊天界面中前缀颜色rgb的r值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
        - ``gameChatPrefixColorG`` -- float，设置当前玩家在网易聊天界面中前缀颜色rgb的g值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
        - ``gameChatPrefixColorB`` -- float，设置当前玩家在网易聊天界面中前缀颜色rgb的b值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
        """
    def PlayerLeftMessageServerEvent(self, args):
        """
        [事件]

        准备显示“xxx离开游戏”的玩家离开提示文字时服务端抛出的事件。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``name`` -- str，玩家昵称
        - ``cancel`` -- bool，是否显示提示文字，允许修改。True：不显示提示
        - ``message`` -- str，玩家离开游戏的提示文字，允许修改
        """
    def PlayerJoinMessageEvent(self, args):
        """
        [事件]

        准备显示“xxx加入游戏”的玩家登录提示文字时服务端抛出的事件。

        -----

        【注意】

        对于联机类游戏（如联机大厅、网络游戏等），请勿在此事件的回调函数中使用 ``SetFootPos`` 接口修改玩家的位置，否则可能会因为触发服务端反作弊机制而传送失败。如需要在进入游戏时使用 ``SetFootPos`` 接口，建议监听 ``AddServerPlayerEvent`` 并设置位置。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``name`` -- str，玩家昵称
        - ``cancel`` -- bool，是否显示提示文字，允许修改。True：不显示提示
        - ``message`` -- str，玩家加入游戏的提示文字，允许修改
        """
    def PlayerIntendLeaveServerEvent(self, args):
        """
        [事件]

        即将删除玩家时触发该事件。

        -----

        【注意】

        与 ``DelServerPlayerEvent`` 事件不同，此时可以通过各种API获取玩家的当前状态。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def PlaceNeteaseStructureFeatureEvent(self, args):
        """
        [事件]

        首次生成地形时，结构特征即将生成时服务端抛出该事件。

        -----

        【注意】

        需要配合 ``AddNeteaseFeatureWhiteList`` 接口一同使用。
        若在本监听事件中调用其他modSDK接口将无法生效，强烈建议本事件仅用于设置结构放置与否。
        事件只会在网易版结构放置时抛出， ``structureName`` 参数修改为不存在结构或者原生结构时，开发包会出现断言。

        -----

        【事件参数】

        - ``structureName`` -- str，结构名称
        - ``x`` -- int，结构坐标最小方块所在的x坐标
        - ``y`` -- int，结构坐标最小方块所在的y坐标
        - ``z`` -- int，结构坐标最小方块所在的z坐标
        - ``biomeType`` -- int，该feature所放置区块的生物群系类型
        - ``biomeName`` -- int，该feature所放置区块的生物群系名称
        - ``dimensionId`` -- int，维度ID
        - ``cancel`` -- bool，设置为True时可阻止该结构的放置

        -----

        【相关接口】

        - `AddNeteaseFeatureWhiteList <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html?key=AddNeteaseFeatureWhiteList&docindex=2&type=0>`_
        - `RemoveNeteaseFeatureWhiteList <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html?key=RemoveNeteaseFeatureWhiteList&docindex=1&type=0>`_
        - `ClearAllNeteaseFeatureWhiteList <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html?key=ClearAllNeteaseFeatureWhiteList&docindex=1&type=0>`_
        """
    def OnRainLevelChangeServerEvent(self, args):
        """
        [事件]

        下雨强度发生改变时触发。

        -----

        【事件参数】

        - ``oldLevel`` -- float，改变前的下雨强度
        - ``newLevel`` -- float，改变后的下雨强度
        """
    def OnLocalRainLevelChangeServerEvent(self, args):
        """
        [事件]

        独立维度天气下雨强度发生改变时触发。

        -----

        【事件参数】

        - ``oldLevel`` -- float，改变前的下雨强度
        - ``newLevel`` -- float，改变后的下雨强度
        - ``dimensionId`` -- int，维度ID
        """
    def OnLocalLightningLevelChangeServerEvent(self, args):
        """
        [事件]

        独立维度天气打雷强度发生改变时触发。

        -----

        【事件参数】

        - ``oldLevel`` -- float，改变前的打雷强度
        - ``newLevel`` -- float，改变后的打雷强度
        - ``dimensionId`` -- int，维度ID
        """
    def OnLightningLevelChangeServerEvent(self, args):
        """
        [事件]

        打雷强度发生改变时触发。

        -----

        【事件参数】

        - ``oldLevel`` -- float，改变前的打雷强度
        - ``newLevel`` -- float，改变后的打雷强度
        """
    def OnContainerFillLoottableServerEvent(self, args):
        """
        [事件]

        随机奖励箱第一次打开根据loottable生成物品时。

        -----

        【注意】

        只有当 ``dirty`` 为 ``True`` 时才会重新读取 ``itemList`` 并生成对应的掉落物，如果不需要修改掉落结果的话请勿随意修改 ``dirty`` 值。

        -----

        【事件参数】

        - ``loottable`` -- str，奖励箱子所读取的loottable的json路径
        - ``playerId`` -- str，打开奖励箱子的玩家的实体ID
        - ``itemList`` -- list[dict]，掉落物品列表，每个元素为一个itemDict，格式可参考 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``dirty`` -- bool，默认为False，如果需要修改掉落列表需将该值设为True
        """
    def OnCommandOutputServerEvent(self, args):
        """
        [事件]

        Command命令执行成功事件。

        -----

        【注意】

        部分命令在返回的时候没有命令名称， ``SetCommand`` 接口需要 ``showOutput`` 参数为 ``True`` 时才会有返回。

        -----

        【事件参数】

        - ``command`` -- str，命令名称
        - ``message`` -- str，命令返回的消息
        """
    def NewOnEntityAreaEvent(self, args):
        """
        [事件]

        通过 ``RegisterEntityAOIEvent`` 注册过AOI事件后，当有实体进入或离开注册感应区域时触发该事件。

        -----

        【注意】

        本事件代替原有的 ``OnEntityAreaEvent`` 事件。

        -----

        【事件参数】

        - ``name`` -- str，感应区域的名称
        - ``enteredEntities`` -- list[str]，进入该感应区域的实体ID列表
        - ``leftEntities`` -- list[str]，离开该感应区域的实体ID列表

        -----

        【相关接口】

        - `RegisterEntityAOIEvent <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html?key=RegisterEntityAOIEvent&docindex=3&type=0>`_
        - `UnRegisterEntityAOIEvent <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E4%B8%96%E7%95%8C.html?key=UnRegisterEntityAOIEvent&docindex=1&type=0>`_
        """
    def LoadServerAddonScriptsAfter(self, args):
        """
        [事件]

        服务器加载完mod时触发。

        -----

        【事件参数】

        无
        """
    def DelServerPlayerEvent(self, args):
        """
        [事件]

        删除玩家时触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``isTransfer`` -- bool，是否是切服时退出服务器，仅用于Apollo。如果是True，则表示切服时退出服务器；若是False，则表示退出网络游戏
        - ``uid`` -- long，玩家的netease uid，玩家的唯一标识
        """
    def CommandEvent(self, args):
        """
        [事件]

        玩家请求执行指令时触发。

        -----

        【注意】

        该事件是玩家请求执行指令时触发的Hook，该事件不响应命令方块的指令和通过modSDK调用的指令，阻止玩家的该条指令只需要将 ``cancel`` 设置为 ``True`` 。

        -----

        【事件参数】

        - ``entityId`` -- str，玩家的实体ID
        - ``command`` -- str，指令字符串
        - ``cancel`` -- bool，是否取消
        """
    def ClientLoadAddonsFinishServerEvent(self, args):
        """
        [事件]

        客户端mod加载完成时，服务端触发此事件。服务器可以使用此事件，往客户端发送数据给其初始化。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        """
    def ChunkLoadedServerEvent(self, args):
        """
        [事件]

        服务端区块加载完成时。

        -----

        【注意】

        服务端的自定义方块实体加载完成时对应的客户端的自定义方块实体并没有初始化完成，无法使用该事件对客户端的自定义方块实体进行相关操作。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``chunkPosX`` -- int，区块的x坐标，对应方块x坐标区间为[x * 16, x * 16 + 15]
        - ``chunkPosZ`` -- int，区块的z坐标，对应方块z坐标区间为[z * 16, z * 16 + 15]
        - ``blockEntities`` -- list[dict]，随区块加载而加载进世界的自定义方块实体的坐标的列表，列表元素dict包含posX，posY，posZ三个int表示自定义方块实体的坐标，blockName表示方块的identifier，包含命名空间及名称
        """
    def ChunkGeneratedServerEvent(self, args):
        """
        [事件]

        区块创建完成时触发。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``chunkPosX`` -- int，区块的x坐标，对应方块x坐标区间为[chunkPosX * 16, chunkPosX * 16 + 15]
        - ``chunkPosZ`` -- int，区块的z坐标，对应方块z坐标区间为[chunkPosZ * 16, chunkPosZ * 16 + 15]
        - ``blockEntityData`` -- list[dict] | None，该区块中的自定义方块实体列表，通常是由自定义特征生成的自定义方块，没有自定义方块实体时该值为None。列表元素dict的结构如下：{'blockName': str, 'posX': int, 'posY': int, 'posZ': int}
        """
    def ChunkAcquireDiscardedServerEvent(self, args):
        """
        [事件]

        服务端区块即将被卸载时触发。

        -----

        【注意】

        区块卸载：游戏只会加载玩家周围的区块，玩家移动到别的区域时，原来所在区域的区块会被卸载。

        -----

        【事件参数】

        - ``dimension`` -- int，维度ID
        - ``chunkPosX`` -- int，区块的x坐标，对应方块x坐标区间为[x * 16, x * 16 + 15]
        - ``chunkPosZ`` -- int，区块的z坐标，对应方块z坐标区间为[z * 16, z * 16 + 15]
        - ``entities`` -- list[str]，随区块卸载而从世界移除的实体ID的列表。注意事件触发时已经无法获取到这些实体的信息，仅供脚本资源回收用
        - ``blockEntities`` -- list[dict]，随区块卸载而从世界移除的自定义方块实体的坐标的列表，列表元素dict包含posX，posY，posZ三个int表示自定义方块实体的坐标。注意事件触发时已经无法获取到这些方块实体的信息，仅供脚本资源回收用
        """
    def AddServerPlayerEvent(self, args):
        """
        [事件]

        玩家加入时触发该事件。

        -----

        【注意】

        触发此事件时，客户端mod未加载完毕，因此响应本事件时不能客户端发送事件。
        若需要在玩家进入世界时，服务器往客户端发送事件，请使用 ``ClientLoadAddonsFinishServerEvent`` 。
        触发此事件时，玩家的实体还未加载完毕，请勿在这时切换维度。请在客户端监听 ``OnLocalPlayerStopLoading`` 事件并发送事件到服务端再进行维度切换。

        -----

        【事件参数】

        - ``id`` -- str，玩家的实体ID
        - ``isTransfer`` -- bool，是否是切服时进入服务器，仅用于Apollo。如果是True，则表示切服时加入服务器，若是False，则表示登录进入网络游戏
        - ``isReconnect`` -- bool，是否是断线重连，仅用于Apollo。如果是True，则表示本次登录是断线重连，若是False，则表示本次是正常登录或者转服
        - ``isPeUser`` -- bool，是否从手机端登录，仅用于Apollo。如果是True，则表示本次登录是从手机端登录，若是False，则表示本次登录是从PC端登录
        - ``transferParam`` -- str，切服传入参数，仅用于Apollo。调用TransferToOtherServer或TransferToOtherServerById传入的切服参数
        - ``uid`` -- long，仅用于Apollo，玩家的netease uid，玩家的唯一标识
        - ``proxyId`` -- int，仅用于Apollo，当前客户端连接的proxy服务器id
        """
    def AchievementCompleteEvent(self, args):
        """
        [事件]

        玩家完成自定义成就时触发该事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``rootNodeId`` -- str，所属的页面的根节点成就ID
        - ``achievementId`` -- str，达成的成就ID
        - ``title`` -- str，成就标题
        - ``description`` -- str，成就描述
        """
    def PlayerAttackEntityEvent(self, args):
        """
        [事件]

        当玩家攻击时触发该事件。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``victimId`` -- str，受击者的实体ID
        - ``damage`` -- float，伤害值，引擎传过来的值是0，允许脚本层修改为其他数
        - ``isValid`` -- int，脚本是否设置伤害值：1表示是，0表示否
        - ``cancel`` -- bool，是否取消该次攻击，默认不取消
        - ``isKnockBack`` -- bool，是否支持击退效果，默认支持，当不支持时将屏蔽武器击退附魔效果
        - ``isCrit`` -- bool，本次攻击是否产生暴击，不支持修改
        """
    def ServerBlockUseEvent(self, args):
        """
        [事件] [tick]

        玩家右键点击新版自定义方块（或者通过接口 ``AddBlockItemListenForUseEvent`` 增加监听的MC原生游戏方块）时服务端抛出该事件（该事件tick执行，需要注意效率问题）。

        -----

        【注意】

        当对原生方块进行使用时，如堆肥桶等类似有使用功能的方块使用物品时，会触发该事件，而 ``ServerItemUseOnEvent`` 则不会被触发。
        有的方块是在 ``ServerBlockUseEvent`` 中设置 ``cancel`` 生效，但是有部分方块是在 ``ClientBlockUseEvent`` 中设置 ``cancel`` 才生效，如有需求建议在两个事件中同时设置 ``cancel`` 以保证生效。
        部分工具对方块的使用效果，如锹犁地，不一定能通过该事件cancel，还需同时使用 ``ItemUseOnServerEvent`` 进行取消，目前已知有：锹犁地相关的方块：草地、泥土、砂土、菌丝体、灰化土、缠根泥土，均需同时通过 ``ServerBlockUseEvent`` 和 ``ItemUseOnServerEvent`` 进行取消。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``aux`` -- int，方块附加值
        - ``cancel`` -- bool，设置为True可拦截与方块交互的逻辑
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``clickX`` -- float，点击点的x比例位置
        - ``clickY`` -- float，点击点的y比例位置
        - ``clickZ`` -- float，点击点的z比例位置
        - ``face`` -- int，点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``itemDict`` -- dict，使用的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``dimensionId`` -- int，维度ID

        -----

        【相关接口】

        - `AddBlockItemListenForUseEvent <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=AddBlockItemListenForUseEvent&docindex=4&type=0>`_
        - `RemoveBlockItemListenForUseEvent <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=RemoveBlockItemListenForUseEvent&docindex=1&type=0>`_
        - `ClearAllListenForBlockUseEventItems <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=ClearAllListenForBlockUseEventItems&docindex=1&type=0>`_
        """
    def OnGroundServerEvent(self, args):
        """
        [事件]

        实体着地事件。实体，掉落的物品，点燃的TNT掉落地面时触发。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def SpawnProjectileServerEvent(self, args):
        """
        [事件]

        抛射物生成时触发。

        -----

        【注意】

        该事件里无法获取弹射物实体的auxvalue。如有需要可以延迟一帧获取，或者在 ``ProjectileDoHitEffectEvent`` 获取。

        -----

        【事件参数】

        - ``projectileId`` -- str，抛射物的实体ID
        - ``projectileIdentifier`` -- str，抛射物的identifier
        - ``spawnerId`` -- str，发射者的实体ID，没有发射者时为-1
        """
    def EntityDieLoottableServerEvent(self, args):
        """
        [事件]

        生物死亡掉落物品时触发。

        -----

        【注意】

        只有当 ``dirty`` 为 ``True`` 时才会重新读取 ``itemList`` 并生成对应的掉落物，如果不需要修改掉落结果的话请勿随意修改 ``dirty`` 值。
        该事件在生物死亡后会触发，无论是否掉落物品，因此掉落物品列表可能存在为空的情况。
        掉落物不包含玩家或生物携带以及背包内的物品，若要获取死亡后由背包扔出的物品请参考 ``EntityDroppedItemServerEvent`` 事件。

        -----

        【事件参数】

        - ``dieEntityId`` -- str，死亡实体ID
        - ``attacker`` -- str，伤害来源实体ID
        - ``itemList`` -- list[dict]，掉落物品列表，每个元素为一个itemDict，格式可参考 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``dirty`` -- bool，默认为False，如果需要修改掉落列表需将该值设为True
        """
    def ActuallyHurtServerEvent(self, args):
        """
        [事件]

        实体实际受到伤害时触发，相比于 ``DamageEvent`` ，该伤害为经过护甲及buff计算后，实际的扣血量。

        -----

        【注意】

        药水与状态效果造成的伤害不触发，可以使用 ``ActorHurtServerEvent`` 。
        为了游戏运行效率请尽可能避免将火的伤害设置为0，因为这样会导致大量触发该事件。
        若要修改 ``damage`` 的值，请确保修改后的值与原值不同，且支持转换为浮点型，否则引擎会忽略这次修改。
        青蛙、山羊跳跃落地时也会触发此伤害事件，但它们的掉落伤害实际会有减免，青蛙减少5，山羊减少10。
        在无懈可击时间内，只要实体受到高于上次受击的伤害，可以连续触发不受 ``SetHurtCD`` 影响，如实体连续受到1伤害，如果在本事件中修改 ``damage`` 为0.5，则引擎会认为每次都有0.5的溢出伤害，可以通过 ``invulnerableTime`` 和 ``lastHurt`` 来判断是否取消这次伤害。

        -----

        【事件参数】

        - ``srcId`` -- str，伤害源实体ID
        - ``projectileId`` -- str，抛射物实体ID
        - ``entityId`` -- str，受伤的实体ID
        - ``damage`` -- float，伤害值（被伤害吸收后的值），允许修改，设置为0则此次造成的伤害为0，若设置数值和原来一样则视为没有修改
        - ``invulnerableTime`` -- int，实体受击后，剩余的无懈可击帧数，在无懈可击时间内，damage为超过上次伤害的部分
        - ``lastHurt`` -- float，实体上次受到的伤害
        - ``cause`` -- str，伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_
        - ``customTag`` -- str，使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
        """
    def HealthChangeBeforeServerEvent(self, args):
        """
        [事件]

        生物生命值发生变化之前触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``from`` -- float，变化前的生命值（请使用event['from']获取该参数）
        - ``to`` -- float，将要变化到的生命值，cancel设置为True时可以取消该变化，但是此参数不变
        - ``byScript`` -- bool，是否通过SetAttrValue或SetAttrMaxValue调用产生的变化
        - ``cancel`` -- bool，是否取消该变化
        """
    def DimensionChangeFinishServerEvent(self, args):
        """
        [事件]

        玩家维度改变完成后服务端抛出。

        -----

        【注意】

        当通过传送门从末地回到主世界时， ``toPos`` 的y值为32767，其他情况一般会比设置值高1.62。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``fromDimensionId`` -- int，维度改变前的维度
        - ``toDimensionId`` -- int，维度改变后的维度
        - ``toPos`` -- tuple[float, float, float]，改变后的位置，其中y值为脚底加上角色的身高值
        """
    def EntityDefinitionsEventServerEvent(self, args):
        """
        [事件]

        生物定义json文件中设置的event触发时同时触发。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``eventName`` -- str，触发的事件名称
        """
    def PlayerDoInteractServerEvent(self, args):
        """
        [事件]

        玩家与有 ``"minecraft:interact"`` 组件的生物交互时触发该事件，例如玩家手持空桶对牛挤奶、玩家手持打火石点燃苦力怕。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``interactEntityId`` -- str，交互生物的实体ID
        """
    def PlayerInteractServerEvent(self, args):
        """
        [事件]

        玩家可以与实体交互时触发。

        -----

        【注意】

        如果是鼠标控制模式，则当准心对着实体时触发。如果是触屏模式，则触发时机与屏幕下方的交互按钮显示的时机相同。
        玩家真正与实体发生交互的事件见 `PlayerDoInteractServerEvent <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E7%8E%A9%E5%AE%B6.html?key=PlayerDoInteractServerEvent&docindex=3&type=0>`_ 。

        -----

        【事件参数】

        - ``cancel`` -- bool，是否取消触发，默认为False，若设为True，可阻止触发后续的实体交互事件
        - ``playerId`` -- str，玩家的实体ID
        - ``itemDict`` -- dict，玩家手持物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``victimId`` -- str，交互生物的实体ID
        """
    def MobDieEvent(self, args):
        """
        [事件]

        生物死亡时触发。

        -----

        【注意】

        不能在该事件回调中对攻击者手持物品进行修改，如 ``SpawnItemToPlayerCarried`` 、 ``ChangePlayerItemTipsAndExtraId`` 等接口。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        - ``attacker`` -- str，攻击者实体ID
        - ``cause`` -- str，伤害来源，详见Minecraft枚举值文档的 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html>`_
        - ``customTag`` -- str，使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
        """
    def AddEntityServerEvent(self, args):
        """
        [事件]

        服务端侧创建新实体，或实体从存档加载时触发。

        -----

        【注意】

        创建玩家时不会触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        - ``posX`` -- float，实体位置x
        - ``posY`` -- float，实体位置y
        - ``posZ`` -- float，实体位置z
        - ``dimensionId`` -- int，维度ID
        - ``isBaby`` -- bool，是否为幼儿
        - ``engineTypeStr`` -- str，实体类型，即实体identifier
        - ``itemName`` -- str，物品identifier（仅当物品实体时存在该字段）
        - ``auxValue`` -- int，物品附加值（仅当物品实体时存在该字段）
        """
    def OnMobHitBlockServerEvent(self, args):
        """
        [事件]

        通过 ``OpenMobHitBlockDetection`` 打开方块碰撞检测后，当生物（不包括玩家）碰撞到方块时触发该事件。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``posX`` -- int，碰撞方块x坐标
        - ``posY`` -- int，碰撞方块y坐标
        - ``posZ`` -- int，碰撞方块z坐标
        - ``blockId`` -- str，碰撞方块的identifier
        - ``auxValue`` -- int，碰撞方块的附加值
        - ``dimensionId`` -- int，维度ID

        -----

        【相关接口】

        - `OpenMobHitBlockDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=OpenMobHitBlockDetection&docindex=3&type=0>`_
        - `CloseMobHitBlockDetection <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E5%AE%9E%E4%BD%93.html?key=CloseMobHitBlockDetection&docindex=1&type=0>`_
        """
    def OnEntityInsideBlockServerEvent(self, args):
        """
        [事件] [tick]

        当实体碰撞盒所在区域有方块时，服务端持续触发。

        -----

        【注意】

        不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： `自定义方块JSON组件 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/2-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%96%B9%E5%9D%97/1-JSON%E7%BB%84%E4%BB%B6.html>`_ ），原版方块需要先通过 ``RegisterOnEntityInside`` 接口注册才能触发。
        如果需要修改 ``slowdownMulti`` / ``cancel`` ，强烈建议与客户端事件同步修改，避免出现客户端表现不一致等非预期现象。
        如果要在脚本层修改 ``slowdownMulti`` ，回传的一定要是浮点型，例如需要赋值1.0而不是1。
        有任意 ``slowdownMulti`` 参数被传回非0值时生效减速比例。
        ``slowdownMulti`` 参数更像是一个Buff，例如并不是立刻计算，而是先保存在实体属性里延后计算。在已经有 ``slowdownMulti`` 属性的情况下会取最低的值、免疫掉落伤害等，与原版蜘蛛网逻辑基本一致。

        -----

        【事件参数】

        - ``entityId`` -- str，实体ID
        - ``slowdownMultiX`` -- float，实体移速x方向的减速比例，可在脚本层被修改
        - ``slowdownMultiY`` -- float，实体移速y方向的减速比例，可在脚本层被修改
        - ``slowdownMultiZ`` -- float，实体移速z方向的减速比例，可在脚本层被修改
        - ``blockX`` -- int，方块位置x
        - ``blockY`` -- int，方块位置y
        - ``blockZ`` -- int，方块位置z
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``cancel`` -- bool，可由脚本层回传True给引擎，阻止触发后续原版逻辑

        -----

        【相关接口】

        - `RegisterOnEntityInside <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=RegisterOnEntityInside&docindex=2&type=0>`_
        - `UnRegisterOnEntityInside <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E4%BA%8B%E4%BB%B6/%E6%96%B9%E5%9D%97.html?key=UnRegisterOnEntityInside&docindex=2&type=0>`_
        """
    def EntityStartRidingEvent(self, args):
        """
        [事件]

        当实体骑乘上另一个实体时触发。

        -----

        【事件参数】

        - ``id`` -- str，骑乘者实体ID
        - ``rideId`` -- str，坐骑实体ID
        """
    def EntityStopRidingEvent(self, args):
        """
        [事件]

        当实体停止骑乘时触发。

        -----

        【注意】

        以下情况不允许取消：

        - ride组件 ``StopEntityRiding`` 接口；
        - 玩家传送时；
        - 坐骑死亡时；
        - 玩家睡觉时；
        - 玩家死亡时；
        - 未驯服的马；
        - 怕水的生物坐骑进入水里；
        - 切换维度。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        - ``rideId`` -- str，坐骑的实体ID
        - ``exitFromRider`` -- bool，是否下坐骑
        - ``entityIsBeingDestroyed`` -- bool，坐骑是否将要销毁
        - ``switchingRides`` -- bool，是否换乘坐骑
        - ``cancel`` -- bool，设置为True可以取消（需要与客户端事件一同取消）
        """
    def ServerItemUseOnEvent(self, args):
        """
        [事件] [tick]

        玩家在对方块使用物品之前服务端抛出的事件。

        -----

        【注意】

        如果需要取消物品的使用需要同时在 ``ClientItemUseOnEvent`` 和 ``ServerItemUseOnEvent`` 中将 ``ret`` 设置为 ``True`` 才能正确取消。
        当对原生方块进行使用时，如堆肥桶等类似有使用功能的方块使用物品时，不会触发该事件。而当原生方块加入监听后， ``ServerBlockUseEvent`` 会触发。
        该事件仅在鼠标模式下为帧事件。

        -----

        【事件参数】

        - ``entityId`` -- str，玩家实体ID
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``blockName`` -- str，方块的identifier，包含命名空间及名称
        - ``blockAuxValue`` -- int，方块的附加值
        - ``face`` -- int，点击方块的面，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``clickX`` -- float，点击点的x比例位置
        - ``clickY`` -- float，点击点的y比例位置
        - ``clickZ`` -- float，点击点的z比例位置
        - ``ret`` -- bool，设为True可取消物品的使用
        """
    def ActorUseItemServerEvent(self, args):
        """
        [事件]

        玩家使用物品生效之前服务端抛出的事件。

        -----

        【注意】

        比较特殊不走该事件的例子：

        - 染料对有水的炼药锅使用；
        - 盔甲架装备盔甲。

        喝牛奶会触发该事件，但是不会触发 ``ActorUseItemClientEvent`` 。

        -----

        【事件参数】

        - ``playerId`` -- str，玩家的实体id
        - ``itemDict`` -- dict， `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``useMethod`` -- int，使用物品的方法，详见 `ItemUseMethodEnum枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemUseMethodEnum.html?key=ItemUseMethodEnum&docindex=1&type=0>`_
        """
    def ActorAcquiredItemServerEvent(self, args):
        """
        [事件]

        玩家获得物品时服务端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点）。

        -----

        【事件参数】

        - ``actor`` -- str，获得物品玩家实体ID
        - ``secondaryActor`` -- str，物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
        - ``itemDict`` -- dict，获得的物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_
        - ``acquireMethod`` -- int，获得物品的方法，详见 `ItemAcquisitionMethod枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ItemAcquisitionMethod.html?key=ItemAcquisitionMethod&docindex=1&type=0>`_
        """
    def DestroyBlockEvent(self, args):
        """
        [事件]

        当方块已经被玩家破坏时触发该事件。

        -----

        【注意】

        在生存模式或创造模式下都会触发。

        -----

        【事件参数】

        - ``x`` -- int，方块x坐标
        - ``y`` -- int，方块y坐标
        - ``z`` -- int，方块z坐标
        - ``face`` -- int，方块被敲击的面向id，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``fullName`` -- str，方块的identifier，包含命名空间及名称
        - ``auxData`` -- int，方块附加值
        - ``playerId`` -- str，破坏方块的玩家实体ID
        - ``dimensionId`` -- int，维度ID
        - ``dropEntityIds`` -- list[str]，掉落物实体ID列表
        """
    def DamageEvent(self, args):
        """
        [事件]

        实体受到伤害时触发。

        -----

        【注意】

        ``damage`` 值会被护甲和absorption等吸收，不一定是最终扣血量。通过设置这个伤害值可以取消伤害，但不会取消由击退效果或者点燃效果带来的伤害。
        该事件在实体受伤之前触发，由于部分伤害是在tick中处理，因此持续触发受伤时（如站在火中）会每帧触发事件（可以使用 ``ActorHurtServerEvent`` 来避免）。
        这里的 ``damage`` 是伤害源具有的攻击伤害值，并非实体真实的扣血量，如果需要获取真实伤害，可以使用 ``ActuallyHurtServerEvent`` 事件。
        当目标无法被击退时， ``knock`` 值无效。
        药水与状态效果造成的伤害不触发，可以使用 ``ActorHurtServerEvent`` 。
        由于点燃的实现原因，此处 ``ignite`` 设置为 ``False`` 并不能取消实体的点燃效果（如果需要取消点燃效果，请通过 ``OnFireHurtEvent`` 事件实现）。

        -----

        【事件参数】

        - ``srcId`` -- str，伤害源实体ID
        - ``projectileId`` -- str，投射物实体ID
        - ``entityId`` -- str，受伤实体ID
        - ``damage`` -- int，伤害值（被伤害吸收前的值），允许修改，设置为0则此次造成的伤害为0
        - ``damage_f`` -- float，伤害值（被伤害吸收前的值），不允许修改
        - ``absorption`` -- int，伤害吸收生命值，详见 `AttrType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/AttrType.html?key=AttrType&docindex=1&type=0>`_ 枚举的ABSORPTION
        - ``cause`` -- str，伤害来源，详见 `ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举
        - ``knock`` -- bool，是否击退被攻击者，允许修改，设置该值为False则不产生击退
        - ``ignite`` -- bool，是否点燃被伤害者，允许修改，设置该值为True产生点燃效果，反之亦然
        - ``customTag`` -- str，使用 `Hurt接口 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E5%AE%9E%E4%BD%93/%E8%A1%8C%E4%B8%BA.html#hurt>`_ 传入的自定义伤害类型
        """
    def ExplosionServerEvent(self, args):
        """
        [事件]

        当发生爆炸时触发。

        -----

        【注意】

        可以通过修改 ``blocks`` 取消爆炸对指定方块的影响。
        某些情况下爆炸创建者实体ID为 ``None`` ，此时受伤实体ID列表也为 ``None`` ，比如爬行者所造成的爆炸。

        -----

        【事件参数】

        - ``blocks`` -- list[list[int, int, int, bool]]，爆炸涉及到的方块列表，每个方块以一个列表表示，前三个元素分别为方块坐标xyz，第四个元素为是否取消爆炸对该方块的影响，将第四个元素设置为True即可取消。
        - ``victims`` -- list[str] | None，受伤实体ID列表，当该爆炸创建者实体ID为None时，victims也为None
        - ``sourceId`` -- str | None，爆炸创建者实体ID
        - ``explodePos`` -- list[float, float, float]，爆炸位置[x, y, z]
        - ``dimensionId`` -- int，维度ID
        """
    def ProjectileDoHitEffectEvent(self, args):
        """
        [事件]

        当抛射物碰撞时触发该事件。

        -----

        【事件参数】

        - ``id`` -- str，子弹的实体ID
        - ``hitTargetType`` -- str，碰撞目标类型，"ENTITY"或"BLOCK"
        - ``targetId`` -- str，碰撞目标的实体ID
        - ``hitFace`` -- int，撞击在方块上的面ID，参考 `Facing枚举 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/Facing.html?key=Facing&docindex=1&type=0>`_
        - ``x`` -- float，碰撞x坐标
        - ``y`` -- float，碰撞y坐标
        - ``z`` -- float，碰撞z坐标
        - ``blockPosX`` -- int，碰撞是方块时，方块x坐标
        - ``blockPosY`` -- int，碰撞是方块时，方块y坐标
        - ``blockPosZ`` -- int，碰撞是方块时，方块z坐标
        - ``srcId`` -- str，抛射物创建者的实体ID
        - ``cancel`` -- bool，是否取消这个碰撞事件，若取消可以设置为True
        """
    def OnCarriedNewItemChangedServerEvent(self, args):
        """
        [事件]

        玩家切换主手物品时触发该事件。

        -----

        【注意】

        切换耐久度不同的相同物品，不会触发该事件。

        -----

        【事件参数】

        - ``oldItemDict`` -- dict | None，旧物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当旧物品为空时，此项属性为None
        - ``newItemDict`` -- dict | None，新物品的 `物品信息字典 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/10-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5/1-%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E5%9F%BA%E7%A1%80%E6%A6%82%E5%BF%B5.html?key=%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8&docindex=1&type=0>`_，当新物品为空时，此项属性为None
        - ``playerId`` -- str，玩家的实体ID
        """
    def EntityRemoveEvent(self, args):
        """
        [事件]

        实体被删除时触发。

        -----

        【注意】

        触发情景：实体从场景中被删除，例如：生物死亡，生物被 `清除 <https://minecraft.fandom.com/zh/wiki/%E7%94%9F%E6%88%90#.E6.B8.85.E9.99.A4>`_，玩家退出游戏，船/盔甲架被破坏，掉落物/经验球被捡起或清除。
        当生物随区块卸载时，不会触发该事件，而是 ``ChunkAcquireDiscardedServerEvent`` 事件。
        关于生物的清除：当生物离玩家大于wiki所说的距离，并且还在玩家的模拟距离内时，会被清除。也就是说，如果玩家瞬间传送到远处，原处的生物马上离开了模拟距离，并不会被清除。
        玩家退出游戏时， ``EntityRemoveEvent`` ， ``DelServerPlayerEvent`` 按顺序依次触发。

        -----

        【事件参数】

        - ``id`` -- str，实体ID
        """
    def OnScriptTickServer(self, args):
        """
        [事件] [tick]

        服务端tick事件，1秒30次。

        -----

        【事件参数】

        无
        """
    def UiInitFinished(self, args):
        """
        [nuoyanlib] [事件]

        客户端玩家UI框架初始化完成时，服务端触发。

        -----

        【事件参数】

        - ``__id__`` -- str，玩家的实体ID
        """
