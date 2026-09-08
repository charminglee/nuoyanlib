# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


if bool(0):
    from typing import Any


import traceback
import bisect
from types import MethodType, FunctionType
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from . import error, _env, _logging
from ._utils import iter_obj_attrs, DefaultLocal
from ..config import ENABLED_EVENT_ARGS_WARPPING


__all__ = [
    "ALL_CLIENT_LIB_EVENTS",
    "ALL_SERVER_LIB_EVENTS",
    "event",
    "listen_event",
    "unlisten_event",
    "listen_all_events",
    "unlisten_all_events",
    "is_listened",
    "EventArgsWrapper",
]


ALL_CLIENT_LIB_EVENTS = {}
ALL_SERVER_LIB_EVENTS = {
    # 'ItemGridChangedServerEvent': _env.LIB_CLIENT_NAME,
    'UiInitFinished': _env.LIB_CLIENT_NAME,
}
ALL_CLIENT_ENGINE_EVENTS = {
    "OnSimTickClientEvent",
    "PhysxTriggerClientEvent",
    "LiquidClippedClientEvent",
    "PlayerAddCustomContainerItemClientEvent",
    "PlayerRemoveCustomContainerItemClientEvent",
    "PhysxTouchClientEvent",
    "OnCustomGamepadChangedEvent",
    "OnCustomGamepadPressInGame",
    "OnCustomKeyChangedEvent",
    "OnCustomKeyPressInGame",
    "UIDefReloadSceneStackAfter",
    "UpdatePlayerSkinClientEvent",
    "PlayerTryRemoveCustomContainerItemClientEvent",
    "PlayerTryAddCustomContainerItemClientEvent",
    "PlayerTryPutCustomContainerItemClientEvent",
    "PlayerPermissionChangeClientEvent",
    "HudButtonChangedClientEvent",
    "BlockAnimateRandomTickEvent",
    "PlayerAttackEntityEvent",
    "OnLocalPlayerActionClientEvent",
    "OnLocalPlayerStartJumpClientEvent",
    "GameRenderTickEvent",
    "GyroSensorChangedClientEvent",
    "ModBlockEntityTickClientEvent",
    "ModBlockEntityRemoveClientEvent",
    "AchievementButtonMovedClientEvent",
    "OnKeyboardControllerLayoutChangeClientEvent",
    "OnGamepadControllerLayoutChangeClientEvent",
    "OnGamepadTriggerClientEvent",
    "OnGamepadStickClientEvent",
    "OnGamepadKeyPressClientEvent",
    "ModBlockEntityLoadedClientEvent",
    "CloseNeteaseShopEvent",
    "PopScreenAfterClientEvent",
    "TapOrHoldReleaseClientEvent",
    "TapBeforeClientEvent",
    "RightClickReleaseClientEvent",
    "RightClickBeforeClientEvent",
    "OnMouseMiddleDownClientEvent",
    "OnKeyPressInGame",
    "OnClientPlayerStopMove",
    "OnClientPlayerStartMove",
    "OnBackButtonReleaseClientEvent",
    "MouseWheelClientEvent",
    "LeftClickReleaseClientEvent",
    "LeftClickBeforeClientEvent",
    "HoldBeforeClientEvent",
    "GetEntityByCoordReleaseClientEvent",
    "GetEntityByCoordEvent",
    "ClientJumpButtonReleaseEvent",
    "ClientJumpButtonPressDownEvent",
    "PlaySoundClientEvent",
    "PlayMusicClientEvent",
    "OnMusicStopClientEvent",
    "ScreenSizeChangedClientEvent",
    "PushScreenEvent",
    "PopScreenEvent",
    "PlayerChatButtonClickClientEvent",
    "OnItemSlotButtonClickedEvent",
    "GridComponentSizeChangedClientEvent",
    "ClientPlayerInventoryOpenEvent",
    "ClientPlayerInventoryCloseEvent",
    "ClientChestOpenEvent",
    "ClientChestCloseEvent",
    "WalkAnimEndClientEvent",
    "WalkAnimBeginClientEvent",
    "AttackAnimEndClientEvent",
    "AttackAnimBeginClientEvent",
    "StopUsingItemClientEvent",
    "StartUsingItemClientEvent",
    "PlayerTryDropItemClientEvent",
    "OnCarriedNewItemChangedClientEvent",
    "ItemReleaseUsingClientEvent",
    "InventoryItemChangedClientEvent",
    "GrindStoneRemovedEnchantClientEvent",
    "ClientShapedRecipeTriggeredEvent",
    "ClientItemUseOnEvent",
    "ClientItemTryUseEvent",
    "AnvilCreateResultItemAfterClientEvent",
    "ActorUseItemClientEvent",
    "ActorAcquiredItemClientEvent",
    "StepOnBlockClientEvent",
    "StartDestroyBlockClientEvent",
    "StepOffBlockClientEvent",
    "ShearsDestoryBlockBeforeClientEvent",
    "PlayerTryDestroyBlockClientEvent",
    "OnStandOnBlockClientEvent",
    "OnModBlockNeteaseEffectCreatedClientEvent",
    "OnEntityInsideBlockClientEvent",
    "OnAfterFallOnBlockClientEvent",
    "FallingBlockCauseDamageBeforeClientEvent",
    "ClientBlockUseEvent",
    "PerspChangeClientEvent",
    "OnPlayerHitBlockClientEvent",
    "GameTypeChangedClientEvent",
    "ExtinguishFireClientEvent",
    "DimensionChangeFinishClientEvent",
    "DimensionChangeClientEvent",
    "CameraMotionStopClientEvent",
    "CameraMotionStartClientEvent",
    "LeaveEntityClientEvent",
    "StartRidingClientEvent",
    "OnMobHitMobClientEvent",
    "OnGroundClientEvent",
    "HealthChangeClientEvent",
    "EntityStopRidingEvent",
    "EntityModelChangedClientEvent",
    "ApproachEntityClientEvent",
    "UnLoadClientAddonScriptsBefore",
    "RemovePlayerAOIClientEvent",
    "RemoveEntityClientEvent",
    "OnLocalPlayerStopLoading",
    "OnCommandOutputClientEvent",
    "LoadClientAddonScriptsAfter",
    "ChunkLoadedClientEvent",
    "ChunkAcquireDiscardedClientEvent",
    "AddPlayerCreatedClientEvent",
    "AddPlayerAOIClientEvent",
    "AddEntityClientEvent",
    "OnScriptTickClient",
    "UiInitFinished",
}
ALL_SERVER_ENGINE_EVENTS = {
    "OnSimTickServerEvent",
    "PlayerStartFishingServerEvent",
    "PlayerFishingAfterServerEvent",
    "PlayerFishingServerEvent",
    "PhysxTriggerServerEvent",
    "LiquidClippedServerEvent",
    "PlayerAddCustomContainerItemServerEvent",
    "PlayerRemoveCustomContainerItemServerEvent",
    "PhysxTouchServerEvent",
    "ItemPullOutCustomContainerServerEvent",
    "ItemPushInCustomContainerServerEvent",
    "PlayerPermissionChangeServerEvent",
    "PlayerTryRemoveCustomContainerItemServerEvent",
    "PlayerTryAddCustomContainerItemServerEvent",
    "PlayerTryPutCustomContainerItemServerEvent",
    "MountTamingEvent",
    "OnPlayerActionServerEvent",
    "CustomCommandTriggerServerEvent",
    "GlobalCommandServerEvent",
    "PlayerPickupArrowServerEvent",
    "EntityDieLoottableAfterServerEvent",
    "PlayerHungerChangeServerEvent",
    "ItemDurabilityChangedServerEvent",
    "PlaceNeteaseLargeFeatureServerEvent",
    "PlayerNamedEntityServerEvent",
    "PlayerFeedEntityServerEvent",
    "lobbyGoodBuySucServerEvent",
    "UrgeShipEvent",
    "PlayerInventoryOpenScriptServerEvent",
    "WalkAnimEndServerEvent",
    "WalkAnimBeginServerEvent",
    "JumpAnimBeginServerEvent",
    "AttackAnimEndServerEvent",
    "AttackAnimBeginServerEvent",
    "UIContainerItemChangedServerEvent",
    "ShearsUseToBlockBeforeServerEvent",
    "ServerPlayerTryTouchEvent",
    "ServerItemTryUseEvent",
    "PlayerDropItemServerEvent",
    "OnPlayerBlockedByShieldBeforeServerEvent",
    "OnPlayerBlockedByShieldAfterServerEvent",
    "OnPlayerActiveShieldServerEvent",
    "OnOffhandItemChangedServerEvent",
    "OnNewArmorExchangeServerEvent",
    "OnItemPutInEnchantingModelServerEvent",
    "ItemUseOnAfterServerEvent",
    "ItemUseAfterServerEvent",
    "ItemReleaseUsingServerEvent",
    "InventoryItemChangedServerEvent",
    "FurnaceBurnFinishedServerEvent",
    "CraftItemOutputChangeServerEvent",
    "ContainerItemChangedServerEvent",
    "StepOnBlockServerEvent",
    "StepOffBlockServerEvent",
    "StartDestroyBlockServerEvent",
    "ShearsDestoryBlockBeforeServerEvent",
    "ServerPlayerTryDestroyBlockEvent",
    "ServerPlaceBlockEntityEvent",
    "ServerEntityTryPlaceBlockEvent",
    "ServerBlockEntityTickEvent",
    "PistonActionServerEvent",
    "OnStandOnBlockServerEvent",
    "OnBeforeFallOnBlockServerEvent",
    "OnAfterFallOnBlockServerEvent",
    "HopperTryPullOutServerEvent",
    "HopperTryPullInServerEvent",
    "HeavyBlockStartFallingServerEvent",
    "GrassBlockToDirtBlockServerEvent",
    "FarmBlockToDirtBlockServerEvent",
    "FallingBlockReturnHeavyBlockServerEvent",
    "FallingBlockCauseDamageBeforeServerEvent",
    "FallingBlockBreakServerEvent",
    "EntityPlaceBlockAfterServerEvent",
    "DirtBlockToGrassBlockServerEvent",
    "CommandBlockUpdateEvent",
    "CommandBlockContainerOpenEvent",
    "ChestBlockTryPairWithServerEvent",
    "BlockStrengthChangedServerEvent",
    "BlockSnowStateChangeServerEvent",
    "BlockSnowStateChangeAfterServerEvent",
    "BlockRemoveServerEvent",
    "BlockRandomTickServerEvent",
    "BlockNeighborChangedServerEvent",
    "BlockLiquidStateChangeServerEvent",
    "BlockLiquidStateChangeAfterServerEvent",
    "BlockDestroyByLiquidServerEvent",
    "StoreBuySuccServerEvent",
    "ServerPlayerGetExperienceOrbEvent",
    "PlayerTrySleepServerEvent",
    "PlayerTeleportEvent",
    "PlayerStopSleepServerEvent",
    "PlayerSleepServerEvent",
    "PlayerRespawnFinishServerEvent",
    "PlayerRespawnEvent",
    "PlayerHurtEvent",
    "PlayerEatFoodServerEvent",
    "PlayerDieEvent",
    "OnPlayerHitBlockServerEvent",
    "GameTypeChangedServerEvent",
    "ExtinguishFireServerEvent",
    "DimensionChangeServerEvent",
    "ChangeLevelUpCostServerEvent",
    "AddLevelEvent",
    "AddExpEvent",
    "WillTeleportToServerEvent",
    "WillAddEffectServerEvent",
    "StartRidingServerEvent",
    "RemoveEffectServerEvent",
    "RefreshEffectServerEvent",
    "ProjectileCritHitEvent",
    "OnMobHitMobServerEvent",
    "OnKnockBackServerEvent",
    "OnFireHurtEvent",
    "MobGriefingBlockServerEvent",
    "HealthChangeServerEvent",
    "EntityTickServerEvent",
    "EntityPickupItemServerEvent",
    "EntityMotionStopServerEvent",
    "EntityMotionStartServerEvent",
    "EntityLoadScriptEvent",
    "EntityEffectDamageServerEvent",
    "EntityDroppedItemServerEvent",
    "EntityChangeDimensionServerEvent",
    "ChangeSwimStateServerEvent",
    "AddEffectServerEvent",
    "ActorHurtServerEvent",
    "ServerSpawnMobEvent",
    "ServerPreBlockPatternEvent",
    "ServerPostBlockPatternEvent",
    "ServerChatEvent",
    "PlayerLeftMessageServerEvent",
    "PlayerJoinMessageEvent",
    "PlayerIntendLeaveServerEvent",
    "PlaceNeteaseStructureFeatureEvent",
    "OnRainLevelChangeServerEvent",
    "OnLocalRainLevelChangeServerEvent",
    "OnLocalLightningLevelChangeServerEvent",
    "OnLightningLevelChangeServerEvent",
    "OnContainerFillLoottableServerEvent",
    "OnCommandOutputServerEvent",
    "NewOnEntityAreaEvent",
    "LoadServerAddonScriptsAfter",
    "DelServerPlayerEvent",
    "CommandEvent",
    "ClientLoadAddonsFinishServerEvent",
    "ChunkLoadedServerEvent",
    "ChunkGeneratedServerEvent",
    "ChunkAcquireDiscardedServerEvent",
    "AddServerPlayerEvent",
    "AchievementCompleteEvent",
    "PlayerAttackEntityEvent",
    "ServerBlockUseEvent",
    "OnGroundServerEvent",
    "SpawnProjectileServerEvent",
    "EntityDieLoottableServerEvent",
    "ActuallyHurtServerEvent",
    "HealthChangeBeforeServerEvent",
    "DimensionChangeFinishServerEvent",
    "EntityDefinitionsEventServerEvent",
    "PlayerDoInteractServerEvent",
    "PlayerInteractServerEvent",
    "MobDieEvent",
    "AddEntityServerEvent",
    "OnMobHitBlockServerEvent",
    "OnEntityInsideBlockServerEvent",
    "EntityStartRidingEvent",
    "EntityStopRidingEvent",
    "ServerItemUseOnEvent",
    "ActorUseItemServerEvent",
    "ActorAcquiredItemServerEvent",
    "DestroyBlockEvent",
    "DamageEvent",
    "ExplosionServerEvent",
    "ProjectileDoHitEffectEvent",
    "OnCarriedNewItemChangedServerEvent",
    "EntityRemoveEvent",
    "OnScriptTickServer",
    "UiInitFinished",
}


