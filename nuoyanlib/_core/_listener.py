# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from types import MethodType as _MethodType
import mod.client.extraClientApi as _client_api
import mod.server.extraServerApi as _server_api
from . import _const, _logging, _sys, _error


ALL_CLIENT_ENGINE_EVENTS = {
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
    "OnScriptTickClient",
    "UiInitFinished",
    "AddEntityClientEvent",
    "AddPlayerAOIClientEvent",
    "AddPlayerCreatedClientEvent",
    "ChunkAcquireDiscardedClientEvent",
    "ChunkLoadedClientEvent",
    "LoadClientAddonScriptsAfter",
    "OnCommandOutputClientEvent",
    "OnLocalPlayerStopLoading",
    "RemoveEntityClientEvent",
    "RemovePlayerAOIClientEvent",
    "UnLoadClientAddonScriptsBefore",
    "ApproachEntityClientEvent",
    "EntityModelChangedClientEvent",
    "EntityStopRidingEvent",
    "HealthChangeClientEvent",
    "OnGroundClientEvent",
    "OnMobHitMobClientEvent",
    "StartRidingClientEvent",
    "LeaveEntityClientEvent",
    "CameraMotionStartClientEvent",
    "CameraMotionStopClientEvent",
    "DimensionChangeClientEvent",
    "DimensionChangeFinishClientEvent",
    "ExtinguishFireClientEvent",
    "GameTypeChangedClientEvent",
    "OnPlayerHitBlockClientEvent",
    "PerspChangeClientEvent",
    "ClientBlockUseEvent",
    "FallingBlockCauseDamageBeforeClientEvent",
    "OnAfterFallOnBlockClientEvent",
    "OnEntityInsideBlockClientEvent",
    "OnModBlockNeteaseEffectCreatedClientEvent",
    "OnStandOnBlockClientEvent",
    "PlayerTryDestroyBlockClientEvent",
    "ShearsDestoryBlockBeforeClientEvent",
    "StepOffBlockClientEvent",
    "StartDestroyBlockClientEvent",
    "StepOnBlockClientEvent",
    "ActorAcquiredItemClientEvent",
    "ActorUseItemClientEvent",
    "AnvilCreateResultItemAfterClientEvent",
    "ClientItemTryUseEvent",
    "ClientItemUseOnEvent",
    "ClientShapedRecipeTriggeredEvent",
    "GrindStoneRemovedEnchantClientEvent",
    "InventoryItemChangedClientEvent",
    "ItemReleaseUsingClientEvent",
    "OnCarriedNewItemChangedClientEvent",
    "PlayerTryDropItemClientEvent",
    "StartUsingItemClientEvent",
    "StopUsingItemClientEvent",
    "AttackAnimBeginClientEvent",
    "AttackAnimEndClientEvent",
    "WalkAnimBeginClientEvent",
    "WalkAnimEndClientEvent",
    "ClientChestCloseEvent",
    "ClientChestOpenEvent",
    "ClientPlayerInventoryCloseEvent",
    "ClientPlayerInventoryOpenEvent",
    "GridComponentSizeChangedClientEvent",
    "OnItemSlotButtonClickedEvent",
    "PlayerChatButtonClickClientEvent",
    "PopScreenEvent",
    "PushScreenEvent",
    "ScreenSizeChangedClientEvent",
    "OnMusicStopClientEvent",
    "PlayMusicClientEvent",
    "PlaySoundClientEvent",
    "ClientJumpButtonPressDownEvent",
    "ClientJumpButtonReleaseEvent",
    "GetEntityByCoordEvent",
    "GetEntityByCoordReleaseClientEvent",
    "HoldBeforeClientEvent",
    "LeftClickBeforeClientEvent",
    "LeftClickReleaseClientEvent",
    "MouseWheelClientEvent",
    "OnBackButtonReleaseClientEvent",
    "OnClientPlayerStartMove",
    "OnClientPlayerStopMove",
    "OnKeyPressInGame",
    "OnMouseMiddleDownClientEvent",
    "RightClickBeforeClientEvent",
    "RightClickReleaseClientEvent",
    "TapBeforeClientEvent",
    "TapOrHoldReleaseClientEvent",
}
ALL_SERVER_ENGINE_EVENTS = {
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
}
ALL_CLIENT_LIB_EVENTS = {}
ALL_SERVER_LIB_EVENTS = {
    'ItemGridChangedServerEvent': _const.LIB_CLIENT_NAME,
    'UiInitFinished': _const.LIB_CLIENT_NAME,
}


