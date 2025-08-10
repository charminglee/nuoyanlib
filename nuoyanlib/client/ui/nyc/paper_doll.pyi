# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-22
|
| ==============================================
"""


from typing import Optional, TypedDict, Dict
from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from .control import NyControl
from ..screen_node import ScreenNodeExtension
from ...._core._types._checker import args_type_check
from ...._core._types._typing import ITuple3, FTuple3


class __RenderEntityParams(TypedDict, total=False):
    entity_id: str
    entity_identifier: str
    scale: float
    render_depth: int
    init_rot_x: float
    init_rot_y: float
    init_rot_z: float
    molang_dict: Dict[str, float]
    rotation_axis: ITuple3


class __RenderSkeletonModelParams(TypedDict, total=False):
    skeleton_model_name: str
    animation: str
    animation_looped: bool
    scale: float
    render_depth: int
    init_rot_x: float
    init_rot_y: float
    init_rot_z: float
    molang_dict: Dict[str, float]
    rotation_axis: ITuple3
    light_direction: FTuple3


class __RenderBlockGeometryModelParams(TypedDict, total=False):
    block_geometry_model_name: str
    scale: float
    init_rot_x: float
    init_rot_y: float
    init_rot_z: float
    molang_dict: Dict[str, float]
    rotation_axis: ITuple3


class NyPaperDoll(NyControl):
    base_control: NeteasePaperDollUIControl
    """
    | 纸娃娃 ``NeteasePaperDollUIControl`` 实例。
    """
    def __init__(
        self: ...,
        screen_node_ex: ScreenNodeExtension,
        paper_doll_control: NeteasePaperDollUIControl,
    ) -> None: ...
    @args_type_check(str, is_method=True)
    def __div__(self, other: str) -> Optional[NyControl]: ...
    def __truediv__(self, other: str) -> Optional[NyControl]: ... # for python3

    def GetModelId(self) -> int:
        """
        | 获取渲染的骨骼模型Id。
        | 注意：请不要在 ``.RenderEntity()`` / ``.RenderSkeletonModel()`` 调用之后立即执行。
        | 骨骼模型Id可用于以下情形：1.绑定一个另外的骨骼模型； 2.绑定序列帧动画； 3.绑定特效粒子动画。

        -----

        :return: 骨骼模型Id，失败或者不存在返回-1
        :rtype: int
        """
    def RenderEntity(self, params: __RenderEntityParams) -> bool:
        """
        | 渲染实体。
        | ``params`` 参数解释如下：
        - ``entity_id`` -- str，渲染生物的实体Id，与实体的identifier二者选其一即可；如果与entity_identifier同时定义，则优先使用entity_id
        - ``entity_identifier`` -- str，渲染生物的identifier，与实体Id二者选其一即可；如果与entity_id同时定义，则优先使用entity_id
        - ``scale`` -- float，渲染缩放比例，默认为1.0
        - ``render_depth`` -- int，渲染深度，对于玩家默认-50，普通生物-15，该参数可解决UI遮挡剔除问题
        - ``init_rot_x`` -- float，初始x方向的朝向
        - ``init_rot_y`` -- float，初始y方向的朝向
        - ``init_rot_z`` -- float，初始z方向的朝向
        - ``molang_dict`` -- dict，molang表达式字典，其中key为str，value为float
        - ``rotation_axis`` -- tuple，选择旋转环绕的轴，如(0, 1, 0)依次代表x、y、z轴，此为绕y轴旋转，该属性只在netease_paper_doll_renderer控件的rotation属性为"freedom_gesture"时起效

        -----

        :param dict params: 渲染参数

        :return: 是否成功
        :rtype: bool
        """
    def RenderSkeletonModel(self, params: __RenderSkeletonModelParams) -> bool:
        """
        | 渲染骨骼模型（不依赖实体）。
        | ``params`` 参数解释如下：
        - ``skeleton_model_name`` -- str，骨骼模型名称
        - ``animation`` -- str，骨骼动作名称，默认为idle
        - ``animation_looped`` -- bool，骨骼动作是否循环播放，默认True
        - ``scale`` -- float，渲染缩放比例，默认为1.0
        - ``render_depth`` -- int，渲染深度，对于玩家默认-50，普通生物-15，该参数可解决UI遮挡剔除问题
        - ``init_rot_x`` -- float，初始x方向的朝向
        - ``init_rot_y`` -- float，初始y方向的朝向
        - ``init_rot_z`` -- float，初始z方向的朝向
        - ``molang_dict`` -- dict，molang表达式字典，其中key为str，value为float
        - ``rotation_axis`` -- tuple，选择旋转环绕的轴，如(0, 1, 0)依次代表x、y、z轴，此为绕y轴旋转，该属性只在netease_paper_doll_renderer控件的rotation属性为"freedom_gesture"时起效
        - ``light_direction`` -- tuple，可选参数；控制骨骼模型在纸娃娃中显示时的光照方向，x控制光照的左右方向，y控制光照的上下方向，z控制光照的前后方向，取值为-1,0,1；不填写该参数时模型默认从底部打光；该属性仅对没有自定义材质的骨骼模型生效，如需要对使用自定义材质的骨骼模型控制其光照方向，可以参考官方骨骼模型vertex shader中getLightColor使用到HIDE_COLOR的这部分代码；该参数对部分安卓低端设备，极低端设备无效

        -----

        :param dict params: 渲染参数

        :return: 是否成功
        :rtype: bool
        """
    def RenderBlockGeometryModel(self, params: __RenderBlockGeometryModelParams) -> bool:
        """
        | 渲染网格体模型。
        | 网格体模型使用 ``CombineBlockPaletteToGeometry()`` 生成。
        | 每次进入游戏需要重新调用本接口渲染网格体模型，可使用 ``SerializeBlockPalette()`` 和 ``DeserializeBlockPalette()`` 实现调色板保存并重载调色板，重新生成网格体模型进行渲染。
        | ``params`` 参数解释如下：
        - ``block_geometry_model_name`` -- str，网格体模型名称，可用CombineBlockPaletteToGeometry()返回值
        - ``scale`` -- float，渲染缩放比例，默认为1.0
        - ``init_rot_x`` -- float，初始x方向的朝向
        - ``init_rot_y`` -- float，初始y方向的朝向
        - ``init_rot_z`` -- float，初始z方向的朝向
        - ``molang_dict`` -- dict，molang表达式字典，其中key为str，value为float
        - ``rotation_axis`` -- tuple，选择旋转环绕的轴，如(0, 1, 0)依次代表x、y、z轴，此为绕y轴旋转，该属性只在netease_paper_doll_renderer控件的rotation属性为"freedom_gesture"时起效

        -----

        :param dict params: 渲染参数

        :return: 是否成功
        :rtype: bool
        """