def _get_event_source(is_client, event_name):
    if is_client:
        if event_name in ALL_CLIENT_LIB_EVENTS:
            return _env.LIB_NAME, ALL_CLIENT_LIB_EVENTS[event_name]
        if event_name in ALL_CLIENT_ENGINE_EVENTS:
            return c_api.GetEngineNamespace(), c_api.GetEngineSystemName()
        # if event_name in ALL_SERVER_ENGINE_EVENTS:
        #     return s_api.GetEngineNamespace(), s_api.GetEngineSystemName()
    else:
        if event_name in ALL_SERVER_LIB_EVENTS:
            return _env.LIB_NAME, ALL_SERVER_LIB_EVENTS[event_name]
        if event_name in ALL_SERVER_ENGINE_EVENTS:
            return s_api.GetEngineNamespace(), s_api.GetEngineSystemName()
        # if event_name in ALL_CLIENT_ENGINE_EVENTS:
        #     return c_api.GetEngineNamespace(), c_api.GetEngineSystemName()


def _parse_listen_args(func, event_name, ns, sys_name):
    if not event_name or not isinstance(event_name, str):
        event_name = func.__name__
    if ns and sys_name:
        return event_name, ns, sys_name
    elif not ns and sys_name:
        return event_name, _env.MOD_NAME, sys_name
    elif ns and not sys_name:
        raise error.EventSourceError(event_name, ns, sys_name)
    else:
        source = _get_event_source(_env.is_client(), event_name)
        if source:
            return event_name, source[0], source[1]
        raise error.EventSourceError(event_name, ns, sys_name)
        # import warnings
        # warnings.warn(str(error.EventSourceError(event_name, ns, sys_name)))


