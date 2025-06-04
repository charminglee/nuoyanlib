# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


import mod.server.extraServerApi as _server_api
from mod.common.minecraftEnum import EntityType as _EntityType
from .._core._server import _comp, _lib_server
from ..utils import (
    mc_math as _mc_math,
    vector as _vector,
)


__all__ = [
    "set_query_mod_var",
    "clear_effects",
    "bounce_entities",
    "attract_entities",
    "is_mob",
    "all_mob",
    "any_mob",
    "entity_filter",
    "is_entity_type",
    "sort_entity_list_by_dist",
    "launch_projectile",
    "entity_plunge",
    "entity_plunge_by_dir",
    "entity_plunge_by_rot",
    "get_all_entities",
    "get_entities_by_name",
    "get_entities_by_type",
    "get_entities_in_area",
    "get_entities_by_locking",
    "get_nearest_entity",
    "attack_nearest_mob",
    "has_effect",
    "get_entities_by_ray",
    "entity_distance",
]


def set_query_mod_var(entity_id, name, value):
    """
    | 设置指定实体 ``query.mod`` 变量的值，全局同步。
    | 若设置的变量未注册，则自动进行注册。

    -----

    :param str entity_id: 实体ID
    :param str name: 变量名
    :param float value: 设置的值

    :return: 是否成功
    :rtype: bool
    """
    lib_sys = _lib_server.instance()
    if not lib_sys:
        return False
    lib_sys._SetQueryVar({'entity_id': entity_id, 'name': name, 'value': value})
    return True


def clear_effects(entity_id):
    """
    | 清除指定实体的全部药水效果。

    -----

    :param str entity_id: 实体ID

    :return: 无
    :rtype: None
    """
    comp = _comp.CF(entity_id).Effect
    effects = comp.GetAllEffects()
    if effects:
        for eff in effects:
            comp.RemoveEffectFromEntity(eff['effectName'])


def bounce_entities(
        pos,
        dim,
        radius,
        power,
        filter_ids=None,
        filter_types=None,
        filter_type_str=None,
        filter_abiotic=False,
):
    """
    | 从中心弹开指定范围内的实体。

    -----

    :param tuple[float,float,float] pos: 弹开中心坐标
    :param int dim: 维度ID
    :param float radius: 弹开半径
    :param float power: 弹开强度
    :param list[str]|None filter_ids: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filter_type_str: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filter_abiotic: 是否过滤非生物实体，默认为不过滤

    :return: 被弹开的实体ID列表
    :rtype: list[str]
    """
    return attract_entities(
        pos, dim, radius, -power, filter_ids, filter_types, filter_type_str, filter_abiotic
    )


def attract_entities(
        pos,
        dim,
        radius,
        power,
        filter_ids=None,
        filter_types=None,
        filter_type_str=None,
        filter_abiotic=False,
):
    """
    | 吸引指定范围内的实体到中心。

    -----

    :param tuple[float,float,float] pos: 吸引中心坐标
    :param int dim: 维度ID
    :param float radius: 吸引半径
    :param float power: 吸引强度
    :param list[str]|None filter_ids: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filter_type_str: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filter_abiotic: 是否过滤非生物实体，默认为不过滤

    :return: 被吸引的实体ID列表
    :rtype: list[str]
    """
    ents = get_entities_in_area(
        pos, radius, dim, filter_ids, filter_types, filter_type_str, filter_abiotic
    )
    res = []
    for eid in ents:
        cf = _comp.CF(eid)
        epos = cf.Pos.GetFootPos()
        if not epos:
            continue
        motion = cf.ActorMotion
        orig_motion = motion.GetMotion()
        vec = _vector.vec_p2p(epos, pos)
        vec = tuple(i * power for i in vec)
        res_motion = _vector.vec_composite(orig_motion, vec)
        etype = cf.EngineType.GetEngineType()
        if etype == _EntityType.Player:
            if motion.SetPlayerMotion(res_motion):
                res.append(eid)
        else:
            if motion.SetMotion(res_motion):
                res.append(eid)
    return res


def is_mob(entity_id):
    """
    | 判断实体是否为生物。

    -----

    :param str entity_id: 实体ID

    :return: 是生物返回True，否则返回False
    :rtype: bool
    """
    type_str = _comp.CF(entity_id).EngineType.GetEngineType()
    return type_str & _EntityType.Mob == _EntityType.Mob


