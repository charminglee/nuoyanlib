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


from typing import Tuple, Union, Dict, Optional
from mod.client.system.clientSystem import ClientSystem
from mod.client.component.particleControlComp import ParticleControlComp
from mod.client.component.particleTransComp import ParticleTransComp
from mod.client.component.particleEntityBindComp import ParticleEntityBindComp
from mod.client.component.particleSkeletonBindComp import ParticleSkeletonBindComp
from mod.client.component.frameAniControlComp import FrameAniControlComp
from mod.client.component.frameAniTransComp import FrameAniTransComp
from mod.client.component.frameAniEntityBindComp import FrameAniEntityBindComp
from mod.client.component.frameAniSkeletonBindComp import FrameAniSkeletonBindComp


class NeteaseParticle(object):
    __cs: ClientSystem
    _id: int
    _ctrl: ParticleControlComp
    _trans: ParticleTransComp
    _bind_ent_comp: ParticleEntityBindComp
    _bind_skel_comp: ParticleSkeletonBindComp
    _bind_ent_id: str
    _bind_ent_offset: Tuple[float, float, float]
    _bind_ent_rot: Tuple[float, float, float]
    _bind_ent_corr: bool
    _bind_skel_model_id: int
    _bind_skel_bone_name: str
    _bind_skel_offset: Tuple[float, float, float]
    _bind_skel_rot: Tuple[float, float, float]
    _playing: bool
    _destroyed: bool
    def __init__(
        self,
        json_path: str,
        pos: Optional[Tuple[float, float, float]] = None,
        bind_entity: Optional[Dict[str, Union[str, Tuple[float, float, float], bool]]] = None,
        bind_skeleton: Optional[Dict[str, Union[int, str, Tuple[float, float, float]]]] = None,
    ) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def ent_id(self) -> str: ...
    @ent_id.setter
    def ent_id(self, value: str) -> None: ...
    @property
    def ent_offset(self) -> Tuple[float, float, float]: ...
    @ent_offset.setter
    def ent_offset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def ent_rot(self) -> Tuple[float, float, float]: ...
    @ent_rot.setter
    def ent_rot(self, value: Tuple[float, float, float]) -> None: ...
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
    def skel_offset(self) -> Tuple[float, float, float]: ...
    @skel_offset.setter
    def skel_offset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def skel_rot(self) -> Tuple[float, float, float]: ...
    @skel_rot.setter
    def skel_rot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def emission_rate(self) -> Tuple[float, float]: ...
    @emission_rate.setter
    def emission_rate(self, value: Tuple[float, float]) -> None: ...
    @property
    def max_num(self) -> int: ...
    @max_num.setter
    def max_num(self, value: int) -> None: ...
    @property
    def size(self) -> Tuple[Tuple[float, float], Tuple[float, float]]: ...
    @size.setter
    def size(self, value: Tuple[Tuple[float, float], Tuple[float, float]]) -> None: ...
    @property
    def volume_size(self) -> Tuple[float, float, float]: ...
    @volume_size.setter
    def volume_size(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def pos(self) -> Tuple[float, float, float]: ...
    @pos.setter
    def pos(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def rot(self) -> Tuple[float, float, float]: ...
    @rot.setter
    def rot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def playing(self) -> bool: ...
    @property
    def destroyed(self) -> bool: ...
    def BindEntity(
        self,
        ent_id: str,
        offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rot: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        correction: bool = False,
    ) -> bool: ...
    def BindSkeleton(
        self,
        model_id: int,
        bone_name: str,
        offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rot: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    ) -> bool: ...
    def Play(self) -> bool: ...
    def Pause(self) -> bool: ...
    def Destroy(self) -> bool: ...
    def SetFadeDistance(self, dist: float) -> bool: ...
    def SetLayer(self, layer: int) -> bool: ...
    def SetRelative(self, relative: bool) -> bool: ...
    def SetUsePointFiltering(self, use: bool) -> bool: ...


class NeteaseFrameAnim(object):
    __cs: ClientSystem
    _id: int
    _ctrl: FrameAniControlComp
    _trans: FrameAniTransComp
    _bind_ent_comp: FrameAniEntityBindComp
    _bind_skel_comp: FrameAniSkeletonBindComp
    _bind_ent_id: str
    _bind_ent_offset: Tuple[float, float, float]
    _bind_ent_rot: Tuple[float, float, float]
    _bind_skel_model_id: int
    _bind_skel_bone_name: str
    _bind_skel_offset: Tuple[float, float, float]
    _bind_skel_rot: Tuple[float, float, float]
    _playing: bool
    _destroyed: bool
    def __init__(
        self,
        json_path: str = "",
        tex_path: str = "",
        pos: Optional[Tuple[float, float, float]] = None,
        rot: Optional[Tuple[float, float, float]] = None,
        bind_entity: Optional[Dict[str, Union[str, Tuple[float, float, float]]]] = None,
        bind_skeleton: Optional[Dict[str, Union[int, str, Tuple[float, float, float]]]] = None,
    ) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def ent_id(self) -> str: ...
    @ent_id.setter
    def ent_id(self, value: str) -> None: ...
    @property
    def ent_offset(self) -> Tuple[float, float, float]: ...
    @ent_offset.setter
    def ent_offset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def ent_rot(self) -> Tuple[float, float, float]: ...
    @ent_rot.setter
    def ent_rot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def model_id(self) -> int: ...
    @model_id.setter
    def model_id(self, value: int) -> None: ...
    @property
    def bone_name(self) -> str: ...
    @bone_name.setter
    def bone_name(self, value: str) -> None: ...
    @property
    def skel_offset(self) -> Tuple[float, float, float]: ...
    @skel_offset.setter
    def skel_offset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def skel_rot(self) -> Tuple[float, float, float]: ...
    @skel_rot.setter
    def skel_rot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def pos(self) -> Tuple[float, float, float]: ...
    @pos.setter
    def pos(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def rot(self) -> Tuple[float, float, float]: ...
    @rot.setter
    def rot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def scale(self) -> Tuple[float, float, float]: ...
    @scale.setter
    def scale(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def playing(self) -> bool: ...
    @property
    def destroyed(self) -> bool: ...
    def BindEntity(
        self,
        bind_entity_id: str,
        offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rot: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> bool: ...
    def BindSkeleton(
        self,
        model_id: int,
        bone_name: str,
        offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rot: Tuple[float, float, float] = (0.0, 0.0, 0.0),
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





















