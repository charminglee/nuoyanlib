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
#   Last Modified : 2023-11-26
#
# ====================================================


from typing import Type, Dict
from mod.server.system.serverSystem import ServerSystem
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer
from mod.common.component.baseComponent import BaseComponent
from mod.server.component.effectCompServer import EffectComponentServer
from mod.server.component.actorMotionCompServer import ActorMotionComponentServer
from mod.server.component.blockInfoCompServer import BlockInfoComponentServer
from mod.server.component.httpToWebServerCompServer import HttpToWebServerCompServer
from mod.server.component.blockCompServer import BlockCompServer
from mod.server.component.scaleCompServer import ScaleComponentServer
from mod.server.component.gravityCompServer import GravityComponentServer
from mod.server.component.itemCompServer import ItemCompServer
from mod.server.component.blockEntityExDataCompServer import BlockEntityExDataCompServer
from mod.server.component.msgCompServer import MsgComponentServer
from mod.server.component.posCompServer import PosComponentServer
from mod.server.component.expCompServer import ExpComponentServer
from mod.server.component.tagCompServer import TagComponentServer
from mod.server.component.flyCompServer import FlyComponentServer
from mod.server.component.nameCompServer import NameComponentServer
from mod.server.component.commandCompServer import CommandCompServer
from mod.server.component.dimensionCompServer import DimensionCompServer
from mod.server.component.mobSpawnCompServer import MobSpawnComponentServer
from mod.server.component.levelCompServer import LevelComponentServer
from mod.server.component.timeCompServer import TimeComponentServer
from mod.server.component.chunkSourceComp import ChunkSourceCompServer
from mod.server.component.chestContainerCompServer import ChestContainerCompServer
from mod.server.component.tameCompServer import TameComponentServer
from mod.server.component.petCompServer import PetComponentServer
from mod.server.component.lootCompServer import LootComponentServer
from mod.server.component.engineTypeCompServer import EngineTypeComponentServer
from mod.server.component.collisionBoxCompServer import CollisionBoxComponentServer
from mod.server.component.redStoneCompServer import RedStoneComponentServer
from mod.server.component.rotCompServer import RotComponentServer
from mod.server.component.modelCompServer import ModelComponentServer
from mod.server.component.moveToCompServer import MoveToComponentServer
from mod.server.component.gameCompServer import GameComponentServer
from mod.server.component.shareableCompServer import ShareableComponentServer
from mod.server.component.rideCompServer import RideCompServer
from mod.server.component.actorPushableCompServer import ActorPushableCompServer
from mod.server.component.bulletAttributesCompServer import BulletAttributesComponentServer
from mod.server.component.weatherCompServer import WeatherComponentServer
from mod.server.component.interactCompServer import InteractComponentServer
from mod.server.component.projectileCompServer import ProjectileComponentServer
from mod.server.component.attrCompServer import AttrCompServer
from mod.server.component.biomeCompServer import BiomeCompServer
from mod.server.component.itemBannedCompServer import ItemBannedCompServer
from mod.server.component.breathCompServer import BreathCompServer
from mod.server.component.blockStateCompServer import BlockStateComponentServer
from mod.server.component.controlAiCompServer import ControlAiCompServer
from mod.server.component.playerCompServer import PlayerCompServer
from mod.server.component.chatExtensionCompServer import ChatExtensionComponentServer
from mod.server.component.explosionCompServer import ExplosionComponentServer
from mod.server.component.persistenceCompServer import PersistenceCompServer
from mod.server.component.portalCompServer import PortalComponentServer
from mod.server.component.hurtCompServer import HurtCompServer
from mod.server.component.recipeCompServer import RecipeCompServer
from mod.server.component.actorCollidableCompServer import ActorCollidableCompServer
from mod.server.component.auxValueCompServer import AuxValueComponentServer
from mod.server.component.achievementCompServer import AchievementCompServer
from mod.server.component.entityEventCompServer import EntityEventComponentServer
from mod.server.component.actionCompServer import ActionCompServer
from mod.server.component.actorOwnerCompServer import ActorOwnerComponentServer
from mod.server.component.entityComponentServer import EntityComponentServer
from mod.server.component.featureCompServer import FeatureCompServer
from mod.server.component.modAttrCompServer import ModAttrComponentServer
from mod.server.component.exDataCompServer import ExDataCompServer
from mod.server.component.blockUseEventWhiteListCompServer import BlockUseEventWhiteListComponentServer
from mod.server.component.actorLootCompServer import ActorLootComponentServer


SERVER_ENGINE_NAMESPACE: str
SERVER_ENGINE_SYSTEM_NAME: str
ServerSystem: Type[ServerSystem]
CompFactory: EngineCompFactoryServer
LEVEL_ID: str


class _CompDescr(object):
    def __init__(self, comp_name: str) -> None: ...
    def __get__(self, ins: _CompPool, cls: Type[_CompPool]) -> BaseComponent: ...


class _CompPool(object):
    Loot: LootComponentServer
    Interact: InteractComponentServer
    Feature: FeatureCompServer
    ActorMotion: ActorMotionComponentServer
    CollisionBox: CollisionBoxComponentServer
    Dimension: DimensionCompServer
    BulletAttributes: BulletAttributesComponentServer
    EngineType: EngineTypeComponentServer
    ActorCollidable: ActorCollidableCompServer
    Player: PlayerCompServer
    RedStone: RedStoneComponentServer
    BlockInfo: BlockInfoComponentServer
    Item: ItemCompServer
    Block: BlockCompServer
    Pet: PetComponentServer
    Attr: AttrCompServer
    Persistence: PersistenceCompServer
    Gravity: GravityComponentServer
    Recipe: RecipeCompServer
    Ride: RideCompServer
    BlockUseEventWhiteList: BlockUseEventWhiteListComponentServer
    Explosion: ExplosionComponentServer
    Scale: ScaleComponentServer
    Biome: BiomeCompServer
    Pos: PosComponentServer
    Fly: FlyComponentServer
    Hurt: HurtCompServer
    Projectile: ProjectileComponentServer
    ExtraData: ExDataCompServer
    ItemBanned: ItemBannedCompServer
    ActorLoot: ActorLootComponentServer
    EntityComponent: EntityComponentServer
    Tag: TagComponentServer
    Breath: BreathCompServer
    BlockState: BlockStateComponentServer
    Achievement: AchievementCompServer
    ChestBlock: ChestContainerCompServer
    Weather: WeatherComponentServer
    Lv: LevelComponentServer
    AuxValue: AuxValueComponentServer
    MoveTo: MoveToComponentServer
    Action: ActionCompServer
    Command: CommandCompServer
    BlockEntityData: BlockEntityExDataCompServer
    ActorOwner: ActorOwnerComponentServer
    Tame: TameComponentServer
    Http: HttpToWebServerCompServer
    Portal: PortalComponentServer
    ChunkSource: ChunkSourceCompServer
    ControlAi: ControlAiCompServer
    MobSpawn: MobSpawnComponentServer 
    Model: ModelComponentServer
    ChatExtension: ChatExtensionComponentServer
    ActorPushable: ActorPushableCompServer
    Exp: ExpComponentServer
    Rot: RotComponentServer
    Game: GameComponentServer
    Shareables: ShareableComponentServer
    Effect: EffectComponentServer
    Msg: MsgComponentServer
    ModAttr: ModAttrComponentServer
    Time: TimeComponentServer
    EntityEvent: EntityEventComponentServer
    Name: NameComponentServer


class LvComp(_CompPool):
    _cache: Dict[str, BaseComponent]



















