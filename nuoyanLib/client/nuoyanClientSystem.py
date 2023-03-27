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
#   Last Modified : 2023-03-18
#
# ====================================================


from types import MethodType as _MethodType
from collections import Callable as _Callable
from .._config import SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME, MOD_NAME as _MOD_NAME
from ..utils.utils import is_method_overridden as _is_method_overridden
from clientTimer import ClientTimer as _ClientTimer
import mod.client.extraClientApi as _clientApi


__all__ = [
    "ALL_ENGINE_EVENTS",
    "listen",
    "NuoyanClientSystem",
]


_ENGINE_NAMESPACE = _clientApi.GetEngineNamespace()
_ENGINE_SYSTEM_NAME = _clientApi.GetEngineSystemName()
_ScreenNode = _clientApi.GetScreenNodeCls()
_ViewBinder = _clientApi.GetViewBinderCls()
_PLAYER_ID = _clientApi.GetLocalPlayerId()
_LEVEL_ID = _clientApi.GetLevelId()
_ClientSystem = _clientApi.GetClientSystemCls()
_CompFactory = _clientApi.GetEngineCompFactory()
_PlayerActorMotionComp = _CompFactory.CreateActorMotion(_PLAYER_ID)
_LevelGameComp = _CompFactory.CreateGame(_LEVEL_ID)
_PlayerItemComp = _CompFactory.CreateItem(_PLAYER_ID)
_PlayerCameraComp = _CompFactory.CreateCamera(_PLAYER_ID)
_LevelBlockInfoComp = _CompFactory.CreateBlockInfo(_PLAYER_ID)
_PlayerPosComp = _CompFactory.CreatePos(_PLAYER_ID)


if "/" in __file__:
    _PATH = __file__[:-3].replace("/", ".")
else:
    _PATH = __file__
_UI_NAMESPACE_GAME_TICK = "_GameTick"
_UI_PATH_GAME_TICK = _PATH + "._GameTick"
_UI_DEF_GAME_TICK = "_GameTick.main"


ALL_ENGINE_EVENTS = (
    ("OnScriptTickClient", "OnScriptTick"),
    ("UiInitFinished", "OnUiInitFinished"),
    ("AddEntityClientEvent", "OnAddEntity"),
    ("AddPlayerAOIClientEvent", "OnAddPlayerAOI"),
    ("AddPlayerCreatedClientEvent", "OnAddPlayerCreated"),
    ("ChunkAcquireDiscardedClientEvent", "OnChunkAcquireDiscarded"),
    ("ChunkLoadedClientEvent", "OnChunkLoaded"),
    ("LoadClientAddonScriptsAfter", "OnLoadClientAddonScriptsAfter"),
    ("OnCommandOutputClientEvent", "OnCommandOutput"),
    ("OnLocalPlayerStopLoading", "OnLocalPlayerStopLoading"),
    ("RemoveEntityClientEvent", "OnRemoveEntity"),
    ("RemovePlayerAOIClientEvent", "OnRemovePlayerAOI"),
    ("UnLoadClientAddonScriptsBefore", "OnUnLoadClientAddonScriptsBefore"),
    ("ApproachEntityClientEvent", "OnApproachEntity"),
    ("EntityModelChangedClientEvent", "OnEntityModelChanged"),
    ("EntityStopRidingEvent", "OnEntityStopRiding"),
    ("HealthChangeClientEvent", "OnHealthChange"),
    ("OnGroundClientEvent", "OnGround"),
    ("OnMobHitMobClientEvent", "OnMobHitMob"),
    ("StartRidingClientEvent", "OnStartRiding"),
    ("LeaveEntityClientEvent", "OnLeaveEntity"),
    ("CameraMotionStartClientEvent", "OnCameraMotionStart"),
    ("CameraMotionStopClientEvent", "OnCameraMotionStop"),
    ("DimensionChangeClientEvent", "OnDimensionChange"),
    ("DimensionChangeFinishClientEvent", "OnDimensionChangeFinish"),
    ("ExtinguishFireClientEvent", "OnExtinguishFire"),
    ("GameTypeChangedClientEvent", "OnGameTypeChanged"),
    ("OnPlayerHitBlockClientEvent", "OnPlayerHitBlock"),
    ("PerspChangeClientEvent", "OnPerspChange"),
    ("ClientBlockUseEvent", "OnBlockUse"),
    ("FallingBlockCauseDamageBeforeClientEvent", "OnFallingBlockCauseDamageBefore"),
    ("OnAfterFallOnBlockClientEvent", "OnAfterFallOnBlock"),
    ("OnEntityInsideBlockClientEvent", "OnEntityInsideBlock"),
    ("OnModBlockNeteaseEffectCreatedClientEvent", "OnModBlockNeteaseEffectCreated"),
    ("OnStandOnBlockClientEvent", "OnStandOnBlock"),
    ("PlayerTryDestroyBlockClientEvent", "OnPlayerTryDestroyBlock"),
    ("ShearsDestoryBlockBeforeClientEvent", "OnShearsDestoryBlockBefore"),
    ("StepOffBlockClientEvent", "OnStepOffBlock"),
    ("StartDestroyBlockClientEvent", "OnStartDestroyBlock"),
    ("StepOnBlockClientEvent", "OnStepOnBlock"),
    ("ActorAcquiredItemClientEvent", "OnActorAcquiredItem"),
    ("ActorUseItemClientEvent", "OnActorUseItem"),
    ("AnvilCreateResultItemAfterClientEvent", "OnAnvilCreateResultItemAfter"),
    ("ClientItemTryUseEvent", "OnItemTryUse"),
    ("ClientItemUseOnEvent", "OnItemUseOn"),
    ("ClientShapedRecipeTriggeredEvent", "OnShapedRecipeTriggered"),
    ("GrindStoneRemovedEnchantClientEvent", "OnGrindStoneRemovedEnchant"),
    ("InventoryItemChangedClientEvent", "OnInventoryItemChanged"),
    ("ItemReleaseUsingClientEvent", "OnItemReleaseUsing"),
    ("OnCarriedNewItemChangedClientEvent", "OnCarriedNewItemChanged"),
    ("PlayerTryDropItemClientEvent", "OnPlayerTryDropItem"),
    ("StartUsingItemClientEvent", "OnStartUsingItem"),
    ("StopUsingItemClientEvent", "OnStopUsingItem"),
    ("AttackAnimBeginClientEvent", "OnAttackAnimBegin"),
    ("AttackAnimEndClientEvent", "OnAttackAnimEnd"),
    ("WalkAnimBeginClientEvent", "OnWalkAnimBegin"),
    ("WalkAnimEndClientEvent", "OnWalkAnimEnd"),
    ("ClientChestCloseEvent", "OnChestClose"),
    ("ClientChestOpenEvent", "OnChestOpen"),
    ("ClientPlayerInventoryCloseEvent", "OnPlayerInventoryClose"),
    ("ClientPlayerInventoryOpenEvent", "OnPlayerInventoryOpen"),
    ("GridComponentSizeChangedClientEvent", "OnGridComponentSizeChanged"),
    ("OnItemSlotButtonClickedEvent", "OnItemSlotButtonClicked"),
    ("PlayerChatButtonClickClientEvent", "OnPlayerChatButtonClick"),
    ("PopScreenEvent", "OnPopScreen"),
    ("PushScreenEvent", "OnPushScreen"),
    ("ScreenSizeChangedClientEvent", "OnScreenSizeChanged"),
    ("OnMusicStopClientEvent", "OnMusicStop"),
    ("PlayMusicClientEvent", "OnPlayMusic"),
    ("PlaySoundClientEvent", "OnPlaySound"),
    ("ClientJumpButtonPressDownEvent", "OnJumpButtonPressDown"),
    ("ClientJumpButtonReleaseEvent", "OnJumpButtonRelease"),
    ("GetEntityByCoordEvent", "OnGetEntityByCoord"),
    ("GetEntityByCoordReleaseClientEvent", "OnGetEntityByCoordRelease"),
    ("HoldBeforeClientEvent", "OnHoldBefore"),
    ("LeftClickBeforeClientEvent", "OnLeftClickBefore"),
    ("LeftClickReleaseClientEvent", "OnLeftClickRelease"),
    ("MouseWheelClientEvent", "OnMouseWheel"),
    ("OnBackButtonReleaseClientEvent", "OnBackButtonRelease"),
    ("OnClientPlayerStartMove", "OnPlayerStartMove"),
    ("OnClientPlayerStopMove", "OnPlayerStopMove"),
    ("OnKeyPressInGame", "OnKeyPressInGame"),
    ("OnMouseMiddleDownClientEvent", "OnMouseMiddleDown"),
    ("RightClickBeforeClientEvent", "OnRightClickBefore"),
    ("RightClickReleaseClientEvent", "OnRightClickRelease"),
    ("TapBeforeClientEvent", "OnTapBefore"),
    ("TapOrHoldReleaseClientEvent", "OnTapOrHoldRelease"),
)


