# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-31
|
| ==============================================
"""


from typing import Type, Any
from mod.server.system.serverSystem import ServerSystem
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer
from mod.server.component.effectCompServer import EffectComponentServer
from mod.server.component.actorMotionCompServer import ActorMotionComponentServer
from mod.server.component.blockInfoCompServer import BlockInfoComponentServer
from mod.server.component.blockEntityCompServer import BlockEntityCompServer
from mod.server.component.blockCompServer import BlockCompServer
from mod.server.component.scaleCompServer import ScaleComponentServer
from mod.server.component.gravityCompServer import GravityComponentServer
from mod.server.component.itemCompServer import ItemCompServer
from mod.server.component.msgCompServer import MsgComponentServer
from mod.server.component.posCompServer import PosComponentServer
from mod.server.component.expCompServer import ExpComponentServer
from mod.server.component.tagCompServer import TagComponentServer
from mod.server.component.flyCompServer import FlyComponentServer
from mod.server.component.nameCompServer import NameComponentServer
from mod.server.component.bulletAttributesCompServer import BulletAttributesComponentServer
from mod.server.component.dimensionCompServer import DimensionCompServer
from mod.server.component.mobSpawnCompServer import MobSpawnComponentServer
from mod.server.component.levelCompServer import LevelComponentServer
from mod.server.component.timeCompServer import TimeComponentServer
from mod.server.component.aiCommandCompServer import AiCommandComponentServer
from mod.server.component.chunkSourceComp import ChunkSourceCompServer
from mod.server.component.biomeCompServer import BiomeCompServer
from mod.server.component.chestContainerCompServer import ChestContainerCompServer
from mod.server.component.tameCompServer import TameComponentServer
from mod.server.component.petCompServer import PetComponentServer
from mod.server.component.lootCompServer import LootComponentServer
from mod.server.component.blockStateCompServer import BlockStateComponentServer
from mod.server.component.collisionBoxCompServer import CollisionBoxComponentServer
from mod.server.component.redStoneCompServer import RedStoneComponentServer
from mod.server.component.rotCompServer import RotComponentServer
from mod.server.component.modelCompServer import ModelComponentServer
from mod.server.component.moveToCompServer import MoveToComponentServer
from mod.server.component.gameCompServer import GameComponentServer
from mod.server.component.engineTypeCompServer import EngineTypeComponentServer
from mod.server.component.rideCompServer import RideCompServer
from mod.server.component.httpToWebServerCompServer import HttpToWebServerCompServer
from mod.server.component.actorPushableCompServer import ActorPushableCompServer
from mod.server.component.commandCompServer import CommandCompServer
from mod.server.component.weatherCompServer import WeatherComponentServer
from mod.server.component.interactCompServer import InteractComponentServer
from mod.server.component.projectileCompServer import ProjectileComponentServer
from mod.server.component.attrCompServer import AttrCompServer
from mod.server.component.exDataCompServer import ExDataCompServer
from mod.server.component.itemBannedCompServer import ItemBannedCompServer
from mod.server.component.breathCompServer import BreathCompServer
from mod.server.component.controlAiCompServer import ControlAiCompServer
from mod.server.component.playerCompServer import PlayerCompServer
from mod.server.component.chatExtensionCompServer import ChatExtensionComponentServer
from mod.server.component.entityDefinitionsCompServer import EntityDefinitionsCompServer
from mod.server.component.explosionCompServer import ExplosionComponentServer
from mod.server.component.persistenceCompServer import PersistenceCompServer
from mod.server.component.actionCompServer import ActionCompServer
from mod.server.component.portalCompServer import PortalComponentServer
from mod.server.component.queryVariableCompServer import QueryVariableComponentServer
from mod.server.component.hurtCompServer import HurtCompServer
from mod.server.component.recipeCompServer import RecipeCompServer
from mod.server.component.actorCollidableCompServer import ActorCollidableCompServer
from mod.server.component.auxValueCompServer import AuxValueComponentServer
from mod.server.component.achievementCompServer import AchievementCompServer
from mod.server.component.entityEventCompServer import EntityEventComponentServer
from mod.server.component.blockEntityExDataCompServer import BlockEntityExDataCompServer
from mod.server.component.actorOwnerCompServer import ActorOwnerComponentServer
from mod.server.component.entityComponentServer import EntityComponentServer
from mod.server.component.featureCompServer import FeatureCompServer
from mod.server.component.modAttrCompServer import ModAttrComponentServer
from mod.server.component.shareableCompServer import ShareableComponentServer
from mod.server.component.blockUseEventWhiteListCompServer import BlockUseEventWhiteListComponentServer
from mod.server.component.actorLootCompServer import ActorLootComponentServer
from .._utils import CachedObject


ENGINE_NAMESPACE: str
ENGINE_SYSTEM_NAME: str
LEVEL_ID: str
ServerSystem: Type[ServerSystem]
CompFactory: EngineCompFactoryServer


class CF(CachedObject):
    _target: str
    def __init__(self: ..., target: str) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    Achievement: AchievementCompServer
    Action: ActionCompServer
    ActorCollidable: ActorCollidableCompServer
    ActorLoot: ActorLootComponentServer
    ActorMotion: ActorMotionComponentServer
    ActorOwner: ActorOwnerComponentServer
    ActorPushable: ActorPushableCompServer
    AiCommand: AiCommandComponentServer
    Attr: AttrCompServer
    AuxValue: AuxValueComponentServer
    Biome: BiomeCompServer
    Block: BlockCompServer
    BlockEntity: BlockEntityCompServer
    BlockEntityData: BlockEntityExDataCompServer
    BlockInfo: BlockInfoComponentServer
    BlockState: BlockStateComponentServer
    BlockUseEventWhiteList: BlockUseEventWhiteListComponentServer
    Breath: BreathCompServer
    BulletAttributes: BulletAttributesComponentServer
    ChatExtension: ChatExtensionComponentServer
    ChestBlock: ChestContainerCompServer
    ChunkSource: ChunkSourceCompServer
    CollisionBox: CollisionBoxComponentServer
    Command: CommandCompServer
    ControlAi: ControlAiCompServer
    Dimension: DimensionCompServer
    Effect: EffectComponentServer
    EngineType: EngineTypeComponentServer
    EntityComponent: EntityComponentServer
    EntityDefinitions: EntityDefinitionsCompServer
    EntityEvent: EntityEventComponentServer
    Exp: ExpComponentServer
    Explosion: ExplosionComponentServer
    ExtraData: ExDataCompServer
    Feature: FeatureCompServer
    Fly: FlyComponentServer
    Game: GameComponentServer
    Gravity: GravityComponentServer
    Http: HttpToWebServerCompServer
    Hurt: HurtCompServer
    Interact: InteractComponentServer
    Item: ItemCompServer
    ItemBanned: ItemBannedCompServer
    Loot: LootComponentServer
    Lv: LevelComponentServer
    MobSpawn: MobSpawnComponentServer
    ModAttr: ModAttrComponentServer
    Model: ModelComponentServer
    MoveTo: MoveToComponentServer
    Msg: MsgComponentServer
    Name: NameComponentServer
    Persistence: PersistenceCompServer
    Pet: PetComponentServer
    Player: PlayerCompServer
    Portal: PortalComponentServer
    Pos: PosComponentServer
    Projectile: ProjectileComponentServer
    QueryVariable: QueryVariableComponentServer
    Recipe: RecipeCompServer
    RedStone: RedStoneComponentServer
    Ride: RideCompServer
    Rot: RotComponentServer
    Scale: ScaleComponentServer
    Shareables: ShareableComponentServer
    Tag: TagComponentServer
    Tame: TameComponentServer
    Time: TimeComponentServer
    Weather: WeatherComponentServer


LvComp: CF
