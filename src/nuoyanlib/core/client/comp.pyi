# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from typing import Type, ClassVar, Dict
from mod.client.system.clientSystem import ClientSystem
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.viewBinder import ViewBinder
from mod.client.ui.viewRequest import ViewRequest
from mod.client.ui.CustomUIScreenProxy import CustomUIScreenProxy
from mod.client.ui.CustomUIControlProxy import CustomUIControlProxy
from mod.client.ui.NativeScreenManager import NativeScreenManager
from mod.client.component.engineCompFactoryClient import EngineCompFactoryClient
from mod.client.component.skyRenderCompClient import SkyRenderCompClient
from mod.client.component.frameAniTransComp import FrameAniTransComp
from mod.client.component.actorRenderCompClient import ActorRenderCompClient
from mod.client.component.actionCompClient import ActionCompClient
from mod.client.component.itemCompClient import ItemCompClient
from mod.client.component.frameAniControlComp import FrameAniControlComp
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
from mod.client.component.blockGeometryCompClient import BlockGeometryCompClient
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
from mod.client.component.neteaseWindowCompClient import NeteaseWindowCompClient
from mod.client.component.configCompClient import ConfigCompClient
from mod.client.component.playerCompClient import PlayerCompClient
from mod.client.component.fogCompClient import FogCompClient
from mod.client.component.particleTransComp import ParticleTransComp
from mod.client.component.textBoardCompClient import TextBoardComponentClient
from mod.client.component.postProcessControlComp import PostProcessComponent
from mod.client.component.auxValueCompClient import AuxValueComponentClient
from mod.client.component.brightnessCompClient import BrightnessCompClient
from mod.client.component.deviceCompClient import DeviceCompClient
from mod.client.component.frameAniEntityBindComp import FrameAniEntityBindComp
from mod.client.component.operationCompClient import OperationCompClient
from mod.client.component.chunkSourceCompClient import ChunkSourceCompClient
from mod.client.component.rotCompClient import RotComponentClient
from mod.client.component.drawingCompClient import DrawingCompClient
from mod.client.component.collisionBoxCompClient import CollisionBoxComponentClient
from mod.client.component.particleControlComp import ParticleControlComp
from mod.client.component.tameCompClient import TameComponentClient
from mod.client.component.modAttrCompClient import ModAttrComponentClient
from mod.client.component.playerAnimCompClient import PlayerAnimCompClient
from mod.client.component.achievementCompClient import AchievementCompClient
from mod.client.component.dimensionCompClient import DimensionCompClient
from mod.common.component.baseComponent import BaseComponent
from .._types._typing import Self, FTuple2, T


