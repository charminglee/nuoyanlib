# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-3-27
#  ⠀
# =================================================


import operator
from mod.common.minecraftEnum import AttrType
from ..core._types._checker import args_type_check
from ..core._sys import get_cf
from ..core._utils import inject_is_client


if not 1:
    from typing import Iterable


__all__ = [
    "FilterFunc",
    "EntityFilter",
]


_OP_MAP = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}


def _eval_op(op, this, other):
    return _OP_MAP[op](this, other) if op else bool(this)


def _eval_molang(entity_id, molang):
    res = get_cf(entity_id).QueryVariable.EvalMolangExpression(molang)
    if not res or 'value' not in res:
        return
    return res['value']


class FilterFunc:
    @staticmethod
    def identifier(entity_id, op, other, *args):
        this = get_cf(entity_id).EngineType.GetEngineTypeStr()
        return _eval_op(op, this, other)

    @staticmethod
    def health(entity_id, op, other, *args):
        this = get_cf(entity_id).Attr.GetAttrValue(AttrType.HEALTH)
        return _eval_op(op, this, other)

    @staticmethod
    def in_water(entity_id, op, other, *args):
        this = _eval_molang(entity_id, "query.is_in_water")
        if this is None:
            return False
        return _eval_op(op, this, other)

    @staticmethod
    def in_lava(entity_id, op, other, *args):
        this = _eval_molang(entity_id, "query.is_in_lava")
        if this is None:
            return False
        return _eval_op(op, this, other)

    @staticmethod
    @inject_is_client
    def on_fire(__is_client__, entity_id, op, other, *args):
        if __is_client__:
            this = _eval_molang(entity_id, "query.is_on_fire")
        else:
            this = get_cf(entity_id).Attr.IsEntityOnFire()
        return _eval_op(op, this, other)

    @staticmethod
    @inject_is_client
    def family(__is_client__, entity_id, op, other, *args):
        if __is_client__:
            return False
            # this = _eval_molang(entity_id, "query.has_any_family('%s')" % other)
            # if this is None:
            #     return False
            # if op == '==':
            #     return bool(this)
            # elif op == '!=':
            #     return not this
        else:
            this = get_cf(entity_id).Attr.GetTypeFamily()
            if not this:
                return False
            if op == '==':
                return other in this
            elif op == '!=':
                return other not in this
        return False

    @staticmethod
    @inject_is_client
    def dimension(__is_client__, entity_id, op, other, *args):
        if __is_client__:
            return True
        else:
            this = get_cf(entity_id).Dimension.GetEntityDimensionId()
            return _eval_op(op, this, other)


class _FilterType(object):
    __slots__ = ('typ', 'args', 'op', 'other', 'conjoin_op')

    def __init__(self, typ, *args):
        self.typ = [typ]
        self.args = [args]
        self.op = [None]
        self.other = [None]
        self.conjoin_op = []

    def __call__(self, entity_id):
        if self.conjoin_op:
            pass
        else:
            func = getattr(FilterFunc, self.typ[0])
            op = self.op[0]
            other = self.other[0]
            return func(entity_id, op, other, *self.args[0])

    def _set_comparison(self, op, other):
        if self.conjoin_op:
            self.op.append(op)
            self.other.append(other)
        else:
            self.op[0] = op
            self.other[0] = other

    def __eq__(self, other):
        self._set_comparison('==', other)
        return self

    def __ne__(self, other):
        self._set_comparison('!=', other)
        return self

    def __gt__(self, other):
        self._set_comparison('>', other)
        return self

    def __lt__(self, other):
        self._set_comparison('<', other)
        return self

    def __ge__(self, other):
        self._set_comparison('>=', other)
        return self

    def __le__(self, other):
        self._set_comparison('<=', other)
        return self

    def _conjoin(self, op, ft):
        self.typ.extend(ft.typ)
        self.args.extend(ft.args)
        self.op.extend(ft.op)
        self.other.extend(ft.other)
        self.conjoin_op.append(op)

    def __and__(self, other):
        self._conjoin('&', other)
        return self

    def __or__(self, other):
        self._conjoin('|', other)
        return self


