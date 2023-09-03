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
#   Last Modified : 2023-09-03
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
    _bindEntComp: ParticleEntityBindComp
    _bindSkelComp: ParticleSkeletonBindComp
    _bindEntId: str
    _bindEntOffset: Tuple[float, float, float]
    _bindEntRot: Tuple[float, float, float]
    _bindEntCorrection: bool
    _bindSkelModelId: int
    _bindSkelBoneName: str
    _bindSkelOffset: Tuple[float, float, float]
    _bindSkelRot: Tuple[float, float, float]
    _playing: bool
    _destroyed: bool
    def __init__(
        self,
        jsonPath: str,
        pos: Optional[Tuple[float, float, float]] = None,
        bindEntity: Optional[Dict[str, Union[str, Tuple[float, float, float], bool]]] = None,
        bindSkeleton: Optional[Dict[str, Union[int, str, Tuple[float, float, float]]]] = None,
    ) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def bindEntId(self) -> str: ...
    @bindEntId.setter
    def bindEntId(self, value: str) -> None: ...
    @property
    def bindEntOffset(self) -> Tuple[float, float, float]: ...
    @bindEntOffset.setter
    def bindEntOffset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def bindEntRot(self) -> Tuple[float, float, float]: ...
    @bindEntRot.setter
    def bindEntRot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def bindEntCorrection(self) -> bool: ...
    @bindEntCorrection.setter
    def bindEntCorrection(self, value: bool) -> None: ...
    @property
    def bindSkelModelId(self) -> int: ...
    @bindSkelModelId.setter
    def bindSkelModelId(self, value: int) -> None: ...
    @property
    def bindSkelBoneName(self) -> str: ...
    @bindSkelBoneName.setter
    def bindSkelBoneName(self, value: str) -> None: ...
    @property
    def bindSkelOffset(self) -> Tuple[float, float, float]: ...
    @bindSkelOffset.setter
    def bindSkelOffset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def bindSkelRot(self) -> Tuple[float, float, float]: ...
    @bindSkelRot.setter
    def bindSkelRot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def emissionRate(self) -> Tuple[float, float]: ...
    @emissionRate.setter
    def emissionRate(self, value: Tuple[float, float]) -> None: ...
    @property
    def maxNum(self) -> int: ...
    @maxNum.setter
    def maxNum(self, value: int) -> None: ...
    @property
    def size(self) -> Tuple[Tuple[float, float], Tuple[float, float]]: ...
    @size.setter
    def size(self, value: Tuple[Tuple[float, float], Tuple[float, float]]) -> None: ...
    @property
    def volumeSize(self) -> Tuple[float, float, float]: ...
    @volumeSize.setter
    def volumeSize(self, value: Tuple[float, float, float]) -> None: ...
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
        bindEntityId: str,
        offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rot: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        correction: bool = False,
    ) -> bool: ...
    def BindSkeleton(
        self,
        modelId: int,
        boneName: str,
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
    _bindEntComp: FrameAniEntityBindComp
    _bindSkelComp: FrameAniSkeletonBindComp
    _bindEntId: str
    _bindEntOffset: Tuple[float, float, float]
    _bindEntRot: Tuple[float, float, float]
    _bindSkelModelId: int
    _bindSkelBoneName: str
    _bindSkelOffset: Tuple[float, float, float]
    _bindSkelRot: Tuple[float, float, float]
    _playing: bool
    _destroyed: bool
    def __init__(
        self,
        jsonPath: str = "",
        texPath: str = "",
        pos: Optional[Tuple[float, float, float]] = None,
        rot: Optional[Tuple[float, float, float]] = None,
        bindEntity: Optional[Dict[str, Union[str, Tuple[float, float, float]]]] = None,
        bindSkeleton: Optional[Dict[str, Union[int, str, Tuple[float, float, float]]]] = None,
    ) -> None: ...
    @property
    def id(self) -> int: ...
    @property
    def bindEntId(self) -> str: ...
    @bindEntId.setter
    def bindEntId(self, value: str) -> None: ...
    @property
    def bindEntOffset(self) -> Tuple[float, float, float]: ...
    @bindEntOffset.setter
    def bindEntOffset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def bindEntRot(self) -> Tuple[float, float, float]: ...
    @bindEntRot.setter
    def bindEntRot(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def bindSkelModelId(self) -> int: ...
    @bindSkelModelId.setter
    def bindSkelModelId(self, value: int) -> None: ...
    @property
    def bindSkelBoneName(self) -> str: ...
    @bindSkelBoneName.setter
    def bindSkelBoneName(self, value: str) -> None: ...
    @property
    def bindSkelOffset(self) -> Tuple[float, float, float]: ...
    @bindSkelOffset.setter
    def bindSkelOffset(self, value: Tuple[float, float, float]) -> None: ...
    @property
    def bindSkelRot(self) -> Tuple[float, float, float]: ...
    @bindSkelRot.setter
    def bindSkelRot(self, value: Tuple[float, float, float]) -> None: ...
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
        bindEntityId: str,
        offset: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rot: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    ) -> bool: ...
    def BindSkeleton(
        self,
        modelId: int,
        boneName: str,
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





















