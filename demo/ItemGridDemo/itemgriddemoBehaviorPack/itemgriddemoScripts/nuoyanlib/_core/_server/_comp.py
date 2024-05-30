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
#   Last Modified : 2024-01-11
#
# ====================================================


import mod.server.extraServerApi as api


__all__ = [
    "SERVER_ENGINE_NAMESPACE",
    "SERVER_ENGINE_SYSTEM_NAME",
    "ServerSystem",
    "CompFactory",
    "LEVEL_ID",
    "LvComp",
]


SERVER_ENGINE_NAMESPACE = api.GetEngineNamespace()
SERVER_ENGINE_SYSTEM_NAME = api.GetEngineSystemName()


ServerSystem = api.GetServerSystemCls()
CompFactory = api.GetEngineCompFactory()


LEVEL_ID = api.GetLevelId()


class _CompDescr(object):
    def __init__(self, comp_name):
        self.comp_name = comp_name

    def __get__(self, ins, cls):
        if self.comp_name not in cls._cache:
            comp = getattr(CompFactory, "Create" + self.comp_name)(LEVEL_ID)
            cls._cache[self.comp_name] = comp
        return cls._cache[self.comp_name]


class _CompPool(object):
    EntityDefinitions = _CompDescr("EntityDefinitions")
    AiCommand = _CompDescr("AiCommand")
    BlockEntity = _CompDescr("BlockEntity")
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


class LvComp(_CompPool):
    _cache = {}


if __name__ == "__main__":
    l = []
    for k, v in _CompPool.__dict__.items():
        if k.startswith("__"):
            continue
        l.append(k == v.comp_name)
    assert all(l)










