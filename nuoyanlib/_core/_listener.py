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
#   Last Modified : 2025-02-21
#
# ====================================================


import mod.client.extraClientApi as _client_api
import mod.server.extraServerApi as _server_api
from ._const import (
    LIB_NAME as _LIB_NAME,
    LIB_SERVER_NAME as _LIB_SERVER_NAME,
    LIB_CLIENT_NAME as _LIB_CLIENT_NAME,
)
from ._sys import (
    is_client as _is_client,
    get_lib_system as _get_lib_system,
)
from ._logging import log as _log


__all__ = [
    "quick_listen",
    "event",
    "lib_sys_event",
]


__ALL_CLIENT_ENGINE_EVENTS = (
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
)
__ALL_CLIENT_LIB_EVENTS = {

}
__ALL_SERVER_ENGINE_EVENTS = (
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
)
__ALL_SERVER_LIB_EVENTS = {
    'ItemGridChangedServerEvent': _LIB_CLIENT_NAME,
    'UiInitFinished': _LIB_CLIENT_NAME,
}


__CLIENT_ENGINE_NAMESPACE = _client_api.GetEngineNamespace()
__CLIENT_ENGINE_SYSTEM_NAME = _client_api.GetEngineSystemName()
__SERVER_ENGINE_NAMESPACE = _server_api.GetEngineNamespace()
__SERVER_ENGINE_SYSTEM_NAME = _server_api.GetEngineSystemName()


def quick_listen(cls):
    """
    | 类装饰器，用于对类启用快捷监听功能。
    | 使用该装饰器后，监听ModSDK事件，只需编写一个与事件同名的方法即可，无需调用 ``ListenForEvent`` 接口；监听自定义事件，可使用 ``event`` 装饰器。
    """
    org_init = cls.__init__
    def new_init(self, *args, **kwargs):
        org_init(self, *args, **kwargs)
        __listen_events(self)
    cls.__init__ = new_init
    return cls


def event(event_name="", namespace="", system_name="", priority=0):
    """
    | 函数装饰器，用于事件监听，须配合 ``quick_listen`` 使用。
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
        if hasattr(func, "_nyl_listener_args"):
            func._nyl_listener_args.append(args)
        else:
            func._nyl_listener_args = [args]
        return func
    # @event(...)
    if isinstance(event_name, str):
        return add_listener
    # @event
    else:
        return add_listener(event_name)


def lib_sys_event(name):
    return event(name, _LIB_NAME, _LIB_SERVER_NAME if _is_client() else _LIB_CLIENT_NAME)


# noinspection PyUnresolvedReferences
def __listen(namespace, system_name, event_name, ins, method, priority=0):
    if not namespace or not system_name or method.__self__ is not ins:
        _log(
            "Failed to listen for event: namespace=%s, system_name=%s, event_name=%s" % (namespace, system_name, event_name),
            ins.__class__, "ERROR"
        )
        return False
    _get_lib_system().ListenForEvent(namespace, system_name, event_name, ins, method, priority)
    return True


def __parse_listen_args(method):
    if _is_client():
        engine_events = __ALL_CLIENT_ENGINE_EVENTS
        engine_ns = __CLIENT_ENGINE_NAMESPACE
        engine_sys = __CLIENT_ENGINE_SYSTEM_NAME
        lib_events = __ALL_CLIENT_LIB_EVENTS
        lib_sys = _LIB_CLIENT_NAME
    else:
        engine_events = __ALL_SERVER_ENGINE_EVENTS
        engine_ns = __SERVER_ENGINE_NAMESPACE
        engine_sys = __SERVER_ENGINE_SYSTEM_NAME
        lib_events = __ALL_SERVER_LIB_EVENTS
        lib_sys = _LIB_SERVER_NAME
    if hasattr(method, "_nyl_listener_args"):
        args = method._nyl_listener_args
        for arg_lst in args:
            namespace, system_name, event_name, priority = arg_lst
            is_engine_event = event_name in engine_events
            is_lib_event = event_name in lib_events
            if not namespace:
                if is_engine_event:
                    arg_lst[0] = engine_ns
                elif is_lib_event:
                    arg_lst[0] = _LIB_NAME
            if not system_name:
                if is_engine_event:
                    arg_lst[1] = engine_sys
                elif is_lib_event:
                    arg_lst[1] = lib_sys
        return args
    else:
        method_name = method.__name__
        if method_name in engine_events:
            return [(engine_ns, engine_sys, method_name, 0)]
        elif method_name in lib_events:
            return [(_LIB_NAME, lib_sys, method_name, 0)]


def __listen_events(ins):
    listened = []
    for attr in dir(ins):
        try:
            method = getattr(ins, attr)
        except:
            continue
        if not callable(method):
            continue
        args = __parse_listen_args(method)
        if not args:
            continue
        for namespace, system_name, event_name, priority in args:
            if __listen(namespace, system_name, event_name, ins, method, priority):
                listened.append(event_name)
    cls = ins.__class__
    if listened:
        _log("Listen for events successfully: %s" % listened, cls)
    else:
        _log("No event to listen", cls)















