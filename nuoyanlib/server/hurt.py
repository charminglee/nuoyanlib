# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-29
|
| ==============================================
"""


from contextlib import contextmanager
import mod.server.extraServerApi as server_api
from mod.common.minecraftEnum import AttrType, ActorDamageCause, EntityComponentType
from mod.common.utils.mcmath import Vector3
from .._core._server.comp import CF, LvComp
from ..utils.mc_math import is_in_sector
from .entity import get_all_entities, get_entities_in_area


__all__ = [
    "ignore_dmg_cd",
    "EntityFilter",
    "hurt",
    "hurt_mobs",
    "explode_damage",
    "cylinder_damage",
    "ball_damage",
    "sector_damage",
    "rectangle_damage",
    "percent_damage",
]


@contextmanager
def ignore_dmg_cd(restore_cd=10):
    """
    [上下文管理器]

    | 用于忽略生物受击后的 `伤害免疫时间 <https://zh.minecraft.wiki/w/%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB>`_ 。

    -----

    【示例】

    ::

        import myScripts.nuoyanlib.server as nyl

        with nyl.ignore_dmg_cd():
            # 在with范围内伤害免疫时间会被设为0
            comp = nyl.CF(entity_id).Hurt
            comp.Hurt(10, "entity_attack")
            comp.Hurt(10, "entity_attack")
        # 上下文管理器退出

    -----

    :param int restore_cd: 上下文管理器退出后恢复的伤害免疫时间（单位为游戏刻），默认为10

    :return: 无
    :rtype: None
    """
    LvComp.Game.SetHurtCD(0)
    yield
    LvComp.Game.SetHurtCD(restore_cd)


class EntityFilter:
    """
    | 实体过滤器，预设了一些常用的过滤条件。
    | 过滤器接受一个实体ID作为参数，且返回一个 ``bool`` 值，返回 ``True`` 时表示该实体符合条件。
    """

    @staticmethod
    def mob(eid):
        """
        | 过滤生物实体。（判定标准为是否具有 ``minecraft:health`` 组件）

        -----

        :param str eid: 实体ID

        :return: 返回True时表示该实体为生物实体
        :rtype: bool
        """
        return CF(eid).EntityComponent.HasComponent(EntityComponentType.health)

    @staticmethod
    def non_mob(eid):
        """
        | 过滤非生物实体。（判定标准为是否具有 ``minecraft:health`` 组件）

        -----

        :param str eid: 实体ID

        :return: 返回True时表示该实体为非生物实体
        :rtype: bool
        """
        return not EntityFilter.mob(eid)

    @staticmethod
    def has_health(eid):
        """
        | 过滤当前生命值大于0的实体。

        -----

        :param str eid: 实体ID

        :return: 返回True时表示该实体当前生命值大于0
        :rtype: bool
        """
        return CF(eid).Attr.GetAttrValue(AttrType.HEALTH) > 0


_SDK_DAMAGE_CAUSE = [
    v
    for k, v in ActorDamageCause.__dict__.items()
    if not k.startswith("_")
]


def hurt(
        entity_id,
        damage,
        cause=ActorDamageCause.EntityAttack,
        attacker=None,
        child_id=None,
        knocked=True,
        force=False,
):
    """
    | 对指定生物造成伤害。

    -----

    :param str entity_id: 生物ID
    :param float damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 伤害来源的子实体ID，默认无子实体
    :param bool knocked: 是否造成击退，默认为是
    :param bool force: 是否无视 `伤害免疫时间 <https://zh.minecraft.wiki/w/%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB>`_ 强制造成伤害，默认为False

    :return: 是否成功
    :rtype: bool
    """
    if cause in _SDK_DAMAGE_CAUSE:
        custom_tag = None
    else:
        custom_tag = cause
        cause = ActorDamageCause.Custom
    _hurt = CF(entity_id).Hurt.Hurt
    if force:
        with ignore_dmg_cd():
            res = _hurt(damage, cause, attacker, child_id, knocked, custom_tag)
    else:
        res = _hurt(damage, cause, attacker, child_id, knocked, custom_tag)
    return res


def hurt_mobs(
        entities,
        damage,
        cause=ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        force=False,
        hurt_attacker=False,
        hurt_child=False,
        ent_filter=None,
        on_hurt_before=None,
        on_hurt_after=None,
):
    """
    | 对多个实体造成伤害。

    -----

    :param list[str] entities: 实体ID列表
    :param float damage: 伤害
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为True
    :param bool force: 是否无视 `伤害免疫时间 <https://zh.minecraft.wiki/w/%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB>`_ 强制造成伤害，默认为False
    :param bool hurt_attacker: 是否对攻击者造成伤害，默认为False
    :param bool hurt_child: 是否对子实体造成伤害，默认为False
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否对该实体造成伤害，返回False时不会对该实体造成伤害，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None
    :param function|None on_hurt_before: 对实体造成伤害之前调用的函数，该函数需接受一个参数，值为受伤实体ID；若该函数返回一个新的实体ID，对原实体造成的伤害将会转移给该实体；默认为None
    :param function|None on_hurt_after: 对实体造成伤害之后调用的函数，该函数需接受两个参数，第一个参数为受伤实体ID，第二个参数为是否成功造成伤害；默认为None

    :return: 最终成功受到伤害的实体ID列表
    :rtype: list[str]
    """
    final_ents = []
    def _hurt():
        for eid in entities:
            if not hurt_attacker and eid == attacker_id:
                continue
            if not hurt_child and eid == child_id:
                continue
            if ent_filter and not ent_filter(eid):
                continue
            if on_hurt_before:
                new_eid = on_hurt_before(eid)
                if new_eid:
                    eid = new_eid
            res = hurt(eid, damage, cause, attacker_id, child_id, knocked)
            if on_hurt_after:
                on_hurt_after(eid)
            if res:
                final_ents.append(eid)
    if force:
        with ignore_dmg_cd():
            _hurt()
    else:
        _hurt()
    return final_ents


def explode_damage(
        r,
        pos,
        source_id,
        dim,
        fire=False,
        breaks=True,
        tile_drops=True,
        mob_loot=True,
        hurt_source=False,
):
    """
    | 造成爆炸伤害。
    
    -----

    :param float r: 爆炸强度
    :param tuple[float,float,float] pos: 爆炸中心坐标
    :param str source_id: 爆炸伤害源的实体ID
    :param int dim: 爆炸维度
    :param bool fire: 是否造成火焰，默认为否
    :param bool breaks: 是否破坏方块，默认为是
    :param bool tile_drops: 破坏方块后是否生成掉落物，默认为是
    :param bool mob_loot: 生物被炸死后是否生成掉落物，默认为是
    :param bool hurt_source: 是否对爆炸伤害源实体造成伤害，默认为否

    :return: 无
    :rtype: None
    """
    for plr in server_api.GetPlayerList():
        if CF(plr).Dimension.GetEntityDimensionId() == dim:
            player_id = plr
            break
    else:
        return
    orig_rule = LvComp.Game.GetGameRulesInfoServer()
    LvComp.Game.SetGameRulesInfoServer({'option_info': {'tile_drops': tile_drops, 'mob_loot': mob_loot}})
    hurt_comp = CF(source_id).Hurt
    try:
        if not hurt_source:
            hurt_comp.ImmuneDamage(True)
        LvComp.Explosion.CreateExplosion(pos, r, fire, breaks, source_id, player_id)
    finally:
        LvComp.Game.SetGameRulesInfoServer(orig_rule)
        if not hurt_source:
            hurt_comp.ImmuneDamage(False)


def cylinder_damage(
        damage,
        r,
        pos1,
        pos2,
        dim,
        cause=ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        force=False,
        hurt_attacker=False,
        hurt_child=False,
        ent_filter=None,
        on_hurt_before=None,
        on_hurt_after=None,
):
    """
    | 对圆柱体区域内所有实体造成伤害。
    
    -----

    :param float damage: 伤害
    :param float r: 半径
    :param tuple[float,float,float] pos1: 圆柱体底面中心坐标
    :param tuple[float,float,float] pos2: 圆柱体另一底面中心坐标
    :param int dim: 维度
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为True
    :param bool force: 是否无视 `伤害免疫时间 <https://zh.minecraft.wiki/w/%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB>`_ 强制造成伤害，默认为False
    :param bool hurt_attacker: 是否对攻击者造成伤害，默认为False
    :param bool hurt_child: 是否对子实体造成伤害，默认为False
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否对该实体造成伤害，返回False时不会对该实体造成伤害，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None
    :param function|None on_hurt_before: 对实体造成伤害之前调用的函数，该函数需接受一个参数，值为受伤实体ID；若该函数返回一个新的实体ID，对原实体造成的伤害将会转移给该实体；默认为None
    :param function|None on_hurt_after: 对实体造成伤害之后调用的函数，该函数需接受两个参数，第一个参数为受伤实体ID，第二个参数为是否成功造成伤害；默认为None

    :return: 受伤生物的实体ID列表
    :rtype: list[str]
    """
    if not pos1 or not pos2 or r <= 0 or damage <= 0:
        return []
    pos1 = Vector3(pos1)
    pos2 = Vector3(pos2)
    def _filter(eid):
        if ent_filter and not ent_filter(eid):
            return False
        cf = CF(eid)
        if cf.Dimension.GetEntityDimensionId() != dim:
            return False
        ep = cf.Pos.GetFootPos()
        if not ep:
            return False
        ep = Vector3(ep)
        axis_vec = pos2 - pos1
        ent_vec = ep - pos1
        axis_len2 = axis_vec.LengthSquared()
        ent_len2 = ent_vec.LengthSquared()
        t = Vector3.Dot(axis_vec, ent_vec) / axis_len2
        if t < 0 or t > 1:
            return False
        dist2 = ent_len2 - t * t * axis_len2
        return dist2 <= r**2
    return hurt_mobs(
        get_all_entities(),
        damage,
        cause,
        attacker_id,
        child_id,
        knocked,
        force,
        hurt_attacker,
        hurt_child,
        _filter,
        on_hurt_before,
        on_hurt_after,
    )


def ball_damage(damage, r, pos, dim, *args, **kwargs):
    """
    | 对球体区域内所有实体造成伤害。
    
    -----

    :param float damage: 伤害
    :param float r: 半径
    :param tuple[float,float,float] pos: 球体中心坐标
    :param int dim: 维度
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为True
    :param bool force: 是否无视 `伤害免疫时间 <https://zh.minecraft.wiki/w/%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB>`_ 强制造成伤害，默认为False
    :param bool hurt_attacker: 是否对攻击者造成伤害，默认为False
    :param bool hurt_child: 是否对子实体造成伤害，默认为False
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否对该实体造成伤害，返回False时不会对该实体造成伤害，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None
    :param function|None on_hurt_before: 对实体造成伤害之前调用的函数，该函数需接受一个参数，值为受伤实体ID；若该函数返回一个新的实体ID，对原实体造成的伤害将会转移给该实体；默认为None
    :param function|None on_hurt_after: 对实体造成伤害之后调用的函数，该函数需接受两个参数，第一个参数为受伤实体ID，第二个参数为是否成功造成伤害；默认为None

    :return: 受伤生物的实体ID列表
    :rtype: list[str]
    """
    if not pos or r <= 0 or damage <= 0:
        return []
    entities = get_entities_in_area(pos, r, dim)
    return hurt_mobs(entities, damage, *args, **kwargs)


def sector_damage(
        damage,
        r,
        angle,
        cause=ActorDamageCause.EntityAttack,
        attacker_id=None,
        child_id=None,
        knocked=True,
        force=False,
        hurt_attacker=False,
        hurt_child=False,
        ent_filter=None,
        on_hurt_before=None,
        on_hurt_after=None,
):
    """
    | 朝攻击者视线前方造成扇形范围伤害。（无视攻击冷却）
    
    -----

    :param float damage: 伤害
    :param float r: 扇形半径
    :param float angle: 扇形张开的角度
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为True
    :param bool force: 是否无视 `伤害免疫时间 <https://zh.minecraft.wiki/w/%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB>`_ 强制造成伤害，默认为False
    :param bool hurt_attacker: 是否对攻击者造成伤害，默认为False
    :param bool hurt_child: 是否对子实体造成伤害，默认为False
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否对该实体造成伤害，返回False时不会对该实体造成伤害，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None
    :param function|None on_hurt_before: 对实体造成伤害之前调用的函数，该函数需接受一个参数，值为受伤实体ID；若该函数返回一个新的实体ID，对原实体造成的伤害将会转移给该实体；默认为None
    :param function|None on_hurt_after: 对实体造成伤害之后调用的函数，该函数需接受两个参数，第一个参数为受伤实体ID，第二个参数为是否成功造成伤害；默认为None

    :return: 受到伤害的实体ID列表
    :rtype: list[str]
    """
    cf = CF(attacker_id)
    attacker_pos = cf.Pos.GetFootPos()
    attacker_rot = cf.Rot.GetRot()[1]
    dim = cf.Dimension.GetEntityDimensionId()
    entities = get_entities_in_area(attacker_pos, r, dim)
    def _filter(eid):
        if ent_filter and not ent_filter(eid):
            return False
        pos = CF(eid).Pos.GetFootPos()
        return is_in_sector(
            (pos[0], attacker_pos[1], pos[2]), attacker_pos, r, angle, attacker_rot
        )
    return hurt_mobs(
        entities,
        damage,
        cause,
        attacker_id,
        child_id,
        knocked,
        force,
        hurt_attacker,
        hurt_child,
        _filter,
        on_hurt_before,
        on_hurt_after,
    )


def rectangle_damage(damage, min_vertex, max_vertex, dim, *args, **kwargs):
    """
    | 对指定矩形区域内所有实体造成伤害。
    
    -----

    :param float damage: 伤害
    :param tuple[float,float,float] min_vertex: 矩形最小顶点坐标
    :param tuple[float,float,float] max_vertex: 矩形最大顶点坐标，最大顶点坐标必须大于最小顶点坐标，否则不会对任何实体造成伤害
    :param int dim: 维度
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker_id: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 攻击者的子实体ID，默认无子实体
    :param bool knocked: 是否产生击退，默认为True
    :param bool force: 是否无视 `伤害免疫时间 <https://zh.minecraft.wiki/w/%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB>`_ 强制造成伤害，默认为False
    :param bool hurt_attacker: 是否对攻击者造成伤害，默认为False
    :param bool hurt_child: 是否对子实体造成伤害，默认为False
    :param function|None ent_filter: 实体过滤器，接受一个实体ID作为参数，需要返回一个bool值，表示是否对该实体造成伤害，返回False时不会对该实体造成伤害，可以使用nuoyanlib预设的过滤器EntityFilter，默认为None
    :param function|None on_hurt_before: 对实体造成伤害之前调用的函数，该函数需接受一个参数，值为受伤实体ID；若该函数返回一个新的实体ID，对原实体造成的伤害将会转移给该实体；默认为None
    :param function|None on_hurt_after: 对实体造成伤害之后调用的函数，该函数需接受两个参数，第一个参数为受伤实体ID，第二个参数为是否成功造成伤害；默认为None

    :return: 受到伤害的实体ID列表
    :rtype: list[str]
    """
    entities = LvComp.Game.GetEntitiesInSquareArea(None, min_vertex, max_vertex, dim)
    return hurt_mobs(entities, damage, *args, **kwargs)


def percent_damage(
        entity_id,
        percent,
        type_name,
        cause=ActorDamageCause.EntityAttack,
        attacker=None,
        child_id=None,
        knocked=True,
        force=False,
):
    """
    | 对生物造成百分比伤害。
    
    -----

    :param str entity_id: 生物ID
    :param float percent: 百分比
    :param str type_name: 伤害基准（可选值为"max_health"、"health"、"hunger"、"attacker_damage"）
    :param str cause: 伤害来源，`ActorDamageCause <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/ActorDamageCause.html?key=ActorDamageCause&docindex=1&type=0>`_ 枚举，支持自定义，默认为ActorDamageCause.EntityAttack
    :param str|None attacker: 攻击者实体ID，默认无攻击者
    :param str|None child_id: 伤害来源的子实体ID，默认无子实体
    :param bool knocked: 是否造成击退，默认为是
    :param bool force: 是否无视攻击冷却或生物的无敌状态强制设置伤害，默认为否
    
    :return: 无
    :rtype: None
    """
    attr = CF(entity_id).Attr
    value = 0
    if type_name == "max_health":
        value = attr.GetAttrMaxValue(AttrType.HEALTH)
    elif type_name == "health":
        value = attr.GetAttrValue(AttrType.HEALTH)
    elif type_name == "hunger":
        value = attr.GetAttrValue(AttrType.HUNGER)
    elif type_name == "attacker_damage" and attacker:
        value = CF(attacker).Attr.GetAttrValue(AttrType.DAMAGE)
    if value > 0:
        damage = int(value * percent)
        if damage > 999999999:
            damage = 999999999
        elif damage < 0:
            damage = 0
        hurt(entity_id, damage, cause, attacker, child_id, knocked, force)





















