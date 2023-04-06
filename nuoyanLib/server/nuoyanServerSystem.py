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
#   Last Modified : 2023-04-03
#
# ====================================================


from types import MethodType as _MethodType
from collections import Callable as _Callable
from ..utils.utils import is_method_overridden as _is_method_overridden
from .._config import CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME, MOD_NAME as _MOD_NAME
from serverTimer import ServerTimer as _ServerTimer
import mod.server.extraServerApi as _serverApi


__all__ = [
    "listen",
    "NuoyanServerSystem",
    "ALL_ENGINE_EVENTS",
]


_ENGINE_NAMESPACE = _serverApi.GetEngineNamespace()
_ENGINE_SYSTEM_NAME = _serverApi.GetEngineSystemName()
_LEVEL_ID = _serverApi.GetLevelId()
_ServerSystem = _serverApi.GetServerSystemCls()
_CompFactory = _serverApi.GetEngineCompFactory()
_LevelGameComp = _CompFactory.CreateGame(_LEVEL_ID)


ALL_ENGINE_EVENTS = [
    "OnScriptTickServer",
    "EntityRemoveEvent",
    "OnCarriedNewItemChangedServerEvent",
    "ProjectileDoHitEffectEvent",
    "ExplosionServerEvent",
    "DamageEvent",
    "DestroyBlockEvent",
    "ActorAcquiredItemServerEvent",
    "ActorUseItemServerEvent",
    "ServerItemUseOnEvent",
    "EntityStartRidingEvent",
    "EntityStopRidingEvent",
    "OnEntityInsideBlockServerEvent",
    "OnMobHitBlockServerEvent",
    "AddEntityServerEvent",
    "MobDieEvent",
    "PlayerInteractServerEvent",
    "PlayerDoInteractServerEvent",
    "EntityDefinitionsEventServerEvent",
    "DimensionChangeFinishServerEvent",
    "HealthChangeBeforeServerEvent",
    "ActuallyHurtServerEvent",
    "EntityDieLoottableServerEvent",
    "SpawnProjectileServerEvent",
    "OnGroundServerEvent",
    "ServerBlockUseEvent",
    "ServerSpawnMobEvent",
    "PlayerAttackEntityEvent",
    "AchievementCompleteEvent",
    "AddServerPlayerEvent",
    "ChunkAcquireDiscardedServerEvent",
    "ChunkGeneratedServerEvent",
    "ChunkLoadedServerEvent",
    "ClientLoadAddonsFinishServerEvent",
    "CommandEvent",
    "DelServerPlayerEvent",
    "LoadServerAddonScriptsAfter",
    "NewOnEntityAreaEvent",
    "OnCommandOutputServerEvent",
    "OnContainerFillLoottableServerEvent",
    "OnLightningLevelChangeServerEvent",
    "OnLocalLightningLevelChangeServerEvent",
    "OnLocalRainLevelChangeServerEvent",
    "OnRainLevelChangeServerEvent",
    "PlaceNeteaseStructureFeatureEvent",
    "PlayerIntendLeaveServerEvent",
    "PlayerJoinMessageEvent",
    "PlayerLeftMessageServerEvent",
    "ServerChatEvent",
    "ServerPostBlockPatternEvent",
    "ServerPreBlockPatternEvent",
    "ServerSpawnMobEvent",
    "ActorHurtServerEvent",
    "AddEffectServerEvent",
    "ChangeSwimStateServerEvent",
    "EntityChangeDimensionServerEvent",
    "EntityDroppedItemServerEvent",
    "EntityEffectDamageServerEvent",
    "EntityLoadScriptEvent",
    "EntityMotionStartServerEvent",
    "EntityMotionStopServerEvent",
    "EntityPickupItemServerEvent",
    "EntityTickServerEvent",
    "HealthChangeServerEvent",
    "MobGriefingBlockServerEvent",
    "OnFireHurtEvent",
    "OnKnockBackServerEvent",
    "OnMobHitMobServerEvent",
    "ProjectileCritHitEvent",
    "RefreshEffectServerEvent",
    "RemoveEffectServerEvent",
    "StartRidingServerEvent",
    "WillAddEffectServerEvent",
    "WillTeleportToServerEvent",
    "AddExpEvent",
    "AddLevelEvent",
    "ChangeLevelUpCostServerEvent",
    "DimensionChangeServerEvent",
    "ExtinguishFireServerEvent",
    "GameTypeChangedServerEvent",
    "OnPlayerHitBlockServerEvent",
    "PlayerDieEvent",
    "PlayerEatFoodServerEvent",
    "PlayerHurtEvent",
    "PlayerRespawnEvent",
    "PlayerRespawnFinishServerEvent",
    "PlayerSleepServerEvent",
    "PlayerStopSleepServerEvent",
    "PlayerTeleportEvent",
    "PlayerTrySleepServerEvent",
    "ServerPlayerGetExperienceOrbEvent",
    "StoreBuySuccServerEvent",
    "BlockDestroyByLiquidServerEvent",
    "BlockLiquidStateChangeAfterServerEvent",
    "BlockLiquidStateChangeServerEvent",
    "BlockNeighborChangedServerEvent",
    "BlockRandomTickServerEvent",
    "BlockRemoveServerEvent",
    "BlockSnowStateChangeAfterServerEvent",
    "BlockSnowStateChangeServerEvent",
    "BlockStrengthChangedServerEvent",
    "ChestBlockTryPairWithServerEvent",
    "CommandBlockContainerOpenEvent",
    "CommandBlockUpdateEvent",
    "DirtBlockToGrassBlockServerEvent",
    "EntityPlaceBlockAfterServerEvent",
    "FallingBlockBreakServerEvent",
    "FallingBlockCauseDamageBeforeServerEvent",
    "FallingBlockReturnHeavyBlockServerEvent",
    "FarmBlockToDirtBlockServerEvent",
    "GrassBlockToDirtBlockServerEvent",
    "HeavyBlockStartFallingServerEvent",
    "HopperTryPullInServerEvent",
    "HopperTryPullOutServerEvent",
    "OnAfterFallOnBlockServerEvent",
    "OnBeforeFallOnBlockServerEvent",
    "OnEntityInsideBlockServerEvent",
    "OnStandOnBlockServerEvent",
    "PistonActionServerEvent",
    "ServerBlockEntityTickEvent",
    "ServerEntityTryPlaceBlockEvent",
    "ServerPlaceBlockEntityEvent",
    "ServerPlayerTryDestroyBlockEvent",
    "ShearsDestoryBlockBeforeServerEvent",
    "StartDestroyBlockServerEvent",
    "StepOffBlockServerEvent",
    "StepOnBlockServerEvent",
    "ContainerItemChangedServerEvent",
    "CraftItemOutputChangeServerEvent",
    "FurnaceBurnFinishedServerEvent",
    "InventoryItemChangedServerEvent",
    "ItemReleaseUsingServerEvent",
    "ItemUseAfterServerEvent",
    "ItemUseOnAfterServerEvent",
    "OnItemPutInEnchantingModelServerEvent",
    "OnNewArmorExchangeServerEvent",
    "OnOffhandItemChangedServerEvent",
    "OnPlayerActiveShieldServerEvent",
    "OnPlayerBlockedByShieldAfterServerEvent",
    "OnPlayerBlockedByShieldBeforeServerEvent",
    "PlayerDropItemServerEvent",
    "ServerItemTryUseEvent",
    "ServerPlayerTryTouchEvent",
    "ShearsUseToBlockBeforeServerEvent",
    "UIContainerItemChangedServerEvent",
    "AttackAnimBeginServerEvent",
    "AttackAnimEndServerEvent",
    "JumpAnimBeginServerEvent",
    "WalkAnimBeginServerEvent",
    "WalkAnimEndServerEvent",
    "PlayerInventoryOpenScriptServerEvent",
    "UrgeShipEvent",
    "lobbyGoodBuySucServerEvent",
]


_lsnFuncArgs = []


def listen(eventName, t=0, namespace="", systemName="", priority=0):
    # type: (str, int, str, str, int) -> ...
    """
    函数装饰器，通过对函数进行装饰即可实现监听。
    示例：
    class MyServerSystem(ServerSystem):
        # 监听客户端传来的自定义事件
        @listen("MyCustomEvent")
        def eventCallback(self, args):
            pass

        # 监听EntityRemoveEvent事件
        @listen("EntityRemoveEvent", 1)
        def OnEntityRemove(self, args):
            pass
    -----------------------------------------------------------
    【eventName: str】 事件名称
    【t: int = 0】 0表示监听客户端传来的自定义事件，1表示监听服务端引擎事件，2表示监听其他Mod的事件
    【namespace: str = ""】 其他Mod的命名空间
    【systemName: str = ""】 其他Mod的系统名称
    【priority: int = 0】 优先级
    """
    if t == 0:
        _namespace = _MOD_NAME
        _systemName = _CLIENT_SYSTEM_NAME
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