def all_mob(entity_id_list):
    """
    | 判断一个实体ID列表内的实体是否均为生物。

    -----

    :param list[str] entity_id_list: 实体ID列表

    :return: 均为生物返回True，否则返回False
    :rtype: bool
    """
    return all(is_mob(i) for i in entity_id_list)


def any_mob(entity_id_list):
    """
    | 判断一个实体ID列表内的实体是否含有生物。

    -----

    :param list[str] entity_id_list: 实体ID列表

    :return: 含有生物返回True，否则返回False
    :rtype: bool
    """
    return any(is_mob(i) for i in entity_id_list)


def entity_filter(entity_list, *args):
    """
    | 实体ID过滤器。
    | 执行过滤时将会从左到右按顺序处理过滤参数，且会自动丢弃无法获取坐标的实体。

    -----

    【过滤参数说明及示例】

    * **传入一个tuple，tuple的第一个元素为坐标，第二个元素为半径，表示保留该坐标半径范围内的所有实体：**
    ::

        # 保留以pos为中心60格半径内的实体
        entity_filter(entity_list, (pos, 60))

    * **将EntityType枚举放入集合传入，表示保留这些类型的所有实体：**
    ::

        # 保留所有生物
        entity_filter(entity_list, {EntityType.Mob})
        # 保留所有猪和狼
        entity_filter(entity_list, {EntityType.Pig, EntityType.Wolf})

    * **将字符串形式的维度ID放入集合传入，表示保留这些维度的所有实体：**
    ::

        # 保留所有主世界和地狱的实体
        entity_filter(entity_list, {"0", "1"})

    * **将实体ID放入列表传入，表示抛弃这些实体ID：**
    ::

        entity_list = ["-123", "-456", "-789"]
        entity_filter(entity_list, ["-123", "-456"]) # ["-789"]

    * **将EntityType枚举放入列表传入，表示抛弃这些类型的所有实体：**
    ::

        # 抛弃所有生物
        entity_filter(entity_list, [EntityType.Mob])
        # 抛弃所有猪和狼
        entity_filter(entity_list, [EntityType.Pig, EntityType.Wolf])

    * **以上5种过滤参数均可混合使用：**
    ::

        # 保留主世界中以pos为中心60格半径内的所有生物
        entity_filter(entity_list, {"0"}, (pos, 60), {EntityType.Mob})

    -----

    :param list[str] entity_list: 实体ID列表
    :param tuple[tuple,float]|int|list[str]|list[int] args: 过滤参数

    :return: 过滤后的实体ID列表
    :rtype: list[str]
    """
    def _filter(eid):
        cf = _comp.CF(eid)
        ent_pos = cf.Pos.GetFootPos()
        ent_type = cf.EngineType.GetEngineType()
        ent_type_str = cf.EngineType.GetEngineTypeStr()
        ent_dim = str(cf.Dimension.GetEntityDimensionId())
        if not ent_pos:
            return False
        for arg in args:
            if not arg:
                continue
            if isinstance(arg, tuple) and _mc_math.pos_distance(arg[0], ent_pos) > arg[1]:
                return False
            if isinstance(arg, set):
                for i in arg:
                    if isinstance(i, str):
                        if ":" in i and i == ent_type_str:
                            break
                        if ":" not in i and i == ent_dim:
                            break
                    if isinstance(i, int) and ent_type & i == i:
                        break
                else:
                    return False
            if isinstance(arg, list):
                for i in arg:
                    if isinstance(i, str):
                        if ":" in i and i == ent_type_str:
                            return False
                        if ":" not in i and i == eid:
                            return False
                    if isinstance(i, int) and ent_type & i == i:
                        return False
        return True
    return filter(_filter, entity_list)


def is_entity_type(entity_id, etype):
    """
    | 判断实体是否是某一类型。

    -----

    :param str entity_id: 实体ID
    :param int|str etype: 实体类型，`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举值或带命名空间的类型名称（如"minecraft:pig"）

    :return: 是则返回True，否则返回False
    :rtype: bool
    """
    if isinstance(etype, int):
        return _comp.CF(entity_id).EngineType.GetEngineType() & etype == etype
    else:
        return _comp.CF(entity_id).EngineType.GetEngineTypeStr() == etype