def _get_listen_args(func):
    if isinstance(func, MethodType):
        func = func.__func__
    return getattr(func, '_nyl__listen_args', None)
    
    
_L = DefaultLocal(dict)


def _make_event_init(org_init):
    def init(self, *args, **kwargs):
        if org_init:
            org_init(self, *args, **kwargs)
        if not hasattr(self, '_nyl__is_listened'):
            listen_all_events(self)
            self._nyl__is_listened = True
            _logging.debug(
                "Instance listening complete: %s.%s",
                self.__class__.__module__, self.__class__.__name__
            )
    return init


def _process_event_listen():
    module_globals = _L.module_globals

    for g in module_globals.values():
        for v in g.values():
            # 处理静态函数
            if isinstance(v, FunctionType):
                args = _get_listen_args(v)
                if args:
                    for a in args:
                        _EventPool.listen(v, *a)

            # 处理类方法，让类实例在初始化时自动调用listen_all_events
            elif isinstance(v, type):
                hook = False
                # 判断类是否有被@event装饰的方法
                for method in v.__dict__.values():
                    if _get_listen_args(method):
                        hook = True
                        break
                if hook and not v.__dict__.get('_nyl__event_init_hooked'):
                    v.__init__ = _make_event_init(getattr(v, '__init__', None))
                    v._nyl__event_init_hooked = True
                    _logging.debug("Hooked __init__() of %s for event listening" % v.__name__)

    module_globals.clear()


