# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-14
#
# ====================================================


from collections import Callable as _Callable
import mod.server.extraServerApi as _serverApi
from ..util.util import is_method_overridden as _is_method_overridden
from .._config import CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME


_ENGINE_NAMESPACE = _serverApi.GetEngineNamespace()
_ENGINE_SYSTEM_NAME = _serverApi.GetEngineSystemName()
_LEVEL_ID = _serverApi.GetLevelId()


_ServerSystem = _serverApi.GetServerSystemCls()


ALL_SYSTEM_EVENTS = [
    ("OnScriptTickServer", "OnScriptTick"),
    ("EntityRemoveEvent", "OnEntityRemove"),
    ("OnCarriedNewItemChangedServerEvent", "OnCarriedNewItemChanged"),
    ("ProjectileDoHitEffectEvent", "OnProjectileDoHitEffect"),
    ("ExplosionServerEvent", "OnExplosion"),
    ("DamageEvent", "OnDamage"),
    ("DestroyBlockEvent", "OnDestroyBlock"),
    ("ActorAcquiredItemServerEvent", "OnActorAcquiredItem"),
    ("ActorUseItemServerEvent", "OnActorUseItem"),
]


# noinspection PyUnresolvedReferences
class NuoyanServerSystem(_ServerSystem):
    """
    ServerSystem扩展类。将自定义ServerSystem继承本类即可使用本类的全部功能。
    -----------------------------------------------------------
    【基础功能】
    1. 所有官方文档中收录的服务端引擎事件以及新增事件均无需手动监听，只需重写对应事件的回调函数即可（支持热更）；
    回调函数的命名规则为：On+去掉“Server”、“Event”、“On”字眼的事件名；
    如：OnScriptTickServer -> OnScriptTick、OnCarriedNewItemChangedServerEvent -> OnCarriedNewItemChanged、EntityRemoveEvent -> OnEntityRemove等；
    2. 支持对在__init__方法中新增的事件监听或服务端属性（变量）执行热更；
    3. 一键调用客户端属性（变量）、方法（函数）；
    4. 无需重写Destroy方法进行事件的反监听。
    -----------------------------------------------------------
    【新增方法】
    1. ListenForEventV2：监听事件（简化版）
    -----------------------------------------------------------
    【新增事件】
    1. UiInitFinished：客户端玩家UI框架初始化完成时，服务端触发
    2. GameTick：频率与游戏当前帧率同步的Tick事件
    -----------------------------------------------------------
    【新增属性】
    1. allPlayerData：用于保存所有玩家数据的字典，key为玩家实体ID，value为玩家数据字典，可自行添加数据；
    玩家加入游戏时（UiInitFinished后）会自动把玩家加入字典，玩家退出游戏时则会自动从字典中删除玩家及其数据；初始值为空字典
    2. homeownerPlayerId：房主玩家的实体ID；初始值为None
    -----------------------------------------------------------
    【注意事项】
    1. 带有*tick*标签的事件为帧事件，需要注意编写相关逻辑；
    2. 事件回调参数中，参数名前面的美元符号“$”表示该参数可进行修改。
    """

    def __init__(self, namespace, systemName):
        super(NuoyanServerSystem, self).__init__(namespace, systemName)
        self._namespace = namespace
        self._systemName = systemName
        self._listen()
        self.allPlayerData = {}
        self._listenGameTick = False
        self.homeownerPlayerId = None
        self._checkOnGameTick()
        self._tick = 0
        self._oldInitFunc = self.__init__
        self.test()
        self._initFinished = 1

    # def __setattr__(self, name, value):
    #     callFunc = _stack()[1][3]
    #     if callFunc == "__init__" and name in self.__dict__:
    #         return
    #     self.__dict__[name] = value
    #     if callFunc == "__init__":
    #         print "__setattr__: " + name
    #
    # def __getattribute__(self, name):
    #     callFunc = _stack()[1][3]
    #     if callFunc == "__init__" and '_initFinished' in object.__getattribute__(self, "__dict__"):
    #         return object.__getattribute__(self, "_emptyFunc")
    #     if callFunc == "__init__":
    #         print "__getattribute__: " + name
    #     return object.__getattribute__(self, name)

    def _listen(self):
        for event, callback in ALL_SYSTEM_EVENTS:
            if _is_method_overridden(self.__class__, NuoyanServerSystem, callback):
                self.ListenForEventV2(event, getattr(self, callback), 1)
        self.ListenForEventV2("GameTick", self.OnGameTick)
        self.ListenForEventV2("UiInitFinished", self._onUiInitFinished, priority=1)
        self.ListenForEventV2("UiInitFinished", self.OnUiInitFinished)
        self.ListenForEventV2("_BroadcastToAllClient", self._broadcastToAllClient)
        self.ListenForEventV2("OnScriptTickServer", self._onTick, 1)

    def Destroy(self):
        """
        服务端系统销毁时触发。
        """
        self.UnListenAllEvents()

    # todo:==================================== System Event Callback ==================================================

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
        pass

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
        pass

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
        pass

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
        pass

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
        pass

    def OnCarriedNewItemChanged(self, args):
        """
        玩家切换主手物品时触发该事件。
        切换耐久度不同的相同物品，不会触发该事件。
        -----------------------------------------------------------
        【oldItemDict: Optional[dict]】 旧物品的物品信息字典，当旧物品为空时，此项属性为None
        【newItemDict: Optional[dict]】 新物品的物品信息字典，当新物品为空时，此项属性为None
        【playerId: str】 玩家的实体ID
        """
        pass

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
        pass

    def OnScriptTick(self):
        """
        *tick*
        服务端tick事件，1秒30次。
        -----------------------------------------------------------
        无参数
        """
        pass

    # todo:==================================== Custom Event Callback ==================================================

    def OnUiInitFinished(self, args):
        """
        客户端玩家UI框架初始化完成时，服务端触发。
        -----------------------------------------------------------
        【__id__: str】 玩家的实体ID
        """
        pass

    def OnPlayerLeave(self, args):
        """
        玩家退出游戏时触发。
        -----------------------------------------------------------
        【playerId: str】 玩家的实体ID
        """
        pass

    def OnGameTick(self, args):
        """
        *tick*
        触发帧率与房主玩家的游戏实时帧率同步的Tick事件。比如房主的游戏帧率为60帧，则该事件每秒触发60次。
        需要注意的是，因为受游戏帧率影响，该事件的触发帧率并不稳定。
        如果没有特殊需求，建议使用OnScriptTick。
        -----------------------------------------------------------
        无参数
        """
        pass

    # todo:======================================= Basic Function ======================================================

    def ListenForEventV2(self, eventName, callback, t=0, namespace="", systemName="", priority=0):
        # type: (str, _Callable[[Any], None], int, str, str, int) -> None
        """
        监听事件（简化版）。
        -----------------------------------------------------------
        【eventName: str】 事件名称
        【callback: (Any) -> None】 回调函数
        【t: int = 0】 0表示监听当前Mod客户端传来的自定义事件，1表示监听当前Mod服务端引擎事件，2表示监听其他Mod的事件
        【namespace: str = ""】 其他Mod的命名空间
        【systemName: str = ""】 其他Mod的系统名称
        【priority: int = 0】 优先级
        -----------------------------------------------------------
        return -> None
        """
        if t == 0:
            namespace = self._namespace
            systemName = _CLIENT_SYSTEM_NAME
        elif t == 1:
            namespace = _ENGINE_NAMESPACE
            systemName = _ENGINE_SYSTEM_NAME
        self.ListenForEvent(namespace, systemName, eventName, callback.__self__, callback, priority)

    # todo:====================================== Internal Method ======================================================

    def _broadcastToAllClient(self, args):
        eventName = args['eventName']
        eventData = args['eventData']
        if isinstance(eventData, dict) and '__id__' in args:
            eventData['__id__'] = args['__id__']
        self.BroadcastToAllClient(eventName, eventData)

    def _listenForGameTickEvent(self):
        if self._listenGameTick:
            return
        self._listenGameTick = True
        if self.homeownerPlayerId:
            self.NotifyToClient(self.homeownerPlayerId, "_ListenServerGameTick", {})

    def _checkOnGameTick(self):
        if _is_method_overridden(self.__class__, NuoyanServerSystem, "OnGameTick"):
            self._listenForGameTickEvent()

    def _onUiInitFinished(self, args):
        playerId = args['__id__']
        self.allPlayerData[playerId] = {}
        if not self.homeownerPlayerId:
            self.homeownerPlayerId = playerId
            if self._listenGameTick:
                self.NotifyToClient(self.homeownerPlayerId, "_ListenServerGameTick", {})

    def _onPlayerLeave(self, args):
        playerId = args['playerId']
        if playerId in self.allPlayerData:
            del self.allPlayerData[playerId]

    def _onTick(self):
        self._tick += 1
        if not self._tick % 30 and self.__init__ != self._oldInitFunc:
            self.__init__(self._namespace, self._systemName)
            self._oldInitFunc = self.__init__
            print "_onTick"

    def test(self):
        print "test"

    def _emptyFunc(self, *args, **kwargs):
        pass





















