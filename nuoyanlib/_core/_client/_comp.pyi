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
#   Last Modified : 2025-02-03
#
# ====================================================


from typing import Type, Any, Dict, Union
from mod.client.system.clientSystem import ClientSystem
from mod.client.component.engineCompFactoryClient import EngineCompFactoryClient
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.viewBinder import ViewBinder
from mod.client.ui.viewRequest import ViewRequest
from mod.client.component.skyRenderCompClient import SkyRenderCompClient
from mod.client.component.frameAniTransComp import FrameAniTransComp
from mod.client.component.actorRenderCompClient import ActorRenderCompClient
from mod.client.component.actionCompClient import ActionCompClient
from mod.client.component.itemCompClient import ItemCompClient
from mod.client.component.blockGeometryCompClient import BlockGeometryCompClient
from mod.client.component.attrCompClient import AttrCompClient
from mod.client.component.textNotifyCompClient import TextNotifyComponet
from mod.client.component.particleSkeletonBindComp import ParticleSkeletonBindComp
from mod.client.component.playerViewCompClient import PlayerViewCompClient
from mod.client.component.queryVariableCompClient import QueryVariableComponentClient
from mod.client.component.effectCompClient import EffectComponentClient
from mod.client.component.particleEntityBindComp import ParticleEntityBindComp
from mod.client.component.virtualWorldCompClient import VirtualWorldCompClient
from mod.client.component.cameraCompClient import CameraComponentClient
from mod.client.component.engineTypeCompClient import EngineTypeComponentClient
from mod.client.component.frameAniControlComp import FrameAniControlComp
from mod.client.component.actorMotionCompClient import ActorMotionComponentClient
from mod.client.component.frameAniSkeletonBindComp import FrameAniSkeletonBindComp
from mod.client.component.healthCompClient import HealthComponentClient
from mod.client.component.rideCompClient import RideCompClient
from mod.client.component.timeCompClient import TimeComponentClient
from mod.client.component.audioCustomCompClient import AudioCustomComponentClient
from mod.client.component.posCompClient import PosComponentClient
from mod.client.component.biomeCompClient import BiomeCompClient
from mod.client.component.neteaseShopCompClient import NeteaseShopCompClient
from mod.client.component.blockCompClient import BlockCompClient
from mod.client.component.blockInfoCompClient import BlockInfoComponentClient
from mod.client.component.engineEffectBindControlComp import EngineEffectBindControlComp
from mod.client.component.recipeCompClient import RecipeCompClient
from mod.client.component.blockUseEventWhiteListCompClient import BlockUseEventWhiteListComponentClient
from mod.client.component.modelCompClient import ModelComponentClient
from mod.client.component.nameCompClient import NameComponentClient
from mod.client.component.gameCompClient import GameComponentClient
from mod.client.component.particleSystemCompClient import ParticleSystemCompClient
from mod.client.component.particleTransComp import ParticleTransComp
from mod.client.component.configCompClient import ConfigCompClient
from mod.client.component.playerCompClient import PlayerCompClient
from mod.client.component.fogCompClient import FogCompClient
from mod.client.component.textBoardCompClient import TextBoardComponentClient
from mod.client.component.postProcessControlComp import PostProcessComponent
from mod.client.component.auxValueCompClient import AuxValueComponentClient
from mod.client.component.brightnessCompClient import BrightnessCompClient
from mod.client.component.deviceCompClient import DeviceCompClient
from mod.client.component.frameAniEntityBindComp import FrameAniEntityBindComp
from mod.client.component.operationCompClient import OperationCompClient
from mod.client.component.chunkSourceCompClient import ChunkSourceCompClient
from mod.client.component.rotCompClient import RotComponentClient
from mod.client.component.collisionBoxCompClient import CollisionBoxComponentClient
from mod.client.component.particleControlComp import ParticleControlComp
from mod.client.component.tameCompClient import TameComponentClient
from mod.client.component.modAttrCompClient import ModAttrComponentClient
from mod.client.component.playerAnimCompClient import PlayerAnimCompClient
from mod.common.component.baseComponent import BaseComponent


CLIENT_ENGINE_NAMESPACE: str
CLIENT_ENGINE_SYSTEM_NAME: str
ClientSystem: Type[ClientSystem]
CompFactory: EngineCompFactoryClient
ScreenNode: Type[ScreenNode]
ViewBinder: Type[ViewBinder]
ViewRequest: Type[ViewRequest]
PLAYER_ID: str
LEVEL_ID: str


class CompDescr(object):
    comp_name: str
    def __init__(self: ..., comp_name: str) -> None: ...
    def __get__(self: ..., ins: Union[PlrComp, LvComp], cls: Union[Type[PlrComp], Type[LvComp]]) -> BaseComponent: ...


class __CompPool(object):
    Action: ActionCompClient
    ActorCollidable: Any
    ActorMotion: ActorMotionComponentClient
    ActorRender: ActorRenderCompClient
    Attr: AttrCompClient
    AuxValue: AuxValueComponentClient
    Biome: BiomeCompClient
    Block: BlockCompClient
    BlockGeometry: BlockGeometryCompClient
    BlockInfo: BlockInfoComponentClient
    BlockUseEventWhiteList: BlockUseEventWhiteListComponentClient
    Brightness: BrightnessCompClient
    Camera: CameraComponentClient
    ChunkSource: ChunkSourceCompClient
    CollisionBox: CollisionBoxComponentClient
    ConfigClient: ConfigCompClient
    CustomAudio: AudioCustomComponentClient
    Device: DeviceCompClient
    Effect: EffectComponentClient
    EngineEffectBindControl: EngineEffectBindControlComp
    EngineType: EngineTypeComponentClient
    Fog: FogCompClient
    FrameAniControl: FrameAniControlComp
    FrameAniEntityBind: FrameAniEntityBindComp
    FrameAniSkeletonBind: FrameAniSkeletonBindComp
    FrameAniTrans: FrameAniTransComp
    Game: GameComponentClient
    Health: HealthComponentClient
    Item: ItemCompClient
    ModAttr: ModAttrComponentClient
    Model: ModelComponentClient
    Name: NameComponentClient
    NeteaseShop: NeteaseShopCompClient
    Operation: OperationCompClient
    ParticleControl: ParticleControlComp
    ParticleEntityBind: ParticleEntityBindComp
    ParticleSkeletonBind: ParticleSkeletonBindComp
    ParticleSystem: ParticleSystemCompClient
    ParticleTrans: ParticleTransComp
    Player: PlayerCompClient
    PlayerAnim: PlayerAnimCompClient
    PlayerView: PlayerViewCompClient
    Pos: PosComponentClient
    PostProcess: PostProcessComponent
    QueryVariable: QueryVariableComponentClient
    Recipe: RecipeCompClient
    Ride: RideCompClient
    Rot: RotComponentClient
    SkyRender: SkyRenderCompClient
    Tame: TameComponentClient
    TextBoard: TextBoardComponentClient
    TextNotifyClient: TextNotifyComponet
    Time: TimeComponentClient
    VirtualWorld: VirtualWorldCompClient


class PlrComp(__CompPool):
    _cache: Dict[str, BaseComponent]
    _target: str


class LvComp(__CompPool):
    _cache: Dict[str, BaseComponent]
    _target: str
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
