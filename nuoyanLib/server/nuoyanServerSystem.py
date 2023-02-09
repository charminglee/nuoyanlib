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
#   Last Modified : 2023-02-08
#
# ====================================================


from types import MethodType as _MethodType
from collections import Callable as _Callable
from ..utils.utils import is_method_overridden as _is_method_overridden
from .._config import CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME, MOD_NAME as _MOD_NAME, \
    SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME
from serverTimer import ServerTimer as _ServerTimer
try:
    import mod.server.extraServerApi as _serverApi
except:
    pass


__all__ = [
    "listen",
    "NuoyanServerSystem",
    "ALL_ENGINE_EVENTS",
]


try:
    _ENGINE_NAMESPACE = _serverApi.GetEngineNamespace()
    _ENGINE_SYSTEM_NAME = _serverApi.GetEngineSystemName()
    _LEVEL_ID = _serverApi.GetLevelId()
    _ServerSystem = _serverApi.GetServerSystemCls()
    _CompFactory = _serverApi.GetEngineCompFactory()
    _LevelGameComp = _CompFactory.CreateGame(_LEVEL_ID)
except:
    from ..mctypes.server.system.serverSystem import ServerSystem
    _ServerSystem = ServerSystem  # type: type[ServerSystem]
    _ENGINE_NAMESPACE = ""
    _ENGINE_SYSTEM_NAME = ""
    _LevelGameComp = None


ALL_ENGINE_EVENTS = (
    ("OnScriptTickServer", "OnScriptTick"),
    ("EntityRemoveEvent", "OnEntityRemove"),
    ("OnCarriedNewItemChangedServerEvent", "OnCarriedNewItemChanged"),
    ("ProjectileDoHitEffectEvent", "OnProjectileDoHitEffect"),
    ("ExplosionServerEvent", "OnExplosion"),
    ("DamageEvent", "OnDamage"),
    ("DestroyBlockEvent", "OnDestroyBlock"),
    ("ActorAcquiredItemServerEvent", "OnActorAcquiredItem"),
    ("ActorUseItemServerEvent", "OnActorUseItem"),
    ("ServerItemUseOnEvent", "OnItemUseOn"),
    ("EntityStartRidingEvent", "OnEntityStartRiding"),
    ("EntityStopRidingEvent", "OnEntityStopRiding"),
    ("OnEntityInsideBlockServerEvent", "OnEntityInsideBlock"),
    ("OnMobHitBlockServerEvent", "OnMobHitBlock"),
    ("AddEntityServerEvent", "OnAddEntity"),
)


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
    【t: int = 0】 0表示监听服务端传来的自定义事件，1表示监听客户端引擎事件，2表示监听其他Mod的事件
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
    3. OnHotUpdate：服务端热更时触发
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
        self.__listen()
        self._checkOnGameTick()

    def Destroy(self):
        """
        服务端系统销毁时触发。
        """
        self.UnListenAllEvents()

    # todo:==================================== Engine Event Callback ==================================================

    def OnAddEntity(self, args):
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

    def OnMobHitBlock(self, args):
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

    def OnEntityInsideBlock(self, args):
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

    def OnEntityStartRiding(self, args):
        """
        当实体骑乘上另一个实体时触发。
        -----------------------------------------------------------
        【id: str】 骑乘者实体ID
        【rideId: str】 坐骑实体ID
        """

    def OnEntityStopRiding(self, args):
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

    def OnItemUseOn(self, args):
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

    def OnActorUseItem(self, args):
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

    def OnActorAcquiredItem(self, args):
        """
        玩家获得物品时服务端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点）。
        -----------------------------------------------------------
        【actor: str】 获得物品玩家实体ID
        【secondaryActor: str】 物品给予者玩家实体ID，如果不存在给予者的话，这里为空字符串
        【itemDict: dict】 获得的物品的物品信息字典
        【acquireMethod: int】 获得物品的方法，详见ItemAcquisitionMethod枚举
        """

    def OnDestroyBlock(self, args):
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

    def OnDamage(self, args):
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

    def OnExplosion(self, args):
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

    def OnProjectileDoHitEffect(self, args):
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

    def OnCarriedNewItemChanged(self, args):
        """
        玩家切换主手物品时触发该事件。
        切换耐久度不同的相同物品，不会触发该事件。
        -----------------------------------------------------------
        【oldItemDict: Optional[dict]】 旧物品的物品信息字典，当旧物品为空时，此项属性为None
        【newItemDict: Optional[dict]】 新物品的物品信息字典，当新物品为空时，此项属性为None
        【playerId: str】 玩家的实体ID
        """

    def OnEntityRemove(self, args):
        """
        实体被删除时触发。
        触发情景：实体从场景中被删除，例如：生物死亡，生物被清除 (opens new window)，玩家退出游戏，船/盔甲架被破坏，掉落物/经验球被捡起或清除。
        当生物随区块卸载时，不会触发该事件，而是ChunkAcquireDiscardedServerEvent事件。
        关于生物的清除：当生物离玩家大于wiki所说的距离，并且还在玩家的模拟距离内时，会被清除。也就是说，如果玩家瞬间传送到远处，原处的生物马上离开了模拟距离，并不会被清除。
        玩家退出游戏时，EntityRemoveEvent，DelServerPlayerEvent按顺序依次触发。
        -----------------------------------------------------------
        【id: str】 实体ID
        """

    def OnScriptTick(self):
        """
        *tick*
        服务端tick事件，1秒30次。
        -----------------------------------------------------------
        无参数
        """

    # todo:==================================== Custom Event Callback ==================================================

    def OnHotUpdate(self):
        """
        服务端热更时触发。
        -----------------------------------------------------------
        无参数
        """

    @listen("UiInitFinished")
    def OnUiInitFinished(self, args):
        """
        客户端玩家UI框架初始化完成时，服务端触发。
        -----------------------------------------------------------
        【__id__: str】 玩家的实体ID
        """

    def OnPlayerLeave(self, args):
        """
        玩家退出游戏时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
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
        示例：

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
        for event, callback in ALL_ENGINE_EVENTS:
            if _is_method_overridden(self.__class__, NuoyanServerSystem, callback):
                self.ListenForEventV2(event, getattr(self, callback), 1)

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


try:
    _ins = _serverApi.GetSystem(_MOD_NAME, _SERVER_SYSTEM_NAME)  # type: NuoyanServerSystem
    if _ins:
        _LevelGameComp.AddTimer(0, _ins.OnHotUpdate)
except:
    pass


def _test():
    pass




















