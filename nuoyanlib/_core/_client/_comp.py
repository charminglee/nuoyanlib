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
#   Last Modified : 2025-05-28
#
# ====================================================


import mod.client.extraClientApi as _client_api


ENGINE_NAMESPACE = _client_api.GetEngineNamespace()
ENGINE_SYSTEM_NAME = _client_api.GetEngineSystemName()
PLAYER_ID = _client_api.GetLocalPlayerId()
LEVEL_ID = _client_api.GetLevelId()
ClientSystem = _client_api.GetClientSystemCls()
CompFactory = _client_api.GetEngineCompFactory()


ScreenNode = _client_api.GetScreenNodeCls()
ViewBinder = _client_api.GetViewBinderCls()
ViewRequest = _client_api.GetViewViewRequestCls()
CustomUIScreenProxy = _client_api.GetUIScreenProxyCls()
CustomUIControlProxy = _client_api.GetCustomUIControlProxyCls()
# noinspection PyUnresolvedReferences
NativeScreenManager = _client_api.GetNativeScreenManagerCls().instance()
MiniMapScreenNode = _client_api.GetMiniMapScreenNodeCls()


class CompDescr(object):
    def __init__(self, comp_name):
        self.comp_name = comp_name

    def __get__(self, ins, cls):
        if self.comp_name not in cls._cache:
            comp = getattr(CompFactory, "Create" + self.comp_name)(cls._target)
            cls._cache[self.comp_name] = comp
        return cls._cache[self.comp_name]


class __CompPool(object):
    Action = CompDescr("Action")
    ActorCollidable = CompDescr("ActorCollidable")
    ActorMotion = CompDescr("ActorMotion")
    ActorRender = CompDescr("ActorRender")
    Attr = CompDescr("Attr")
    AuxValue = CompDescr("AuxValue")
    Biome = CompDescr("Biome")
    Block = CompDescr("Block")
    BlockGeometry = CompDescr("BlockGeometry")
    BlockInfo = CompDescr("BlockInfo")
    BlockUseEventWhiteList = CompDescr("BlockUseEventWhiteList")
    Brightness = CompDescr("Brightness")
    Camera = CompDescr("Camera")
    ChunkSource = CompDescr("ChunkSource")
    CollisionBox = CompDescr("CollisionBox")
    ConfigClient = CompDescr("ConfigClient")
    CustomAudio = CompDescr("CustomAudio")
    Device = CompDescr("Device")
    Effect = CompDescr("Effect")
    EngineEffectBindControl = CompDescr("EngineEffectBindControl")
    EngineType = CompDescr("EngineType")
    Fog = CompDescr("Fog")
    FrameAniControl = CompDescr("FrameAniControl")
    FrameAniEntityBind = CompDescr("FrameAniEntityBind")
    FrameAniSkeletonBind = CompDescr("FrameAniSkeletonBind")
    FrameAniTrans = CompDescr("FrameAniTrans")
    Game = CompDescr("Game")
    Health = CompDescr("Health")
    Item = CompDescr("Item")
    ModAttr = CompDescr("ModAttr")
    Model = CompDescr("Model")
    Name = CompDescr("Name")
    NeteaseShop = CompDescr("NeteaseShop")
    Operation = CompDescr("Operation")
    ParticleControl = CompDescr("ParticleControl")
    ParticleEntityBind = CompDescr("ParticleEntityBind")
    ParticleSkeletonBind = CompDescr("ParticleSkeletonBind")
    ParticleSystem = CompDescr("ParticleSystem")
    ParticleTrans = CompDescr("ParticleTrans")
    Player = CompDescr("Player")
    PlayerAnim = CompDescr("PlayerAnim")
    PlayerView = CompDescr("PlayerView")
    Pos = CompDescr("Pos")
    PostProcess = CompDescr("PostProcess")
    QueryVariable = CompDescr("QueryVariable")
    Recipe = CompDescr("Recipe")
    Ride = CompDescr("Ride")
    Rot = CompDescr("Rot")
    SkyRender = CompDescr("SkyRender")
    Tame = CompDescr("Tame")
    TextBoard = CompDescr("TextBoard")
    TextNotifyClient = CompDescr("TextNotifyClient")
    Time = CompDescr("Time")
    VirtualWorld = CompDescr("VirtualWorld")


class PlrComp(__CompPool):
    _cache = {}
    _target = PLAYER_ID


class LvComp(__CompPool):
    _cache = {}
    _target = LEVEL_ID


if __name__ == "__main__":
    l = []
    for k, v in __CompPool.__dict__.items():
        if k.startswith("__"):
            continue
        l.append(k == v.comp_name)
    assert all(l)