class NuoyanServerSystem(_ServerSystem):
    """
    ServerSystem扩展类。将自定义ServerSystem继承本类即可使用本类的全部功能。
    -----------------------------------------------------------
    【基础功能】
    1. 所有官方文档中收录的服务端引擎事件以及新增事件均无需手动监听，只需重写对应事件的同名方法即可（支持热更）；
    2. 支持对在__init__方法中新增的事件监听或服务端属性（变量）执行热更；
    3. 无需重写Destroy方法进行事件的反监听。
    -----------------------------------------------------------
    【新增接口】
    1. ListenForEventV2：监听事件（简化版）
    2. CallClient：调用客户端属性（包括变量和函数）
    3. TestMode：开启或关闭服务端测试模式
    -----------------------------------------------------------
    【新增事件】
    1. UiInitFinished：客户端玩家UI框架初始化完成时，服务端触发
    2. OnGameTick：频率与游戏当前帧率同步的Tick事件
    -----------------------------------------------------------
    【新增属性】
    1. allPlayerData：用于保存所有玩家数据的字典，key为玩家实体ID，value为玩家数据字典，可自行添加数据；玩家加入游戏时（UiInitFinished后）会自动把玩家加入字典，玩家退出游戏时则会自动从字典中删除玩家及其数据；初始值为空字典
    2. homeownerPlayerId：房主玩家的实体ID；初始值为"-1"
    -----------------------------------------------------------
    【注意事项】
    1. 带有*tick*标签的事件为帧事件，需要注意编写相关逻辑；
    2. 事件回调参数中，参数名前面的美元符号“$”表示该参数可进行修改。
    """

    def __init__(self, namespace, systemName):
        super(NuoyanServerSystem, self).__init__(namespace, systemName)
        self.allPlayerData = {}
        self._listenGameTick = False
        self.homeownerPlayerId = "-1"
        self._initFinished = 1
        self.__timer = None  # type: _ServerTimer
        self._3dItems = []
        self.__listen()
        self._checkOnGameTick()

    def Destroy(self):
        """
        服务端系统销毁时触发。
        """
        self.UnListenAllEvents()

    # todo:==================================== Engine Event Callback ==================================================

    def lobbyGoodBuySucServerEvent(self, args):
        """
        玩家登录联机大厅服务器，或者联机大厅游戏内购买商品时触发。如果是玩家登录，触发时玩家客户端已经触发了UiInitFinished事件。
        -----------------------------------------------------------
        【eid: str】 玩家的实体ID
        【buyItem: bool】 玩家登录时为False，玩家购买了商品时为True
        """

    def UrgeShipEvent(self, args):
        """
        玩家点击商城催促发货按钮时触发该事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def PlayerInventoryOpenScriptServerEvent(self, args):
        """
        某个客户端打开物品背包界面时触发。
        可以监听此事件判定客户端是否打开了创造背包。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【isCreative: str】 是否是创造模式背包界面
        """

    def WalkAnimEndServerEvent(self, args):
        """
        当走路动作结束时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def WalkAnimBeginServerEvent(self, args):
        """
        当走路动作开始时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def JumpAnimBeginServerEvent(self, args):
        """
        当跳跃动作开始时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def AttackAnimEndServerEvent(self, args):
        """
        当攻击动作结束时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def AttackAnimBeginServerEvent(self, args):
        """
        当攻击动作开始时触发。
        使用SetModel替换骨骼模型后，该事件才生效。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def UIContainerItemChangedServerEvent(self, args):
        """
        合成容器物品发生变化时触发。
        合成容器包括工作台、铁砧、附魔台、织布机、砂轮、切石机、制图台、锻造台，输入物品发生变化时会触发本事件。
        可通过容器槽位区分不同的生成容器类型。
        合成容器的生成槽位生成物品时不触发本事件，生成物品可通过CraftItemOutputChangeServerEvent监听。
        储物容器(箱子，潜影箱)，熔炉，酿造台，发射器，投掷器，漏斗，炼药锅，唱片机，高炉，烟熏炉中物品发生变化不会触发此事件，此类容器可通过ContainerItemChangedServerEvent监听。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【slot: int】 容器槽位，含义见：PlayerUISlot枚举
        【oldItemDict: dict】 旧物品信息字典
        【newItemDict: dict】 生成的物品信息字典
        """

    def ShearsUseToBlockBeforeServerEvent(self, args):
        """
        *tick*
        实体手持剪刀对方块使用时，有剪刀特殊效果的方块会在服务端线程触发该事件。
        目前会触发该事件的方块：南瓜、蜂巢。
        该事件触发在ServerItemUseOnEvent之后，如果ServerItemUseOnEvent中取消了物品使用，该事件无法被触发。
        和ServerItemUseOnEvent一样该事件判定在tick执行，意味着如果取消剪刀效果该事件可能会多次触发（取决于玩家按下使用键时长）。
        -----------------------------------------------------------
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockY: int】 方块y坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxData: str】 方块附加值
        【dropName: str】 触发剪刀效果的掉落物identifier，包含命名空间及名称
        【dropCount: str】 触发剪刀效果的掉落物数量
        【entityId: str】 触发剪刀效果的实体ID，目前仅玩家会触发
        【dimensionId: int】 维度ID
        【$cancelShears: int】 是否取消剪刀效果
        """

    def ServerPlayerTryTouchEvent(self, args):
        """
        玩家即将捡起物品时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【entityId: str】 物品的实体ID
        【itemDict: dict】 物品信息字典
        【$cancel: bool】 设置为True时将取消本次拾取
        【pickupDelay: int】 取消拾取后重新设置该物品的拾取cd，小于15帧将视作15帧，大于等于97813帧将视作无法拾取
        """

    def ServerItemTryUseEvent(self, args):
        """
        玩家点击右键尝试使用物品时服务端抛出的事件。
        注：如果需要取消物品的使用需要同时在ClientItemTryUseEvent和ServerItemTryUseEvent中将cancel设置为True才能正确取消。
        ServerItemTryUseEvent/ClientItemTryUseEvent不能取消对方块使用物品的行为，如使用生物蛋，使用桶倒出/收集，使用打火石点燃草等；如果想要取消这种行为，请使用ClientItemUseOnEvent和ServerItemUseOnEvent。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        【$cancel: bool】 设为True可取消物品的使用
        """

    def PlayerDropItemServerEvent(self, args):
        """
        玩家丢弃物品时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemEntityId: str】 物品的实体ID
        """

    def OnPlayerBlockedByShieldBeforeServerEvent(self, args):
        """
        玩家使用盾牌抵挡伤害之前触发。
        盾牌抵挡了所有伤害时，才会触发事件；部分抛射物造成的伤害无法全部抵挡，无法触发事件，例如带有穿透魔咒的弩。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【sourceId: str】 伤害来源实体ID，没有实体返回"-1"
        【itemDict: dict】 盾牌物品字典物品信息字典
        【damage: dict】 抵挡的伤害数值
        """

    def OnPlayerBlockedByShieldAfterServerEvent(self, args):
        """
        玩家使用盾牌抵挡伤害之后触发.
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【sourceId: str】 伤害来源实体ID，没有实体返回"-1"
        【itemDict: dict】 盾牌物品字典物品信息字典
        【damage: dict】 抵挡的伤害数值
        """

    def OnPlayerActiveShieldServerEvent(self, args):
        """
        玩家激活/取消激活盾牌触发的事件。包括玩家持盾进入潜行状态，以及在潜行状态切换盾牌（切换耐久度不同的相同盾牌不会触发）。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【isActive: str】 True:尝试激活，False:尝试取消激活
        【itemDict: dict】 盾牌物品的物品信息字典
        【cancelable: dict】 是否可以取消。如果玩家在潜行状态切换盾牌，则无法取消
        【$cancel: bool】 是否取消这次激活
        """

    def OnOffhandItemChangedServerEvent(self, args):
        """
        玩家切换副手物品时触发该事件。
        当原有的物品槽内容为空时，oldItemName值为'minecraft:air'，且oldItem其余字段不存在。
        当切换原有物品，且新物品为空时，参数值同理。
        -----------------------------------------------------------
        【oldArmorDict: Optional[dict]】 旧物品的物品信息字典，当旧物品为空时，此项属性为None
        【newArmorDict: Optional[dict]】 新物品的物品信息字典，当新物品为空时，此项属性为None
        【playerId: str】 玩家的实体ID
        """

    def OnNewArmorExchangeServerEvent(self, args):
        """
        玩家切换盔甲时触发该事件。
        当玩家登录时，每个盔甲槽位会触发两次该事件，第一次为None切换到身上的装备，第二次的old和new都为身上装备。如果槽位为空，则是触发两次从None切换到None的事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【slot: int】 槽位ID
        【oldArmorDict: Optional[dict]】 旧装备的物品信息字典，当旧装备为空时，此项属性为None
        【newArmorDict: Optional[dict]】 新装备的物品信息字典，当新装备为空时，此项属性为None
        """

    def OnItemPutInEnchantingModelServerEvent(self, args):
        """
        玩家将可附魔物品放到附魔台上时触发。
        options为包含三个dict的list，单个dict的格式形如{'cost': 1, 'enchantData': [(1,1)], 'modEnchantData': [('custom_enchant, 1')]}，cost为解锁该选项所需的玩家等级，enchantData为该附魔选项包含的原版附魔数据，modEnchantData为该选项包含的自定义附魔数据。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【slotType: int】 玩家放入物品的EnchantSlotType
        【options: List[dict]】 附魔台选项
        【$change: bool】 传入True时，附魔台选项会被新传入的options覆盖
        """

    def ItemUseOnAfterServerEvent(self, args):
        """
        玩家在对方块使用物品之后服务端抛出的事件。
        在ServerItemUseOnEvent和原版物品使用事件（例如StartUsingItemClientEvent）之后触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【itemDict: dict】 物品信息字典
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【face: int】 点击方块的面，参考Facing枚举
        【clickX: float】 点击点的x比例位置
        【clickY: float】 点击点的y比例位置
        【clickZ: float】 点击点的z比例位置
        【blockName: str】 方块的identifier，包含命名空间及名称
        【blockAuxValue: int】 方块的附加值
        【dimensionId: int】 维度ID
        """

    def ItemUseAfterServerEvent(self, args):
        """
        玩家在使用物品之后服务端抛出的事件。
        做出使用物品这个动作之后触发，一些需要蓄力的物品使用事件(ActorUseItemServerEvent)会在之后触发。如投掷三叉戟，先触发本事件，投出去之后再触发ActorUseItemServerEvent。
        -----------------------------------------------------------
        【entityId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        """

    def ItemReleaseUsingServerEvent(self, args):
        """
        释放正在使用的物品时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【durationLeft: float】 蓄力剩余时间(当物品缺少"minecraft:maxduration"组件时,蓄力剩余时间为负数)
        【itemDict: dict】 使用的物品的物品信息字典
        【maxUseDuration: int】 最大蓄力时长
        【$cancel: bool】 设置为True可以取消，需要同时取消客户端事件ItemReleaseUsingClientEvent
        """

    def InventoryItemChangedServerEvent(self, args):
        """
        玩家背包物品变化时服务端抛出的事件。
        如果槽位变空，变化后槽位中物品为空气。
        触发时槽位物品仍为变化前物品。
        玩家进入游戏时，身上的物品会触发该事件。
        背包内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【slot: int】 背包槽位
        【oldItemDict: dict】 变化前的物品信息字典
        【newItemDict: dict】 变化后的物品信息字典
        """

    def FurnaceBurnFinishedServerEvent(self, args):
        """
        服务端熔炉烧制触发事件。熔炉、高炉、烟熏炉烧出物品时触发。
        -----------------------------------------------------------
        【dimensionId: int】 维度ID
        【posX: float】 位置x
        【posY: float】 位置y
        【posZ: float】 位置z
        【itemDict: dict】 物品信息字典
        """

    def CraftItemOutputChangeServerEvent(self, args):
        """
        玩家从容器拿出生成物品时触发。
        支持工作台，铁砧，砂轮等工作方块。
        screenContainerType = serverApi.GetMinecraftEnum().ContainerType.INVENTORY时，表示从创造模式物品栏中拿出物品，或者从合成栏中拿出合成物品。
        通过cancel参数取消生成物品，可用于禁止外挂刷物品。
        cancel=True时无法从创造模式物品栏拿物品。
        cancel=True时铁砧无法修复或重命名物品，但仍会扣除经验值。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        【itemDict: dict】 当前界面类型，类型含义见：ContainerType枚举枚举
        【$cancel: bool】 是否取消生成物品
        """

    def ContainerItemChangedServerEvent(self, args):
        """
        容器物品变化事件。
        储物容器(箱子，潜影箱)，熔炉，酿造台，发射器，投掷器，漏斗，炼药锅，唱片机，高炉，烟熏炉中物品发生变化会触发此事件。
        工作台、铁砧、附魔台、织布机、砂轮、切石机、制图台、锻造台为合成容器，不会触发此事件，此类容器可通过UIContainerItemChangedServerEvent监听具体生成容器物品变化。
        炼药锅只在使用染料时触发本事件，且slot为2。
        唱片机只在从漏斗放入唱片触发此事件。
        -----------------------------------------------------------
        【pos: Optional[Tuple[int, int, int]]】 容器坐标
        【containerType: int】 容器类型，类型含义见：ContainerType枚举
        【slot: int】 容器槽位
        【dimensionId: int】 维度ID
        【oldItemDict: dict】 旧物品信息字典
        【newItemDict: dict】 新物品信息字典
        """

    def StepOnBlockServerEvent(self, args):
        """
        实体刚移动至一个新实心方块时触发。
        在合并微软更新之后，本事件触发时机与微软molang实验性玩法组件"minecraft:on_step_on"一致。
        压力板与绊线钩在过去的版本的事件是可以触发的，但在更新后这种非实心方块并不会触发，有需要的可以使用OnEntityInsideBlockServerEvent事件。
        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关，原版方块需要先通过RegisterOnStepOn接口注册才能触发。原版的红石矿默认注册了，但深层红石矿没有默认注册。
        如果需要修改cancel，强烈建议配合客户端事件同步修改，避免出现客户端表现不一致等非预期现象。
        -----------------------------------------------------------
        【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【entityId: str】 实体ID
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        """

    def StepOffBlockServerEvent(self, args):
        """
        实体移动离开一个实心方块时触发。
        不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关，原版方块需要先通过RegisterOnStepOff接口注册才能触发。
        压力板与绊线钩这种非实心方块不会触发。
        -----------------------------------------------------------
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【entityId: str】 实体ID
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        -----------------------------------------------------------
        【相关接口】
        BlockInfoComponentServer.RegisterOnStepOff(blockName) -> bool
        BlockInfoComponentServer.UnRegisterOnStepOff(blockName) -> bool
        """

    def StartDestroyBlockServerEvent(self, args):
        """
        玩家开始挖方块时触发。创造模式下不触发。
        如果是隔着火焰挖方块，即使将该事件cancel掉，火焰也会被扑灭。如果要阻止火焰扑灭，需要配合ExtinguishFireServerEvent使用。
        -----------------------------------------------------------
        【pos: Tuple[float, float, float]】 方块坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        【playerId: str】 玩家的实体ID
        【dimensionId: int】 维度ID
        【$cancel: bool】 修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockClientEvent一起修改
        """

    def ShearsDestoryBlockBeforeServerEvent(self, args):
        """
        玩家手持剪刀破坏方块时，有剪刀特殊效果的方块会在服务端线程触发该事件。
        该事件触发在ServerPlayerTryDestroyBlockEvent之后，如果在ServerPlayerTryDestroyBlockEvent事件中设置了取消Destroy或取消掉落物会导致该事件不触发。
        取消剪刀效果后不掉落任何东西的方块类型：蜘蛛网、枯萎的灌木、草丛、下界苗、树叶、海草、藤蔓。
        绊线取消剪刀效果需要配合ShearsDestoryBlockBeforeClientEvent同时使用，否则在表现上可能展现出来的还是剪刀剪断后的效果。绊线取消剪刀效果后依然会掉落成线。
        -----------------------------------------------------------
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxData: int】 方块附加值
        【dropName: str】 触发剪刀效果的掉落物identifier，包含命名空间及名称
        【dropCount: int】 触发剪刀效果的掉落物数量
        【playerId: str】 玩家的实体ID
        【dimensionId: int】 维度ID
        【$cancelShears: bool】 是否取消剪刀效果
        """

    def ServerPlayerTryDestroyBlockEvent(self, args):
        """
        当玩家即将破坏方块时，服务端线程触发该事件。
        若需要禁止某些特殊方块的破坏，需要配合PlayerTryDestroyBlockClientEvent一起使用，例如床，旗帜，箱子这些根据方块实体数据进行渲染的方块。
        -----------------------------------------------------------
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【face: int】 方块被敲击的面向id，参考Facing枚举
        【fullName: str】 方块的identifier，包含命名空间及名称
        【auxData: int】 方块附加值
        【playerId: str】 试图破坏方块的玩家的实体ID
        【dimensionId: int】 维度ID
        【$cancel: bool】 默认为False，在脚本层设置为True就能取消该方块的破坏
        【$spawnResources: bool】 是否生成掉落物，默认为True，在脚本层设置为False就能取消生成掉落物
        """

    def ServerPlaceBlockEntityEvent(self, args):
        """
        手动放置或通过接口创建含自定义方块实体的方块时触发，此时可向该方块实体中存放数据。
        -----------------------------------------------------------
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimension: int】 维度ID
        【posX: int】 方块x坐标
        【posY: int】 方块y坐标
        【posZ: int】 方块z坐标
        """

    def ServerEntityTryPlaceBlockEvent(self, args):
        """
        当生物试图放置方块时触发该事件。
        部分放置后会产生实体的方块、可操作的方块、带有特殊逻辑的方块，不会触发该事件，包括但不限于床、门、告示牌、花盆、红石中继器、船、炼药锅、头部模型、蛋糕、酿造台、盔甲架等。
        -----------------------------------------------------------
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【fullName: str】 方块的identifier，包含命名空间及名称
        【auxData: int】 方块附加值
        【entityId: str】 试图放置方块的生物的实体ID
        【dimensionId: int】 维度ID
        【face: int】 点击方块的面，参考Facing枚举
        【$cancel: bool】 默认为False，在脚本层设置为True就能取消该方块的放置
        """

    def ServerBlockEntityTickEvent(self, args):
        """
        *tick*
        自定义方块配置了netease:block_entity组件并设tick为true，方块在玩家的模拟距离（新建存档时可以设置，默认为4个区块）内，或者在tickingarea内的时候触发。
        方块实体的tick事件频率为每秒钟20次。
        触发本事件时，若正在退出游戏，将无法获取到抛出本事件的方块实体数据（GetBlockEntityData函数返回None），也无法对其进行操作。
        -----------------------------------------------------------
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimension: int】 维度ID
        【posX: int】 方块x坐标
        【posY: int】 方块y坐标
        【posZ: int】 方块z坐标
        """

    def PistonActionServerEvent(self, args):
        """
        活塞或者粘性活塞推送/缩回影响附近方块时触发。
        -----------------------------------------------------------
        【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止触发后续的事件
        【action: str】 推送时=expanding；缩回时=retracting
        【pistonFacing: int】 活塞的朝向，参考Facing枚举
        【pistonMoveFacing: int】 活塞的运动方向，参考Facing枚举
        【dimensionId: int】 维度ID
        【pistonX: int】 活塞方块的x坐标
        【pistonY: int】 活塞方块的y坐标
        【pistonZ: int】 活塞方块的z坐标
        【blockList: List[Tuple[int, int, int]]】 活塞运动影响到产生被移动效果的方块坐标(x,y,z)，均为int类型
        【breakBlockList: List[Tuple[int, int, int]]】 活塞运动影响到产生被破坏效果的方块坐标(x,y,z)，均为int类型
        【entityList: List[str]】 活塞运动影响到产生被移动或被破坏效果的实体ID列表
        """

    def OnStandOnBlockServerEvent(self, args):
        """
        当实体站立到方块上时服务端持续触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【dimensionId: int】 维度ID
        【posX: float】 实体位置x
        【posY: float】 实体位置y
        【posZ: float】 实体位置z
        【motionX: float】 瞬时移动x方向的力
        【motionY: float】 瞬时移动y方向的力
        【motionZ: float】 瞬时移动z方向的力
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【$cancel: bool】 可由脚本层回传True给引擎，阻止触发后续原版逻辑
        """

    def OnBeforeFallOnBlockServerEvent(self, args):
        """
        当实体刚降落到方块上时服务端触发，主要用于伤害计算。
        不是所有方块都会触发该事件，需要在json中先配置触发开关。
        如果要在脚本层修改fallDistance，回传的一定要是浮点型，例如需要赋值0.0而不是0。
        可能会因为轻微的反弹触发多次，可在脚本层针对fallDistance的值进行判断。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【$fallDistance: float】 实体下降距离，可在脚本层传给引擎
        【$cancel: bool】 是否取消引擎对实体下降伤害的计算
        """

    def OnAfterFallOnBlockServerEvent(self, args):
        """
        当实体降落到方块后服务端触发，主要用于力的计算。
        不是所有方块都会触发该事件，需要在json中先配置触发开关。
        如果要在脚本层修改motion，回传的需要是浮点型，例如需要赋值0.0而不是0。
        如果需要修改实体的力，最好配合客户端事件同步修改，避免产生非预期现象。
        因为引擎最后一定会按照原版方块规则计算力（普通方块置0，床、粘液块等反弹），所以脚本层如果想直接修改当前力需要将calculate设为true取消原版计算，按照传回值计算。
        引擎在落地之后，OnAfterFallOnBlockServerEvent会一直触发，因此请在脚本层中做对应的逻辑判断。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【posX: float】 实体位置x
        【posY: float】 实体位置y
        【posZ: float】 实体位置z
        【motionX: float】 瞬时移动x方向的力
        【motionY: float】 瞬时移动y方向的力
        【motionZ: float】 瞬时移动z方向的力
        【blockName: str】 方块的identifier，包含命名空间及名称
        【$calculate: bool】 是否按脚本层传值计算力
        """

    def HopperTryPullOutServerEvent(self, args):
        """
        当漏斗以毗邻的方式连接容器时，即从旁边连接容器时，漏斗向容器开始输出物品时触发，事件仅触发一次。
        -----------------------------------------------------------
        【x: int】 漏斗x坐标
        【y: int】 漏斗y坐标
        【z: int】 漏斗z坐标
        【attachedPosX: int】 交互的容器的x坐标
        【attachedPosY: int】 交互的容器的y坐标
        【attachedPosZ: int】 交互的容器的z坐标
        【dimensionId: int】 维度ID
        【$canHopper: bool】 是否允许容器往漏斗加东西(要关闭此交互，需先监听此事件再放置容器)
        """

    def HopperTryPullInServerEvent(self, args):
        """
        当漏斗上方连接容器后，容器往漏斗开始输入物品时触发，事件仅触发一次。
        -----------------------------------------------------------
        【x: int】 漏斗x坐标
        【y: int】 漏斗y坐标
        【z: int】 漏斗z坐标
        【abovePosX: int】 交互的容器位置x
        【abovePosY: int】 交互的容器位置y
        【abovePosZ: int】 交互的容器位置z
        【dimensionId: int】 维度ID
        【$canHopper: bool】 是否允许容器往漏斗加东西(要关闭此交互，需先监听此事件再放置容器)
        """

    def HeavyBlockStartFallingServerEvent(self, args):
        """
        当重力方块变为下落的方块实体后，服务端触发该事件。
        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关。
        -----------------------------------------------------------
        【fallingBlockId: str】 下落的方块实体ID
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        """

    def GrassBlockToDirtBlockServerEvent(self, args):
        """
        草方块变成泥土方块时触发。
        指令或者接口的设置不会触发该事件。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        """

    def FarmBlockToDirtBlockServerEvent(self, args):
        """
        耕地退化为泥土时触发。
        指令或者接口的设置不会触发该事件。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【setBlockType: int】 耕地退化为泥土的原因，参考SetBlockType枚举
        """

    def FallingBlockReturnHeavyBlockServerEvent(self, args):
        """
        当下落的方块实体变回普通重力方块时，服务端触发该事件。
        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关。
        -----------------------------------------------------------
        【fallingBlockId: str】 下落的方块实体ID
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【heavyBlockName: int】 重力方块的identifier，包含命名空间及名称
        【prevHereBlockName: int】 变回重力方块时，原本方块位置的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        【fallTickAmount: int】 下落的方块实体持续下落了多少tick
        """

    def FallingBlockCauseDamageBeforeServerEvent(self, args):
        """
        当下落的方块开始计算砸到实体的伤害时，服务端触发该事件。
        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关。
        服务端通常触发在客户端之后，而且有时会相差一个tick，这就意味着可能发生以下现象：服务端fallTickAmount比配置强制破坏时间多1tick，下落的距离、下落的伤害计算出来比客户端时间多1tick的误差。
        -----------------------------------------------------------
        【fallingBlockId: str】 下落的方块实体ID
        【fallingBlockX: float】 下落的方块实体位置x
        【fallingBlockY: float】 下落的方块实体位置y
        【fallingBlockZ: float】 下落的方块实体位置z
        【blockName: str】 重力方块的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        【collidingEntitys: Optional[List[str]]】 当前碰撞到的实体ID的列表，如果没有的话是None
        【fallTickAmount: int】 下落的方块实体持续下落了多少tick
        【fallDistance: float】 下落的方块实体持续下落了多少距离
        【$isHarmful: bool】 是否计算对实体的伤害，引擎传来的值由json配置和伤害是否大于0决定，可在脚本层修改传回引擎
        【$fallDamage: int】 对实体的伤害，引擎传来的值距离和json配置决定，可在脚本层修改传回引擎
        """

    def FallingBlockBreakServerEvent(self, args):
        """
        当下落的方块实体被破坏时，服务端触发该事件。
        不是所有下落的方块都会触发该事件，需要在json中先配置触发开关。
        -----------------------------------------------------------
        【fallingBlockId: str】 下落的方块实体ID
        【fallingBlockX: float】 下落的方块实体位置x
        【fallingBlockY: float】 下落的方块实体位置y
        【fallingBlockZ: float】 下落的方块实体位置z
        【blockName: str】 重力方块的identifier，包含命名空间及名称
        【fallTickAmount: int】 下落的方块实体持续下落了多少tick
        【dimensionId: int】 维度ID
        【$cancelDrop: bool】 是否取消方块物品掉落，可以在脚本层中设置
        """

    def EntityPlaceBlockAfterServerEvent(self, args):
        """
        当生物成功放置方块后触发。
        部分放置后会产生实体的方块、可操作的方块、带有特殊逻辑的方块，不会触发该事件，包括但不限于床、门、告示牌、花盆、红石中继器、船、炼药锅、头部模型、蛋糕、酿造台、盔甲架等。
        -----------------------------------------------------------
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【fullName: str】 方块的identifier，包含命名空间及名称
        【auxData: int】 方块附加值
        【entityId: str】 实体ID
        【dimensionId: int】 维度ID
        【face: int】 点击方块的面，参考Facing枚举
        """

    def DirtBlockToGrassBlockServerEvent(self, args):
        """
        泥土方块变成草方块时触发。
        指令或者接口的设置不会触发该事件。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        """

    def CommandBlockUpdateEvent(self, args):
        """
        玩家尝试修改命令方块的内置命令时。
        当修改的目标为命令方块矿车时（此时isBlock为False），设置cancel为True，依旧可以阻止修改命令方块矿车的内部指令，但是从客户端能够看到命令方块矿车的内部指令变化了，不过这仅仅是假象，重新登录或者其他客户端打开命令方块矿车的设置界面，就会发现其实内部指令没有变化。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【playerUid: long】 玩家的uid
        【command: str】 企图修改的命令方块中的命令内容字符串
        【isBlock: bool】 是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义
        【blockX: int】 命令方块位置x，当isBlock为True时有效
        【blockY: int】 命令方块位置y，当isBlock为True时有效
        【blockZ: int】 命令方块位置z，当isBlock为True时有效
        【victimId: str】 命令方块对应的逻辑实体的实体ID，当isBlock为False时有效
        【$cancel: bool】 修改为True时，可以阻止玩家修改命令方块的内置命令
        """

    def CommandBlockContainerOpenEvent(self, args):
        """
        玩家点击命令方块，尝试打开命令方块的设置界面。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【isBlock: bool】 是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义
        【blockX: int】 命令方块位置x，当isBlock为True时有效
        【blockY: int】 命令方块位置y，当isBlock为True时有效
        【blockZ: int】 命令方块位置z，当isBlock为True时有效
        【victimId: str】 命令方块对应的逻辑实体的实体ID，当isBlock为False时有效
        【$cancel: bool】 修改为True时，可以阻止玩家打开命令方块的设置界面
        """

    def ChestBlockTryPairWithServerEvent(self, args):
        """
        两个并排的小箱子方块准备组合为一个大箱子方块时触发。
        -----------------------------------------------------------
        【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止小箱子组合成为一个大箱子
        【blockX: int】 小箱子方块x坐标
        【blockY: int】 小箱子方块y坐标
        【blockZ: int】 小箱子方块z坐标
        【otherBlockX: int】 将要与之组合的另外一个小箱子方块x坐标
        【otherBlockY: int】 将要与之组合的另外一个小箱子方块y坐标
        【otherBlockZ: int】 将要与之组合的另外一个小箱子方块z坐标
        【dimensionId: int】 维度ID
        """

    def BlockStrengthChangedServerEvent(self, args):
        """
        自定义机械元件方块红石信号量发生变化时触发。
        -----------------------------------------------------------
        【posX: int】 方块x坐标
        【posY: int】 方块y坐标
        【posZ: int】 方块z坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        【newStrength: int】 变化后的红石信号量
        【dimensionId: int】 维度ID
        """

    def BlockSnowStateChangeServerEvent(self, args):
        """
        方块转为含雪或者脱离含雪前触发。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【turnSnow: bool】 是否转为含雪，true则转为含雪，false则脱离含雪
        【setBlockType: int】 方块进入脱离含雪的原因，参考SetBlockType枚举
        """

    def BlockSnowStateChangeAfterServerEvent(self, args):
        """
        方块转为含雪或者脱离含雪后触发。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【turnSnow: bool】 是否转为含雪，true则转为含雪，false则脱离含雪
        【setBlockType: int】 方块进入脱离含雪的原因，参考SetBlockType枚举
        """

    def BlockRemoveServerEvent(self, args):
        """
        监听该事件的方块在销毁时触发，可以通过ListenOnBlockRemoveEvent方法进行监听，或者通过json组件netease:listen_block_remove进行配置。
        -----------------------------------------------------------
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【fullName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        【dimension: int】 维度ID
        -----------------------------------------------------------
        【相关接口】
        BlockInfoComponentServer.ListenOnBlockRemoveEvent(identifier, listen) -> bool
        """

    def BlockRandomTickServerEvent(self, args):
        """
        自定义方块配置netease:random_tick随机tick时触发。
        -----------------------------------------------------------
        【dimensionId: int】 维度ID
        【posX: int】 方块x坐标
        【posY: int】 方块y坐标
        【posZ: int】 方块z坐标
        【blockName: str】 方块名称
        【fullName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        """

    def BlockNeighborChangedServerEvent(self, args):
        """
        自定义方块周围的方块发生变化时，需要配置netease:neighborchanged_sendto_script。
        -----------------------------------------------------------
        【dimensionId: int】 维度ID
        【posX: int】 方块x坐标
        【posY: int】 方块y坐标
        【posZ: int】 方块z坐标
        【blockName: str】 方块的identifier，包含命名空间及名称
        【neighborPosX: int】 变化方块x坐标
        【neighborPosY: int】 变化方块y坐标
        【neighborPosZ: int】 变化方块z坐标
        【fromBlockName: str】 方块变化前的identifier，包含命名空间及名称
        【fromBlockAuxValue: int】 方块变化前附加值
        【toBlockName: str】 方块变化后的identifier，包含命名空间及名称
        【toAuxValue: int】 方块变化后附加值
        """

    def BlockLiquidStateChangeServerEvent(self, args):
        """
        方块转为含水或者脱离含水(流体)前触发。
        -----------------------------------------------------------
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        【dimension: int】 维度ID
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【turnLiquid: bool】 是否转为含水，True则转为含水，False则脱离含水
        """

    def BlockLiquidStateChangeAfterServerEvent(self, args):
        """
        方块转为含水或者脱离含水(流体)后触发。
        -----------------------------------------------------------
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        【dimension: int】 维度ID
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【turnLiquid: bool】 是否转为含水，True则转为含水，False则脱离含水
        """

    def BlockDestroyByLiquidServerEvent(self, args):
        """
        方块被水流破坏的事件。
        指令或者接口的设置不会触发该事件。
        -----------------------------------------------------------
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【liquidName: str】 流体方块identifier
        【blockName: str】 方块的identifier，包含命名空间及名称
        【auxValue: int】 方块的附加值
        """

    def StoreBuySuccServerEvent(self, args):
        """
        玩家游戏内购买商品时服务端抛出的事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def ServerPlayerGetExperienceOrbEvent(self, args):
        """
        玩家获取经验球时触发的事件。
        cancel值设为True时，捡起的经验球不会增加经验值，但是经验球一样会消失。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【experienceValue: int】 经验球经验值
        【$cancel: bool】 是否取消
        """

    def PlayerTrySleepServerEvent(self, args):
        """
        玩家尝试使用床睡觉时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【$cancel: bool】 是否取消
        """

    def PlayerTeleportEvent(self, args):
        """
        当玩家传送时触发该事件，如：玩家使用末影珍珠或tp指令时。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        """

    def PlayerStopSleepServerEvent(self, args):
        """
        玩家停止睡觉时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def PlayerSleepServerEvent(self, args):
        """
        玩家使用床睡觉成功时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def PlayerRespawnFinishServerEvent(self, args):
        """
        玩家复活完毕时触发。
        该事件触发时玩家已重生完毕，可以安全使用切维度等操作。
        通过末地传送门回到主世界时也算重生，同样也会触发该事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def PlayerRespawnEvent(self, args):
        """
        玩家复活时触发该事件。
        该事件为玩家点击重生按钮时触发，但是触发时玩家可能尚未完成复活，此时请勿对玩家进行切维度或设置生命值等操作，一般情况下推荐使用PlayerRespawnFinishServerEvent。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        """

    def PlayerHurtEvent(self, args):
        """
        当玩家受伤害前触发该事件。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【attacker: str】 伤害来源实体ID，若没有实体攻击，例如高空坠落，该值为"-1"
        """

    def PlayerEatFoodServerEvent(self, args):
        """
        玩家吃下食物时触发。
        吃蛋糕以及喝牛奶不触发该事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 食物的物品信息字典
        【$hunger: int】 食物增加的饥饿值，可修改
        【$nutrition: float】 食物的营养价值，回复饱和度 = 食物增加的饥饿值 * 食物的营养价值 * 2，饱和度最大不超过当前饥饿值，可修改
        """

    def PlayerDieEvent(self, args):
        """
        当玩家死亡时触发该事件。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【attacker: str】 伤害来源的实体ID
        """

    def OnPlayerHitBlockServerEvent(self, args):
        """
        通过OpenPlayerHitBlockDetection打开方块碰撞检测后，当玩家碰撞到方块时触发该事件。
        监听玩家着地请使用客户端的OnGroundClientEvent。
        客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【posX: int】 碰撞方块x坐标
        【posY: int】 碰撞方块y坐标
        【posY: int】 碰撞方块z坐标
        【blockId: float】 碰撞方块的identifier
        【auxValue: int】 碰撞方块的附加值
        【dimensionId: int】 维度ID
        -----------------------------------------------------------
        【相关接口】
        PlayerCompServer.OpenPlayerHitBlockDetection(precision) -> bool
        PlayerCompServer.ClosePlayerHitBlockDetection() -> bool
        """

    def GameTypeChangedServerEvent(self, args):
        """
        个人游戏模式发生变化时服务端触发。
        游戏模式：Survival，Creative，Adventure分别为0~2。
        默认游戏模式发生变化时最后反映在个人游戏模式之上。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID，SetDefaultGameType接口改变游戏模式时该参数为空字符串
        【oldGameType: int】 切换前的游戏模式
        【newGameType: int】 切换后的游戏模式
        """

    def ExtinguishFireServerEvent(self, args):
        """
        玩家扑灭火焰时触发。
        下雨，倒水等方式熄灭火焰不会触发。
        -----------------------------------------------------------
        【pos: Tuple[float, float, float]】 火焰方块的坐标
        【playerId: str】 玩家的实体ID
        【$cancel: bool】 修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireClientEvent一起修改
        """

    def DimensionChangeServerEvent(self, args):
        """
        玩家维度改变时服务端抛出。
        当通过传送门从末地回到主世界时，toY值为32767，其他情况一般会比设置值高1.62。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【fromDimensionId: int】 维度改变前的维度ID
        【toDimensionId: int】 维度改变前的维度ID
        【fromX: float】 改变前的位置x
        【fromY: float】 改变前的位置y
        【fromZ: float】 改变前的位置z
        【toX: float】 改变后的位置x
        【toY: float】 改变后的位置y
        【toZ: float】 改变后的位置z
        """

    def ChangeLevelUpCostServerEvent(self, args):
        """
        获取玩家下一个等级升级经验时触发，用于重载玩家的升级经验，每个等级在重置之前都只会触发一次。
        -----------------------------------------------------------
        【level: int】 玩家当前等级
        【$levelUpCostExp: int】 当前等级升级到下个等级需要的经验值，当设置升级经验小于1时会被强制调整到1
        【$changed: bool】 设置为True，重载玩家升级经验才会生效
        -----------------------------------------------------------
        【相关接口】
        PlayerCompServer.ClearDefinedLevelUpCost(level) -> bool
        """

    def AddLevelEvent(self, args):
        """
        当玩家升级时触发该事件。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【addLevel: int】 增加的等级值
        【newLevel: int】 新的等级
        """

    def AddExpEvent(self, args):
        """
        当玩家增加经验时触发该事件。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【addExp: int】 增加的经验值
        """

    def WillTeleportToServerEvent(self, args):
        """
        实体即将传送或切换维度时触发。
        假如目标维度尚未在内存中创建（即服务器启动之后，到传送之前，没有玩家进入过这个维度），那么此时事件中返回的目标地点坐标是算法生成的，不能保证正确。
        -----------------------------------------------------------
        【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止触发后续的传送
        【entityId: str】 实体ID
        【fromDimensionId: int】 传送前所在的维度
        【toDimensionId: int】 传送后的目标维度
        【fromX: float】 传送前的位置x
        【fromY: float】 传送前的位置y
        【fromZ: float】 传送前的位置z
        【toX: float】 传送后的位置x
        【toY: float】 传送后的位置y
        【toZ: float】 传送后的位置z
        【cause: str】 传送理由，详情见EntityTeleportCause枚举
        """

    def WillAddEffectServerEvent(self, args):
        """
        实体即将获得状态效果前触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【effectName: str】 状态效果的名字
        【effectDuration: int】 状态效果的持续时间，单位秒
        【effectAmplifier: int】 状态效果等级
        【$cancel: bool】 设置为True可以取消
        【damage: int】 状态将会造成的伤害值，如药水；需要注意，该值不一定是最终的伤害值，例如被伤害吸收效果扣除。只有持续时间为0时有用
        """

    def StartRidingServerEvent(self, args):
        """
        一个实体即将骑乘另外一个实体时触发。
        -----------------------------------------------------------
        【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止触发后续的实体交互事件
        【actorId: str】 骑乘者的实体ID
        【victimId: str】 被骑乘的实体ID
        """

    def RemoveEffectServerEvent(self, args):
        """
        实体身上状态效果被移除时触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【effectName: str】 被移除状态效果的名字
        【effectDuration: int】 被移除状态效果的剩余持续时间，单位秒
        【effectAmplifier: int】 被移除状态效果等级
        """

    def RefreshEffectServerEvent(self, args):
        """
        实体身上状态效果更新时触发，更新条件1、新增状态等级较高，更新状态等级及时间；2、新增状态等级不变，时间较长，更新状态持续时间。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【effectName: str】 更新状态效果的名字
        【effectDuration: int】 更新后状态效果剩余持续时间，单位秒
        【effectAmplifier: int】 更新后的状态效果等级
        【damage: int】 状态造成的伤害值，如药水
        """

    def ProjectileCritHitEvent(self, args):
        """
        当抛射物与头部碰撞时触发该事件。
        注：需调用OpenPlayerCritBox开启玩家爆头后才能触发。
        -----------------------------------------------------------
        【id: str】 抛射物的实体ID
        【targetId: str】 碰撞目标的实体ID
        -----------------------------------------------------------
        【相关接口】
        PlayerCompServer.OpenPlayerCritBox() -> None
        PlayerCompServer.ClosePlayerCritBox() -> None
        """

    def OnMobHitMobServerEvent(self, args):
        """
        通过OpenPlayerHitMobDetection打开生物碰撞检测后，当生物间（包含玩家）碰撞时触发该事件。
        注：客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。
        本事件代替原有的OnPlayerHitMobServerEvent事件。
        -----------------------------------------------------------
        【mobId: str】 当前生物的实体ID
        【hittedMobList: List[str]】 当前生物碰撞到的其他所有生物实体ID的list
        -----------------------------------------------------------
        【相关接口】
        PlayerCompServer.OpenPlayerHitMobDetection() -> bool
        PlayerCompServer.ClosePlayerHitMobDetection() -> bool
        """

    def OnKnockBackServerEvent(self, args):
        """
        实体被击退时触发。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnFireHurtEvent(self, args):
        """
        生物受到火焰伤害时触发。
        -----------------------------------------------------------
        【victim: str】 受伤实体ID
        【src: str】 火焰创建者的实体ID
        【fireTime: str】 着火时间，单位秒
        【$cancel: bool】 是否取消此处火焰伤害
        """

    def MobGriefingBlockServerEvent(self, args):
        """
        环境生物改变方块时触发，触发的时机与mobgriefing游戏规则影响的行为相同。
        触发的时机包括：生物踩踏耕地、破坏单个方块、破门、火矢点燃方块、凋灵boss破坏方块、末影龙破坏方块、末影人捡起方块、蠹虫破坏被虫蚀的方块、蠹虫把方块变成被虫蚀的方块、凋零杀死生物生成凋零玫瑰、生物踩坏海龟蛋。
        -----------------------------------------------------------
        【$cancel: bool】 是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
        【blockX: int】 方块x坐标
        【blockY: int】 方块y坐标
        【blockZ: int】 方块z坐标
        【entityId: str】 实体ID
        【blockName: str】 方块的identifier，包含命名空间及名称
        【dimensionId: int】 维度ID
        """

    def HealthChangeServerEvent(self, args):
        """
        生物生命值发生变化时触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【from: str】 变化前的生命值
        【to: str】 变化后的生命值
        【byScript: str】 是否通过SetAttrValue或SetAttrMaxValue调用产生的变化
        """

    def EntityTickServerEvent(self, args):
        """
        *tick*
        实体tick时触发。该事件为20帧每秒。需要使用AddEntityTickEventWhiteList添加触发该事件的实体类型白名单。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【identifier: str】 实体identifier
        -----------------------------------------------------------
        【相关接口】
        extraServerApi.AddEntityTickEventWhiteList(identifier) -> bool
        """

    def EntityPickupItemServerEvent(self, args):
        """
        有minecraft:behavior.pickup_items行为的生物拾取物品时触发该事件，例如村民拾取面包、猪灵拾取金锭。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【itemDict: dict】 物品信息字典
        【secondaryActor: str】 物品给予者的实体ID（一般是玩家），如果不存在给予者的话，这里为空字符串
        """

    def EntityMotionStopServerEvent(self, args):
        """
        实体运动器停止事件。实体（包含玩家）添加运动器并开始运行后，运动器自动停止时触发。
        注意：该事件触发表示运动器播放顺利完成，手动调用的StopEntityMotion、RemoveEntityMotion以及实体被销毁导致的运动器停止不会触发该事件。
        -----------------------------------------------------------
        【motionId: int】 运动器ID
        【entityId: str】 实体ID
        【$remove: bool】 是否移除该运动器，设置为False则保留，默认为True，即运动器停止后自动移除，该参数设置只对非玩家实体有效
        """

    def EntityMotionStartServerEvent(self, args):
        """
        实体运动器开始事件。实体（包含玩家）添加运动器后，运动器开始运行时触发。
        -----------------------------------------------------------
        【motionId: int】 运动器ID
        【entityId: str】 实体ID
        """

    def EntityLoadScriptEvent(self, args):
        """
        数据库加载实体自定义数据时触发。
        只有使用过extraData组件的SetExtraData接口的实体才有此事件，触发时可以通过extraData组件的GetExtraData或GetWholeExtraData接口获取该实体的自定义数据。
        -----------------------------------------------------------
        【args: list】 该事件的参数为长度为2的list，而非dict，其中list的第一个元素为实体ID
        """

    def EntityEffectDamageServerEvent(self, args):
        """
        生物受到状态伤害/回复事件。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【damage: int】 伤害值（伤害吸收后实际扣血量），负数表示生命回复量
        【attributeBuffType: int】 状态类型，参考AttributeBuffType
        【duration: float】 状态持续时间，单位秒
        【lifeTimer: float】 状态生命时间，单位秒
        【isInstantaneous: bool】 是否为立即生效状态
        """

    def EntityDroppedItemServerEvent(self, args):
        """
        生物扔出物品时触发。
        -----------------------------------------------------------
        【entityId: str】 生物的实体ID
        【itemDict: dict】 物品信息字典
        【itemEntityId: str】 物品的实体ID
        """

    def EntityChangeDimensionServerEvent(self, args):
        """
        实体维度改变时服务端抛出。
        实体转移维度时，如果对应维度的对应位置的区块尚未加载，实体会缓存在维度自身的缓冲区中，直到对应区块被加载时才会创建对应的实体，此事件的抛出只代表实体从原维度消失，不代表必定会在对应维度出现。
        注意，玩家维度改变时不触发该事件，而是会触发DimensionChangeServerEvent事件。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【fromDimensionId: int】 维度改变前的维度ID
        【toDimensionId: int】 维度改变后的维度ID
        【fromX: float】 改变前的位置x
        【fromY: float】 改变前的位置y
        【fromZ: float】 改变前的位置z
        【toX: float】 改变后的位置x
        【toY: float】 改变后的位置y
        【toZ: float】 改变后的位置z
        """

    def ChangeSwimStateServerEvent(self, args):
        """
        实体开始或者结束游泳时触发。
        当实体的状态没有变化时，不会触发此事件，即formState和toState必定一真一假。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【formState: bool】 事件触发前，实体是否在游泳状态
        【toState: bool】 事件触发后，实体是否在游泳状态
        """

    def AddEffectServerEvent(self, args):
        """
        实体获得状态效果时触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【effectName: str】 实体获得状态效果的名字
        【effectDuration: int】 状态效果的持续时间，单位秒
        【effectAmplifier: int】 状态效果的等级
        【damage: int】 状态造成的伤害值（真实扣除生命值的量）。只有持续时间为0时有用
        """

    def ActorHurtServerEvent(self, args):
        """
        生物（包括玩家）受伤时触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【cause: str】 伤害来源，详见Minecraft枚举值文档的ActorDamageCause
        【damage: int】 伤害值（被伤害吸收后的值），不可修改
        【damage_f: float】 伤害值（被伤害吸收后的值），不可修改
        【absorbedDamage: int】 被伤害吸收效果吸收的伤害值
        """

    def ServerSpawnMobEvent(self, args):
        """
        游戏内自动生成生物，以及使用api生成生物时触发。
        如果通过MOD API生成，identifier命名空间为custom。
        如果需要屏蔽原版的生物生成，可以判断identifier命名空间不为custom时设置cancel为True。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【identifier: str】 生成实体的命名空间
        【type: str】 生成实体的类型，参考EntityType
        【baby: str】 生成怪物是否是幼年怪
        【x: str】 生成实体坐标x
        【y: str】 生成实体坐标y
        【z: str】 生成实体坐标z
        【dimensionId: int】 生成实体的维度ID，默认值为0（0为主世界，1为地狱，2为末地）
        【realIdentifier: int】 生成实体的命名空间，通过MOD API生成的生物在这个参数也能获取到真正的命名空间，而不是以custom开头的
        【$cancel: bool】 是否取消生成该实体
        """

    def ServerPreBlockPatternEvent(self, args):
        """
        用方块组合生成生物，在放置最后一个组成方块时触发该事件。
        -----------------------------------------------------------
        【$enable: bool】 是否允许继续生成。若设为False，可阻止生成生物
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【dimensionId: int】 维度ID
        【entityWillBeGenerated: str】 即将生成生物的名字，如"minecraft:pig"
        """

    def ServerPostBlockPatternEvent(self, args):
        """
        用方块组合生成生物，生成生物之后触发该事件。
        -----------------------------------------------------------
        【entityId: str】 生成生物的实体ID
        【entityGenerated: str】 生成生物的名字，如"minecraft:pig"
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【dimensionId: int】 维度ID
        """

    def ServerChatEvent(self, args):
        """
        玩家发送聊天信息时触发。
        -----------------------------------------------------------
        【username: str】 玩家名称
        【playerId: str】 玩家的实体ID
        【message: str】 玩家发送的聊天消息内容
        【$cancel: bool】 是否取消这个聊天事件，若取消可以设置为True
        【$bChatById: bool】 是否把聊天消息发送给指定在线玩家，而不是广播给所有在线玩家，若只发送某些玩家可以设置为True
        【$bForbid: bool】 是否禁言，仅apollo可用。True：被禁言，玩家聊天会提示“你已被管理员禁言”
        【$toPlayerIds: List[str]】 接收聊天消息的玩家实体ID的列表，bChatById为True时生效
        【$gameChatPrefix: str】 设置当前玩家在网易聊天界面中的前缀，字数限制4，从字符串头部开始取。前缀文本输入非字符串格式时会被置为空。若cancel为True，会取消掉本次的前缀修改
        【$gameChatPrefixColorR: float】 设置当前玩家在网易聊天界面中前缀颜色rgb的r值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
        【$gameChatPrefixColorG: float】 设置当前玩家在网易聊天界面中前缀颜色rgb的g值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
        【$gameChatPrefixColorB: float】 设置当前玩家在网易聊天界面中前缀颜色rgb的b值，范围为[0,1]。颜色数值输入其他格式时会被置为0。若cancel为True，会取消掉本次的颜色修改
        """

    def PlayerLeftMessageServerEvent(self, args):
        """
        准备显示“xxx离开游戏”的玩家离开提示文字时服务端抛出的事件。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【name: str】 玩家昵称
        【$cancel: bool】 是否显示提示文字，允许修改。True：不显示提示
        【$message: str】 玩家离开游戏的提示文字，允许修改
        """

    def PlayerJoinMessageEvent(self, args):
        """
        准备显示“xxx加入游戏”的玩家登录提示文字时服务端抛出的事件。
        对于联机类游戏（如联机大厅、网络游戏等），请勿在此事件的回调函数中使用SetFootPos接口修改玩家的位置，否则可能会因为触发服务端反作弊机制而传送失败。如需要在进入游戏时使用SetFootPos接口，建议监听AddServerPlayerEvent并设置位置。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【name: str】 玩家昵称
        【$cancel: bool】 是否显示提示文字，允许修改。True：不显示提示
        【$message: str】 玩家加入游戏的提示文字，允许修改
        """

    def PlayerIntendLeaveServerEvent(self, args):
        """
        即将删除玩家时触发该事件。
        与DelServerPlayerEvent事件不同，此时可以通过各种API获取玩家的当前状态。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def PlaceNeteaseStructureFeatureEvent(self, args):
        """
        首次生成地形时，结构特征即将生成时服务端抛出该事件。
        需要配合AddNeteaseFeatureWhiteList接口一同使用。
        若在本监听事件中调用其他modSDK接口将无法生效，强烈建议本事件仅用于设置结构放置与否。
        -----------------------------------------------------------
        【structureName: str】 结构名称
        【x: int】 结构坐标最小方块所在的x坐标
        【y: int】 结构坐标最小方块所在的y坐标
        【z: int】 结构坐标最小方块所在的z坐标
        【biomeType: int】 该feature所放置区块的生物群系类型
        【biomeName: int】 该feature所放置区块的生物群系名称
        【dimensionId: int】 维度ID
        【$cancel: bool】 设置为True时可阻止该结构的放置
        -----------------------------------------------------------
        【相关接口】
        FeatureCompServer.AddNeteaseFeatureWhiteList(structureName) -> bool
        FeatureCompServer.RemoveNeteaseFeatureWhiteList(structureName) -> bool
        FeatureCompServer.ClearAllNeteaseFeatureWhiteList() -> bool
        """

    def OnRainLevelChangeServerEvent(self, args):
        """
        下雨强度发生改变时触发。
        -----------------------------------------------------------
        【oldLevel: float】 改变前的下雨强度
        【newLevel: float】 改变后的下雨强度
        """

    def OnLocalRainLevelChangeServerEvent(self, args):
        """
        独立维度天气下雨强度发生改变时触发。
        -----------------------------------------------------------
        【oldLevel: float】 改变前的下雨强度
        【newLevel: float】 改变后的下雨强度
        【dimensionId: int】 维度ID
        """

    def OnLocalLightningLevelChangeServerEvent(self, args):
        """
        独立维度天气打雷强度发生改变时触发。
        -----------------------------------------------------------
        【oldLevel: float】 改变前的打雷强度
        【newLevel: float】 改变后的打雷强度
        【dimensionId: int】 维度ID
        """

    def OnLightningLevelChangeServerEvent(self, args):
        """
        打雷强度发生改变时触发。
        -----------------------------------------------------------
        【oldLevel: float】 改变前的打雷强度
        【newLevel: float】 改变后的打雷强度
        """

    def OnContainerFillLoottableServerEvent(self, args):
        """
        随机奖励箱第一次打开根据loottable生成物品时。
        只有当dirty为True时才会重新读取item列表并生成对应的掉落物，如果不需要修改掉落结果的话请勿随意修改dirty值。
        -----------------------------------------------------------
        【loottable: str】 奖励箱子所读取的loottable的json路径
        【playerId: str】 打开奖励箱子的玩家的实体ID
        【itemList: List[dict]】 掉落物品列表，每个元素为一个itemDict，格式可参考物品信息字典
        【$dirty: bool】 默认为False，如果需要修改掉落列表需将该值设为True
        """

    def OnCommandOutputServerEvent(self, args):
        """
        Command命令执行成功事件。
        部分命令在返回的时候没有命令名称，SetCommand接口需要showOutput参数为True时才会有返回。
        -----------------------------------------------------------
        【command: str】 命令名称
        【message: str】 命令返回的消息
        """

    def NewOnEntityAreaEvent(self, args):
        """
        通过RegisterEntityAOIEvent注册过AOI事件后，当有实体进入或离开注册感应区域时触发该事件。
        本事件代替原有的OnEntityAreaEvent事件。
        -----------------------------------------------------------
        【name: str】 感应区域的名称
        【enteredEntities: List[str]】 进入该感应区域的实体ID列表
        【leftEntities: List[str]】 离开该感应区域的实体ID列表
        -----------------------------------------------------------
        【相关接口】
        DimensionCompServer.RegisterEntityAOIEvent(dimension, name, aabb, ignoredEntities, entityType) -> bool
        DimensionCompServer.UnRegisterEntityAOIEvent(dimension, name) -> bool
        """

    def LoadServerAddonScriptsAfter(self, args):
        """
        服务器加载完mod时触发。
        -----------------------------------------------------------
        无参数
        """

    def DelServerPlayerEvent(self, args):
        """
        删除玩家时触发该事件。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【isTransfer: bool】 是否是切服时退出服务器，仅用于Apollo。如果是True，则表示切服时退出服务器；若是False，则表示退出网络游戏
        【uid: long】 玩家的netease uid，玩家的唯一标识
        """

    def CommandEvent(self, args):
        """
        玩家请求执行指令时触发。
        该事件是玩家请求执行指令时触发的Hook，该事件不响应命令方块的指令和通过modSDK调用的指令，阻止玩家的该条指令只需要将cancel设置为True。
        -----------------------------------------------------------
        【entityId: str】 玩家的实体ID
        【command: str】 指令字符串
        【$cancel: bool】 是否取消
        """

    def ClientLoadAddonsFinishServerEvent(self, args):
        """
        客户端mod加载完成时，服务端触发此事件。服务器可以使用此事件，往客户端发送数据给其初始化。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """

    def ChunkLoadedServerEvent(self, args):
        """
        服务端区块加载完成时。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【chunkPosX: int】 区块的x坐标，对应方块x坐标区间为[x * 16, x * 16 + 15]
        【chunkPosZ: int】 区块的z坐标，对应方块z坐标区间为[z * 16, z * 16 + 15]
        """

    def ChunkGeneratedServerEvent(self, args):
        """
        区块创建完成时触发。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【blockEntityData: Optional[List[dict]]】 该区块中的自定义方块实体列表，通常是由自定义特征生成的自定义方块，没有自定义方块实体时该值为None。列表元素dict的结构如下：{'blockName':str, 'posX':int, 'posY':int, 'posZ':int}
        """

    def ChunkAcquireDiscardedServerEvent(self, args):
        """
        服务端区块即将被卸载时触发。
        区块卸载：游戏只会加载玩家周围的区块，玩家移动到别的区域时，原来所在区域的区块会被卸载。
        -----------------------------------------------------------
        【dimension: int】 维度ID
        【chunkPosX: int】 区块的x坐标，对应方块x坐标区间为[x * 16, x * 16 + 15]
        【chunkPosZ: int】 区块的z坐标，对应方块z坐标区间为[z * 16, z * 16 + 15]
        【entities: List[str]】 随区块卸载而从世界移除的实体ID的列表。注意事件触发时已经无法获取到这些实体的信息，仅供脚本资源回收用。
        【blockEntities: List[dict]】 随区块卸载而从世界移除的自定义方块实体的坐标的列表，列表元素dict包含posX，posY，posZ三个int表示自定义方块实体的坐标。注意事件触发时已经无法获取到这些方块实体的信息，仅供脚本资源回收用。
        """

    def AddServerPlayerEvent(self, args):
        """
        玩家加入时触发该事件。
        触发此事件时，客户端mod未加载完毕，因此响应本事件时不能客户端发送事件。
        若需要在玩家进入世界时，服务器往客户端发送事件，请使用ClientLoadAddonsFinishServerEvent。
        触发此事件时，玩家的实体还未加载完毕，请勿在这时切换维度。请在客户端监听OnLocalPlayerStopLoading事件并发送事件到服务端再进行维度切换。
        -----------------------------------------------------------
        【id: str】 玩家的实体ID
        【isTransfer: bool】 是否是切服时进入服务器，仅用于Apollo。如果是True，则表示切服时加入服务器，若是False，则表示登录进入网络游戏
        【isReconnect: bool】 是否是断线重连，仅用于Apollo。如果是True，则表示本次登录是断线重连，若是False，则表示本次是正常登录或者转服
        【isPeUser: bool】 是否从手机端登录，仅用于Apollo。如果是True，则表示本次登录是从手机端登录，若是False，则表示本次登录是从PC端登录
        【transferParam: str】 切服传入参数，仅用于Apollo。调用TransferToOtherServer或TransferToOtherServerById传入的切服参数
        【uid: long】 仅用于Apollo，玩家的netease uid，玩家的唯一标识
        【proxyId: int】 仅用于Apollo，当前客户端连接的proxy服务器id
        """

    def AchievementCompleteEvent(self, args):
        """
        玩家完成自定义成就时触发该事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【rootNodeId: str】 所属的页面的根节点成就ID
        【achievementId: str】 达成的成就ID
        【title: str】 成就标题
        【description: str】 成就描述
        """

    def PlayerAttackEntityEvent(self, args):
        """
        当玩家攻击时触发该事件。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【victimId: str】 受击者的实体ID
        【$damage: int】 伤害值，引擎传过来的值是0，允许脚本层修改为其他数
        【isValid: int】 脚本是否设置伤害值：1表示是，0表示否
        【$cancel: bool】 是否取消该次攻击，默认不取消
        【$isKnockBack: bool】 是否支持击退效果，默认支持，当不支持时将屏蔽武器击退附魔效果
        """

    def ServerBlockUseEvent(self, args):
        """
        *tick*
        玩家右键点击新版自定义方块（或者通过接口AddBlockItemListenForUseEvent增加监听的MC原生游戏方块）时服务端抛出该事件（该事件tick执行，需要注意效率问题）。
        当对原生方块进行使用时，如堆肥桶等类似有使用功能的方块使用物品时，会触发该事件，而ServerItemUseOnEvent则不会被触发。
        有的方块是在ServerBlockUseEvent中设置cancel生效，但是有部分方块是在ClientBlockUseEvent中设置cancel才生效，如有需求建议在两个事件中同时设置cancel以保证生效。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【blockName: str】 方块的identifier，包含命名空间及名称
        【aux: int】 方块附加值
        【$cancel: bool】 设置为True可拦截与方块交互的逻辑
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【dimensionId: int】 维度ID
        -----------------------------------------------------------
        【相关接口】
        BlockUseEventWhiteListComponentServer.AddBlockItemListenForUseEvent(blockName) -> bool
        BlockUseEventWhiteListComponentServer.RemoveBlockItemListenForUseEvent(blockName) -> bool
        BlockUseEventWhiteListComponentServer.ClearAllListenForBlockUseEventItems() -> bool
        """

    def OnGroundServerEvent(self, args):
        """
        实体着地事件。实体，掉落的物品，点燃的TNT掉落地面时触发。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def SpawnProjectileServerEvent(self, args):
        """
        抛射物生成时触发。
        该事件里无法获取弹射物实体的auxvalue。如有需要可以延迟一帧获取，或者在ProjectileDoHitEffectEvent获取。
        -----------------------------------------------------------
        【projectileId: str】 抛射物的实体ID
        【projectileIdentifier: str】 抛射物的identifier
        【spawnerId: str】 发射者的实体ID，没有发射者时为-1
        """

    def EntityDieLoottableServerEvent(self, args):
        """
        生物死亡掉落物品时触发。
        只有当dirty为True时才会重新读取item列表并生成对应的掉落物，如果不需要修改掉落结果的话请勿随意修改dirty值。
        -----------------------------------------------------------
        【dieEntityId: str】 死亡实体ID
        【attacker: str】 伤害来源实体ID
        【itemList: List[dict]】 掉落物品列表，每个元素为一个itemDict，格式可参考物品信息字典
        【dirty: bool】 默认为False，如果需要修改掉落列表需将该值设为True
        """

    def ActuallyHurtServerEvent(self, args):
        """
        实体实际受到伤害时触发，相比于DamageEvent，该伤害为经过护甲及buff计算后，实际的扣血量。
        药水与状态效果造成的伤害不触发，可以使用ActorHurtServerEvent。
        为了游戏运行效率请尽可能避免将火的伤害设置为0，因为这样会导致大量触发该事件。
        若要修改damage或damage_f的值，请确保修改后的值与原值不同，且需要使用原来的数据类型(int/float)，否则引擎会忽略这次修改。
        -----------------------------------------------------------
        【srcId: str】 伤害源实体ID
        【projectileId: str】 抛射物实体ID
        【entityId: str】 受伤的实体ID
        【damage: int】 伤害值（被伤害吸收后的值），允许修改，设置为0则此次造成的伤害为0，若设置数值和原来一样则视为没有修改
        【damage_f: float】 伤害值（被伤害吸收后的值），允许修改，若修改该值，则会覆盖damage的修改效果
        【cause: str】 伤害来源，详见Minecraft枚举值文档的ActorDamageCause
        """

    def HealthChangeBeforeServerEvent(self, args):
        """
        生物生命值发生变化之前触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【from: float】 变化前的生命值
        【to: float】 将要变化到的生命值，cancel设置为True时可以取消该变化，但是此参数不变
        【byScript: bool】 是否通过SetAttrValue或SetAttrMaxValue调用产生的变化
        【$cancel: bool】 是否取消该变化
        """

    def DimensionChangeFinishServerEvent(self, args):
        """
        玩家维度改变完成后服务端抛出。
        当通过传送门从末地回到主世界时，toPos的y值为32767，其他情况一般会比设置值高1.62。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【fromDimensionId: int】 维度改变前的维度
        【toDimensionId: int】 维度改变后的维度
        【toPos: Tuple[float, float, float]】 改变后的位置，其中y值为脚底加上角色的身高值
        """

    def EntityDefinitionsEventServerEvent(self, args):
        """
        生物定义json文件中设置的event触发时同时触发。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【eventName: str】 触发的事件名称
        """

    def PlayerDoInteractServerEvent(self, args):
        """
        玩家与有minecraft:interact组件的生物交互时触发该事件，例如玩家手持空桶对牛挤奶、玩家手持打火石点燃苦力怕。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 物品信息字典
        【interactEntityId: str】 交互生物的实体ID
        """

    def PlayerInteractServerEvent(self, args):
        """
        玩家可以与实体交互时触发。
        如果是鼠标控制模式，则当准心对着实体时触发。如果是触屏模式，则触发时机与屏幕下方的交互按钮显示的时机相同。
        玩家真正与实体发生交互的事件见PlayerDoInteractServerEvent。
        -----------------------------------------------------------
        【$cancel: bool】 是否取消触发，默认为False，若设为True，可阻止触发后续的实体交互事件
        【playerId: str】 玩家的实体ID
        【itemDict: dict】 玩家手持物品的物品信息字典
        【victimId: str】 交互生物的实体ID
        """

    def MobDieEvent(self, args):
        """
        生物死亡时触发。
        注意：不能在该事件回调中对攻击者手持物品进行修改，如SpawnItemToPlayerCarried、ChangePlayerItemTipsAndExtraId等接口。
        -----------------------------------------------------------
        【id: str】 实体ID
        【attacker: str】 攻击者实体ID
        """

    def AddEntityServerEvent(self, args):
        """
        服务端侧创建新实体，或实体从存档加载时触发。
        创建玩家时不会触发该事件。
        -----------------------------------------------------------
        【id: str】 实体ID
        【posX: float】 实体位置x
        【posY: float】 实体位置y
        【posZ: float】 实体位置z
        【dimensionId: int】 维度ID
        【isBaby: bool】 是否为幼儿
        【engineTypeStr: str】 实体类型，即实体identifier
        【itemName: str】 物品identifier（仅当物品实体时存在该字段）
        【auxValue: int】 物品附加值（仅当物品实体时存在该字段）
        """

    def OnMobHitBlockServerEvent(self, args):
        """
        通过OpenMobHitBlockDetection打开方块碰撞检测后，当生物（不包括玩家）碰撞到方块时触发该事件。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【posX: int】 碰撞方块x坐标
        【posY: int】 碰撞方块y坐标
        【posZ: int】 碰撞方块z坐标
        【blockId: str】 碰撞方块的identifier
        【auxValue: int】 碰撞方块的附加值
        【dimensionId: int】 维度ID
        -----------------------------------------------------------
        【相关接口】
        GameComponentServer.OpenMobHitBlockDetection(entityId: str, precision: float) -> bool
        GameComponentServer.CloseMobHitBlockDetection(entityId: str) -> bool
        """

    def OnEntityInsideBlockServerEvent(self, args):
        """
        *tick*
        当实体碰撞盒所在区域有方块时，服务端持续触发。
        不是所有方块都会触发该事件，需要在json中先配置触发开关，原版方块需要先通过RegisterOnEntityInside接口注册才能触发。
        如果需要修改slowdownMulti/cancel，强烈建议与客户端事件同步修改，避免出现客户端表现不一致等非预期现象。
        如果要在脚本层修改slowdownMulti，回传的一定要是浮点型，例如需要赋值1.0而不是1。
        有任意slowdownMulti参数被传回非0值时生效减速比例。
        slowdownMulti参数更像是一个Buff，例如并不是立刻计算，而是先保存在实体属性里延后计算。在已经有slowdownMulti属性的情况下会取最低的值、免疫掉落伤害等，与原版蜘蛛网逻辑基本一致。
        -----------------------------------------------------------
        【entityId: str】 实体ID
        【$slowdownMultiX: float】 实体移速x方向的减速比例，可在脚本层被修改
        【$slowdownMultiY: float】 实体移速y方向的减速比例，可在脚本层被修改
        【$slowdownMultiZ: float】 实体移速z方向的减速比例，可在脚本层被修改
        【blockX: int】 方块位置x
        【blockY: int】 方块位置y
        【blockZ: int】 方块位置z
        【blockName: str】 方块的identifier，包含命名空间及名称
        【$cancel: bool】 可由脚本层回传True给引擎，阻止触发后续原版逻辑
        -----------------------------------------------------------
        【相关接口】
        BlockInfoComponentServer.RegisterOnEntityInside(blockName: str) -> bool
        BlockInfoComponentServer.UnRegisterOnEntityInside(blockName: str) -> bool
        """

    def EntityStartRidingEvent(self, args):
        """
        当实体骑乘上另一个实体时触发。
        -----------------------------------------------------------
        【id: str】 骑乘者实体ID
        【rideId: str】 坐骑实体ID
        """

    def EntityStopRidingEvent(self, args):
        """
        当实体停止骑乘时触发。
        以下情况不允许取消：
        1. ride组件StopEntityRiding接口
        2. 玩家传送时；
        3. 坐骑死亡时；
        4. 玩家睡觉时；
        5. 玩家死亡时；
        6. 未驯服的马；
        7. 怕水的生物坐骑进入水里；
        8. 切换维度。
        -----------------------------------------------------------
        【id: str】 实体ID
        【rideId: str】 坐骑的实体ID
        【exitFromRider: bool】 是否下坐骑
        【entityIsBeingDestroyed: bool】 坐骑是否将要销毁
        【switchingRides: bool】 是否换乘坐骑
        【$cancel: bool】 设置为True可以取消（需要与客户端事件一同取消）
        """

    def ServerItemUseOnEvent(self, args):
        """
        *tick*
        玩家在对方块使用物品之前服务端抛出的事件。
        注：如果需要取消物品的使用需要同时在ClientItemUseOnEvent和ServerItemUseOnEvent中将ret设置为True才能正确取消。
        当对原生方块进行使用时，如堆肥桶等类似有使用功能的方块使用物品时，不会触发该事件。而当原生方块加入监听后，ServerBlockUseEvent会触发。
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

    def ActorUseItemServerEvent(self, args):
        """
        玩家使用物品生效之前服务端抛出的事件。
        比较特殊不走该事件的例子：
        1. 喝牛奶；
        2. 染料对有水的炼药锅使用；
        3. 盔甲架装备盔甲。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体id
        【itemDict: dict】 物品信息字典
        【useMethod: int】 使用物品的方法，详见ItemUseMethodEnum枚举
        """

    def ActorAcquiredItemServerEvent(self, args):
        """
        玩家获得物品时服务端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点）。
        -----------------------------------------------------------
        【actor: str】 获得物品玩家实体ID
        【secondaryActor: str】 物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
        【itemDict: dict】 获得的物品的物品信息字典
        【acquireMethod: int】 获得物品的方法，详见ItemAcquisitionMethod枚举
        """

    def DestroyBlockEvent(self, args):
        """
        当方块已经被玩家破坏时触发该事件。
        在生存模式或创造模式下都会触发。
        -----------------------------------------------------------
        【x: int】 方块x坐标
        【y: int】 方块y坐标
        【z: int】 方块z坐标
        【face: int】 方块被敲击的面向id，参考Facing枚举
        【fullName: str】 方块的identifier，包含命名空间及名称
        【auxData: int】 方块附加值
        【playerId: str】 破坏方块的玩家实体ID
        【dimensionId: int】 维度ID
        """

    def DamageEvent(self, args):
        """
        实体受到伤害时触发。
        damage值会被护甲和absorption等吸收，不一定是最终扣血量。通过设置这个伤害值可以取消伤害，但不会取消由击退效果或者点燃效果带来的伤害。
        该事件在实体受伤之前触发，由于部分伤害是在tick中处理，因此持续触发受伤时（如站在火中）会每帧触发事件（可以使用ActorHurtServerEvent来避免）。
        这里的damage是伤害源具有的攻击伤害值，并非实体真实的扣血量，如果需要获取真实伤害，可以使用ActuallyHurtServerEvent事件。
        当目标无法被击退时，knock值无效。
        药水与状态效果造成的伤害不触发，可以使用ActorHurtServerEvent。
        -----------------------------------------------------------
        【srcId: str】 伤害源实体ID
        【projectileId: str】 投射物实体ID
        【entityId: str】 受伤实体ID
        【$damage: int】 伤害值（被伤害吸收前的值），允许修改，设置为0则此次造成的伤害为0
        【damage_f: float】 伤害值（被伤害吸收前的值），不允许修改
        【absorption: int】 伤害吸收生命值，详见AttrType枚举的ABSORPTION
        【cause: str】 伤害来源，详见ActorDamageCause枚举
        【$knock: bool】 是否击退被攻击者，允许修改，设置该值为False则不产生击退
        【$ignite: bool】 是否点燃被伤害者，允许修改，设置该值为True产生点燃效果，反之亦然
        """

    def ExplosionServerEvent(self, args):
        """
        当发生爆炸时触发。
        可以通过修改blocks取消爆炸对指定方块的影响。
        某些情况下爆炸创建者实体ID为None，此时受伤实体ID列表也为None，比如爬行者所造成的爆炸。
        -----------------------------------------------------------
        【$blocks: List[List[int, int, int, bool]]】 爆炸涉及到的方块列表，每个方块以一个列表表示，前三个元素分别为方块坐标xyz，第四个元素为是否取消爆炸对该方块的影响，将第四个元素设置为True即可取消。
        【victims: Optional[List[str]]】 受伤实体ID列表，当该爆炸创建者实体ID为None时，victims也为None
        【sourceId: Optional[str]】 爆炸创建者实体ID
        【explodePos: List[float, float, float]】 爆炸位置[x, y, z]
        【dimensionId: int】 维度ID
        """

    def ProjectileDoHitEffectEvent(self, args):
        """
        当抛射物碰撞时触发该事件。
        -----------------------------------------------------------
        【id: str】 子弹的实体ID
        【hitTargetType: str】 碰撞目标类型，"ENTITY"或"BLOCK"
        【targetId: str】 碰撞目标的实体ID
        【hitFace: int】 撞击在方块上的面ID，参考Facing枚举
        【x: float】 碰撞x坐标
        【y: float】 碰撞y坐标
        【z: float】 碰撞z坐标
        【blockPosX: int】 碰撞是方块时，方块x坐标
        【blockPosY: int】 碰撞是方块时，方块y坐标
        【blockPosZ: int】 碰撞是方块时，方块z坐标
        【srcId: str】 抛射物创建者的实体ID
        【$cancel: bool】 是否取消这个碰撞事件，若取消可以设置为True
        """

    def OnCarriedNewItemChangedServerEvent(self, args):
        """
        玩家切换主手物品时触发该事件。
        切换耐久度不同的相同物品，不会触发该事件。
        -----------------------------------------------------------
        【oldItemDict: Optional[dict]】 旧物品的物品信息字典，当旧物品为空时，此项属性为None
        【newItemDict: Optional[dict]】 新物品的物品信息字典，当新物品为空时，此项属性为None
        【playerId: str】 玩家的实体ID
        """

    def EntityRemoveEvent(self, args):
        """
        实体被删除时触发。
        触发情景：实体从场景中被删除，例如：生物死亡，生物被清除 (opens new window)，玩家退出游戏，船/盔甲架被破坏，掉落物/经验球被捡起或清除。
        当生物随区块卸载时，不会触发该事件，而是ChunkAcquireDiscardedServerEvent事件。
        关于生物的清除：当生物离玩家大于wiki所说的距离，并且还在玩家的模拟距离内时，会被清除。也就是说，如果玩家瞬间传送到远处，原处的生物马上离开了模拟距离，并不会被清除。
        玩家退出游戏时，EntityRemoveEvent，DelServerPlayerEvent按顺序依次触发。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnScriptTickServer(self):
        """
        *tick*
        服务端tick事件，1秒30次。
        -----------------------------------------------------------
        无参数
        """

    # todo:====================================== New Event Callback ===================================================

    @listen("UiInitFinished")
    def UiInitFinished(self, args):
        """
        客户端玩家UI框架初始化完成时，服务端触发。
        -----------------------------------------------------------
        【__id__: str】 玩家的实体ID
        """

    @listen("OnGameTick")
    def OnGameTick(self, args):
        """
        *tick*
        触发帧率与房主玩家的游戏实时帧率同步的Tick事件。比如房主的游戏帧率为60帧，则该事件每秒触发60次。
        需要注意的是，因为受游戏帧率影响，该事件的触发帧率并不稳定。
        如果没有特殊需求，建议使用OnScriptTick。
        -----------------------------------------------------------
        无参数
        """

    # todo:======================================= Basic Function ======================================================

    # def TestMode(self, enable):
    #     # type: (bool) -> None
    #     """
    #     开启或关闭服务端测试模式。
    #     内容包括：
    #     1. 显示玩家坐标；
    #     2. 开启终为白日、保留物品栏、立即重生、作弊；
    #     3. 关闭天气更替；
    #     4. 屏蔽饥饿度；
    #     5. 夜视。
    #     -----------------------------------------------------------
    #     【enable: bool】 是否开启
    #     -----------------------------------------------------------
    #     NoReturn
    #     """
    #     if self.__timer:
    #         self.__timer.Destroy()
    #         self.__timer = None
    #         for p in _serverApi.GetPlayerList():
    #             _CompFactory.CreateGame(p).SetDisableHunger(False)
    #     if enable:
    #         @_ServerTimer.Repeat(1)
    #         def func():
    #             for _p in _serverApi.GetPlayerList():
    #                 _CompFactory.CreateEffect(_p).AddEffectToEntity(_EffectType.NIGHT_VISION, 12, 0, False)
    #                 _CompFactory.CreateGame(_p).SetDisableHunger(True)
    #         self.__timer = func()
    #     _LevelGameComp.SetGameRulesInfoServer({
    #         'option_info': {
    #             'show_coordinates': enable,
    #             'immediate_respawn': enable,
    #         },
    #         'cheat_info': {
    #             'always_day': enable,
    #             'keep_inventory': enable,
    #             'weather_cycle': not enable,
    #             'enable': enable,
    #         }
    #     })

    def ListenForEventV2(self, eventName, callback, t=0, namespace="", systemName="", priority=0):
        # type: (str, _MethodType, int, str, str, int) -> None
        """
        监听事件（简化版）。
        -----------------------------------------------------------
        【eventName: str】 事件名称
        【callback: Method】 回调函数（方法）
        【t: int = 0】 0表示监听当前Mod客户端传来的自定义事件，1表示监听服务端引擎事件，2表示监听其他Mod的事件
        【namespace: str = ""】 其他Mod的命名空间
        【systemName: str = ""】 其他Mod的系统名称
        【priority: int = 0】 优先级
        -----------------------------------------------------------
        NoReturn
        """
        if t == 0:
            namespace = _MOD_NAME
            systemName = _CLIENT_SYSTEM_NAME
        elif t == 1:
            namespace = _ENGINE_NAMESPACE
            systemName = _ENGINE_SYSTEM_NAME
        self.ListenForEvent(namespace, systemName, eventName, callback.__self__, callback, priority)

    def CallClient(self, playerId, name, callback=None, *args):
        # type: (str, str, _Callable[[...], None] | None, ...) -> None
        """
        调用客户端属性（包括变量和函数）。
        -----------------------------------------------------------
        【playerId: str】 客户端对应的玩家实体ID
        【name: str】 客户端属性名
        【callback: Optional[(Any) -> None] = None】 回调函数，调用客户端成功后客户端会返回结果并调用该函数，该函数接受一个参数，即调用结果，具体用法请看示例
        【*args: Any】 调用参数；如果调用的客户端属性为变量，则args会赋值给该变量（不写调用参数则不会进行赋值）；如果调用的客户端属性为函数，则args会作为参数传入该函数
        -----------------------------------------------------------
        NoReturn
        """

    # todo:====================================== Internal Method ======================================================

    @listen("_BroadcastToAllClient")
    def _OnBroadcastToAllClient(self, args):
        eventName = args['eventName']
        eventData = args['eventData']
        if isinstance(eventData, dict) and '__id__' in args:
            eventData['__id__'] = args['__id__']
        self.BroadcastToAllClient(eventName, eventData)

    @listen("UiInitFinished", priority=1)
    def _OnUiInitFinished(self, args):
        playerId = args['__id__']
        self.allPlayerData[playerId] = {}
        if self.homeownerPlayerId == "-1":
            self.homeownerPlayerId = playerId
            if self._listenGameTick:
                self.NotifyToClient(self.homeownerPlayerId, "_ListenServerGameTick", {})

    def __listen(self):
        for args in _lsnFuncArgs:
            args[1] = getattr(self, args[1])
            self.ListenForEventV2(*args)
        for event in ALL_ENGINE_EVENTS:
            if _is_method_overridden(self.__class__, NuoyanServerSystem, event):
                self.ListenForEventV2(event, getattr(self, event), 1)

    def _listenForGameTickEvent(self):
        if self._listenGameTick:
            return
        self._listenGameTick = True
        if self.homeownerPlayerId != "-1":
            self.NotifyToClient(self.homeownerPlayerId, "_ListenServerGameTick", {})

    def _checkOnGameTick(self):
        if _is_method_overridden(self.__class__, NuoyanServerSystem, "OnGameTick"):
            self._listenForGameTickEvent()

    def _onPlayerLeave(self, args):
        playerId = args['playerId']
        if playerId in self.allPlayerData:
            del self.allPlayerData[playerId]
