def event(event_name="", ns="", sys_name="", priority=0, is_method=True):
    """
    [装饰器]

    监听事件。

    支持静态函数和类方法。

    示例
    ----

    >>> class MyClientSystem(nyl.NyClientSystem):
    ...     def __init__(self, namespace, system_name):
    ...         super(MyClientSystem, self).__init__(namespace, system_name)
    ...
    ...     # 监听MyCustomEvent自定义事件，事件来源为MyMod:MyServerSystem
    ...     @nyl.event("MyCustomEvent", "MyMod", "MyServerSystem")
    ...     def EventCallback(self, args):
    ...         pass
    ...
    ...    # 函数名与事件名相同时，可省略event_name参数
    ...    @nyl.event(ns="MyMod", sys_name="MyServerSystem")
    ...    def MyCustomEvent(self, args):
    ...        pass
    ...
    ...     # 监听ModSDK事件且函数名与事件名相同时，可省略所有参数
    ...     @nyl.event
    ...     def UiInitFinished(self, args):
    ...         pass
    ...
    ...     def Destroy(self):
    ...         # 默认情况下，「nuoyanlib」会在客户端/服务端销毁时自动反监听所有监听过的事件
    ...         # 必要时，调用以下函数可取消当前类中所有被@event装饰的方法的事件监听
    ...         nyl.unlisten_all_events(self)
    ...         # 调用以下函数可取消监听特定事件
    ...         # nyl.unlisten_event(self.MyCustomEvent)

    对静态函数使用示例：

    >>> @nyl.event(ns="MyMod", sys_name="MyServerSystem")
    ... def MyCustomEvent(args):
    ...     pass

    参见
    ----

    - ``listen_event()`` -- 监听指定事件。
    - ``unlisten_event()`` -- 反监听指定事件。
    - ``listen_all_events()`` -- 监听当前类中所有被 @event 装饰的方法。
    - ``unlisten_all_events()`` -- 反监听当前类中所有被 @event 装饰的方法。
    - ``is_listened()`` -- 判断指定事件是否被监听。

    -----

    :param str|function event_name: 事件名称；默认为被装饰函数名
    :param str ns: 事件来源命名空间；默认为当前模组名称，如需监听其他模组可手动传入；监听 ModSDK 事件时，可省略该参数
    :param str sys_name: 事件来源系统名称；监听 ModSDK 事件时，可省略该参数
    :param int priority: 优先级，值越大优先级越高；默认为 0
    :param bool is_method: [已废弃] 被装饰函数是否是实例方法；默认为 True
    """
    def add_listener(func):
        if func.__module__ not in _L.module_globals:
            _L.module_globals[func.__module__] = func.__globals__
        args = _parse_listen_args(func, event_name, ns, sys_name)
        if not hasattr(func, '_nyl__listen_args'):
            func._nyl__listen_args = []
        func._nyl__listen_args.append(args + (priority,))
        # 非实例方法，立即执行监听
        # if not is_method:
        #     _EventPool.listen(func, *args, priority=priority)
        return func
    # @event(...)
    if isinstance(event_name, str):
        return add_listener
    # @event
    else:
        return add_listener(event_name) # noqa