class _MiniMapBaseScreen(ScreenNode):
    def __init__(self: Self, namespace: str, name: str, param: dict) -> None: ...
    def AddEntityMarker(
        self,
        entity_id: str,
        texture_path: str,
        size: FTuple2 = (4, 4),
        enable_rotation: bool = False,
        is_revert_z_rot: bool = False
    ) -> bool:
        """
        增加实体位置标记。

        -----

        :param str entity_id: 实体ID
        :param str texture_path: 头顶ICON贴图，如textures/blocks/border
        :param tuple[float,float] size: 贴图大小，默认为(4, 4)
        :param bool enable_rotation: 是否启用实体朝向，默认为False
        :param bool is_revert_z_rot: 是否翻转实体Z轴旋转，默认为False

        :return: 是否增加成功
        :rtype: bool
        """
    def RemoveEntityMarker(self, entity_id: str) -> bool:
        """
        删除实体位置标记。

        -----

        :param str entity_id: 实体ID

        :return: 是否删除成功
        :rtype: bool
        """
    def AddStaticMarker(self, key: str, vec2: FTuple2, texture_path: str, size: FTuple2 = (4, 4)) -> bool:
        """
        增加地图上静态位置的标记。
        如使用该接口请勿将地图缩小倍数设置过大（建议 ``ZoomOut`` 设置后的地图倍数不小于原地图大小的0.5倍），以免造成地图缩小后静态标记位置失效等问题。

        -----

        :param str key: 标记ID
        :param tuple[float,float] vec2: 地图位置二维坐标(x,z)
        :param str texture_path: 贴图路径
        :param tuple[float,float] size: 贴图大小，默认为(4,4)

        :return: 是否成功
        :rtype: bool
        """
    def RemoveStaticMarker(self, key: str) -> bool:
        """
        删除静态位置标记。

        -----

        :param key: 标记ID

        :return: 是否成功
        :rtype: bool
        """
    def ZoomIn(self, value: float = 0.05) -> bool:
        """
        放大地图。

        -----

        :param float value: 在原有基础上的增量值，可以控制放大速度，默认为0.05

        :return: 是否成功
        :rtype: bool
        """
    def ZoomOut(self, value: float = 0.05) -> bool:
        """
        缩小地图。
        客户端地图区块加载有限，如果地图UI界面太大或者缩小地图倍数太大，会导致小地图无法显示未加载的区块。

        -----

        :param float value: 在原有基础上的减少值，可以控制缩小速度，默认为0.05

        :return: 是否成功
        :rtype: bool
        """
    def ZoomReset(self) -> bool:
        """
        恢复地图放缩大小为默认值。

        -----

        :return: 是否成功
        :rtype: bool
        """
    def SetHighestY(self, highest_y: int) -> bool:
        """
        设置绘制地图的最大高度。
        动态调整高度值后，已经绘制过的区块不会刷新为新的高度值，只有没有绘制过的区块会以新的高度值来绘制。

        -----

        :param int highest_y: 绘制高度值

        :return: 是否成功
        :rtype: bool
        """
    def AddEntityTextMarker(self, entity_id: str, text: str, scale: float) -> bool:
        """
        在小地图上增加实体文本标记。

        -----

        :param str entity_id: 实体ID
        :param str text: 文本的内容，可以支持样式代码（§可以设置文字的颜色、格式等，该种用法更加灵活多变）
        :param float scale: 文本缩放倍数，等于文本控件json中的font_scale_factor参数，默认缩放倍数为1.0

        :return: 是否成功
        :rtype: bool
        """
    def RemoveEntityTextMarker(self, entity_id: str) -> bool:
        """
        在小地图上删除实体文本标记。

        -----

        :param str entity_id: 实体ID

        :return: 是否成功
        :rtype: bool
        """
    def AddStaticTextMarker(self, key: str, vec2: FTuple2, text: str, scale: float) -> bool:
        """
        在小地图上增加静态文本的标记。

        -----

        :param str key: 标记ID
        :param tuple[float,float] vec2: 地图位置二维坐标(x,z)
        :param str text: 文本的内容，可以支持样式代码（§可以设置文字的颜色、格式等，该种用法更加灵活多变）
        :param float scale: 文本缩放倍数，等于文本控件json中的font_scale_factor参数，默认缩放倍数为1.0

        :return: 是否成功
        :rtype: bool
        """
    def RemoveStaticTextMarker(self, key: str) -> bool:
        """
        在小地图上删除静态文本标记。

        -----

        :param str key: 标记ID

        :return: 是否成功
        :rtype: bool
        """


ENGINE_NAMESPACE: str
ENGINE_SYSTEM_NAME: str
PLAYER_ID: str
LEVEL_ID: str
ClientSystem: Type[ClientSystem]
ScreenNode: Type[ScreenNode]
ViewBinder: Type[ViewBinder]
ViewRequest: Type[ViewRequest]
CustomUIScreenProxy: Type[CustomUIScreenProxy]
CustomUIControlProxy: Type[CustomUIControlProxy]
NativeScreenManager: NativeScreenManager
MiniMapScreenNode: Type[_MiniMapBaseScreen]
CompFactory: EngineCompFactoryClient


class CF(object):
    __cache__: ClassVar[Dict[str, CF]]
    _target: str
    def __new__(cls: Type[T], target: str) -> T: ...
    def __init__(self: Self, target: str) -> None: ...
    def __getattr__(self, name: str) -> BaseComponent: ...
    Drawing: DrawingCompClient
    Achievement: AchievementCompClient
    Action: ActionCompClient
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
    Dimension: DimensionCompClient
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
    NeteaseWindow: NeteaseWindowCompClient
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


PlrComp: CF
LvComp: CF
