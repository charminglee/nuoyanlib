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
#   Last Modified : 2023-09-06
#
# ====================================================


"""

clientComps
===========

该模块提供了使用存档ID（Level Id）和本地玩家ID创建客户端组件的快捷方法，同时，还提供了一些常用的变量，直接导入即可使用，无需再使用接口获取，节省了大量编写代码的时间。

-----

【模块变量说明】

1、CLIENT_ENGINE_NAMESPACE：客户端引擎事件的命名空间。

2、CLIENT_ENGINE_SYSTEM_NAME：客户端引擎系统名。

3、ClientSystem：客户端system基类。

4、ClientCompFactory：客户端引擎组件工厂。

5、ScreenNode：ScreenNode类。

6、ViewBinder：ViewBinder类。

7、ViewRequest：ViewRequest类。

8、PLAYER_ID：本地玩家ID。

9、LEVEL_ID：存档ID。

10、ClientPlayerComps：保存了使用本地玩家ID创建的所有客户端组件。

11、ClientLevelComps：保存了使用存档ID创建的所有客户端组件。

-----

【示例】

>>> from nuoyanlib import ClientPlayerComps as cpc, ClientLevelComps as clc

调用Item组件获取本地玩家手持物品，等价于clientApi.GetEngineCompFactory().CreateItem(clientApi.GetLocalPlayerId()).GetPlayerItem(2)。

>>> cpc.Item.GetPlayerItem(2)

调用Game组件添加定时器，等价于clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId()).AddTimer(1, func)。

>>> def func():
...     print("hello")
>>> clc.Game.AddTimer(1, func)

"""


import mod.client.extraClientApi as _clientApi


__all__ = [
    "CLIENT_ENGINE_NAMESPACE",
    "CLIENT_ENGINE_SYSTEM_NAME",
    "ClientSystem",
    "ClientCompFactory",
    "ScreenNode",
    "ViewBinder",
    "ViewRequest",
    "PLAYER_ID",
    "LEVEL_ID",
    "ClientPlayerComps",
    "ClientLevelComps",
]


CLIENT_ENGINE_NAMESPACE = _clientApi.GetEngineNamespace()
CLIENT_ENGINE_SYSTEM_NAME = _clientApi.GetEngineSystemName()


ClientSystem = _clientApi.GetClientSystemCls()
ClientCompFactory = _clientApi.GetEngineCompFactory()


ScreenNode = _clientApi.GetScreenNodeCls()
ViewBinder = _clientApi.GetViewBinderCls()
ViewRequest = _clientApi.GetViewViewRequestCls()


PLAYER_ID = _clientApi.GetLocalPlayerId()
LEVEL_ID = _clientApi.GetLevelId()


class _CompDescr(object):
    def __init__(self, compName):
        self.compName = compName

    def __get__(self, ins, cls):
        if self.compName not in cls._cache:
            comp = getattr(ClientCompFactory, "Create" + self.compName)(cls._target)
            # comp = self.compName
            cls._cache[self.compName] = comp
        return cls._cache[self.compName]


class ClientCompPool(object):
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


class ClientPlayerComps(ClientCompPool):
    _cache = {}
    _target = PLAYER_ID


class ClientLevelComps(ClientCompPool):
    _cache = {}
    _target = LEVEL_ID


if __name__ == "__main__":
    l = []
    for k, v in ClientCompPool.__dict__.items():
        if k.startswith("__"):
            continue
        l.append(k == v.compName)
    assert all(l)











