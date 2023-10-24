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
#   Last Modified : 2023-10-01
#
# ====================================================


from collections import Callable as _Callable
from copy import copy as _copy
from mod.common.minecraftEnum import (
    EntityType as _EntityType,
    AttrType as _AttrType,
    ActorDamageCause as _ActorDamageCause,
)
from ..utils.calculator import (
    is_in_sector as _is_in_sector,
    pos_distance_to_line as _pos_distance_to_line,
)
from ..utils.vector import vec_angle as _vec_angle
from entity import (
    entity_filter as _entity_filter,
    get_entities_in_area as _get_entities_in_area,
    get_all_entities as _get_all_entities,
)
from serverComps import (
    ServerCompFactory as _ServerCompFactory,
    ServerLevelComps as _ServerLevelComps,
)


__all__ = [
    "explode_hurt",
    "aoe_damage",
    "sector_aoe_damage",
    "rectangle_aoe_damage",
    "hurt_by_set_health",
    "hurt",
    "percent_damage",
    "line_damage",
]


def explode_hurt(radius, pos, sourceId, playerId, fire=False, breaks=True, tileDrops=True, mobLoot=True,
                 hurtPlayer=False):
    """
    造成爆炸伤害。
    -----------------------------------------------------------
    【radius: float】 爆炸强度
    【pos: Tuple[float, float, float]】 爆炸中心坐标
    【sourceId: str】 爆炸伤害源的实体ID
    【playerId: str】 创造爆炸的实体ID
    【fire: bool = False】 是否造成火焰
    【breaks: bool = True】 是否破坏方块
    【tileDrops: bool = True】 破坏方块后是否生成掉落物
    【mobLoot: bool = True】 生物被炸死后是否生成掉落物
    【hurtPlayer: bool = False】 是否对爆炸创造者造成伤害
    -----------------------------------------------------------
    NoReturn
    """
    origRule = _ServerLevelComps.Game.GetGameRulesInfoServer()
    _ServerLevelComps.Game.SetGameRulesInfoServer({'option_info': {'tile_drops': tileDrops, 'mob_loot': mobLoot}})
    comp = _ServerCompFactory.CreateHurt(playerId)
    try:
        if not hurtPlayer:
            comp.ImmuneDamage(True)
        _ServerLevelComps.Explosion.CreateExplosion(pos, radius, fire, breaks, sourceId, playerId)
    finally:
        _ServerLevelComps.Game.SetGameRulesInfoServer(origRule)
        if not hurtPlayer:
            comp.ImmuneDamage(False)


def line_damage(damage, radius, startPos, endPos, dim, attackerId="", childAttackerId="", cause=_ActorDamageCause.NONE,
                knocked=True, filterIdList=None, filterTypeIdList=None, filterTypeStrList=None, funcBeforeHurt=None,
                funcAfterHurt=None, force=False):
    """
    对一条线段上的生物造成伤害。（无视攻击冷却）
    -----------------------------------------------------------
    【damage: int】 伤害
    【radius: float】 伤害半径（生物到直线上的最大距离）
    【startPos: Tuple[float, float, float]】 线段起点坐标
    【endPos: Tuple[float, float, float]】 线段终点坐标
    【dim: int】 维度
    【attackerId: str = ""】 攻击者实体ID
    【childAttackerId: str = ""】 攻击者的子实体ID，比如玩家使用抛射物造成伤害，该值应为抛射物实体ID
    【cause: str = ActorDamageCause.NONE】 伤害类型，ActorDamageCause枚举
    【knocked: bool = True】 是否产生击退
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表，列表中的实体将不会受到伤害
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表，这些类型的实体将不会受到伤害
    【filterTypeStrList: Optional[List[str]] = None】 过滤的实体类型ID列表，这些类型的实体将不会受到伤害
    【funcBeforeHurt: Optional[(str, str, str) -> Optional[str]] = None】 对生物造成伤害之前调用的函数，该函数第一个参数为受伤生物的实体ID，第二个为攻击者的实体ID，第三个参数为攻击者的子实体ID；该函数可返回一个新的实体ID，新的实体ID将会替换原受伤生物的实体ID进入最终返回的受伤生物实体ID列表中
    【funcAfterHurt: Optional[(str, str, str) -> Optional[str]] = None】 对生物造成伤害之后调用的函数，功能同上
    【force: bool = False】 是否无视攻击冷却或生物的无敌状态强制设置伤害
    -----------------------------------------------------------
    return: List[str] -> 受伤生物的实体ID列表
    """
    if not startPos or not endPos or radius <= 0 or damage <= 0:
        return []
    if filterIdList is None:
        filterIdList = []
    if attackerId:
        filterIdList = _copy(filterIdList)
        filterIdList.append(attackerId)
    entities = _get_all_entities()
    entities = _entity_filter(
        entities, {_EntityType.Mob}, {str(dim)}, filterIdList, filterTypeIdList, filterTypeStrList
    )
    hurtEnt = []
    for eid in entities:
        ep = _ServerCompFactory.CreatePos(eid).GetFootPos()
        dis = _pos_distance_to_line(ep, startPos, endPos)
        if dis > radius:
            continue
        v1 = tuple(a - b for a, b in zip(startPos, ep))
        v2 = tuple(a - b for a, b in zip(endPos, ep))
        if _vec_angle(v1, v2) < 1.57:
            continue
        if funcBeforeHurt:
            retEid = funcBeforeHurt(eid, attackerId, childAttackerId)
            if retEid:
                eid = retEid
        hurt(eid, damage, cause, attackerId, childAttackerId, knocked, force)
        if funcAfterHurt:
            retEid = funcAfterHurt(eid, attackerId, childAttackerId)
            if retEid:
                eid = retEid
        hurtEnt.append(eid)
    return hurtEnt