class EventArgsProxy(object):
    def __init__(self, arg_dict):
        self.arg_dict = arg_dict
        self.copy = arg_dict.copy
        self.iterkeys = arg_dict.iterkeys
        self.itervalues = arg_dict.itervalues
        self.iteritems = arg_dict.iteritems
        self.viewkeys = arg_dict.viewkeys
        self.viewvalues = arg_dict.viewvalues
        self.viewitems = arg_dict.viewitems
        self.get = arg_dict.get
        self.keys = arg_dict.keys
        self.values = arg_dict.values
        self.items = arg_dict.items

    def __getattr__(self, key):
        if key in self.arg_dict:
            return self.arg_dict[key]
        raise _error.EventArgsError(key)

    def __setattr__(self, key, value):
        # 兼容可修改的事件参数
        object.__setattr__(self, key, value)
        if key in self.arg_dict:
            self.arg_dict[key] = value

    def __repr__(self):
        s = "EventArgs:\n"
        for k, v in self.arg_dict.items():
            s += "    .%s = %s\n" % (k, repr(v))
        return s

    __len__ = lambda self: self.arg_dict.__len__()
    __contains__ = lambda self, *a: self.arg_dict.__contains__(*a)
    __getitem__ = lambda self, *a: self.arg_dict.__getitem__(*a)
    __setitem__ = lambda self, *a: self.arg_dict.__setitem__(*a)
    __cmp__ = lambda self, *a: self.arg_dict.__cmp__(*a)
    __delitem__ = lambda self, *a: self.arg_dict.__delitem__(*a)
    __eq__ = lambda self, *a: self.arg_dict.__eq__(*a)
    __ge__ = lambda self, *a: self.arg_dict.__ge__(*a)
    __gt__ = lambda self, *a: self.arg_dict.__gt__(*a)
    __iter__ = lambda self: self.arg_dict.__iter__()
    __le__ = lambda self, *a: self.arg_dict.__le__(*a)
    __lt__ = lambda self, *a: self.arg_dict.__lt__(*a)
    __ne__ = lambda self, *a: self.arg_dict.__ne__(*a)