def sort_entity_list_by_dist(entity_list, pos):
    """
    | 根据距离从小到大对实体列表进行排序。该函数直接修改原列表，无法获取坐标的实体将会从列表中删除。

    -----

    :param list[str] entity_list: 实体ID列表
    :param tuple[float,float,float] pos: 参照坐标

    :return: 无
    :rtype: None
    """
    if not entity_list or not pos:
        return []
    not_exist = []
    def func(eid):
        ep = _comp.CF(eid).Pos.GetFootPos()
        if not ep:
            not_exist.append(eid)
        return _mc_math.pos_distance(ep, pos)
    entity_list.sort(key=func)
    for i in not_exist:
        entity_list.remove(i)


def launch_projectile(
        projectile_name,
        spawner_id,
        power=None,
        damage=None,
        position=None,
        direction=None,
        gravity=None,
        target_id="",
        damage_owner=False,
):
    """
    | 发射抛射物。

    -----

    :param str projectile_name: 抛射物类型ID
    :param str spawner_id: 发射者的实体ID
    :param float|None power: 抛射物威力（速度），默认为json配置中的值
    :param int|None damage: 抛射物伤害，默认为json配置中的值
    :param tuple[float,float,float]|None position: 初始位置，默认为比发射者脚底高1.6格的位置
    :param tuple[float,float,float]|None direction: 初始朝向，默认为发射者准星方向
    :param float|None gravity: 抛射物重力，默认为json配置中的值
    :param str target_id: 抛射物目标（指定了target_id之后，会和潜影贝导弹是一个效果），默认无目标
    :param bool damage_owner: 对创建者是否造成伤害，默认为不造成

    :return: 抛射物ID；创建失败返回"-1"
    :rtype: str
    """
    cf = _comp.CF(spawner_id)
    if not position:
        position = cf.Pos.GetFootPos()
        if not position:
            return "-1"
        position = (position[0], position[1] + 1.6, position[2])
    if not direction:
        rot = cf.Rot.GetRot()
        if not rot:
            return "-1"
        direction = _server_api.GetDirFromRot(rot)
    param = {
        'position': position,
        'direction': direction,
        'isDamageOwner': damage_owner,
    }
    if power is not None:
        param['power'] = power
    if damage is not None:
        param['damage'] = damage
    if gravity is not None:
        param['gravity'] = gravity
    if target_id:
        param['targetId'] = target_id
    return _comp.LvComp.Projectile.CreateProjectileEntity(spawner_id, projectile_name, param)


def entity_plunge(entity_id1, entity_id2, speed):
    """
    | 使实体1向实体2的准星方向突进。

    -----

    :param str entity_id1: 实体1ID
    :param str entity_id2: 实体2ID
    :param float speed: 突进速度

    :return: 无
    :rtype: None
    """
    rot = _comp.CF(entity_id2).Rot.GetRot()
    if not rot:
        return
    entity_plunge_by_rot(entity_id1, rot, speed)


def entity_plunge_by_dir(entity_id, direction, speed):
    """
    | 使实体以指定方向和速度突进。

    -----

    :param str entity_id: 实体ID
    :param tuple[float,float,float] direction: 方向的单位向量
    :param float speed: 速度大小

    :return: 无
    :rtype: None
    """
    cf = _comp.CF(entity_id)
    motion = tuple(map(lambda x: x * speed, direction))
    motion_comp = cf.ActorMotion
    etype = cf.EngineType.GetEngineType()
    if etype == _EntityType.Player:
        motion_comp.SetPlayerMotion(motion)
    else:
        motion_comp.SetMotion(motion)


def entity_plunge_by_rot(entity_id, rot, speed):
    """
    | 使实体向指定视角方向突进。

    -----

    :param str entity_id: 实体ID
    :param tuple[float, float] rot: 视角
    :param float speed: 速度

    :return: 无
    :rtype: None
    """
    direction = _server_api.GetDirFromRot(rot)
    entity_plunge_by_dir(entity_id, direction, speed)


def get_all_entities(ent_filter=None):
    """
    | 获取所有实体，包括玩家。

    -----

    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否获取该实体，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None

    :return: 实体ID列表
    :rtype: list[str]
    """
    return filter(ent_filter, _server_api.GetEngineActor().keys() + _server_api.GetPlayerList())