def listen_event(func, event_name="", ns="", sys_name="", priority=0, use_decorator=False):
    """
    监听事件。

    参见
    ----

    - ``@event`` -- 事件监听装饰器。
    - ``unlisten_event()`` -- 反监听指定事件。
    - ``listen_all_events()`` -- 监听当前类中所有被 @event 装饰的方法。
    - ``is_listened()`` -- 判断指定事件是否被监听。

    -----

    :param function func: 事件回调函数，支持普通函数与实例方法
    :param str event_name: 事件名称；事件名与函数名相同时，可省略该参数
    :param str ns: 事件来源命名空间；默认为当前模组名称，如需监听其他模组可手动传入；监听 ModSDK 事件时，可省略该参数
    :param str sys_name: 事件来源系统名称；监听 ModSDK 事件时，可省略该参数
    :param int priority: 优先级，值越大优先级越高；默认为 0
    :param bool use_decorator: 是否使用从 @event 装饰器传入的参数，设为 True 时，忽略 event_name、ns、sys_name 和 priority 参数；默认为 False

    :return: 无
    :rtype: None
    """
    if use_decorator:
        all_args = _get_listen_args(func)
        for args in all_args:
            _EventPool.listen(func, *args)
    else:
        args = _parse_listen_args(func, event_name, ns, sys_name)
        if not args:
            return
        _EventPool.listen(func, *args, priority=priority)