def hurt_mobs(entityIdList, damage, attackerId="", childAttackerId="", cause=_ActorDamageCause.NONE, knocked=True,
              force=False):
    # type: (list[str], int, str, str, str, bool, bool) -> None
    """
    对多个生物造成伤害。（无视攻击冷却）
    -----------------------------------------------------------
    【entityIdList: List[str]】 实体ID列表
    【damage: int】 伤害
    【attackerId: str = ""】 攻击者实体ID
    【childAttackerId: str = ""】 攻击者的子实体ID，比如玩家使用抛射物造成伤害，该值应为抛射物实体ID
    【cause: str = ActorDamageCause.NONE】 伤害类型，ActorDamageCause枚举
    【knocked: bool = True】 是否产生击退
    【force: bool = False】 是否无视攻击冷却或生物的无敌状态强制设置伤害
    -----------------------------------------------------------
    NoReturn
    """
    for entityId in entityIdList:
        hurt(entityId, damage, cause, attackerId, childAttackerId, knocked, force)


def aoe_damage(damage, radius, pos, dim, attackerId="", childAttackerId="", cause=_ActorDamageCause.NONE, knocked=True,
               filterIdList=None, filterTypeIdList=None, funcBeforeHurt=None, funcAfterHurt=None, force=False):
    # type: (int, float, tuple[float, float, float], int, str, str, str, bool, list[str] | None, list[int] | None, _Callable[[str, str, str], str | None] | None, _Callable[[str, str, str], str | None] | None, bool) -> list[str]
    """
    在指定坐标造成范围伤害。（无视攻击冷却）
    -----------------------------------------------------------
    【damage: int】 伤害
    【radius: float】 伤害半径
    【pos: Tuple[float, float, float]】 产生范围伤害的中心点坐标
    【dim: int】 维度
    【attackerId: str = ""】 攻击者实体ID
    【childAttackerId: str = ""】 攻击者的子实体ID，比如玩家使用抛射物造成伤害，该值应为抛射物实体ID
    【cause: str = ActorDamageCause.NONE】 伤害类型，ActorDamageCause枚举
    【knocked: bool = True】 是否产生击退
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表，列表中的实体将不会受到伤害
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表，这些类型的实体将不会受到伤害
    【funcBeforeHurt: Optional[(str, str, str) -> Optional[str]] = None】 对生物造成伤害之前调用的函数，该函数第一个参数为受伤生物的实体ID，第二个为攻击者的实体ID，第三个参数为攻击者的子实体ID；该函数可返回一个新的实体ID，新的实体ID将会替换原受伤生物的实体ID进入最终返回的受伤生物实体ID列表中
    【funcAfterHurt: Optional[(str, str, str) -> Optional[str]] = None】 对生物造成伤害之后调用的函数，功能同上
    【force: bool = False】 是否无视攻击冷却或生物的无敌状态强制设置伤害
    -----------------------------------------------------------
    return: List[str] -> 受伤生物的实体ID列表
    """
    if not pos or radius <= 0 or damage <= 0:
        return []
    if filterIdList is None:
        filterIdList = []
    if attackerId:
        filterIdList = _copy(filterIdList)
        filterIdList.append(attackerId)
    startPos = tuple(i - radius for i in pos)
    endPos = tuple(i + radius for i in pos)
    entities = _ServerLevelComps.Game.GetEntitiesInSquareArea(None, startPos, endPos, dim)
    entities = _entity_filter(entities, (pos, radius), {_EntityType.Mob}, filterIdList, filterTypeIdList)
    hurtEnt = []
    for eid in entities:
        if funcBeforeHurt:
            retEid = funcBeforeHurt(eid, attackerId, childAttackerId)
            if retEid:
                eid = retEid
        hurt(eid, damage, cause, attackerId, childAttackerId, knocked, force)
        if funcAfterHurt:
            retEid = funcAfterHurt(eid, attackerId, childAttackerId)
            if retEid:
                eid = retEid
        hurtEnt.append(eid)
    return hurtEnt


