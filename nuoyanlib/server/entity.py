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
#   Last Modified : 2023-10-05
#
# ====================================================


from copy import copy as _copy
import mod.server.extraServerApi as _serverApi
from mod.common.minecraftEnum import EntityType as _EntityType
from ..utils.calculator import (
    pos_distance as _pos_distance,
    ray_aabb_intersection as _ray_aabb_intersection,
)
from ..utils.vector import (
    vec_p2p as _vec_p2p,
    vec_composite as _vec_composite,
)
from serverComps import (
    ServerCompFactory as _ServerCompFactory,
    ServerLevelComps as _ServerLevelComps,
)


__all__ = [
    "clear_effects",
    "bounce_entities",
    "attract_entities",
    "is_mob",
    "all_mob",
    "has_mob",
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


def clear_effects(entityId):
    """
    清除指定实体的全部药水效果。

    -----

    :param str entityId: 实体ID

    :return: 无
    :rtype: None
    """
    comp = _ServerCompFactory.CreateEffect(entityId)
    effects = comp.GetAllEffects()
    if effects:
        for eff in effects:
            comp.RemoveEffectFromEntity(eff['effectName'])


def bounce_entities(
        pos,
        dim,
        radius,
        power,
        filterIdList=None,
        filterTypeIdList=None,
        filterTypeStrList=None,
        filterAbiotic=False,
):
    """
    从中心弹开指定范围内的实体。

    -----

    :param tuple[float,float,float] pos: 弹开中心坐标
    :param int dim: 维度ID
    :param float radius: 弹开半径
    :param float power: 弹开强度
    :param list[str]|None filterIdList: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filterTypeIdList: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filterTypeStrList: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filterAbiotic: 是否过滤非生物实体，默认为不过滤

    :return: 被弹开的实体ID列表
    :rtype: list[str]
    """
    return attract_entities(
        pos, dim, radius, -power, filterIdList, filterTypeIdList, filterTypeStrList, filterAbiotic
    )


def attract_entities(
        pos,
        dim,
        radius,
        power,
        filterIdList=None,
        filterTypeIdList=None,
        filterTypeStrList=None,
        filterAbiotic=False,
):
    """
    吸引指定范围内的实体到中心。

    -----

    :param tuple[float,float,float] pos: 吸引中心坐标
    :param int dim: 维度ID
    :param float radius: 吸引半径
    :param float power: 吸引强度
    :param list[str]|None filterIdList: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filterTypeIdList: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filterTypeStrList: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filterAbiotic: 是否过滤非生物实体，默认为不过滤

    :return: 被吸引的实体ID列表
    :rtype: list[str]
    """
    ents = get_entities_in_area(
        pos, radius, dim, filterIdList, filterTypeIdList, filterTypeStrList, filterAbiotic
    )
    res = []
    for eid in ents:
        epos = _ServerCompFactory.CreatePos(eid).GetFootPos()
        if not epos:
            continue
        comp = _ServerCompFactory.CreateActorMotion(eid)
        origMotion = comp.GetMotion()
        vec = _vec_p2p(epos, pos)
        vec = tuple(i * power for i in vec)
        resMotion = _vec_composite(origMotion, vec)
        etype = _ServerCompFactory.CreateEngineType(eid).GetEngineType()
        if etype == _EntityType.Player:
            if comp.SetPlayerMotion(resMotion):
                res.append(eid)
        else:
            if comp.SetMotion(resMotion):
                res.append(eid)
    return res


def is_mob(entityId):
    """
    判断实体是否为生物。

    -----

    :param str entityId: 实体ID

    :return: 是生物返回True，否则返回False
    :rtype: bool
    """
    typeStr = _ServerCompFactory.CreateEngineType(entityId).GetEngineType()
    return typeStr & _EntityType.Mob == _EntityType.Mob


def all_mob(entityIdList):
    """
    判断一个实体ID列表内的实体是否均为生物。

    -----

    :param list[str] entityIdList: 实体ID列表

    :return: 均为生物返回True，否则返回False
    :rtype: bool
    """
    return all(is_mob(i) for i in entityIdList)


def has_mob(entityIdList):
    """
    判断一个实体ID列表内的实体是否含有生物。

    -----

    :param list[str] entityIdList: 实体ID列表

    :return: 含有生物返回True，否则返回False
    :rtype: bool
    """
    return any(is_mob(i) for i in entityIdList)


def entity_filter(entityList, *args):
    """
    实体ID过滤器。

    执行过滤时将会从左到右按顺序处理过滤参数，且会自动丢弃无法获取坐标的实体。

    -----

    【过滤参数说明及示例】

    1、传入一个tuple，tuple的第一个元素为坐标，第二个元素为半径，表示保留该坐标半径范围内的所有实体；

    >>> entity_filter(entityList, (pos, 60)) # 保留以pos为中心60格半径内的实体

    2、将EntityType枚举放入集合传入，表示保留这些类型的所有实体；

    >>> entity_filter(entityList, {EntityType.Mob}) # 保留所有生物
    >>> entity_filter(entityList, {EntityType.Pig, EntityType.Wolf}) # 保留所有猪和狼

    3、将字符串形式的维度ID放入集合传入，表示保留这些维度的所有实体；

    >>> entity_filter(entityList, {"0", "1"}) # 保留所有主世界和地狱的实体

    4、将实体ID放入列表传入，表示抛弃这些实体ID；

    >>> entityList = ["-123", "-456", "-789"]
    >>> entity_filter(entityList, ["-123", "-456"]) # ["-789"]

    5、将EntityType枚举放入列表传入，表示抛弃这些类型的所有实体；

    >>> entity_filter(entityList, [EntityType.Mob]) # 抛弃所有生物
    >>> entity_filter(entityList, [EntityType.Pig, EntityType.Wolf]) # 抛弃所有猪和狼

    6、以上5种过滤参数均可混合使用；

    >>> entity_filter(entityList, {"0"}, (pos, 60), {EntityType.Mob}) # 保留主世界中以pos为中心60格半径内的所有生物

    -----

    :param list[str] entityList: 实体ID列表
    :param tuple[tuple,float]|int|list[str]|list[int] args: 过滤参数

    :return: 过滤后的实体ID列表
    :rtype: list[str]
    """
    def _filter(eid):
        entPos = _ServerCompFactory.CreatePos(eid).GetFootPos()
        entType = _ServerCompFactory.CreateEngineType(eid).GetEngineType()
        entTypeStr = _ServerCompFactory.CreateEngineType(eid).GetEngineTypeStr()
        entDim = str(_ServerCompFactory.CreateDimension(eid).GetEntityDimensionId())
        if not entPos:
            return False
        for arg in args:
            if not arg:
                continue
            if isinstance(arg, tuple) and _pos_distance(arg[0], entPos) > arg[1]:
                return False
            if isinstance(arg, set):
                for i in arg:
                    if isinstance(i, str):
                        if ":" in i and i == entTypeStr:
                            break
                        if ":" not in i and i == entDim:
                            break
                    if isinstance(i, int) and entType & i == i:
                        break
                else:
                    return False
            if isinstance(arg, list):
                for i in arg:
                    if isinstance(i, str):
                        if ":" in i and i == entTypeStr:
                            return False
                        if ":" not in i and i == eid:
                            return False
                    if isinstance(i, int) and entType & i == i:
                        return False
        return True
    return filter(_filter, entityList)


def is_entity_type(entityId, typeId):
    """
    判断实体是否是某一类型。

    -----

    【示例】

    >>> is_entity_type(pigEntityId, EntityType.Pig)
    True
    >>> is_entity_type(pigEntityId, EntityType.Mob)
    True
    >>> is_entity_type(pigEntityId, EntityType.Wolf)
    False
    >>> is_entity_type(pigEntityId, EntityType.Monster)
    False

    -----

    :param str entityId: 实体ID
    :param int typeId: 实体类型ID（网易版）

    :return: 是则返回True，否则返回False
    :rtype: bool
    """
    et = _ServerCompFactory.CreateEngineType(entityId).GetEngineType()
    return et & typeId == typeId


def sort_entity_list_by_dist(entityList, pos):
    """
    根据距离从小到大对实体列表进行排序。该函数直接修改原列表，无法获取坐标的实体将会从列表中删除。

    -----

    :param list[str] entityList: 实体ID列表
    :param tuple[float,float,float] pos: 参照坐标

    :return: 无
    :rtype: None
    """
    if not entityList or not pos:
        return []
    notExist = []
    def func(eid):
        ep = _ServerCompFactory.CreatePos(eid).GetFootPos()
        if not ep:
            notExist.append(eid)
        return _pos_distance(ep, pos)
    entityList.sort(key=func)
    for i in notExist:
        entityList.remove(i)


def launch_projectile(
        projectileName,
        spawnerId,
        power=None,
        damage=None,
        position=None,
        direction=None,
        gravity=None,
        targetId="",
        isDamageOwner=False,
):
    """
    发射抛射物。

    -----

    :param str projectileName: 抛射物类型ID
    :param str spawnerId: 发射者的实体ID
    :param float|None power: 抛射物威力（速度），默认为json配置中的值
    :param int|None damage: 抛射物伤害，默认为json配置中的值
    :param tuple[float,float,float]|None position: 初始位置，默认为比发射者脚底高1.6格的位置
    :param tuple[float,float,float]|None direction: 初始朝向，默认为发射者准星方向
    :param float|None gravity: 抛射物重力，默认为json配置中的值
    :param str targetId: 抛射物目标（指定了targetId之后，会和潜影贝导弹是一个效果），默认无目标
    :param bool isDamageOwner: 对创建者是否造成伤害，默认为不造成

    :return: 抛射物ID；创建失败返回"-1"
    :rtype: str
    """
    if not position:
        position = _ServerCompFactory.CreatePos(spawnerId).GetFootPos()
        if not position:
            return "-1"
        position = (position[0], position[1] + 1.6, position[2])
    if not direction:
        rot = _ServerCompFactory.CreateRot(spawnerId).GetRot()
        if not rot:
            return "-1"
        direction = _serverApi.GetDirFromRot(rot)
    param = {
        'position': position,
        'direction': direction,
        'isDamageOwner': isDamageOwner,
    }
    if power is not None:
        param['power'] = power
    if damage is not None:
        param['damage'] = damage
    if gravity is not None:
        param['gravity'] = gravity
    if targetId:
        param['targetId'] = targetId
    return _ServerLevelComps.Projectile.CreateProjectileEntity(spawnerId, projectileName, param)


def entity_plunge(entityId1, entityId2, speed):
    """
    使实体1向实体2的准星方向突进。

    -----

    :param str entityId1: 实体1ID
    :param str entityId2: 实体2ID
    :param float speed: 突进速度

    :return: 无
    :rtype: None
    """
    rot = _ServerCompFactory.CreateRot(entityId2).GetRot()
    if not rot:
        return
    entity_plunge_by_rot(entityId1, rot, speed)


def entity_plunge_by_dir(entityId, direction, speed):
    """
    使实体以指定方向和速度突进。

    -----

    :param str entityId: 实体ID
    :param tuple[float,float,float] direction: 方向的单位向量
    :param float speed: 速度大小

    :return: 无
    :rtype: None
    """
    motion = tuple(map(lambda x: x * speed, direction))
    comp = _ServerCompFactory.CreateActorMotion(entityId)
    etype = _ServerCompFactory.CreateEngineType(entityId).GetEngineType()
    if etype == _EntityType.Player:
        comp.SetPlayerMotion(motion)
    else:
        comp.SetMotion(motion)


def entity_plunge_by_rot(entityId, rot, speed):
    """
    使实体向指定视角方向突进。

    -----

    :param str entityId: 实体ID
    :param tuple[float, float] rot: 视角
    :param float speed: 速度

    :return: 无
    :rtype: None
    """
    direction = _serverApi.GetDirFromRot(rot)
    entity_plunge_by_dir(entityId, direction, speed)


def get_all_entities():
    """
    获取所有实体，包括玩家。

    -----

    :return: 实体ID列表
    :rtype: list[str]
    """
    return _serverApi.GetEngineActor().keys() + _serverApi.GetPlayerList()


def get_entities_in_area(
        pos,
        radius,
        dimension=0,
        filterIdList=None,
        filterTypeIdList=None,
        filterTypeStrList=None,
        filterAbiotic=False,
):
    """
    获取给定区域内的所有实体。

    -----

    :param tuple[float,float,float] pos: 区域中心点坐标
    :param float radius: 区域半径
    :param int dimension: 维度，默认为0
    :param list[str]|None filterIdList: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filterTypeIdList: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filterTypeStrList: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filterAbiotic: 是否过滤非生物实体，默认为不过滤

    :return: 实体ID列表
    :rtype: list[str]
    """
    if not pos or radius <= 0:
        return []
    startPos = tuple(i - radius for i in pos)
    endPos = tuple(i + radius for i in pos)
    entities = _ServerLevelComps.Game.GetEntitiesInSquareArea(None, startPos, endPos, dimension)
    fa = {_EntityType.Mob} if filterAbiotic else None
    entities = entity_filter(
        entities, (pos, radius), fa, filterIdList, filterTypeIdList, filterTypeStrList
    )
    return entities


def get_entities_by_type(typeId, pos=None, dimension=0, radius=0.0):
    """
    获取指定类型的所有实体。

    -----

    :param int typeId: 实体类型ID（网易版）
    :param tuple[float,float,float] pos: 获取位置坐标（传入None表示全图范围），默认为全图范围
    :param int dimension: 获取维度（指定pos时生效）
    :param float radius: 获取半径（指定pos时生效）

    :return: 实体ID列表
    :rtype: list[str]
    """
    if pos:
        startPos = tuple(i - radius for i in pos)
        endPos = tuple(i + radius for i in pos)
        entities = _ServerLevelComps.Game.GetEntitiesInSquareArea(None, startPos, endPos, dimension)
        entities = entity_filter(entities, {typeId}, (pos, radius))
    else:
        entities = get_all_entities()
        entities = entity_filter(entities, {typeId})
    return entities


def get_entities_by_name(name):
    """
    获取自定义名称为name的所有实体。

    -----

    :param str name: 自定义名称

    :return: 实体ID列表
    :rtype: list[str]
    """
    result = []
    for i in get_all_entities():
        en = _ServerCompFactory.CreateName(i).GetName()
        if en == name:
            result.append(i)
    return result


def get_entities_by_locking(entityId, getDistance=-1, filterIdList=None, filterTypeIdList=None):
    """
    获取攻击目标为指定生物的所有生物。

    -----

    :param str entityId: 生物的实体ID
    :param float getDistance: 最远获取距离，-1表示无视距离，默认为无视距离
    :param list[str]|None filterIdList: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filterTypeIdList: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤

    :return: 实体ID列表
    :rtype: list[str]
    """
    pos = _ServerCompFactory.CreatePos(entityId).GetFootPos()
    if not pos:
        return []
    if filterIdList is None:
        filterIdList = []
    filterIdList.append(entityId)
    ents = get_all_entities()
    r = (pos, getDistance) if getDistance != -1 else None
    ents = entity_filter(ents, r, _EntityType.Mob, filterIdList, filterTypeIdList)
    result = []
    for eid in ents:
        target = _ServerCompFactory.CreateAction(eid).GetAttackTarget()
        if target == entityId:
            result.append(eid)
    return result


def get_nearest_entity(
        obj,
        count=1,
        dim=0,
        radius=-1.0,
        filterIdList=None,
        filterTypeIdList=None,
        filterAbiotic=False,
):
    """
    获取距离指定实体或位置最近的实体。

    -----

    :param str|tuple[float,float,float] obj: 实体ID或坐标
    :param int count: 获取的实体数量，默认为1
    :param int dim: 获取维度（obj传入坐标时生效），默认为0
    :param float radius: 获取半径，-1.0表示全图范围，默认为全图范围
    :param list[str]|None filterIdList: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filterTypeIdList: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param bool filterAbiotic: 是否过滤非生物实体，默认为不过滤

    :return: 若count==1，返回实体ID；若count>1，返回实体ID列表；获取不到实体返回None
    :rtype: str|list[str]|None
    """
    if isinstance(obj, str):
        pos = _ServerCompFactory.CreatePos(obj).GetFootPos()
        dim = _ServerCompFactory.CreateDimension(obj).GetEntityDimensionId()
        if filterIdList is None:
            filterIdList = []
        filterIdList = _copy(filterIdList)
        filterIdList.append(obj)
    else:
        pos = obj
    if not pos:
        return
    allEnts = get_all_entities()
    sort_entity_list_by_dist(allEnts, pos)
    r = (pos, radius) if radius != -1 else None
    fa = {_EntityType.Mob} if filterAbiotic else None
    allEnts = entity_filter(allEnts, r, fa, filterIdList, filterTypeIdList, {str(dim)})
    if not allEnts:
        return
    result = allEnts[:count]
    return result if count > 1 else result[0]


def attack_nearest_mob(entityId, r=15.0, filterIdList=None, filterTypeIdList=None):
    """
    令指定实体攻击距离其最近的实体。

    -----

    :param str entityId: 实体ID
    :param float r: 最远攻击距离，默认为15.0
    :param list[str]|None filterIdList: 过滤的实体ID列表，默认为不过滤
    :param list[int]|None filterTypeIdList: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤

    :return: 攻击目标的实体ID；无攻击目标返回None
    :rtype: str|None
    """
    nearest = get_nearest_entity(
        entityId, radius=r, filterIdList=filterIdList, filterTypeIdList=filterTypeIdList, filterAbiotic=True
    )
    if nearest:
        _ServerCompFactory.CreateAction(entityId).SetAttackTarget(nearest)
    return nearest


def has_effect(entityId, effectId):
    """
    检测生物是否存在指定药水效果。

    -----

    :param str entityId: 生物的实体ID
    :param str effectId: 药水效果ID

    :return: 存在返回True，否则返回False
    :rtype: bool
    """
    effects = _ServerCompFactory.CreateEffect(entityId).GetAllEffects()
    for effDict in effects:
        if effDict['effectName'] == effectId:
            return True
    return False


def get_entities_by_ray(
        startPos,
        direction,
        length,
        dimension=0,
        count=0,
        filterIdList=None,
        filterTypeIdList=None,
        filterTypeStrList=None,
        filterAbiotic=False,
):
    """
    从指定位置射出一条射线，获取该射线接触到的所有实体。

    返回一个列表，实体按照由近到远的顺序排列，列表每个元素为一个字典，结构如下：

    >>> {
    ...     "entityId": str, # 实体ID
    ...     "pos": Tuple[float, float, float], # 实体坐标
    ...     "intersection": Tuple[float, float, float], # 射线与实体的第一个交点的坐标
    ...     "size": Tuple[float, float], # 实体的碰撞箱尺寸，与GetSize接口获取的相同
    ... }

    -----

    :param tuple[float,float,float] startPos: 射线起始坐标
    :param tuple[float,float,float] direction: 射线方向向量（单位向量）
    :param float length: 射线长度
    :param int dimension: 维度，默认为0
    :param int count: 获取到多少个实体后停止，默认为0，表示不限制数量
    :param list[str]|None filterIdList: 过滤的实体ID列表，默认为不过滤
    :param list[str]|None filterTypeIdList: 过滤的网易版实体类型ID列表（`EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?key=EntityType&docindex=1&type=0>`_ 枚举），默认为不过滤
    :param list[str]|None filterTypeStrList: 过滤的原版实体类型ID列表（如"minecraft:zombie"），默认为不过滤
    :param bool filterAbiotic: 是否过滤非生物实体，默认为不过滤

    :return: 射线经过的实体的列表，顺序为由近到远，列表每个元素为一个字典，字典结构请见上方
    :rtype: list[dict[str, str|tuple]]
    """
    if not startPos or not direction or length <= 0:
        return []
    fa = {_EntityType.Mob} if filterAbiotic else None
    entities = get_all_entities()
    entities = entity_filter(
        entities, fa, filterIdList, filterTypeIdList, filterTypeStrList, {str(dimension)}
    )
    entities.sort(key=lambda x: _pos_distance(_ServerCompFactory.CreatePos(x).GetFootPos(), startPos))
    entList = []
    for entityId in entities:
        size = _ServerCompFactory.CreateCollisionBox(entityId).GetSize()
        if not size:
            continue
        entPos = _ServerCompFactory.CreatePos(entityId).GetFootPos()
        center = (entPos[0], entPos[1] + size[1] / 2.0, entPos[2])
        cubeSize = (size[0], size[1], size[0])
        intersection = _ray_aabb_intersection(startPos, direction, length, center, cubeSize)
        if intersection:
            entList.append({
                'entityId': entityId,
                'pos': entPos,
                'intersection': intersection,
                'size': size,
            })
            if len(entList) >= count > 0:
                break
    return entList


def entity_distance(ent1, ent2):
    """
    计算两个实体的距离。

    -----

    :param str ent1: 实体ID
    :param str ent2: 实体ID

    :return: 两个实体的距离
    :rtype: float
    """
    pos1 = _ServerCompFactory.CreatePos(ent1).GetFootPos()
    pos2 = _ServerCompFactory.CreatePos(ent2).GetFootPos()
    return _pos_distance(pos1, pos2)

























