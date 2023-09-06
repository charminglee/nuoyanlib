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

serverComps
===========

该模块提供了使用存档ID（Level Id）创建服务端组件的快捷方法，同时，还提供了一些常用的变量，直接导入即可使用，无需再使用接口获取，节省了大量编写代码的时间。

-----

【模块变量说明】

1、SERVER_ENGINE_NAMESPACE：服务端引擎事件的命名空间。

2、SERVER_ENGINE_SYSTEM_NAME：服务端引擎系统名。

3、ClientSystem：服务端system基类。

4、ServerCompFactory：服务端引擎组件工厂。

5、LEVEL_ID：存档ID。

6、LevelComps：保存了使用存档ID创建的所有服务端组件。

-----

【示例】

>>> from nuoyanlib import ServerLevelComps as slc

调用Game组件添加定时器，等价于serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId()).AddTimer(1, func)。

>>> def func():
...     print("hello")
>>> slc.Game.AddTimer(1, func)

"""


import mod.server.extraServerApi as _serverApi


__all__ = [
    "SERVER_ENGINE_NAMESPACE",
    "SERVER_ENGINE_SYSTEM_NAME",
    "ServerSystem",
    "ServerCompFactory",
    "LEVEL_ID",
    "ServerLevelComps",
]


SERVER_ENGINE_NAMESPACE = _serverApi.GetEngineNamespace()
SERVER_ENGINE_SYSTEM_NAME = _serverApi.GetEngineSystemName()


ServerSystem = _serverApi.GetServerSystemCls()
ServerCompFactory = _serverApi.GetEngineCompFactory()


LEVEL_ID = _serverApi.GetLevelId()


class _CompDescr(object):
    def __init__(self, compName):
        self.compName = compName

    def __get__(self, ins, cls):
        if self.compName not in cls._cache:
            comp = getattr(ServerCompFactory, "Create" + self.compName)(LEVEL_ID)
            # comp = self.compName
            cls._cache[self.compName] = comp
        return cls._cache[self.compName]


class ServerCompPool(object):
    Loot = _CompDescr("Loot")
    Interact = _CompDescr("Interact")
    Feature = _CompDescr("Feature")
    ActorMotion = _CompDescr("ActorMotion")
    CollisionBox = _CompDescr("CollisionBox")
    Dimension = _CompDescr("Dimension")
    BulletAttributes = _CompDescr("BulletAttributes")
    EngineType = _CompDescr("EngineType")
    ActorCollidable = _CompDescr("ActorCollidable")
    Player = _CompDescr("Player")
    RedStone = _CompDescr("RedStone")
    BlockInfo = _CompDescr("BlockInfo")
    Item = _CompDescr("Item")
    Block = _CompDescr("Block")
    Pet = _CompDescr("Pet")
    Attr = _CompDescr("Attr")
    Persistence = _CompDescr("Persistence")
    Gravity = _CompDescr("Gravity")
    Recipe = _CompDescr("Recipe")
    Ride = _CompDescr("Ride")
    BlockUseEventWhiteList = _CompDescr("BlockUseEventWhiteList")
    Explosion = _CompDescr("Explosion")
    Scale = _CompDescr("Scale")
    Biome = _CompDescr("Biome")
    Pos = _CompDescr("Pos")
    Fly = _CompDescr("Fly")
    Hurt = _CompDescr("Hurt")
    Projectile = _CompDescr("Projectile")
    ExtraData = _CompDescr("ExtraData")
    ItemBanned = _CompDescr("ItemBanned")
    ActorLoot = _CompDescr("ActorLoot")
    EntityComponent = _CompDescr("EntityComponent")
    Tag = _CompDescr("Tag")
    Breath = _CompDescr("Breath")
    BlockState = _CompDescr("BlockState")
    Achievement = _CompDescr("Achievement")
    ChestBlock = _CompDescr("ChestBlock")
    Weather = _CompDescr("Weather")
    Lv = _CompDescr("Lv")
    AuxValue = _CompDescr("AuxValue")
    MoveTo = _CompDescr("MoveTo")
    Action = _CompDescr("Action")
    Command = _CompDescr("Command")
    BlockEntityData = _CompDescr("BlockEntityData")
    ActorOwner = _CompDescr("ActorOwner")
    Tame = _CompDescr("Tame")
    Http = _CompDescr("Http")
    Portal = _CompDescr("Portal")
    ChunkSource = _CompDescr("ChunkSource")
    ControlAi = _CompDescr("ControlAi")
    MobSpawn = _CompDescr("MobSpawn")
    Model = _CompDescr("Model")
    ChatExtension = _CompDescr("ChatExtension")
    ActorPushable = _CompDescr("ActorPushable")
    Exp = _CompDescr("Exp")
    Rot = _CompDescr("Rot")
    Game = _CompDescr("Game")
    Shareables = _CompDescr("Shareables")
    Effect = _CompDescr("Effect")
    Msg = _CompDescr("Msg")
    ModAttr = _CompDescr("ModAttr")
    Time = _CompDescr("Time")
    EntityEvent = _CompDescr("EntityEvent")
    Name = _CompDescr("Name")


class ServerLevelComps(ServerCompPool):
    _cache = {}


if __name__ == "__main__":
    l = []
    for k, v in ServerCompPool.__dict__.items():
        if k.startswith("__"):
            continue
        l.append(k == v.compName)
    assert all(l)