def unlisten_event(func, event_name="", ns="", sys_name="", priority=0, use_decorator=False):
    """
    反监听通过 ``listen_event()`` 监听的事件。

    参见
    ----

    - ``unlisten_all_events()`` -- 反监听当前类中所有被 @event 装饰的方法。
    - ``is_listened()`` -- 判断指定事件是否被监听。

    -----

    :param function func: 事件回调函数，支持普通函数与实例方法
    :param str event_name: 事件名称；事件名与函数名相同时，可省略该参数
    :param str ns: 事件来源命名空间；默认为当前模组名称，如需监听其他模组可手动传入；监听 ModSDK 事件时，可省略该参数
    :param str sys_name: 事件来源系统名称；监听 ModSDK 事件时，可省略该参数
    :param int priority: 优先级，值越大优先级越高；默认为 0
    :param bool use_decorator: 是否使用从 @event 装饰器传入的参数，设为 True 时，忽略 event_name、ns、sys_name 和 priority 参数；默认为 False

    :return: 无
    :rtype: None
    """
    if use_decorator:
        all_args = _get_listen_args(func)
        for args in all_args:
            _EventPool.unlisten(func, *args)
    else:
        args = _parse_listen_args(func, event_name, ns, sys_name)
        if not args:
            return
        _EventPool.unlisten(func, *args, priority=priority)


def _iter_all_events(ins):
    for attr in iter_obj_attrs(ins):
        args = _get_listen_args(attr)
        if args:
            yield attr, args


def listen_all_events(ins):
    """
    对实例中所有被 ``@event`` 装饰的方法进行事件监听。

    参见
    ----

    - ``@event`` -- 事件监听装饰器。
    - ``listen_event()`` -- 监听指定事件。
    - ``unlisten_all_events()`` -- 反监听当前类中所有被 @event 装饰的方法。
    - ``is_listened()`` -- 判断指定事件是否被监听。

    -----

    :param Any ins: 类实例（通常为 self 参数）

    :return: 无
    :rtype: None
    """
    for method, all_args in _iter_all_events(ins):
        for args in all_args:
            _EventPool.listen(method, *args)


def unlisten_all_events(ins):
    """
    反监听实例中所有被 ``@event`` 装饰的方法。

    参见
    ----

    - ``unlisten_event()`` -- 反监听指定事件。
    - ``is_listened()`` -- 判断指定事件是否被监听。

    -----

    :param Any ins: 类实例（通常为 self 参数）

    :return: 无
    :rtype: None
    """
    for method, all_args in _iter_all_events(ins):
        for args in all_args:
            _EventPool.unlisten(method, *args)


def is_listened(func, event_name="", ns="", sys_name=""):
    """
    判断函数是否已监听某事件。

    参见
    ----

    - ``@event`` -- 事件监听装饰器。
    - ``listen_event()`` -- 监听指定事件。
    - ``listen_all_events()`` -- 监听当前类中所有被 @event 装饰的方法。

    -----

    :param function func: 事件回调函数，支持普通函数与实例方法
    :param str event_name: 事件名称；事件名与函数名相同时，可省略该参数
    :param str ns: 事件来源命名空间；默认为当前模组名称，如需监听其他模组可手动传入；监听 ModSDK 事件时，可省略该参数
    :param str sys_name: 事件来源系统名称；监听 ModSDK 事件时，可省略该参数

    :return: 已监听返回 True，否则返回 False
    :rtype: bool
    """
    args = _parse_listen_args(func, event_name, ns, sys_name)
    if not args:
        return
    return _EventPool.is_listened(func, *args)