_lsnFuncArgs = []


def listen(eventName, t=0, namespace="", systemName="", priority=0):
    # type: (str, int, str, str, int) -> ...
    """
    函数装饰器，通过对函数进行装饰即可实现监听。
    -----------------------------------------------------------
    【eventName: str】 事件名称
    【t: int = 0】 0表示监听服务端传来的自定义事件，1表示监听客户端引擎事件，2表示监听其他Mod的事件
    【namespace: str = ""】 其他Mod的命名空间
    【systemName: str = ""】 其他Mod的系统名称
    【priority: int = 0】 优先级
    -----------------------------------------------------------
    示例：
    class MyClientSystem(ClientSystem):
        # 监听服务端传来的自定义事件
        @listen("MyCustomEvent")
        def eventCallback(self, args):
            pass

        # 监听AddEntityClientEvent事件
        @listen("AddEntityClientEvent", 1)
        def OnAddEntity(self, args):
            pass
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


class NuoyanClientSystem(_ClientSystem):
    """
    ClientSystem扩展类。将自定义ClientSystem继承本类即可使用本类的全部功能。
    -----------------------------------------------------------
    【基础功能】
    1. 所有官方文档中收录的客户端引擎事件以及新增事件均无需手动监听，只需重写对应事件的同名方法即可（支持热更）；
    2. 支持对在__init__方法中新增的事件监听或客户端属性（变量）执行热更；
    3. 无需重写Destroy方法进行事件的反监听。
    -----------------------------------------------------------
    【新增接口】
    1. BroadcastToAllClient：广播事件到所有玩家的客户端
    2. ListenForEventV2：监听事件（简化版）
    3. RegisterAndCreateUI：注册并创建UI
    4. CallServer：调用服务端属性（包括变量和函数）
    5. TestMode：开启或关闭客户端测试模式
    6. AddPlayerRenderResources：一键添加玩家渲染资源，包括模型、贴图、材质、渲染控制器、动画、动画控制器、音效和粒子特效
    7. SetQueryVar：设置指定实体query.mod变量的值，支持全局同步（即所有客户端同步设置该变量的值）
    -----------------------------------------------------------
    【新增事件】
    1. OnGameTick：频率与游戏实时帧率同步的Tick事件
    -----------------------------------------------------------
    【新增属性】
    -----------------------------------------------------------
    【注意事项】
    1. 带有*tick*标签的事件为帧事件，需要注意编写相关逻辑；
    2. 事件回调参数中，参数名前面的美元符号“$”表示该参数可进行修改。
    """

    def __init__(self, namespace, systemName):
        super(NuoyanClientSystem, self).__init__(namespace, systemName)
        self._gameTickNode = None
        self._uiInitFinished = False
        self.__handle = 0
        self.__timer = None  # type: _ClientTimer
        self.__lastPos = None
        self._3dItemRes = {}
        self.__listen()
        self._checkOnGameTick()

    def Destroy(self):
        """
        客户端系统销毁时触发。
        """
        self.UnListenAllEvents()

    # todo:==================================== Engine Event Callback ==================================================

    def OnTapOrHoldRelease(self, args):
        """
        玩家点击屏幕后松手时触发。
        仅在移动端或pc的F11模式下触发。
        pc的非F11模式可以使用LeftClickReleaseClientEvent与RightClickReleaseClientEvent事件监听鼠标松开。
        短按及长按后松手都会触发该事件。
        -----------------------------------------------------------
        无参数
        """

    def OnTapBefore(self, args):
        """
        玩家点击屏幕并松手，即将响应到游戏内时触发。
        仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用LeftClickBeforeClientEvent事件监听鼠标左键。
        玩家点击屏幕的处理顺序为：
        1. 玩家点击屏幕，没有进行拖动，并在短按判定时间（250毫秒）内松手；
        2. 触发该事件；
        3. 若事件没有cancel，则根据准心处的物体类型以及与玩家的距离，进行攻击或放置等操作。
        与GetEntityByCoordEvent事件不同的是，被ui层捕获，没有穿透到世界的点击不会触发该事件，例如：
        1. 点击原版的移动/跳跃等按钮；
        2. 通过SetIsHud(0)屏蔽了游戏操作；
        3. 对按钮使用AddTouchEventHandler接口时isSwallow参数设置为True。
        -----------------------------------------------------------
        【$cancel: bool】 设置为True可拦截原版的攻击或放置响应
        """

    def OnRightClickRelease(self, args):
        """
        玩家松开鼠标右键时触发。
        仅在pc的普通控制模式（即非F11模式）下触发。
        在F11下右键，按下会触发RightClickBeforeClientEvent，松开时会触发TapOrHoldReleaseClientEvent。
        -----------------------------------------------------------
        无参数
        """

    def OnRightClickBefore(self, args):
        """
        玩家按下鼠标右键时触发。仅在pc下触发（普通控制模式及F11模式都会触发）。
        -----------------------------------------------------------
        【$cancel: bool】 设置为True可拦截原版的物品使用/实体交互响应
        """

    def OnMouseMiddleDown(self, args):
        """
        鼠标按下中键时触发。
        仅通过PushScreen创建的界面能够正常返回坐标，开启F11模式的时候，返回最后点击屏幕时的坐标。
        -----------------------------------------------------------
        【isDown: str】 是否按下，按下为1，弹起为0
        【mousePositionX: float】 按下时的x坐标
        【mousePositionY: float】 按下时的y坐标
        """

    def OnKeyPressInGame(self, args):
        """
        按键按下或按键释放时触发。
        -----------------------------------------------------------
        【screenName: str】 当前screenName
        【key: str】 键码（注：这里的int型被转成了str型，比如"1"对应的就是枚举值文档中的1），详见KeyBoardType枚举
        【isDown: str】 是否按下，按下为1，弹起为0
        """

    def OnPlayerStopMove(self):
        """
        移动按钮按下释放时触发事件，同时按下多个方向键，需要释放所有的方向键才会触发事件。
        -----------------------------------------------------------
        无参数
        """

    def OnPlayerStartMove(self):
        """
        移动按钮按下触发事件，在按住一个方向键的同时，去按另外一个方向键，不会触发第二次。
        -----------------------------------------------------------
        无参数
        """

    def OnBackButtonRelease(self, args):
        """
        返回按钮（目前特指安卓系统导航中的返回按钮）松开时触发。
        -----------------------------------------------------------
        无参数
        """

    def OnMouseWheel(self, args):
        """
        鼠标滚轮滚动时触发。
        -----------------------------------------------------------
        【direction: int】 1为向上滚动，0为向下滚动
        """

    def OnLeftClickRelease(self, args):
        """
        玩家松开鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。
        -----------------------------------------------------------
        无参数
        """

    def OnLeftClickBefore(self, args):
        """
        玩家按下鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。
        -----------------------------------------------------------
        【$cancel: bool】 设置为True可拦截原版的挖方块或攻击响应
        """

    def OnHoldBefore(self, args):
        """
        玩家长按屏幕，即将响应到游戏内时触发。
        仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用RightClickBeforeClientEvent事件监听鼠标右键。
        玩家长按屏幕的处理顺序为：
        1. 玩家点击屏幕，在长按判定时间内（默认为400毫秒，可通过SetHoldTimeThreshold接口修改）一直没有进行拖动或松手；
        2. 触发该事件；
        3. 若事件没有cancel，则根据主手上的物品，准心处的物体类型以及与玩家的距离，进行挖方块/使用物品/与实体交互等操作。
        即该事件只会在到达长按判定时间的瞬间触发一次，后面一直按住不会连续触发，可以使用TapOrHoldReleaseClientEvent监听长按后松手。
        与TapBeforeClientEvent事件类似，被ui层捕获，没有穿透到世界的点击不会触发该事件。
        -----------------------------------------------------------
        【$cancel: bool】 设置为True可拦截原版的挖方块/使用物品/与实体交互响应
        """

    def OnGetEntityByCoordRelease(self, args):
        """
        玩家点击屏幕后松开时触发，多个手指点在屏幕上时，只有最后一个手指松开时触发。
        -----------------------------------------------------------
        【x: int】 手指点击位置x坐标
        【y: int】 手指点击位置y坐标
        """

    def OnGetEntityByCoord(self, args):
        """
        玩家点击屏幕时触发，多个手指点在屏幕上时，只有第一个会触发。
        -----------------------------------------------------------
        无参数
        """

    def OnJumpButtonRelease(self, args):
        """
        跳跃按钮按下释放事件。
        -----------------------------------------------------------
        无参数
        """

    def OnJumpButtonPressDown(self, args):
        """
        跳跃按钮按下事件，返回值设置参数只对当次按下事件起作用。
        -----------------------------------------------------------
        【$continueJump: bool】 设置是否执行跳跃逻辑
        """

    def OnPlaySound(self, args):
        """
        播放场景音效或UI音效时触发。
        -----------------------------------------------------------
        【name: str】 即资源包中sounds/sound_definitions.json中的key
        【pos: Tuple[float, float, float]】 音效播放的位置，UI音效为(0,0,0)
        【volume: float】 音量，范围为0-1
        【pitch: float】 播放速度，正常速度为1
        【$cancel: bool】 设为True可屏蔽该次音效播放
        """

    def OnPlayMusic(self, args):
        """
        播放背景音乐时触发。
        -----------------------------------------------------------
        【name: str】 即资源包中sounds/music_definitions.json中的event_name，并且对应sounds/sound_definitions.json中的key
        【$cancel: bool】 设为True可屏蔽该次音效播放
        """

    def OnMusicStop(self, args):
        """
        音乐停止时，当玩家调用StopCustomMusic来停止自定义背景音乐时，会触发该事件。
        -----------------------------------------------------------
        【musicName: str】 音乐名称
        """

    def OnScreenSizeChanged(self, args):
        """
        改变屏幕大小时会触发的事件。
        该事件仅支持PC。
        -----------------------------------------------------------
        【beforeX: float】 屏幕大小改变前的宽度
        【beforeY: float】 屏幕大小改变前的高度
        【afterX: float】 屏幕大小改变后的宽度
        【afterY: float】 屏幕大小改变后的高度
        """

    def OnPushScreen(self, args):
        """
        screen创建触发。
        -----------------------------------------------------------
        【screenName: str】 UI名字
        """

    def OnPopScreen(self, args):
        """
        screen移除触发。
        -----------------------------------------------------------
        【screenName: str】 UI名字
        """

    def OnPlayerChatButtonClick(self, args):
        """
        玩家点击聊天按钮或回车键触发呼出聊天窗口时客户端抛出的事件。
        -----------------------------------------------------------
        无参数
        """

    def OnItemSlotButtonClicked(self, args):
        """
        点击快捷栏和背包栏的物品槽时触发。
        -----------------------------------------------------------
        【slotIndex: int】 点击的物品槽的编号
        """

    def OnGridComponentSizeChanged(self, args):
        """
        UI grid组件里格子数目发生变化时触发。
        -----------------------------------------------------------
        无参数
        """

    def OnPlayerInventoryOpen(self, args):
        """
        打开物品背包界面时触发。
        -----------------------------------------------------------
        【isCreative: bool】 是否是创造模式背包界面
        【$cancel: bool】 是否取消打开物品背包界面。
        """

    def OnPlayerInventoryClose(self, args):
        """
        关闭物品背包界面时触发。
        -----------------------------------------------------------
        无参数
        """

    def OnChestOpen(self, args):
        """
        打开箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【x: int】 箱子x坐标
        【y: int】 箱子y坐标
        【z: int】 箱子z坐标
        """

    def OnChestClose(self, args):
        """
        关闭箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子。
        -----------------------------------------------------------
        无参数
        """

    def OnWalkAnimEnd(self, args):
        """
        走路动作结束时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnWalkAnimBegin(self, args):
        """
        走路动作开始时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnAttackAnimEnd(self, args):
        """
        攻击动作结束时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnAttackAnimBegin(self, args):
        """
        攻击动作开始时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnStopUsingItem(self, args):
        """
        玩家停止使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        """

    def OnStartUsingItem(self, args):
        """
        玩家使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        """

    def OnPlayerTryDropItem(self, args):
        """
        玩家丢弃物品时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        【$cancel: bool】 是否取消此次操作
        """

    def OnCarriedNewItemChanged(self, args):
        """
        手持物品发生变化时，触发该事件；数量改变不会通知。
        -----------------------------------------------------------
        【itemDict: dict】 切换后的物品信息字典
        """

    def OnItemReleaseUsing(self, args):
        """
        释放正在使用的物品时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【durationLeft: float】 蓄力剩余时间（当物品缺少"minecraft:maxduration"组件时，蓄力剩余时间为负数）
        【itemDict: dict】 物品信息字典
        【maxUseDuration: int】 最大蓄力时长
        【$cancel: bool】 设置为True可以取消，需要同时取消服务端事件ItemReleaseUsingServerEvent
        """

    def OnInventoryItemChanged(self, args):
        """
        玩家背包物品变化时客户端抛出的事件。
        如果槽位变空，变化后槽位中物品为空气。
        触发时槽位物品仍为变化前物品。
        背包内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【slot: int】 背包槽位
        【oldItemDict: dict】 变化前槽位中的物品信息字典
        【newItemDict: dict】 变化后槽位中的物品信息字典
        """

    def OnGrindStoneRemovedEnchant(self, args):
        """
        玩家点击砂轮合成得到的物品时抛出的事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【oldItemDict: dict】 合成前的物品物品信息字典（砂轮内第一个物品）
        【additionalItemDict: dict】 作为合成材料的物品物品信息字典（砂轮内第二个物品）
        【newItemDict: dict】 合成后的物品物品信息字典
        【exp: int】 本次合成返还的经验
        """

    def OnShapedRecipeTriggered(self, args):
        """
        玩家合成物品时触发。
        -----------------------------------------------------------
        【recipeId: str】 配方ID，对应配方json文件中的identifier字段
        """

    def OnItemUseOn(self, args):
        """
        *tick*
        玩家在对方块使用物品时客户端抛出的事件。
        注：如果需要取消物品的使用需要同时在ClientItemUseOnEvent和ServerItemUseOnEvent中将ret设置为True才能正确取消。
        该事件仅在鼠标模式下为帧事件。
        -----------------------------------------------------------
        【entityId: str】 玩家实体ID
        【itemDict: dict】 物品信息字典
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【blockAuxValue: int】 方块的附加值
        【face: int】 点击方块的面，参考Facing枚举
        【clickX: float】 点击点的x比例位置
        【clickY: float】 点击点的y比例位置
        【clickZ: float】 点击点的z比例位置
        【$ret: bool】 设为True可取消物品的使用
        """

    def OnItemTryUse(self, args):
        """
        玩家点击右键尝试使用物品时客户端抛出的事件，可以通过设置cancel为True取消使用物品。
        注：如果需要取消物品的使用需要同时在ClientItemTryUseEvent和ServerItemTryUseEvent中将cancel设置为True才能正确取消。
        ServerItemTryUseEvent/ClientItemTryUseEvent不能取消对方块使用物品的行为，如使用生物蛋，使用桶倒出/收集，使用打火石点燃草等；
        如果想要取消这种行为，请使用ClientItemUseOnEvent和ServerItemUseOnEvent。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        【$cancel: bool】 是否取消使用物品
        """

    def OnAnvilCreateResultItemAfter(self, args):
        """
        玩家点击铁砧合成得到的物品时抛出的事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemShowName: str】 合成后的物品显示名称
        【itemDict: dict】 合成后的物品的物品信息字典
        【oldItemDict: dict】 合成前的物品的物品信息字典（铁砧内第一个物品）
        【materialItemDict: dict】 合成所使用材料的物品信息字典（铁砧内第二个物品）
        """

    def OnActorUseItem(self, args):
        """
        玩家使用物品时客户端抛出的事件（比较特殊不走该事件的例子：1.喝牛奶；2.染料对有水的炼药锅使用；3.盔甲架装备盔甲）。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        【useMethod: int】 使用物品的方法，详见ItemUseMethodEnum枚举
        """

    def OnActorAcquiredItem(self, args):
        """
        玩家获得物品时客户端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点）。
        -----------------------------------------------------------
        【actor: str】 获得物品玩家实体ID
        【secondaryActor: str】 物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
        【itemDict: dict】 获取到的物品的物品信息字典
        【acquireMethod: int】 获得物品的方法，详见ItemAcquisitionMethod
        """

    def OnStepOnBlock(self, args):
        """
        实体刚移动至一个新实心方块时触发。
        在合并微软更新之后，本事件触发时机与微软molang实验性玩法组件"minecraft:on_step_on"一致。
        压力板与绊线钩在过去的版本的事件是可以触发的，但在更新后这种非实心方块并不会触发，有需要的可以使用OnEntityInsideBlockClientEvent事件。
        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关，原版方块需要先通过RegisterOnStepOn接口注册才能触发。
        原版的红石矿默认注册了，但深层红石矿没有默认注册。
        如果需要修改cancel，强烈建议配合服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        -----------------------------------------------------------
        【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止触发后续原版逻辑
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【entityId: str】 实体ID
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        -----------------------------------------------------------
        【相关接口】
        BlockInfoComponentClient.RegisterOnStepOn(blockName: str, sendPythonEvent: bool) -> bool
        BlockInfoComponentClient.UnRegisterOnStepOn(blockName: str) -> bool
        """

    def OnStartDestroyBlock(self, args):
        """
        玩家开始挖方块时触发。创造模式下不触发。
        如果是隔着火焰挖方块，即使将该事件cancel掉，火焰也会被扑灭。如果要阻止火焰扑灭，需要配合ExtinguishFireClientEvent使用。
        -----------------------------------------------------------
        【pos: Tuple[float, float, float]】 方块的坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        【playerId: str】 玩家的实体ID
        【$cancel: bool】 修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockServerEvent一起修改。
        """

    def OnStepOffBlock(self, args):
        """
        实体移动离开一个实心方块时触发。
        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关，原版方块需要先通过RegisterOnStepOff接口注册才能触发。
        压力板与绊线钩这种非实心方块不会触发。
        -----------------------------------------------------------
        【blockX: int】 方块位置x
        【blockY: int】 方块位置y
        【blockZ: int】 方块位置z
        【entityId: str】 实体ID
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        -----------------------------------------------------------
        【相关接口】
        BlockInfoComponentClient.RegisterOnStepOff(blockName: str, sendPythonEvent: bool) -> bool
        BlockInfoComponentClient.UnRegisterOnStepOff(blockName: str) -> bool
        """

    def OnShearsDestoryBlockBefore(self, args):
        """
        玩家手持剪刀破坏方块时，有剪刀特殊效果的方块会在客户端线程触发该事件。
        目前仅绊线会触发，需要取消剪刀效果得配合ShearsDestoryBlockBeforeServerEvent同时使用。
        -----------------------------------------------------------
        【blockX: int】 方块位置x
        【blockY: int】 方块位置y
        【blockZ: int】 方块位置z
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxData: int】 方块附加值
        【dropName: str】 触发剪刀效果的掉落物identifier，包含命名空间及名称
        【dropCount: int】 触发剪刀效果的掉落物数量
        【playerId: str】 触发剪刀效果的玩家ID
        【dimensionId: int】 玩家触发时的维度ID
        【$cancelShears: bool】 是否取消剪刀效果
        """

    def OnPlayerTryDestroyBlock(self, args):
        """
        当玩家即将破坏方块时，客户端线程触发该事件。
        主要用于床，旗帜，箱子这些根据方块实体数据进行渲染的方块，一般情况下请使用ServerPlayerTryDestroyBlockEvent。
        -----------------------------------------------------------
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【face: int】 方块被敲击的面向ID，参考Facing枚举
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxData: int】 方块附加值
        【playerId: str】 试图破坏方块的玩家的实体ID
        【$cancel: bool】 默认为False，在脚本层设置为True就能取消该方块的破坏
        """

    def OnStandOnBlock(self, args):
        """
        *tick*
        当实体站立到方块上时客户端持续触发。
        不是所有方块都会触发该事件，需要在json中先配置触发开关，原版方块需要先通过RegisterOnStandOn接口注册才能触发.
        如果要在脚本层修改motion/cancel，强烈建议配合OnStandOnBlockServerEvent服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        如果要在脚本层修改motion，回传的一定要是浮点型，例如需要赋值0.0而不是0。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【dimensionId: int】 实体所在维度ID
        【posX: float】 实体位置x
        【posY: float】 实体位置y
        【posZ: float】 实体位置z
        【$motionX: float】 瞬时移动x方向的力
        【$motionY: float】 瞬时移动y方向的力
        【$motionZ: float】 瞬时移动z方向的力
        【blockX: int】 方块位置x
        【blockY: int】 方块位置y
        【blockZ: int】 方块位置z
        【blockName: str】 方块的identifier，包含命名空间及名称
        【$cancel: bool】 可由脚本层回传True给引擎，阻止触发后续原版逻辑
        -----------------------------------------------------------
        【相关接口】
        BlockInfoComponentClient.RegisterOnStandOn(blockName: str, sendPythonEvent: bool) -> bool
        BlockInfoComponentClient.UnRegisterOnStandOn(blockName: str) -> bool
        """

    def OnModBlockNeteaseEffectCreated(self, args):
        """
        自定义方块实体绑定的特效创建成功事件。
        以及使用接口CreateFrameEffectForBlockEntity或CreateParticleEffectForBlockEntity为自定义方块实体添加特效成功时触发。
        -----------------------------------------------------------
        【effectName: str】 创建成功的特效的自定义键值名称
        【id: int】 该特效的ID
        【effectType: int】 该特效的类型，0为粒子特效，1为序列帧特效
        【blockPos: Tuple[float, float, float]】 该特效绑定的自定义方块实体的世界坐标
        """

    def OnEntityInsideBlock(self, args):
        """
        *tick*
        当实体碰撞盒所在区域有方块时，客户端持续触发。
        不是所有方块都会触发该事件，需要在json中先配置触发开关，原版方块需要先通过RegisterOnEntityInside接口注册才能触发。
        如果需要修改slowdownMulti/cancel，强烈建议与服务端事件同步修改，避免出现被服务端矫正等非预期现象。
        如果要在脚本层修改slowdownMulti，回传的一定要是浮点型，例如需要赋值1.0而不是1。
        有任意slowdownMulti参数被传回非0值时生效减速比例。
        slowdownMulti参数更像是一个Buff，并不是立刻计算，而是先保存在实体属性里延后计算、在已经有slowdownMulti属性的情况下会取最低的值、免疫掉落伤害等，与原版蜘蛛网逻辑基本一致。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【dimensionId: int】 实体所在维度ID
        【$slowdownMultiX: float】 实体移速x方向的减速比例
        【$slowdownMultiY: float】 实体移速y方向的减速比例
        【$slowdownMultiZ: float】 实体移速z方向的减速比例
        【blockX: int】 方块位置x
        【blockY: int】 方块位置y
        【blockZ: int】 方块位置z
        【blockName: str】 方块的identifier，包含命名空间及名称
        【$cancel: bool】 可由脚本层回传True给引擎，阻止触发后续原版逻辑
        -----------------------------------------------------------
        【相关接口】
        BlockInfoComponentClient.RegisterOnEntityInside(blockName: str, sendPythonEvent: bool) -> bool
        BlockInfoComponentClient.UnRegisterOnEntityInside(blockName: str) -> bool
        """

    def OnAfterFallOnBlock(self, args):
        """
        *tick*
        当实体降落到方块后客户端触发，主要用于力的计算。
        不是所有方块都会触发该事件，需要在json中先配置触发开关。
        如果要在脚本层修改motion，回传的需要是浮点型，例如需要赋值0.0而不是0。
        如果需要修改实体的力，最好配合服务端事件同步修改，避免产生非预期现象。
        因为引擎最后一定会按照原版方块规则计算力（普通方块置0，床、粘液块等反弹），所以脚本层如果想直接修改当前力需要将calculate设为True取消原版计算，按照传回值计算。
        引擎在落地之后OnAfterFallOnBlockClientEvent会一直触发，因此请在脚本层中做对应的逻辑判断。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【posX: float】 实体位置x
        【posY: float】 实体位置y
        【posZ: float】 实体位置z
        【$motionX: float】 瞬时移动x方向的力
        【$motionY: float】 瞬时移动y方向的力
        【$motionZ: float】 瞬时移动z方向的力
        【blockName: str】 方块的identifier，包含命名空间及名称
        【$calculate: bool】 是否按脚本层传值计算力
        """

    def OnFallingBlockCauseDamageBefore(self, args):
        """
        当下落的方块开始计算砸到实体的伤害时，客户端触发该事件。
        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关。
        当该事件的参数数据与服务端事件FallingBlockCauseDamageBeforeServerEvent数据有差异时，请以服务端事件数据为准。
        -----------------------------------------------------------
        【fallingBlockId: str】 下落的方块实体ID
        【fallingBlockX: float】 下落的方块实体位置x
        【fallingBlockY: float】 下落的方块实体位置y
        【fallingBlockZ: float】 下落的方块实体位置z
        【blockName: str】 重力方块的identifier，包含命名空间及名称
        【dimensionId: int】 下落的方块实体维度ID
        【collidingEntitys: Optional[List[str]]】 当前碰撞到的实体ID列表（客户端只能获取到玩家），如果没有的话是None
        【fallTickAmount: int】 下落的方块实体持续下落了多少tick
        【fallDistance: float】 下落的方块实体持续下落了多少距离
        【isHarmful: bool】 客户端始终为false，因为客户端不会计算伤害值
        【fallDamage: int】 对实体的伤害
        """
        # print args['fallingBlockId']

    def OnBlockUse(self, args):
        """
        *tick*
        玩家右键点击新版自定义方块（或者通过接口AddBlockItemListenForUseEvent增加监听的MC原生游戏方块）时客户端抛出该事件。
        有的方块是在ServerBlockUseEvent中设置cancel生效，但是有部分方块是在ClientBlockUseEvent中设置cancel才生效，如有需求建议在两个事件中同时设置cancel以保证生效。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【blockName: str】 方块的identifier，包含命名空间及名称
        【aux: int】 方块附加值
        【$cancel: bool】 设置为True可拦截与方块交互的逻辑
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        """

    def OnPerspChange(self, args):
        """
        视角切换时会触发的事件。
        视角数字代表含义 0: 第一人称 1: 第三人称背面 2: 第三人称正面。
        -----------------------------------------------------------
        【from: int】 切换前的视角
        【to: int】 切换后的视角
        """

    def OnPlayerHitBlock(self, args):
        """
        通过OpenPlayerHitBlockDetection打开方块碰撞检测后，当玩家碰撞到方块时触发该事件。
        玩家着地时会触发OnGroundClientEvent，而不是该事件。
        客户端和服务端分别作碰撞检测，可能两个事件返回的结果略有差异。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【posX: int】 碰撞方块x坐标
        【posY: int】 碰撞方块y坐标
        【posZ: int】 碰撞方块z坐标
        【blockId: str】 碰撞方块的identifier
        【auxValue: int】 碰撞方块的附加值
        -----------------------------------------------------------
        【相关接口】
        PlayerCompClient.OpenPlayerHitBlockDetection(precision: float) -> bool
        PlayerCompClient.ClosePlayerHitBlockDetection() -> bool
        """

    def OnGameTypeChanged(self, args):
        """
        个人游戏模式发生变化时客户端触发。
        游戏模式：生存，创造，冒险分别为0~2。
        默认游戏模式发生变化时最后反映在个人游戏模式之上。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【oldGameType: int】 切换前的游戏模式
        【newGameType: int】 切换后的游戏模式
        """

    def OnExtinguishFire(self, args):
        """
        玩家扑灭火焰时触发。下雨，倒水等方式熄灭火焰不会触发。
        -----------------------------------------------------------
        【pos: Tuple[float, float, float]】 火焰方块的坐标
        【playerId: str】 玩家的实体ID
        【$cancel: bool】 修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireServerEvent一起修改。
        """

    def OnDimensionChangeFinish(self, args):
        """
        玩家维度改变完成后触发。
        当通过传送门从末地回到主世界时，toPos的y值为32767，其他情况一般会比设置值高1.62
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【fromDimensionId: int】 维度改变前的维度
        【toDimensionId: int】 维度改变后的维度
        【toPos: Tuple[float, float, float]】 改变后的位置(x,y,z)，其中y值为脚底加上角色的身高值
        """

    def OnDimensionChange(self, args):
        """
        玩家维度改变时触发。
        当通过传送门从末地回到主世界时，toY值为32767，其他情况一般会比设置值高1.62
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【fromDimensionId: int】 维度改变前的维度
        【toDimensionId: int】 维度改变后的维度
        【fromX: float】 改变前的位置x
        【fromY: float】 改变前的位置y
        【fromZ: float】 改变前的位置z
        【toX: float】 改变后的位置x
        【toY: float】 改变后的位置y
        【toZ: float】 改变后的位置z
        """

    def OnCameraMotionStop(self, args):
        """
        相机运动器停止事件。相机添加运动器并开始运行后，运动器自动停止时触发。
        注意：该事件触发表示运动器播放顺利完成，手动调用的StopCameraMotion、RemoveCameraMotion不会触发该事件。
        -----------------------------------------------------------
        【motionId: int】 运动器ID
        【$remove: bool】 是否移除该运动器，设置为False则保留，默认为True，即运动器停止后自动移除
        """

    def OnCameraMotionStart(self, args):
        """
        相机运动器开始事件。相机添加运动器后，运动器开始运行时触发。
        -----------------------------------------------------------
        【motionId: int】 运动器ID
        """

    def OnLeaveEntity(self, args):
        """
        玩家远离生物时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【entityId: str】 远离的生物的实体ID
        """

    def OnStartRiding(self, args):
        """
        一个实体即将骑乘另外一个实体时触发。
        如果需要修改cancel，请通过服务端事件StartRidingServerEvent修改，客户端触发该事件时，实体已经骑乘成功。
        -----------------------------------------------------------
        【actorId: str】 骑乘者的实体ID
        【victimId: str】 被骑乘者的实体ID
        """

    def OnMobHitMob(self, args):
        """
        通过OpenPlayerHitMobDetection打开生物碰撞检测后，当生物间（包含玩家）碰撞时触发该事件。
        注：客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。
        本事件代替原有的OnPlayerHitMobClientEvent事件。
        -----------------------------------------------------------
        【mobId: str】 当前生物的实体ID
        【hittedMobList: List[str]】 当前生物碰撞到的其他所有生物的实体ID的list
        -----------------------------------------------------------
        【相关接口】
        PlayerCompClient.OpenPlayerHitMobDetection() -> bool
        PlayerCompClient.ClosePlayerHitMobDetection() -> bool
        """

    def OnGround(self, args):
        """
        实体着地事件。玩家，沙子，铁砧，掉落的物品，点燃的TNT掉落地面时触发，其余实体着地不触发。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnHealthChange(self, args):
        """
        生物生命值发生变化时触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【from: float】 变化前的生命值
        【to: float】 变化后的生命值
        """

    def OnEntityStopRiding(self, args):
        """
        当实体停止骑乘时触发。
        以下情况不允许取消：
        1. 玩家传送时；
        2. 坐骑死亡时；
        3. 玩家睡觉时；
        4. 玩家死亡时；
        5. 未驯服的马；
        6. 怕水的生物坐骑进入水里；
        7. 切换维度；
        8. ride组件StopEntityRiding接口。
        -----------------------------------------------------------
        【id: str】 实体ID
        【rideId: str】 坐骑的实体ID
        【exitFromRider: bool】 是否下坐骑
        【entityIsBeingDestroyed: bool】 坐骑是否将要销毁
        【switchingRides: bool】 是否换乘坐骑
        【$cancel: bool】 设置为True可以取消（需要与服务端事件一同取消）
        """

    def OnEntityModelChanged(self, args):
        """
        实体模型切换时触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【newModel: str】 新的模型名字
        【oldModel: str】 旧的模型名字
        """

    def OnApproachEntity(self, args):
        """
        玩家靠近生物时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【entityId: str】 靠近的生物的实体ID
        """
    
    def OnUnLoadClientAddonScriptsBefore(self, args):
        """
        客户端卸载mod之前触发。
        -----------------------------------------------------------
        无参数
        """

    def OnRemovePlayerAOI(self, args):
        """
        玩家离开当前玩家同一个区块时触发AOI事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def OnRemoveEntity(self, args):
        """
        客户端侧实体被移除时触发。
        客户端接收服务端AOI事件时触发，原事件名 RemoveEntityPacketEvent。
        -----------------------------------------------------------
        【id: str】 移除的实体ID
        """

    def OnLocalPlayerStopLoading(self, args):
        """
        玩家进入存档，出生点地形加载完成时触发。该事件触发时可以进行切换维度的操作。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def OnCommandOutput(self, args):
        """
        当command命令有成功消息输出时触发。
        部分命令在返回的时候没有命令名称，命令组件需要showOutput参数为True时才会有返回。
        -----------------------------------------------------------
        【command: str】 命令名称
        【message: str】 命令返回的消息
        """

    def OnLoadClientAddonScriptsAfter(self, args):
        """
        客户端加载mod完成事件。
        -----------------------------------------------------------
        无参数
        """

    def OnChunkLoaded(self, args):
        """
        客户端区块加载完成时触发。
        -----------------------------------------------------------
        【dimension: int】 区块所在维度
        【chunkPosX: int】 区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
        【chunkPosZ: int】 区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]
        """

    def OnChunkAcquireDiscarded(self, args):
        """
        客户端区块即将被卸载时触发。
        区块卸载：游戏只会加载玩家周围的区块，玩家移动到别的区域时，原来所在区域的区块会被卸载。
        -----------------------------------------------------------
        【dimension: int】 区块所在维度
        【chunkPosX: int】 区块的x坐标，对应方块x坐标区间为[x*16, x*16 + 15]
        【chunkPosZ: int】 区块的z坐标，对应方块z坐标区间为[z*16, z*16 + 15]
        """

    def OnAddPlayerCreated(self, args):
        """
        玩家进入当前玩家所在的区块AOI后，玩家皮肤数据异步加载完成后触发的事件。
        由于玩家皮肤是异步加载的原因，该事件触发时机比AddPlayerAOIClientEvent晚，触发该事件后可以对该玩家调用相关玩家渲染接口。
        当前客户端每加载好一个玩家的皮肤，就会触发一次该事件，比如刚进入世界时，本地玩家加载好会触发一次，周围的所有玩家加载好后也会分别触发一次。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def OnAddPlayerAOI(self, args):
        """
        玩家加入游戏或者其余玩家进入当前玩家所在的区块时触发的AOI事件，替换AddPlayerEvent。
        该事件触发只表明在服务端数据中接收到了新玩家，并不能代表此时玩家在客户端中可见，若想在玩家进入AOI后立马调用玩家渲染相关接口，建议使用AddPlayerCreatedClientEvent。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def OnAddEntity(self, args):
        """
        客户端侧创建新实体时触发。
        创建玩家时不会触发该事件。
        -----------------------------------------------------------
        【id: str】 实体ID
        【posX: float】 位置x
        【posY: float】 位置y
        【posZ: float】 位置z
        【dimensionId: int】 实体维度
        【isBaby: bool】 是否为幼儿
        【engineTypeStr: str】 实体类型
        【itemName: str】 物品identifier（仅当物品实体时存在该字段）
        【auxValue: int】 物品附加值（仅当物品实体时存在该字段）
        """

    def OnScriptTick(self):
        """
        *tick*
        客户端tick事件，1秒30次。
        -----------------------------------------------------------
        无参数
        """

    def OnUiInitFinished(self, args):
        """
        UI初始化框架完成，此时可以创建UI。
        切换维度后会重新初始化UI并触发该事件。
        -----------------------------------------------------------
        无参数
        """

    # todo:==================================== Custom Event Callback ==================================================

    def OnGameTick(self):
        """
        *tick*
        频率与游戏实时帧率同步的Tick事件。比如游戏当前帧率为60帧，则该事件每秒触发60次。
        需要注意的是，因为受游戏帧率影响，该事件的触发帧率并不稳定。
        如果没有特殊需求，建议使用OnScriptTick。
        -----------------------------------------------------------
        无参数
        """

    # todo:======================================= Basic Function ======================================================

    def SetQueryVar(self, entityId, name, value, sync=True):
        """
        设置指定实体query.mod变量的值，支持全局同步（即所有客户端同步设置该变量的值）。
        若不进行全局同步，则本次设置只对当前客户端有效。
        若设置的变量未注册，则自动进行注册。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【name: str】 变量名
        【value: float】 设置的值
        【sync: bool = True】 是否进行全局同步
        -----------------------------------------------------------
        NoReturn
        """
        if sync:
            self.BroadcastToAllClient("_SetQueryVar", {'entityId': entityId, 'name': name, 'value': value})
        else:
            self._setQuery({'entityId': entityId, 'name': name, 'value': value})

    def AddPlayerRenderResources(self, playerId, *resTuple):
        # type: (str, *tuple[str, str]) -> tuple[bool, ...]
        """
        一键添加玩家渲染资源，包括模型、贴图、材质、渲染控制器、动画、动画控制器、音效和粒子特效。
        注意：如需添加音效，音效名称必须至少包含一个“.”，如“sound.abc”，否则本接口将无法识别。
        -----------------------------------------------------------
        【playerId: str】 玩家实体ID
        【*resTuple: Tuple[str, str]】 可变位置参数，渲染资源元组，格式详见示例
        -----------------------------------------------------------
        return: Tuple[bool, ...] -> 返回添加结果的元组，每个元素为一个bool，与传入的resTuple参数相对应
        -----------------------------------------------------------
        示例：
        self.AddPlayerRenderResources(
            playerId,
            ("my_geo", "geometry.abc"),     # 模型：(Key, 模型名称)
            ("my_tex", "textures/entity/abc"),     # 贴图：(Key, 贴图所在路径)
            ("my_mat", "abc"),     # 材质：(Key, 材质名称)
            ("controller.render.abc", "1.0"),     # 渲染控制器：(渲染控制器名称, 生效条件)
            ("my_anim", "animation.abc"),     # 动画：(Key, 动画名称)
            ("my_ctrler", "controller.animation.abc"),     # 动画控制器：(Key, 动画控制器名称)
            ("my_sound", "my_sound.abc"),     # 音效：(Key, 音效名称)
            ("my_eff", "nuoyan:my_particle"),     # 粒子特效：(Key, 粒子特效名称)
        )
        """
        res = []
        comp = _CompFactory.CreateActorRender(playerId)
        for arg in resTuple:
            if arg[1].startswith("geometry."):
                res.append(comp.AddPlayerGeometry(*arg))
            elif arg[1].startswith("textures/"):
                res.append(comp.AddPlayerTexture(*arg))
            elif arg[0].startswith("controller.render."):
                res.append(comp.AddPlayerRenderController(*arg))
            elif arg[1].startswith("animation."):
                res.append(comp.AddPlayerAnimation(*arg))
            elif arg[1].startswith("controller.animation."):
                res.append(comp.AddPlayerAnimationController(*arg))
            elif ":" in arg[1]:
                res.append(comp.AddPlayerParticleEffect(*arg))
            elif "." in arg[1]:
                res.append(comp.AddPlayerSoundEffect(*arg))
            else:
                res.append(comp.AddPlayerRenderMaterial(*arg))
        comp.RebuildPlayerRender()
        return tuple(res)

    def CallServer(self, name, callback=None, *args):
        # type: (str, _Callable[[...], None] | None, ...) -> None
        """
        调用服务端属性（包括变量和函数）。
        -----------------------------------------------------------
        【name: str】 服务端属性名
        【callback: Optional[(Any) -> None] = None】 回调函数，调用服务端成功后服务端会返回结果并调用该函数，该函数接受一个参数，即调用结果，具体用法请看示例
        【*args: Any】 调用参数；如果调用的服务端属性为变量，则args会赋值给该变量（不写调用参数则不会进行赋值）；如果调用的服务端属性为函数，则args会作为参数传入该函数
        -----------------------------------------------------------
        NoReturn
        -----------------------------------------------------------
        示例：

        """

    # def TestMode(self, enable):
    #     # type: (bool) -> None
    #     """
    #     开启或关闭客户端测试模式。
    #     内容包括：
    #     1. 显示准星处生物或方块的信息；
    #     2. 显示手持物品信息；
    #     3. 显示玩家当前运动速度。
    #     -----------------------------------------------------------
    #     【enable: bool】 是否开启
    #     -----------------------------------------------------------
    #     NoReturn
    #     """
    #     if self.__timer:
    #         self.__timer.Destroy()
    #         self.__timer = None
    #     if enable:
    #         @_ClientTimer.Repeat(1)
    #         def func():
    #             carried = _PlayerItemComp.GetCarriedItem()
    #             if carried:
    #                 text = "carried: %s:%d" % (carried['newItemName'], carried['newAuxValue'])
    #             else:
    #                 text = "carried: None"
    #             facing = _PlayerCameraComp.PickFacing()
    #             if facing and facing['type'] != "None":
    #                 text += "\n" + "-" * 30
    #                 text += "\ntype: %s" % facing['type']
    #                 if 'entityId' in facing:
    #                     entityId = facing['entityId']
    #                     pos = _CompFactory.CreatePos(entityId).GetFootPos()
    #                     text += "\nentityId: " + entityId
    #                     text += "\ntypeStr: " + _CompFactory.CreateEngineType(entityId).GetEngineTypeStr()
    #                 else:
    #                     pos = facing['x'], facing['y'], facing['z']
    #                     blockInfo = _LevelBlockInfoComp.GetBlock(pos)
    #                     text += "\nblock: %s:%d" % blockInfo
    #                 text += "\npos: (%d, %d, %d)" % pos
    #             text += "\n" + "-" * 30
    #             pos = _PlayerPosComp.GetFootPos()
    #             speed = _pos_distance(self.__lastPos, pos) if self.__lastPos else 0.0
    #             self.__lastPos = pos
    #             text += "\nspeed: {:.2f}".format(speed)
    #             _LevelGameComp.SetTipMessage(text)
    #         self.__timer = func()

    def BroadcastToAllClient(self, eventName, eventData):
        # type: (str, ...) -> None
        """
        广播事件到所有玩家的客户端。
        注：因为全局广播要经过服务端，所以监听事件时监听的是服务端而不是客户端。
        若传递的数据为字典，则客户端接收到的字典会内置一个key：__id__，其value为发送广播的玩家实体ID
        -----------------------------------------------------------
        【eventName: str】 事件名称
        【eventData: Any】 数据
        -----------------------------------------------------------
        NoReturn
        -----------------------------------------------------------
        示例：
        self.BroadcastToAllClient("MyEvent", {'num': 123})
        def func(self, args):
            print args     # {'num': 123, '__id__': "..."}
        self.ListenForEvent(serverNamespace, serverSystemName, "MyEvent", self, self.func)
        """
        self.NotifyToServer("_BroadcastToAllClient", {
            'eventName': eventName,
            'eventData': eventData,
        })

    def ListenForEventV2(self, eventName, callback, t=0, namespace="", systemName="", priority=0):
        # type: (str, _MethodType, int, str, str, int) -> None
        """
        监听事件（简化版）。
        -----------------------------------------------------------
        【eventName: str】 事件名称
        【callback: Method】 回调函数（方法）
        【t: int = 0】 0表示监听当前Mod服务端传来的自定义事件，1表示监听客户端引擎事件，2表示监听其他Mod的事件
        【namespace: str = ""】 其他Mod的命名空间
        【systemName: str = ""】 其他Mod的系统名称
        【priority: int = 0】 优先级
        -----------------------------------------------------------
        NoReturn
        """
        if t == 0:
            namespace = _MOD_NAME
            systemName = _SERVER_SYSTEM_NAME
        elif t == 1:
            namespace = _ENGINE_NAMESPACE
            systemName = _ENGINE_SYSTEM_NAME
        self.ListenForEvent(namespace, systemName, eventName, callback.__self__, callback, priority)

    def RegisterAndCreateUI(self, namespace, clsPath, uiScreenDef, param=None):
        # type: (str, str, str, dict | None) -> _ScreenNode
        """
        注册并创建UI。
        示例：
        self.myUiNode = self.RegisterAndCreateUI(namespace, clsPath, uiScreenDef)
        -----------------------------------------------------------
        【namespace: str】 UI的名称，对应UI的json文件中“namespace”的值
        【clsPath: str】 UI的类路径
        【uiScreenDef: str】 UI画布路径，格式为“namespace.screenName”，screenName对应想打开的画布的名称（一般为main）
        【param: dict = None】 创建UI的参数，会传到UI类的__init__方法中，默认为{'isHud': 1}
        -----------------------------------------------------------
        return: ScreenNode -> UI类实例
        """
        _clientApi.RegisterUI(_MOD_NAME, namespace, clsPath, uiScreenDef)
        if not param:
            param = {
                'isHud': 1,
                '__cs__': self,
            }
        else:
            param['__cs__'] = self
        return _clientApi.CreateUI(_MOD_NAME, namespace, param)

    # todo:====================================== Internal Method ======================================================

    @listen("_SetQueryVar")
    def _setQuery(self, args):
        entityId = args['entityId']
        name = args['name']
        value = args['value']
        comp = _CompFactory.CreateQueryVariable(entityId)
        if comp.Get(name) == -1.0:
            comp.Register(name, 0.0)
        comp.Set(name, value)

    @listen("_ListenServerGameTick")
    def _OnListenServerGameTick(self, args=None):
        if self._uiInitFinished:
            if not self._gameTickNode:
                self._startGameTick()
            self._gameTickNode.notifySv = True
        else:
            self.__handle = 2

    def _listenClientGameTick(self):
        if self._uiInitFinished:
            if not self._gameTickNode:
                self._startGameTick()
            self._gameTickNode.notifyCl = True
        else:
            self.__handle = 1

    @listen("UiInitFinished", 1)
    def _OnUiInitFinished(self, args):
        self.NotifyToServer("UiInitFinished", {})
        self._uiInitFinished = True
        if self.__handle == 1:
            self._listenClientGameTick()
        elif self.__handle == 2:
            self._OnListenServerGameTick()

    @listen("_SetMotion")
    def _OnSetMotion(self, motion):
        _PlayerActorMotionComp.SetMotion(motion)

    def __listen(self):
        for args in _lsnFuncArgs:
            args[1] = getattr(self, args[1])
            self.ListenForEventV2(*args)
        for event, callback in ALL_ENGINE_EVENTS:
            if _is_method_overridden(self.__class__, NuoyanClientSystem, callback):
                self.ListenForEventV2(event, getattr(self, callback), 1)

    def _startGameTick(self):
        self._gameTickNode = self.RegisterAndCreateUI(_UI_NAMESPACE_GAME_TICK, _UI_PATH_GAME_TICK, _UI_DEF_GAME_TICK)

    def _checkOnGameTick(self):
        if _is_method_overridden(self.__class__, NuoyanClientSystem, "OnGameTick"):
            self._listenClientGameTick()


class _GameTick(_ScreenNode):
    def __init__(self, namespace, name, param):
        super(_GameTick, self).__init__(namespace, name, param)
        self.cs = param['__cs__']
        self.notifySv = False
        self.notifyCl = False

    @_ViewBinder.binding(_ViewBinder.BF_BindString, "#main.gametick")
    def OnGameTick(self):
        if self.notifySv:
            self.cs.NotifyToServer("OnGameTick", {})
        if self.notifyCl:
            self.cs.OnGameTick()

























