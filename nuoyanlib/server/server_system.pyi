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
#   Last Modified : 2025-01-26
#
# ====================================================


from typing import Any, Dict
from mod.server.system.serverSystem import ServerSystem
from .._core._typing import EventArgs
from .._core._server._lib_server import NuoyanLibServerSystem
from .._core._server._listener import event, lib_sys_event


class NuoyanServerSystem(ServerSystem):
    all_player_data: Dict[str, Any]
    first_player_id: str
    __lib_sys: NuoyanLibServerSystem
    def __init__(self: ..., namespace: str, system_name: str) -> None: ...
    def Destroy(self: ...): ...
    def OnPlayerActionServerEvent(self: ..., args: T): ...
    def CustomCommandTriggerServerEvent(self: ..., args: EventArgs): ...
    def GlobalCommandServerEvent(self: ..., args: EventArgs): ...
    def PlayerPickupArrowServerEvent(self: ..., args: EventArgs): ...
    def EntityDieLoottableAfterServerEvent(self: ..., args: EventArgs): ...
    def PlayerHungerChangeServerEvent(self: ..., args: EventArgs): ...
    def ItemDurabilityChangedServerEvent(self: ..., args: EventArgs): ...
    def PlaceNeteaseLargeFeatureServerEvent(self: ..., args: EventArgs): ...
    def PlayerNamedEntityServerEvent(self: ..., args: EventArgs): ...
    def PlayerFeedEntityServerEvent(self: ..., args: EventArgs): ...
    def OnScriptTickServer(self: ...): ...
    def EntityRemoveEvent(self: ..., args: EventArgs): ...
    def OnCarriedNewItemChangedServerEvent(self: ..., args: EventArgs): ...
    def ProjectileDoHitEffectEvent(self: ..., args: EventArgs): ...
    def ExplosionServerEvent(self: ..., args: EventArgs): ...
    def DamageEvent(self: ..., args: EventArgs): ...
    def DestroyBlockEvent(self: ..., args: EventArgs): ...
    def ActorAcquiredItemServerEvent(self: ..., args: EventArgs): ...
    def ActorUseItemServerEvent(self: ..., args: EventArgs): ...
    def ServerItemUseOnEvent(self: ..., args: EventArgs): ...
    def EntityStartRidingEvent(self: ..., args: EventArgs): ...
    def EntityStopRidingEvent(self: ..., args: EventArgs): ...
    def OnEntityInsideBlockServerEvent(self: ..., args: EventArgs): ...
    def OnMobHitBlockServerEvent(self: ..., args: EventArgs): ...
    def AddEntityServerEvent(self: ..., args: EventArgs): ...
    def MobDieEvent(self: ..., args: EventArgs): ...
    def PlayerInteractServerEvent(self: ..., args: EventArgs): ...
    def PlayerDoInteractServerEvent(self: ..., args: EventArgs): ...
    def EntityDefinitionsEventServerEvent(self: ..., args: EventArgs): ...
    def DimensionChangeFinishServerEvent(self: ..., args: EventArgs): ...
    def HealthChangeBeforeServerEvent(self: ..., args: EventArgs): ...
    def ActuallyHurtServerEvent(self: ..., args: EventArgs): ...
    def EntityDieLoottableServerEvent(self: ..., args: EventArgs): ...
    def SpawnProjectileServerEvent(self: ..., args: EventArgs): ...
    def OnGroundServerEvent(self: ..., args: EventArgs): ...
    def ServerBlockUseEvent(self: ..., args: EventArgs): ...
    def ServerSpawnMobEvent(self: ..., args: EventArgs): ...
    def PlayerAttackEntityEvent(self: ..., args: EventArgs): ...
    def AchievementCompleteEvent(self: ..., args: EventArgs): ...
    def AddServerPlayerEvent(self: ..., args: EventArgs): ...
    def ChunkAcquireDiscardedServerEvent(self: ..., args: EventArgs): ...
    def ChunkGeneratedServerEvent(self: ..., args: EventArgs): ...
    def ChunkLoadedServerEvent(self: ..., args: EventArgs): ...
    def ClientLoadAddonsFinishServerEvent(self: ..., args: EventArgs): ...
    def CommandEvent(self: ..., args: EventArgs): ...
    def DelServerPlayerEvent(self: ..., args: EventArgs): ...
    def LoadServerAddonScriptsAfter(self: ..., args: EventArgs): ...
    def NewOnEntityAreaEvent(self: ..., args: EventArgs): ...
    def OnCommandOutputServerEvent(self: ..., args: EventArgs): ...
    def OnContainerFillLoottableServerEvent(self: ..., args: EventArgs): ...
    def OnLightningLevelChangeServerEvent(self: ..., args: EventArgs): ...
    def OnLocalLightningLevelChangeServerEvent(self: ..., args: EventArgs): ...
    def OnLocalRainLevelChangeServerEvent(self: ..., args: EventArgs): ...
    def OnRainLevelChangeServerEvent(self: ..., args: EventArgs): ...
    def PlaceNeteaseStructureFeatureEvent(self: ..., args: EventArgs): ...
    def PlayerIntendLeaveServerEvent(self: ..., args: EventArgs): ...
    def PlayerJoinMessageEvent(self: ..., args: EventArgs): ...
    def PlayerLeftMessageServerEvent(self: ..., args: EventArgs): ...
    def ServerChatEvent(self: ..., args: EventArgs): ...
    def ServerPostBlockPatternEvent(self: ..., args: EventArgs): ...
    def ServerPreBlockPatternEvent(self: ..., args: EventArgs): ...
    def ActorHurtServerEvent(self: ..., args: EventArgs): ...
    def AddEffectServerEvent(self: ..., args: EventArgs): ...
    def ChangeSwimStateServerEvent(self: ..., args: EventArgs): ...
    def EntityChangeDimensionServerEvent(self: ..., args: EventArgs): ...
    def EntityDroppedItemServerEvent(self: ..., args: EventArgs): ...
    def EntityEffectDamageServerEvent(self: ..., args: EventArgs): ...
    def EntityLoadScriptEvent(self: ..., args: EventArgs): ...
    def EntityMotionStartServerEvent(self: ..., args: EventArgs): ...
    def EntityMotionStopServerEvent(self: ..., args: EventArgs): ...
    def EntityPickupItemServerEvent(self: ..., args: EventArgs): ...
    def EntityTickServerEvent(self: ..., args: EventArgs): ...
    def HealthChangeServerEvent(self: ..., args: EventArgs): ...
    def MobGriefingBlockServerEvent(self: ..., args: EventArgs): ...
    def OnFireHurtEvent(self: ..., args: EventArgs): ...
    def OnKnockBackServerEvent(self: ..., args: EventArgs): ...
    def OnMobHitMobServerEvent(self: ..., args: EventArgs): ...
    def ProjectileCritHitEvent(self: ..., args: EventArgs): ...
    def RefreshEffectServerEvent(self: ..., args: EventArgs): ...
    def RemoveEffectServerEvent(self: ..., args: EventArgs): ...
    def StartRidingServerEvent(self: ..., args: EventArgs): ...
    def WillAddEffectServerEvent(self: ..., args: EventArgs): ...
    def WillTeleportToServerEvent(self: ..., args: EventArgs): ...
    def AddExpEvent(self: ..., args: EventArgs): ...
    def AddLevelEvent(self: ..., args: EventArgs): ...
    def ChangeLevelUpCostServerEvent(self: ..., args: EventArgs): ...
    def DimensionChangeServerEvent(self: ..., args: EventArgs): ...
    def ExtinguishFireServerEvent(self: ..., args: EventArgs): ...
    def GameTypeChangedServerEvent(self: ..., args: EventArgs): ...
    def OnPlayerHitBlockServerEvent(self: ..., args: EventArgs): ...
    def PlayerDieEvent(self: ..., args: EventArgs): ...
    def PlayerEatFoodServerEvent(self: ..., args: EventArgs): ...
    def PlayerHurtEvent(self: ..., args: EventArgs): ...
    def PlayerRespawnEvent(self: ..., args: EventArgs): ...
    def PlayerRespawnFinishServerEvent(self: ..., args: EventArgs): ...
    def PlayerSleepServerEvent(self: ..., args: EventArgs): ...
    def PlayerStopSleepServerEvent(self: ..., args: EventArgs): ...
    def PlayerTeleportEvent(self: ..., args: EventArgs): ...
    def PlayerTrySleepServerEvent(self: ..., args: EventArgs): ...
    def ServerPlayerGetExperienceOrbEvent(self: ..., args: EventArgs): ...
    def StoreBuySuccServerEvent(self: ..., args: EventArgs): ...
    def BlockDestroyByLiquidServerEvent(self: ..., args: EventArgs): ...
    def BlockLiquidStateChangeAfterServerEvent(self: ..., args: EventArgs): ...
    def BlockLiquidStateChangeServerEvent(self: ..., args: EventArgs): ...
    def BlockNeighborChangedServerEvent(self: ..., args: EventArgs): ...
    def BlockRandomTickServerEvent(self: ..., args: EventArgs): ...
    def BlockRemoveServerEvent(self: ..., args: EventArgs): ...
    def BlockSnowStateChangeAfterServerEvent(self: ..., args: EventArgs): ...
    def BlockSnowStateChangeServerEvent(self: ..., args: EventArgs): ...
    def BlockStrengthChangedServerEvent(self: ..., args: EventArgs): ...
    def ChestBlockTryPairWithServerEvent(self: ..., args: EventArgs): ...
    def CommandBlockContainerOpenEvent(self: ..., args: EventArgs): ...
    def CommandBlockUpdateEvent(self: ..., args: EventArgs): ...
    def DirtBlockToGrassBlockServerEvent(self: ..., args: EventArgs): ...
    def EntityPlaceBlockAfterServerEvent(self: ..., args: EventArgs): ...
    def FallingBlockBreakServerEvent(self: ..., args: EventArgs): ...
    def FallingBlockCauseDamageBeforeServerEvent(self: ..., args: EventArgs): ...
    def FallingBlockReturnHeavyBlockServerEvent(self: ..., args: EventArgs): ...
    def FarmBlockToDirtBlockServerEvent(self: ..., args: EventArgs): ...
    def GrassBlockToDirtBlockServerEvent(self: ..., args: EventArgs): ...
    def HeavyBlockStartFallingServerEvent(self: ..., args: EventArgs): ...
    def HopperTryPullInServerEvent(self: ..., args: EventArgs): ...
    def HopperTryPullOutServerEvent(self: ..., args: EventArgs): ...
    def OnAfterFallOnBlockServerEvent(self: ..., args: EventArgs): ...
    def OnBeforeFallOnBlockServerEvent(self: ..., args: EventArgs): ...
    def OnStandOnBlockServerEvent(self: ..., args: EventArgs): ...
    def PistonActionServerEvent(self: ..., args: EventArgs): ...
    def ServerBlockEntityTickEvent(self: ..., args: EventArgs): ...
    def ServerEntityTryPlaceBlockEvent(self: ..., args: EventArgs): ...
    def ServerPlaceBlockEntityEvent(self: ..., args: EventArgs): ...
    def ServerPlayerTryDestroyBlockEvent(self: ..., args: EventArgs): ...
    def ShearsDestoryBlockBeforeServerEvent(self: ..., args: EventArgs): ...
    def StartDestroyBlockServerEvent(self: ..., args: EventArgs): ...
    def StepOffBlockServerEvent(self: ..., args: EventArgs): ...
    def StepOnBlockServerEvent(self: ..., args: EventArgs): ...
    def ContainerItemChangedServerEvent(self: ..., args: EventArgs): ...
    def CraftItemOutputChangeServerEvent(self: ..., args: EventArgs): ...
    def FurnaceBurnFinishedServerEvent(self: ..., args: EventArgs): ...
    def InventoryItemChangedServerEvent(self: ..., args: EventArgs): ...
    def ItemReleaseUsingServerEvent(self: ..., args: EventArgs): ...
    def ItemUseAfterServerEvent(self: ..., args: EventArgs): ...
    def ItemUseOnAfterServerEvent(self: ..., args: EventArgs): ...
    def OnItemPutInEnchantingModelServerEvent(self: ..., args: EventArgs): ...
    def OnNewArmorExchangeServerEvent(self: ..., args: EventArgs): ...
    def OnOffhandItemChangedServerEvent(self: ..., args: EventArgs): ...
    def OnPlayerActiveShieldServerEvent(self: ..., args: EventArgs): ...
    def OnPlayerBlockedByShieldAfterServerEvent(self: ..., args: EventArgs): ...
    def OnPlayerBlockedByShieldBeforeServerEvent(self: ..., args: EventArgs): ...
    def PlayerDropItemServerEvent(self: ..., args: EventArgs): ...
    def ServerItemTryUseEvent(self: ..., args: EventArgs): ...
    def ServerPlayerTryTouchEvent(self: ..., args: EventArgs): ...
    def ShearsUseToBlockBeforeServerEvent(self: ..., args: EventArgs): ...
    def UIContainerItemChangedServerEvent(self: ..., args: EventArgs): ...
    def AttackAnimBeginServerEvent(self: ..., args: EventArgs): ...
    def AttackAnimEndServerEvent(self: ..., args: EventArgs): ...
    def JumpAnimBeginServerEvent(self: ..., args: EventArgs): ...
    def WalkAnimBeginServerEvent(self: ..., args: EventArgs): ...
    def WalkAnimEndServerEvent(self: ..., args: EventArgs): ...
    def PlayerInventoryOpenScriptServerEvent(self: ..., args: EventArgs): ...
    def UrgeShipEvent(self: ..., args: EventArgs): ...
    def lobbyGoodBuySucServerEvent(self: ..., args: EventArgs): ...
    def ItemGridChangedServerEvent(self: ..., args: EventArgs): ...
    def UiInitFinished(self: ..., args: EventArgs): ...
    @lib_sys_event("_ButtonCallbackTrigger")
    def _on_btn_callback_trigger(self: ..., args: EventArgs) -> None: ...
    @lib_sys_event("AddServerPlayerEvent")
    def _on_add_player(self: ..., args: EventArgs) -> None: ...
    @event("PlayerIntendLeaveServerEvent")
    def _on_player_intend_leave(self: ..., args: EventArgs) -> None: ...
    @lib_sys_event("ItemGridChangedServerEvent")
    def _on_item_grid_changed(self: ..., args: EventArgs) -> None: ...
    def _set_print_log(self: ...) -> None: ...