class _EventPool(object):
    __slots__ = ('__name__', 'pool', 'priorities', 'lock', 'remove_lst', 'add_lst')

    def __init__(self, event_id):
        self.pool = {}
        self.priorities = []
        self.lock = False
        self.remove_lst = []
        self.add_lst = []
        self.__name__ = event_id

    def __bool__(self):
        return any(v for v in self.pool.values())

    __nonzero__ = __bool__

    # 事件触发（modsdk调用入口）
    def __call__(self, args=None):
        # 加锁，防止在回调执行过程中再次监听/反监听了同一个事件，导致for循环抛出异常
        self.lock = True

        if ENABLED_EVENT_ARGS_WARPPING:
            args = EventArgsWrapper(args, self.__name__) if args else None

        # 按优先级调用
        for p in self.priorities:
            for f in self.pool[p]:
                try:
                    f(args)
                except:
                    traceback.print_exc()

        self.lock = False
        while self.remove_lst:
            self._remove(*self.remove_lst.pop())
        while self.add_lst:
            self._add(*self.add_lst.pop())

    def _add(self, func, priority=0):
        p = -priority
        if p not in self.pool:
            self.pool[p] = set()
            # 插入优先级并排序
            bisect.insort(self.priorities, p)

        func_set = self.pool[p]
        if func in func_set:
            return
        if not self.lock:
            func_set.add(func)
        else:
            self.add_lst.append((func, priority))

    def _remove(self, func, priority=0):
        p = -priority
        if p not in self.pool:
            return
        func_set = self.pool[p]
        if func not in func_set:
            return
        if not self.lock:
            func_set.remove(func)
        else:
            self.remove_lst.append((func, priority))

    @staticmethod
    def get(event_name, ns, sys_name, new=True):
        event_id = "%s:%s:%s" % (ns, sys_name, event_name)
        event_pool_map = _L.event_pool_map
        ep = event_pool_map.get(event_id)
        if new and ep is None:
            ep = _EventPool(event_id)
            event_pool_map[event_id] = ep
            # modsdk触发回调函数逻辑：getattr(ep, ep.__call__.__name__)(args)
            lib_sys = _env.get_lib_system()
            lib_sys.native_listen(ns, sys_name, event_name, ep.__call__)
        return ep

    @staticmethod
    def listen(func, event_name, ns, sys_name, priority=0):
        ep = _EventPool.get(event_name, ns, sys_name)
        ep._add(func, priority)
        _logging.debug(
            "Listen for event: %s:%s:%s, function: %s",
            ns, sys_name, event_name, func.__module__ + "." + func.__name__
        )

    @staticmethod
    def unlisten(func, event_name, ns, sys_name, priority=0):
        ep = _EventPool.get(event_name, ns, sys_name, False)
        if ep is None:
            return
        ep._remove(func, priority)
        _logging.debug(
            "Unlisten for event: %s:%s:%s, function: %s",
            ns, sys_name, event_name, func.__module__ + "." + func.__name__
        )

    @staticmethod
    def is_listened(func, event_name, ns, sys_name):
        ep = _EventPool.get(event_name, ns, sys_name, False)
        if ep is None:
            return False
        for funcs in ep.pool.values():
            if func in funcs:
                return True
        return False


