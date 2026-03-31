# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-2-11
#  ⠀
# =================================================


import mod.server.extraServerApi as s_api
from mod.common.minecraftEnum import EntityType
from ..core._sys import get_lib_system
from ..core.server.comp import CF
from ..common.enum import TimeEaseFunc
from ..common.mc_math.vector import vec_normalize


__all__ = [
    "set_motion",
    "start_mover",
    "move_entity",
    "entity_plunge",
    "entity_plunge_by_dir",
    "entity_plunge_by_rot",
]


def set_motion(entity_id, motion):
    """
    设置实体（包括玩家）的瞬时移动方向向量。

    -----

    :param str entity_id: 实体ID
    :param tuple[float,float,float] motion: 瞬时移动方向向量

    :return: 无
    :rtype: None
    """
    cf = CF(entity_id)
    if cf.EngineType.GetEngineType() == EntityType.Player:
        cf.ActorMotion.SetPlayerMotion(motion)
    else:
        cf.ActorMotion.SetMotion(motion)


def start_mover(entity_id, mover_id):
    """
    启动实体（包括玩家）身上的运动器。

    -----

    :param str entity_id: 实体ID
    :param int mover_id: 运动器ID

    :return: 无
    :rtype: None
    """
    cf = CF(entity_id)
    if cf.EngineType.GetEngineType() == EntityType.Player:
        cf.ActorMotion.StartPlayerMotion(mover_id)
    else:
        cf.ActorMotion.StartEntityMotion(mover_id)


def move_entity(entity_id, direction, dist, time, is_throughable=False, ease_func=TimeEaseFunc.LINEAR):
    """
    设置实体位移。

    -----

    :param str entity_id: 实体ID
    :param tuple[float,float,float] direction: 位移方向向量
    :param float dist: 位移距离
    :param float time: 位移总时间，单位秒
    :param bool is_throughable: 是否可穿墙；默认为 False
    :param function ease_func: 位移缓动函数；默认为 TimeEaseFunc.LINEAR

    :return: 无
    :rtype: None
    """
    direction = vec_normalize(direction)
    if is_throughable:
        _move_entity_throughable(entity_id, direction, dist, time, ease_func)
    else:
        get_lib_system().move_entity(entity_id, direction, dist, time, ease_func)


def _move_entity_throughable(entity_id, direction, dist, time, ease_func=TimeEaseFunc.LINEAR):
    pass


def entity_plunge(entity_id1, entity_id2, speed):
    """
    使实体1向实体2的准星方向突进。

    -----

    :param str entity_id1: 实体1ID
    :param str entity_id2: 实体2ID
    :param float speed: 突进速度

    :return: 无
    :rtype: None
    """
    rot = CF(entity_id2).Rot.GetRot()
    if not rot:
        return
    entity_plunge_by_rot(entity_id1, rot, speed)


def entity_plunge_by_dir(entity_id, direction, speed):
    """
    使实体以指定方向和速度突进。

    -----

    :param str entity_id: 实体ID
    :param tuple[float,float,float] direction: 方向的单位向量
    :param float speed: 速度大小

    :return: 无
    :rtype: None
    """
    cf = CF(entity_id)
    motion = tuple(map(lambda x: x * speed, direction))
    motion_comp = cf.ActorMotion
    etype = cf.EngineType.GetEngineType()
    if etype == EntityType.Player:
        motion_comp.SetPlayerMotion(motion)
    else:
        motion_comp.SetMotion(motion)


def entity_plunge_by_rot(entity_id, rot, speed):
    """
    使实体向指定视角方向突进。

    -----

    :param str entity_id: 实体ID
    :param tuple[float, float] rot: 视角
    :param float speed: 速度

    :return: 无
    :rtype: None
    """
    direction = s_api.GetDirFromRot(rot)
    entity_plunge_by_dir(entity_id, direction, speed)



