def get_entities_in_area(
        pos,
        radius,
        dimension=0,
        filter_ids=None,
        filter_types=None,
        filter_type_str=None,
        filter_abiotic=False,
):
    """
    | 获取给定区域内的所有实体。

    -----

    :param tuple[float,float,float] pos: 区域中心点坐标
    :param float radius: 区域半径
    :param int dimension: 维度，默认为0
    :param list[str]|None filter_ids: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filter_type_str: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filter_abiotic: 是否过滤非生物实体，默认为不过滤

    :return: 实体ID列表
    :rtype: list[str]
    """
    if not pos or radius <= 0:
        return []
    start_pos = tuple(i - radius for i in pos)
    end_pos = tuple(i + radius for i in pos)
    entities = _comp.LvComp.Game.GetEntitiesInSquareArea(None, start_pos, end_pos, dimension)
    fa = {_EntityType.Mob} if filter_abiotic else None
    entities = entity_filter(
        entities, (pos, radius), fa, filter_ids, filter_types, filter_type_str
    )
    return entities


def get_entities_by_type(type_id, pos=None, dimension=0, radius=0.0):
    """
    | 获取指定类型的所有实体。

    -----

    :param int type_id: 实体类型ID（网易版）
    :param tuple[float,float,float]|None pos: 获取位置坐标（传入None表示全图范围），默认为全图范围
    :param int dimension: 获取维度（指定pos时生效）
    :param float radius: 获取半径（指定pos时生效）

    :return: 实体ID列表
    :rtype: list[str]
    """
    if pos:
        start_pos = tuple(i - radius for i in pos)
        end_pos = tuple(i + radius for i in pos)
        entities = _comp.LvComp.Game.GetEntitiesInSquareArea(None, start_pos, end_pos, dimension)
        entities = entity_filter(entities, {type_id}, (pos, radius))
    else:
        entities = get_all_entities()
        entities = entity_filter(entities, {type_id})
    return entities


def get_entities_by_name(name):
    """
    | 获取自定义名称为 ``name`` 的所有实体。

    -----

    :param str name: 自定义名称

    :return: 实体ID列表
    :rtype: list[str]
    """
    result = []
    for i in get_all_entities():
        en = _comp.CF(i).Name.GetName()
        if en == name:
            result.append(i)
    return result


def get_entities_by_locking(entity_id, dist=-1.0, filter_ids=None, filter_types=None):
    """
    | 获取攻击目标为指定生物的所有生物。

    -----

    :param str entity_id: 生物的实体ID
    :param float dist: 最远获取距离，-1.0表示无视距离，默认为无视距离
    :param list[str]|None filter_ids: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤

    :return: 实体ID列表
    :rtype: list[str]
    """
    pos = _comp.CF(entity_id).Pos.GetFootPos()
    if not pos:
        return []
    if filter_ids is None:
        filter_ids = []
    else:
        filter_ids = filter_ids[:]
    filter_ids.append(entity_id)
    ents = get_all_entities()
    r = (pos, dist) if dist >= 0 else None
    ents = entity_filter(ents, r, _EntityType.Mob, filter_ids, filter_types)
    return [
        eid for eid in ents
        if _comp.CF(eid).Action.GetAttackTarget() == entity_id
    ]


def get_nearest_entity(
        obj,
        count=1,
        dim=0,
        radius=-1.0,
        filter_ids=None,
        filter_types=None,
        filter_abiotic=False,
):
    """
    | 获取距离指定实体或坐标位置最近的实体。

    -----

    :param str|tuple[float,float,float] obj: 实体ID或坐标
    :param int count: 获取的实体数量，默认为1
    :param int dim: 获取维度（obj传入坐标时生效），默认为0
    :param float radius: 获取半径，-1.0表示全图范围，默认为全图范围w
    :param list[str]|None filter_ids: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param bool filter_abiotic: 是否过滤非生物实体，默认为不过滤

    :return: 若count==1，返回实体ID；若count>1，返回实体ID列表；获取不到实体返回None
    :rtype: str|list[str]|None
    """
    if filter_ids is None:
        filter_ids = []
    else:
        filter_ids = filter_ids[:]
    if isinstance(obj, str):
        cf = _comp.CF(obj)
        pos = cf.Pos.GetFootPos()
        dim = cf.Dimension.GetEntityDimensionId()
        filter_ids.append(obj)
    else:
        pos = obj
    if not pos:
        return
    all_ents = get_all_entities()
    sort_entity_list_by_dist(all_ents, pos)
    r = (pos, radius) if radius != -1 else None
    fa = {_EntityType.Mob} if filter_abiotic else None
    all_ents = entity_filter(all_ents, r, fa, filter_ids, filter_types, {str(dim)})
    if not all_ents:
        return
    result = all_ents[:count]
    return result if count > 1 else result[0]


