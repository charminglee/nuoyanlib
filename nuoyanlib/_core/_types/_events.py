# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


from .._error import EventNotFoundError
from .._utils import assert_error


__all__ = [
    "ClientEventEnum",
    "ALL_CLIENT_ENGINE_EVENTS",
    "ALL_CLIENT_LIB_EVENTS",
    "ServerEventEnum",
    "ALL_SERVER_ENGINE_EVENTS",
    "ALL_SERVER_LIB_EVENTS",
]


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
ALL_CLIENT_LIB_EVENTS = set()
ALL_SERVER_LIB_EVENTS = {
    "ItemGridChangedServerEvent",
    "UiInitFinished",
}


class _Event:
    def __init__(self, pool, is_client):
        self.pool = pool
        self.is_client = is_client

    def __getattr__(self, item):
        if item not in self.pool:
            raise EventNotFoundError(item, self.is_client)
        return item


ClientEventEnum = _Event(ALL_CLIENT_ENGINE_EVENTS.union(ALL_CLIENT_LIB_EVENTS), True)
ServerEventEnum = _Event(ALL_SERVER_ENGINE_EVENTS.union(ALL_SERVER_LIB_EVENTS), False)


def __test__():
    assert ClientEventEnum.ClientBlockUseEvent == "ClientBlockUseEvent"
    assert ServerEventEnum.DamageEvent == "DamageEvent"
    def f():
        ClientEventEnum.ABC
    assert_error(f, (), EventNotFoundError)






