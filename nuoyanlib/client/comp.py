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


"""

clientComps
===========

该模块提供了使用存档ID（Level Id）和本地玩家ID创建客户端组件的快捷方法，同时，还提供了一些常用的变量，直接导入即可使用，无需再使用接口获取，节省了大量编写代码的时间。

"""


import mod.client.extraClientApi as _clientApi


__all__ = [
    "CLIENT_ENGINE_NAMESPACE",
    "CLIENT_ENGINE_SYSTEM_NAME",
    "ClientSystem",
    "CompFactory",
    "ScreenNode",
    "ViewBinder",
    "ViewRequest",
    "PLAYER_ID",
    "LEVEL_ID",
    "PlrComp",
    "LvComp",
]


CLIENT_ENGINE_NAMESPACE = _clientApi.GetEngineNamespace()
CLIENT_ENGINE_SYSTEM_NAME = _clientApi.GetEngineSystemName()


ClientSystem = _clientApi.GetClientSystemCls()
CompFactory = _clientApi.GetEngineCompFactory()


ScreenNode = _clientApi.GetScreenNodeCls()
ViewBinder = _clientApi.GetViewBinderCls()
ViewRequest = _clientApi.GetViewViewRequestCls()


PLAYER_ID = _clientApi.GetLocalPlayerId()
LEVEL_ID = _clientApi.GetLevelId()


class _CompDescr(object):
    def __init__(self, comp_name):
        self.comp_name = comp_name

    def __get__(self, ins, cls):
        if self.comp_name not in cls._cache:
            comp = getattr(CompFactory, "Create" + self.comp_name)(cls._target)
            cls._cache[self.comp_name] = comp
        return cls._cache[self.comp_name]


class _CompPool(object):
    Action = _CompDescr("Action")
    ActorCollidable = _CompDescr("ActorCollidable")
    ActorMotion = _CompDescr("ActorMotion")
    ActorRender = _CompDescr("ActorRender")
    Attr = _CompDescr("Attr")
    AuxValue = _CompDescr("AuxValue")
    Biome = _CompDescr("Biome")
    Block = _CompDescr("Block")
    BlockGeometry = _CompDescr("BlockGeometry")
    BlockInfo = _CompDescr("BlockInfo")
    BlockUseEventWhiteList = _CompDescr("BlockUseEventWhiteList")
    Brightness = _CompDescr("Brightness")
    Camera = _CompDescr("Camera")
    ChunkSource = _CompDescr("ChunkSource")
    CollisionBox = _CompDescr("CollisionBox")
    ConfigClient = _CompDescr("ConfigClient")
    CustomAudio = _CompDescr("CustomAudio")
    Device = _CompDescr("Device")
    Effect = _CompDescr("Effect")
    EngineEffectBindControl = _CompDescr("EngineEffectBindControl")
    EngineType = _CompDescr("EngineType")
    Fog = _CompDescr("Fog")
    FrameAniControl = _CompDescr("FrameAniControl")
    FrameAniEntityBind = _CompDescr("FrameAniEntityBind")
    FrameAniSkeletonBind = _CompDescr("FrameAniSkeletonBind")
    FrameAniTrans = _CompDescr("FrameAniTrans")
    Game = _CompDescr("Game")
    Health = _CompDescr("Health")
    Item = _CompDescr("Item")
    ModAttr = _CompDescr("ModAttr")
    Model = _CompDescr("Model")
    Name = _CompDescr("Name")
    NeteaseShop = _CompDescr("NeteaseShop")
    Operation = _CompDescr("Operation")
    ParticleControl = _CompDescr("ParticleControl")
    ParticleEntityBind = _CompDescr("ParticleEntityBind")
    ParticleSkeletonBind = _CompDescr("ParticleSkeletonBind")
    ParticleSystem = _CompDescr("ParticleSystem")
    ParticleTrans = _CompDescr("ParticleTrans")
    Player = _CompDescr("Player")
    PlayerAnim = _CompDescr("PlayerAnim")
    PlayerView = _CompDescr("PlayerView")
    Pos = _CompDescr("Pos")
    PostProcess = _CompDescr("PostProcess")
    QueryVariable = _CompDescr("QueryVariable")
    Recipe = _CompDescr("Recipe")
    Ride = _CompDescr("Ride")
    Rot = _CompDescr("Rot")
    SkyRender = _CompDescr("SkyRender")
    Tame = _CompDescr("Tame")
    TextBoard = _CompDescr("TextBoard")
    TextNotifyClient = _CompDescr("TextNotifyClient")
    Time = _CompDescr("Time")
    VirtualWorld = _CompDescr("VirtualWorld")


class PlrComp(_CompPool):
    _cache = {}
    _target = PLAYER_ID


class LvComp(_CompPool):
    _cache = {}
    _target = LEVEL_ID


if __name__ == "__main__":
    l = []
    for k, v in _CompPool.__dict__.items():
        if k.startswith("__"):
            continue
        l.append(k == v.comp_name)
    assert all(l)








