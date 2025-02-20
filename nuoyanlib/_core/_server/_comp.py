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


import mod.server.extraServerApi as _server_api


__all__ = [
    "SERVER_ENGINE_NAMESPACE",
    "SERVER_ENGINE_SYSTEM_NAME",
    "ServerSystem",
    "CompFactory",
    "LEVEL_ID",
    "LvComp",
]


SERVER_ENGINE_NAMESPACE = _server_api.GetEngineNamespace()
SERVER_ENGINE_SYSTEM_NAME = _server_api.GetEngineSystemName()


ServerSystem = _server_api.GetServerSystemCls()
CompFactory = _server_api.GetEngineCompFactory()


LEVEL_ID = _server_api.GetLevelId()


class CompDescr(object):
    def __init__(self, comp_name):
        self._comp_name = comp_name

    def __get__(self, ins, cls):
        if self._comp_name not in cls._cache:
            comp = getattr(CompFactory, "Create" + self._comp_name)(LEVEL_ID)
            cls._cache[self._comp_name] = comp
        return cls._cache[self._comp_name]


class __CompPool(object):
    EntityDefinitions = CompDescr("EntityDefinitions")
    AiCommand = CompDescr("AiCommand")
    BlockEntity = CompDescr("BlockEntity")
    Loot = CompDescr("Loot")
    Interact = CompDescr("Interact")
    Feature = CompDescr("Feature")
    ActorMotion = CompDescr("ActorMotion")
    CollisionBox = CompDescr("CollisionBox")
    Dimension = CompDescr("Dimension")
    BulletAttributes = CompDescr("BulletAttributes")
    EngineType = CompDescr("EngineType")
    ActorCollidable = CompDescr("ActorCollidable")
    Player = CompDescr("Player")
    RedStone = CompDescr("RedStone")
    BlockInfo = CompDescr("BlockInfo")
    Item = CompDescr("Item")
    Block = CompDescr("Block")
    Pet = CompDescr("Pet")
    Attr = CompDescr("Attr")
    Persistence = CompDescr("Persistence")
    Gravity = CompDescr("Gravity")
    Recipe = CompDescr("Recipe")
    Ride = CompDescr("Ride")
    BlockUseEventWhiteList = CompDescr("BlockUseEventWhiteList")
    Explosion = CompDescr("Explosion")
    Scale = CompDescr("Scale")
    Biome = CompDescr("Biome")
    Pos = CompDescr("Pos")
    Fly = CompDescr("Fly")
    Hurt = CompDescr("Hurt")
    Projectile = CompDescr("Projectile")
    ExtraData = CompDescr("ExtraData")
    ItemBanned = CompDescr("ItemBanned")
    ActorLoot = CompDescr("ActorLoot")
    EntityComponent = CompDescr("EntityComponent")
    Tag = CompDescr("Tag")
    Breath = CompDescr("Breath")
    BlockState = CompDescr("BlockState")
    Achievement = CompDescr("Achievement")
    ChestBlock = CompDescr("ChestBlock")
    Weather = CompDescr("Weather")
    Lv = CompDescr("Lv")
    AuxValue = CompDescr("AuxValue")
    MoveTo = CompDescr("MoveTo")
    Action = CompDescr("Action")
    Command = CompDescr("Command")
    BlockEntityData = CompDescr("BlockEntityData")
    ActorOwner = CompDescr("ActorOwner")
    Tame = CompDescr("Tame")
    Http = CompDescr("Http")
    Portal = CompDescr("Portal")
    ChunkSource = CompDescr("ChunkSource")
    ControlAi = CompDescr("ControlAi")
    MobSpawn = CompDescr("MobSpawn")
    Model = CompDescr("Model")
    ChatExtension = CompDescr("ChatExtension")
    ActorPushable = CompDescr("ActorPushable")
    Exp = CompDescr("Exp")
    Rot = CompDescr("Rot")
    Game = CompDescr("Game")
    Shareables = CompDescr("Shareables")
    Effect = CompDescr("Effect")
    Msg = CompDescr("Msg")
    ModAttr = CompDescr("ModAttr")
    Time = CompDescr("Time")
    EntityEvent = CompDescr("EntityEvent")
    Name = CompDescr("Name")


class LvComp(__CompPool):
    _cache = {}


if __name__ == "__main__":
    l = []
    for k, v in __CompPool.__dict__.items():
        if k.startswith("__"):
            continue
        l.append(k == v._comp_name)
    assert all(l)