class EntityFilter(object):
    """
    实体过滤器。

    用于从实体ID序列中快速筛选出符合条件的实体ID。

    示例
    ----

    使用 ``GetEngineActor()`` 构造一个 ``EntityFilter`` 。

    >>> import mod.server.extraServerApi as server_api
    >>> all_entities = server_api.GetEngineActor()
    >>> ef = nyl.EntityFilter(all_entities)

    使用简单条件过滤实体，过滤结果将以列表返回。支持所有 Python 比较运算符。

    >>> ef[ef.health > 0]
    [all_entities中生命值大于0的实体ID...]
    >>> ef[ef.identifier == "minecraft:zombie"]
    [identifier为"minecraft:zombie"的实体ID...]
    >>> ef[ef.in_water]
    [位于水中的实体ID...]
    >>> ef[ef.family == "mob"]
    [family为mob的实体ID...]

    使用复合条件过滤实体。
    ``&`` 等价于 ``and`` ， ``|`` 等价于 ``or`` ，不能使用 ``and`` ``or`` ``not`` 。
    使用 ``&``  ``|`` 时需注意运算符优先级。

    >>> ef[ef.on_fire & (ef.identifier == "minecraft:zombie")]
    [处于燃烧状态的僵尸的实体ID...]
    >>> ef[ef.in_water | ef.in_lava]
    [位于水或岩浆中的实体ID...]

    使用自定义过滤函数。
    过滤函数需接受一个实体ID参数，并返回一个布尔值；返回 ``True`` 时，该实体ID将会出现在过滤结果列表中。

    >>> def is_near_player(entity_id):
    ...     # 与任一玩家的距离小于10时返回True
    ...     for player_id in server_api.GetPlayerList():
    ...         dist = nyl.distance(entity_id, player_id)
    ...         if dist < 10:
    ...             return True
    ...     return False
    ...
    >>> ef[is_near_player]
    [与任一玩家的距离小于10的实体ID...]

    -----

    :param Iterable[str] entities: 元素为实体ID的可迭代对象（如列表、元组、字典等）
    """

    def __init__(self, entities):
        self.entities = entities

    @args_type_check((_FilterType, callable))
    def __getitem__(self, key):
        return filter(key, self.entities)

    @property
    def identifier(self):
        """
        [只读属性]

        实体 ``identifier`` 。

        :rtype: _FilterType
        """
        return _FilterType("identifier")

    @property
    def health(self):
        """
        [只读属性]

        实体生命值。

        说明
        ----

        作用与 json filter ``actor_health`` 相同，详见 `微软文档 <https://learn.microsoft.com/zh-cn/minecraft/creator/reference/content/entityreference/examples/filters/actor_health?view=minecraft-bedrock-stable>`_ 。

        :rtype: _FilterType
        """
        return _FilterType("health")

    @property
    def in_water(self):
        """
        [只读属性]

        实体是否在水中。

        说明
        ----

        作用与 json filter ``in_water`` 相同，详见 `微软文档 <https://learn.microsoft.com/zh-cn/minecraft/creator/reference/content/entityreference/examples/filters/in_water?view=minecraft-bedrock-stable>`_ 。

        :rtype: _FilterType
        """
        return _FilterType("in_water")

    @property
    def in_lava(self):
        """
        [只读属性]

        实体是否在岩浆中。

        说明
        ----

        作用与 json filter ``in_lava`` 相同，详见 `微软文档 <https://learn.microsoft.com/zh-cn/minecraft/creator/reference/content/entityreference/examples/filters/in_lava?view=minecraft-bedrock-stable>`_ 。

        :rtype: _FilterType
        """
        return _FilterType("in_lava")

    @property
    def on_fire(self):
        """
        [只读属性]

        实体是否在燃烧。

        说明
        ----

        作用与 json filter ``on_fire`` 相同，详见 `微软文档 <https://learn.microsoft.com/zh-cn/minecraft/creator/reference/content/entityreference/examples/filters/on_fire?view=minecraft-bedrock-stable>`_ 。

        :rtype: _FilterType
        """
        return _FilterType("on_fire")

    @property
    def family(self):
        """
        实体 ``family`` 。

        说明
        ----

        作用与 json filter ``is_family`` 相同，详见 `微软文档 <https://learn.microsoft.com/zh-cn/minecraft/creator/reference/content/entityreference/examples/filters/is_family?view=minecraft-bedrock-stable>`_ 。

        :rtype: _FilterType
        """
        return _FilterType("family")

    @property
    def dimension(self):
        """
        实体所在维度ID。

        :rtype: _FilterType
        """
        return _FilterType("dimension")


def __benchmark__(n, timer, **kwargs):
    import mod.client.extraClientApi as api
    # import mod.server.extraServerApi as api
    from .mc_math.mc_math import distance

    all_entities = api.GetEngineActor()
    all_players = api.GetPlayerList()
    ef = EntityFilter(all_entities)

    def is_near_player(entity_id):
        for player_id in all_players:
            dist = distance(entity_id, player_id)
            if dist < 10:
                return True
            return False

    timer.start("identifier")
    for _ in xrange(n):
        ef[ef.identifier == "minecraft:zombie"]
    timer.end("identifier")

    timer.start("health")
    for _ in xrange(n):
        ef[ef.health > 0]
    timer.end("health")

    timer.start("in_water")
    for _ in xrange(n):
        ef[ef.in_water]
    timer.end("in_water")

    timer.start("on_fire")
    for _ in xrange(n):
        ef[ef.on_fire]
    timer.end("on_fire")

    timer.start("family")
    for _ in xrange(n):
        ef[ef.family == "mob"]
    timer.end("family")

    timer.start("on_fire & identifier")
    for _ in xrange(n):
        ef[ef.on_fire & (ef.identifier == "minecraft:zombie")]
    timer.end("on_fire & identifier")

    timer.start("in_water | in_lava")
    for _ in xrange(n):
        ef[ef.in_water | ef.in_lava]
    timer.end("in_water | in_lava")

    timer.start("is_near_player")
    for _ in xrange(n):
        ef[is_near_player]
    timer.end("is_near_player")





