class BaseEventProxy(object):
    def __init__(self, *args, **kwargs):
        super(BaseEventProxy, self).__init__(*args, **kwargs)
        self._lib_sys = _sys.get_lib_system()
        self._listen_events()

    def _listen_events(self):
        for attr in dir(self):
            try:
                method = getattr(self, attr)
            except:
                continue
            if not callable(method):
                continue
            args = self._parse_listen_args(method)
            if args is None:
                continue
            event_type, arg_lst = args
            for a in arg_lst:
                if event_type == 0:
                    self._listen(a[0], a[1], a[2], method, a[3])
                else:
                    self._listen_proxy(a[0], a[1], a[2], method, a[3])

    def _parse_listen_args(self, method):
        if hasattr(method, "_nyl_listen_args"):
            args = method._nyl_listen_args
            for arg_lst in args:
                namespace, system_name, event_name, _ = arg_lst
                is_engine_event = event_name in self._engine_events
                is_lib_event = event_name in self._lib_events
                if not namespace:
                    if is_engine_event:
                        arg_lst[0] = self._engine_ns
                    elif is_lib_event:
                        arg_lst[0] = _const.LIB_NAME
                if not system_name:
                    if is_engine_event:
                        arg_lst[1] = self._engine_sys
                    elif is_lib_event:
                        arg_lst[1] = self._lib_events[event_name]
            return 0, args
        else:
            method_name = method.__name__
            if method_name in self._engine_events:
                return 1, [[self._engine_ns, self._engine_sys, method_name, 0]]
            elif method_name in self._lib_events:
                return 2, [[_const.LIB_NAME, self._lib_events[method_name], method_name, 0]]

    def _listen_proxy(self, namespace, system_name, event_name, method, priority=0):
        def proxy(_, args=None):
            method(EventArgsProxy(args) if args else None)
        proxy_name = "_proxy_%s" % event_name
        proxy.__name__ = proxy_name
        proxy = _MethodType(proxy, self)
        setattr(self, proxy_name, proxy)
        self._lib_sys.ListenForEvent(namespace, system_name, event_name, self, proxy, priority)

    def _listen(self, namespace, system_name, event_name, method, priority=0):
        if not namespace or not system_name or method.__self__ is not self:
            _logging.error(
                "Failed to listen for event: namespace=%s, system_name=%s, event_name=%s"
                % (namespace, system_name, event_name)
            )
            return
        self._lib_sys.ListenForEvent(namespace, system_name, event_name, self, method, priority)


class ClientEventProxy(BaseEventProxy):
    """
    | 客户端事件代理类，继承该类的客户端将获得以下功能：
    - 所有客户端事件无需监听，编写一个与事件同名的方法即可使用该事件，且事件参数采用对象形式，支持补全。
    - 可使用 ``@event`` 装饰器便捷监听自定义事件。
    """
    _engine_events = ALL_CLIENT_ENGINE_EVENTS
    _engine_ns = _client_api.GetEngineNamespace()
    _engine_sys = _client_api.GetEngineSystemName()
    _lib_events = ALL_CLIENT_LIB_EVENTS


class ServerEventProxy(BaseEventProxy):
    """
    | 服务端事件代理类，继承该类的服务端将获得以下功能：
    - 所有服务端事件无需监听，编写一个与事件同名的方法即可使用该事件，且事件参数采用对象形式，支持补全。
    - 可使用 ``@event`` 装饰器便捷监听自定义事件。
    """
    _engine_events = ALL_SERVER_ENGINE_EVENTS
    _engine_ns = _server_api.GetEngineNamespace()
    _engine_sys = _server_api.GetEngineSystemName()
    _lib_events = ALL_SERVER_LIB_EVENTS


def event(event_name="", namespace="", system_name="", priority=0):
    """
    [装饰器]

    | 用于事件监听，被装饰函数所在的类需继承 ``ClientEventProxy`` 或 ``ServerEventProxy`` 。
    | 监听ModSDK事件（ ``event_name`` 或函数名为ModSDK事件名）时，可省略 ``namespace`` 和 ``system_name`` 参数。

    -----

    :param str event_name: 事件名称，默认为被装饰函数名
    :param str namespace: 事件来源命名空间
    :param str system_name: 事件来源系统名称
    :param int priority: 优先级，默认为0
    """
    def add_listener(func):
        if event_name and isinstance(event_name, str):
            _event_name = event_name
        else:
            _event_name = func.__name__
        args = [namespace, system_name, _event_name, priority]
        if hasattr(func, "_nyl_listen_args"):
            func._nyl_listen_args.append(args)
        else:
            func._nyl_listen_args = [args]
        return func
    # @event(...)
    if isinstance(event_name, str):
        return add_listener
    # @event
    else:
        return add_listener(event_name)


def lib_sys_event(name):
    return event(
        name,
        _const.LIB_NAME,
        _const.LIB_SERVER_NAME if _sys.is_client() else _const.LIB_CLIENT_NAME,
    )





