class EventArgsWrapper(object):
    """
    事件参数包装类。

    ``EventArgsWrapper`` 对象支持通过 ``.`` 获取/修改事件参数，详见示例。
    此外， ``EventArgsWrapper`` 对象兼容所有 Python 2 字典操作方法，可以将 ``EventArgsWrapper`` 对象完全当成字典使用。

    说明
    ----

    将 ``nuoyanlib.config.ENABLED_EVENT_ARGS_WARPPING`` 设为 ``True`` 后，所有通过「nuoyanlib」监听的事件的参数均会被自动包装成 ``EventArgsWrapper`` 对象。

    示例
    ----

    >>> @nyl.event
    ... def ServerItemUseOnEvent(args):
    ...     item_dict = args.itemDict # 也可写成 args['itemDict']
    ...     # 取消骨粉使用
    ...     if item_dict and item_dict['newItemName'] == "minecraft:bone_meal":
    ...         args.ret = True

    通过使用类型注释，可为 ``args`` 指定事件参数类型，这样 IDE 就知道参数中有哪些字段并提供补全功能。

    >>> @nyl.event
    ... def ServerItemUseOnEvent(args):
    ...     # type: (nyl.ServerEvent.ServerItemUseOnEvent) -> None
    ...     pass

    参见
    ----

    - ``@event`` -- 事件监听装饰器。
    - ``listen_event()`` -- 监听指定事件。
    - ``listen_all_events()`` -- 监听当前类中所有被 @event 装饰的方法。
    """

    __slots__ = ('_arg_dict', '_event_id')

    def __init__(self, arg_dict, event_id):
        self._arg_dict = arg_dict
        self._event_id = event_id

    def __getattr__(self, key):
        # 事件参数获取
        if key == "from_":
            key = "from"
        if key in self._arg_dict:
            return self._arg_dict[key]
        raise error.EventParameterError(self._event_id, key)

    __getitem__ = __getattr__

    def __setattr__(self, key, value):
        if key in EventArgsWrapper.__slots__:
            object.__setattr__(self, key, value)
            return
        # 事件参数修改
        if key in self._arg_dict:
            self._arg_dict[key] = value
        else:
            raise error.EventParameterError(self._event_id, key)

    __setitem__ = __setattr__

    def __repr__(self):
        s = "<EventArgsWrapper of '%s':" % self._event_id
        for k, v in self._arg_dict.items():
            s += "\n    .%s = %s" % (k, repr(v))
        s += "\n>"
        return s

    __iter__        = lambda self, *args: self._arg_dict.__iter__()
    __eq__          = lambda self, *args: self._arg_dict.__eq__(*args)
    __ne__          = lambda self, *args: self._arg_dict.__ne__(*args)
    __len__         = lambda self, *args: self._arg_dict.__len__()
    __contains__    = lambda self, *args: self._arg_dict.__contains__(*args)
    keys            = lambda self, *args: self._arg_dict.keys()
    values          = lambda self, *args: self._arg_dict.values()
    items           = lambda self, *args: self._arg_dict.items()
    iterkeys        = lambda self, *args: self._arg_dict.iterkeys()
    itervalues      = lambda self, *args: self._arg_dict.itervalues()
    iteritems       = lambda self, *args: self._arg_dict.iteritems()
    get             = lambda self, *args: self._arg_dict.get(*args)
    copy            = lambda self, *args: self._arg_dict.copy()


def _lib_sys_event(name="", from_client=None):
    if from_client is None:
        from_client = not _env.is_client()
    return event(
        name,
        _env.LIB_NAME,
        _env.LIB_CLIENT_NAME if from_client else _env.LIB_SERVER_NAME,
    )


def __benchmark__(n, timer, **kwargs):
    class C(s_api.GetServerSystemCls()):
        def __init__(self, namespace, system_name):
            super(C, self).__init__(namespace, system_name)
            listen_event(self.OnMobHitBlockServerEvent)
            ep = _EventPool.get("OnMobHitBlockServerEvent", "Minecraft", "Engine")

            timer.start("nuoyanlib listen")
            for _ in xrange(n):
                listen_event(self.OnMobHitBlockServerEvent)
            timer.end("nuoyanlib listen")

            timer.start("nuoyanlib unlisten")
            for _ in xrange(n):
                unlisten_event(self.OnMobHitBlockServerEvent)
            timer.end("nuoyanlib unlisten")

            timer.start("modsdk listen")
            for _ in xrange(n):
                self.ListenForEvent("Minecraft", "Engine", "OnMobHitBlockServerEvent", self, self.OnMobHitBlockServerEvent) # noqa
            timer.end("modsdk listen")

            timer.start("modsdk unlisten")
            for _ in xrange(n):
                self.UnListenForEvent("Minecraft", "Engine", "OnMobHitBlockServerEvent", self, self.OnMobHitBlockServerEvent) # noqa
            timer.end("modsdk unlisten")

            timer.start("event call")
            for _ in xrange(n):
                ep({})
            timer.end("event call")

            timer.start("common call")
            for _ in xrange(n):
                self.OnMobHitBlockServerEvent({}) # noqa
            timer.end("common call")

        @event
        def OnMobHitBlockServerEvent(self, args):
            pass

    C("", "")