def sector_aoe_damage(attackerId, sectorRadius, sectorAngle, damage, knocked=True, filterIdList=None,
                      filterTypeIdList=None, force=False):
    # type: (str, float, float, int, bool, list[str] | None, list[int] | None, bool) -> list[str]
    """
    朝攻击者视线前方造成扇形范围伤害。（无视攻击冷却）
    -----------------------------------------------------------
    【attackerId: str】 攻击者ID
    【sectorRadius: float】 扇形半径
    【sectorAngle: float】 扇形张开的角度
    【damage: int】 伤害
    【knocked: bool = True】 是否击退
    【filterIdList: Optional[List[str] = None]】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    【force: bool = False】 是否无视攻击冷却或生物的无敌状态强制设置伤害
    -----------------------------------------------------------
    return: List[str] -> 受到伤害的实体ID列表
    """
    if filterIdList is None:
        filterIdList = []
    filterIdList = _copy(filterIdList)
    filterIdList.append(attackerId)
    attackerPos = _ServerCompFactory.CreatePos(attackerId).GetFootPos()
    attackerRot = _ServerCompFactory.CreateRot(attackerId).GetRot()[1]
    dim = _ServerCompFactory.CreateDimension(attackerId).GetEntityDimensionId()
    entityList = _get_entities_in_area(attackerPos, sectorRadius, dim, filterIdList, filterTypeIdList, True)
    result = []
    for eid in entityList:
        pos = _ServerCompFactory.CreatePos(eid).GetFootPos()
        test = _is_in_sector((pos[0], attackerPos[1], pos[2]), attackerPos, sectorRadius, sectorAngle, attackerRot)
        if test:
            hurt(eid, damage, "entity_attack", attackerId, "", knocked, force)
            result.append(eid)
    return result


def rectangle_aoe_damage(topPos1, topPos2, dim, damage, attackerId="", knocked=True, filterIdList=None,
                         filterTypeIdList=None, force=False):
    # type: (tuple[float, float, float], tuple[float, float, float], int, int, str, bool, list[str] | None, list[int] | None, bool) -> list[str]
    """
    对指定矩形区域内所有实体造成伤害。（无视攻击冷却）
    -----------------------------------------------------------
    【topPos1: Tuple[float, float, float]】 矩形顶点坐标1
    【topPos2: Tuple[float, float, float]】 矩形顶点坐标2
    【dim: int】 维度
    【damage: int】 伤害
    【attackerId: str = ""】 攻击者ID
    【knocked: bool = True】 是否击退
    【filterIdList: Optional[List[str]] = None】 过滤的实体ID列表
    【filterTypeIdList: Optional[List[int]] = None】 过滤的实体类型ID（网易版）列表
    【force: bool = False】 是否无视攻击冷却或生物的无敌状态强制设置伤害
    -----------------------------------------------------------
    return: List[str] -> 受到伤害的实体ID列表
    """
    if filterIdList is None:
        filterIdList = []
    if attackerId:
        filterIdList.append(attackerId)
    result = []
    entitiesList = _ServerLevelComps.Game.GetEntitiesInSquareArea(None, topPos1, topPos2, dim)
    entitiesList = _entity_filter(entitiesList, _EntityType.Mob, filterIdList, filterTypeIdList)
    for eid in entitiesList:
        hurt(eid, damage, "entity_attack", attackerId, "", knocked, force)
        result.append(eid)
    return result


