# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-09
|
| ==============================================
"""


from typing import Tuple, Union, Dict, Optional
from mod.client.component.particleControlComp import ParticleControlComp
from mod.client.component.particleTransComp import ParticleTransComp
from mod.client.component.particleEntityBindComp import ParticleEntityBindComp
from mod.client.component.particleSkeletonBindComp import ParticleSkeletonBindComp
from mod.client.component.frameAniControlComp import FrameAniControlComp
from mod.client.component.frameAniTransComp import FrameAniTransComp
from mod.client.component.frameAniEntityBindComp import FrameAniEntityBindComp
from mod.client.component.frameAniSkeletonBindComp import FrameAniSkeletonBindComp
from .._core._client._lib_client import NuoyanLibClientSystem
from .._core._types._typing import FTuple3, FTuple2


class NeteaseParticle(object):
    __lib_sys: NuoyanLibClientSystem
    _id: int
    _ctrl: ParticleControlComp
    _trans: ParticleTransComp
    _bind_ent_comp: ParticleEntityBindComp
    _bind_skel_comp: ParticleSkeletonBindComp
    _bind_ent_id: str
    _bind_ent_offset: FTuple3
    _bind_ent_rot: FTuple3
    _bind_ent_corr: bool
    _bind_skel_model_id: int
    _bind_skel_bone_name: str
    _bind_skel_offset: FTuple3
    _bind_skel_rot: FTuple3
    _playing: bool
    _destroyed: bool
    def __init__(
        self: ...,
        json_path: str,
        pos: Optional[FTuple3] = None,
        bind_entity: Optional[Dict[str, Union[str, FTuple3, bool]]] = None,
        bind_skeleton: Optional[Dict[str, Union[int, str, FTuple3]]] = None,
    ) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def ent_id(self) -> str: ...
    @ent_id.setter
    def ent_id(self, value: str) -> None: ...
    @property
    def ent_offset(self) -> FTuple3: ...
    @ent_offset.setter
    def ent_offset(self, value: FTuple3) -> None: ...
    @property
    def ent_rot(self) -> FTuple3: ...
    @ent_rot.setter
    def ent_rot(self, value: FTuple3) -> None: ...
    @property
    def correction(self) -> bool: ...
    @correction.setter
    def correction(self, value: bool) -> None: ...
    @property
    def model_id(self) -> int: ...
    @model_id.setter
    def model_id(self, value: int) -> None: ...
    @property
    def bone_name(self) -> str: ...
    @bone_name.setter
    def bone_name(self, value: str) -> None: ...
    @property
    def skel_offset(self) -> FTuple3: ...
    @skel_offset.setter
    def skel_offset(self, value: FTuple3) -> None: ...
    @property
    def skel_rot(self) -> FTuple3: ...
    @skel_rot.setter
    def skel_rot(self, value: FTuple3) -> None: ...
    @property
    def emission_rate(self) -> FTuple2: ...
    @emission_rate.setter
    def emission_rate(self, value: FTuple2) -> None: ...
    @property
    def max_num(self) -> int: ...
    @max_num.setter
    def max_num(self, value: int) -> None: ...
    @property
    def size(self) -> Tuple[FTuple2, FTuple2]: ...
    @size.setter
    def size(self, value: Tuple[FTuple2, FTuple2]) -> None: ...
    @property
    def volume_size(self) -> FTuple3: ...
    @volume_size.setter
    def volume_size(self, value: FTuple3) -> None: ...
    @property
    def pos(self) -> FTuple3: ...
    @pos.setter
    def pos(self, value: FTuple3) -> None: ...
    @property
    def rot(self) -> FTuple3: ...
    @rot.setter
    def rot(self, value: FTuple3) -> None: ...
    @property
    def playing(self) -> bool: ...
    @property
    def destroyed(self) -> bool: ...
    def BindEntity(
        self,
        ent_id: str,
        offset: FTuple3 = (0, 0, 0),
        rot: FTuple3 = (0, 0, 0),
        correction: bool = False,
    ) -> bool: ...
    def BindSkeleton(
        self,
        model_id: int,
        bone_name: str,
        offset: FTuple3 = (0, 0, 0),
        rot: FTuple3 = (0, 0, 0)
    ) -> bool: ...
    def Play(self) -> bool: ...
    def Pause(self) -> bool: ...
    def Destroy(self) -> bool: ...
    def SetFadeDistance(self, dist: float) -> bool: ...
    def SetLayer(self, layer: int) -> bool: ...
    def SetRelative(self, relative: bool) -> bool: ...
    def SetUsePointFiltering(self, use: bool) -> bool: ...


class NeteaseFrameAnim(object):
    __lib_sys: NuoyanLibClientSystem
    _id: int
    _ctrl: FrameAniControlComp
    _trans: FrameAniTransComp
    _bind_ent_comp: FrameAniEntityBindComp
    _bind_skel_comp: FrameAniSkeletonBindComp
    _bind_ent_id: str
    _bind_ent_offset: FTuple3
    _bind_ent_rot: FTuple3
    _bind_skel_model_id: int
    _bind_skel_bone_name: str
    _bind_skel_offset: FTuple3
    _bind_skel_rot: FTuple3
    _playing: bool
    _destroyed: bool
    def __init__(
        self: ...,
        json_path: str = "",
        tex_path: str = "",
        pos: Optional[FTuple3] = None,
        rot: Optional[FTuple3] = None,
        bind_entity: Optional[Dict[str, Union[str, FTuple3]]] = None,
        bind_skeleton: Optional[Dict[str, Union[int, str, FTuple3]]] = None,
    ) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def ent_id(self) -> str: ...
    @ent_id.setter
    def ent_id(self, value: str) -> None: ...
    @property
    def ent_offset(self) -> FTuple3: ...
    @ent_offset.setter
    def ent_offset(self, value: FTuple3) -> None: ...
    @property
    def ent_rot(self) -> FTuple3: ...
    @ent_rot.setter
    def ent_rot(self, value: FTuple3) -> None: ...
    @property
    def model_id(self) -> int: ...
    @model_id.setter
    def model_id(self, value: int) -> None: ...
    @property
    def bone_name(self) -> str: ...
    @bone_name.setter
    def bone_name(self, value: str) -> None: ...
    @property
    def skel_offset(self) -> FTuple3: ...
    @skel_offset.setter
    def skel_offset(self, value: FTuple3) -> None: ...
    @property
    def skel_rot(self) -> FTuple3: ...
    @skel_rot.setter
    def skel_rot(self, value: FTuple3) -> None: ...
    @property
    def pos(self) -> FTuple3: ...
    @pos.setter
    def pos(self, value: FTuple3) -> None: ...
    @property
    def rot(self) -> FTuple3: ...
    @rot.setter
    def rot(self, value: FTuple3) -> None: ...
    @property
    def scale(self) -> FTuple3: ...
    @scale.setter
    def scale(self, value: FTuple3) -> None: ...
    @property
    def playing(self) -> bool: ...
    @property
    def destroyed(self) -> bool: ...
    def BindEntity(self, bind_entity_id: str, offset: FTuple3 = (0, 0, 0), rot: FTuple3 = (0, 0, 0)) -> bool: ...
    def BindSkeleton(
        self,
        model_id: int,
        bone_name: str,
        offset: FTuple3 = (0, 0, 0),
        rot: FTuple3 = (0, 0, 0),
    ) -> bool: ...
    def Play(self) -> bool: ...
    def Pause(self) -> bool: ...
    def Destroy(self) -> bool: ...
    def SetDeepTest(self, enabled: bool) -> bool: ...
    def SetFaceCamera(self, face: bool) -> bool: ...
    def SetFadeDistance(self, dist: float) -> bool: ...
    def SetLayer(self, layer: int) -> bool: ...
    def SetLoop(self, loop: bool) -> bool: ...
    def SetUsePointFiltering(self, use: bool) -> bool: ...
    def SetGlobal(self, isGlobal: bool) -> bool: ...





