def attack_nearest_mob(entity_id, r=15.0, filter_ids=None, filter_types=None):
    """
    | 令指定实体攻击距离其最近的实体。

    -----

    :param str entity_id: 实体ID
    :param float r: 最远攻击距离，默认为15.0
    :param list[str]|None filter_ids: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤

    :return: 攻击目标的实体ID；无攻击目标返回None
    :rtype: str|None
    """
    nearest = get_nearest_entity(
        entity_id, radius=r, filter_ids=filter_ids, filter_types=filter_types, filter_abiotic=True
    )
    if nearest:
        _comp.CF(entity_id).Action.SetAttackTarget(nearest)
    return nearest


def has_effect(entity_id, effect_id):
    """
    | 检测生物是否存在指定药水效果。

    -----

    :param str entity_id: 生物的实体ID
    :param str effect_id: 药水效果ID

    :return: 存在返回True，否则返回False
    :rtype: bool
    """
    effects = _comp.CF(entity_id).Effect.GetAllEffects()
    for eff in effects:
        if eff['effectName'] == effect_id:
            return True
    return False


def get_entities_by_ray(
        start_pos,
        direction,
        length,
        dimension=0,
        count=0,
        filter_ids=None,
        filter_types=None,
        filter_type_str=None,
        filter_abiotic=False,
):
    """
    | 从指定位置射出一条射线，获取该射线接触到的所有实体。
    | 返回一个列表，实体按照由近到远的顺序排列，列表每个元素为一个字典，结构如下：
    ::

        {
            'entity_id': str, # 实体ID
            'pos': Tuple[float, float, float], # 实体坐标
            'intersection': Tuple[float, float, float], # 射线与实体的第一个交点的坐标
            'size': Tuple[float, float], # 实体的碰撞箱尺寸，与GetSize接口获取的相同
        }

    -----

    :param tuple[float,float,float] start_pos: 射线起始坐标
    :param tuple[float,float,float] direction: 射线方向向量（单位向量）
    :param float length: 射线长度
    :param int dimension: 维度，默认为0
    :param int count: 获取到多少个实体后停止，默认为0，表示不限制数量
    :param list[str]|None filter_ids: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filter_types: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filter_type_str: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filter_abiotic: 是否过滤非生物实体，默认为不过滤

    :return: 射线经过的实体的列表，顺序为由近到远，列表每个元素为一个字典，字典结构请见上方
    :rtype: list[dict[str,str|tuple]]
    """
    if not start_pos or not direction or length <= 0:
        return []
    fa = {_EntityType.Mob} if filter_abiotic else None
    entities = get_all_entities()
    entities = entity_filter(
        entities, fa, filter_ids, filter_types, filter_type_str, {str(dimension)}
    )
    entities.sort(
        key=lambda x: _mc_math.pos_distance(_comp.CF(x).Pos.GetFootPos(), start_pos)
    )
    ent_list = []
    for entity_id in entities:
        cf = _comp.CF(entity_id)
        size = cf.CollisionBox.GetSize()
        if not size:
            continue
        ent_pos = cf.Pos.GetFootPos()
        center = (ent_pos[0], ent_pos[1] + size[1] / 2.0, ent_pos[2])
        cube_size = (size[0], size[1], size[0])
        intersection = _mc_math.ray_aabb_intersection(start_pos, direction, length, center, cube_size)
        if intersection:
            ent_list.append({
                'entity_id': entity_id,
                'pos': ent_pos,
                'intersection': intersection,
                'size': size,
            })
            if len(ent_list) >= count > 0:
                break
    return ent_list


def entity_distance(ent1, ent2):
    """
    | 计算两个实体的距离。

    -----

    :param str ent1: 实体ID
    :param str ent2: 实体ID

    :return: 两个实体的距离
    :rtype: float
    """
    pos1 = _comp.CF(ent1).Pos.GetFootPos()
    pos2 = _comp.CF(ent2).Pos.GetFootPos()
    return _mc_math.pos_distance(pos1, pos2)

