def hurt_by_set_health(entityId, damage):
    # type: (str, int) -> None
    """
    通过设置生命值的方式对实体造成伤害。
    -----------------------------------------------------------
    【entityId: str】 实体ID
    【damage: int】 伤害
    -----------------------------------------------------------
    NoReturn
    """
    attr = _ServerCompFactory.CreateAttr(entityId)
    health = attr.GetAttrValue(_AttrType.HEALTH)
    newHealth = int(health) - int(damage)
    attr.SetAttrValue(_AttrType.HEALTH, newHealth)


def hurt(entityId, damage, cause=_ActorDamageCause.NONE, attacker="", childAttackerId="", knocked=True, force=False):
    # type: (str, int, str, str, str, bool, bool) -> None
    """
    对指定生物造成伤害。
    -----------------------------------------------------------
    【entityId: str】 生物ID
    【damage: int】 伤害
    【cause: str = ActorDamageCause.Override】 伤害来源
    【attacker: str = ""】 攻击者实体ID
    【childAttackerId: str = ""】 伤害来源的子实体ID
    【knocked: bool = True】 是否造成击退
    【force: bool = False】 是否无视攻击冷却或生物的无敌状态强制设置伤害
    -----------------------------------------------------------
    NoReturn
    """
    hurtResult = _ServerCompFactory.CreateHurt(entityId).Hurt(int(damage), cause, attacker, childAttackerId, knocked)
    if not hurtResult and force:
        hurt_by_set_health(entityId, damage)


def percent_damage(entityId, percent, typeName, cause=_ActorDamageCause.NONE, attacker="", childAttackerId="",
                   knocked=True, force=False):
    # type: (str, float, str, str, str, str, bool, bool) -> None
    """
    对生物造成百分比伤害。（无视攻击冷却）
    -----------------------------------------------------------
    【entityId: str】 生物ID
    【percent: float】 百分比
    【typeName: str】 伤害基准（可选值为"max_health"、"health"、"hunger"、"attacker_damage"）
    【cause: str = ActorDamageCause.Override】 伤害来源
    【attacker: str = ""】 攻击者实体ID
    【childAttackerId: str = ""】 伤害来源的子实体ID
    【knocked: bool = True】 是否造成击退
    【force: bool = False】 是否无视攻击冷却或生物的无敌状态强制设置伤害
    -----------------------------------------------------------
    NoReturn
    -----------------------------------------------------------
    【示例】
    # 造成生物最大生命值百分之50的伤害
    percent_damage(entityId, 0.5, "max_health")
    # 造成生物当前生命值百分之50的伤害
    percent_damage(entityId, 0.5, "health")
    # 造成生物当前饥饿值百分之50的伤害
    percent_damage(entityId, 0.5, "hunger")
    # 对生物造成攻击者攻击力两倍的伤害
    percent_damage(entityId, 2.0, "attacker_damage", attacker=attackerId)
    """
    attr = _ServerCompFactory.CreateAttr(entityId)
    value = 0
    if typeName == "max_health":
        value = attr.GetAttrMaxValue(_AttrType.HEALTH)
    elif typeName == "health":
        value = attr.GetAttrValue(_AttrType.HEALTH)
    elif typeName == "hunger":
        value = attr.GetAttrValue(_AttrType.HUNGER)
    elif typeName == "attacker_damage" and attacker:
        value = _ServerCompFactory.CreateAttr(attacker).GetAttrValue(_AttrType.DAMAGE)
    if value > 0:
        damage = int(value * percent)
        if damage > 999999999:
            damage = 999999999
        elif damage < 0:
            damage = 0
        hurt(entityId, damage, cause, attacker, childAttackerId, knocked, force)





















