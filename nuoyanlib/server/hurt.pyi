# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


from contextlib import contextmanager
from typing import List, Optional, Callable, ContextManager
from mod.common.minecraftEnum import ActorDamageCause
from .._core._types._typing import FTuple3


@contextmanager
def ignore_dmg_cd(restore_cd: int = 10) -> ContextManager: ...


class EntityFilter:
    @staticmethod
    def non_mob(eid: str) -> bool: ...
    @staticmethod
    def mob(eid: str) -> bool: ...
    @staticmethod
    def has_health(eid: str) -> bool: ...


def explode_hurt(
    radius: float,
    pos: FTuple3,
    source_id: str,
    dim: int,
    fire: bool = False,
    breaks: bool = True,
    tile_drops: bool = True,
    mob_loot: bool = True,
    hurt_source: bool = False,
) -> None: ...
def line_damage(
    radius: float,
    start_pos: FTuple3,
    end_pos: FTuple3,
    dim: int,
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    before_hurt_callback: Optional[Callable[[str, str, str], Optional[str]]] = None,
    after_hurt_callback: Optional[Callable[[str, str, str], Optional[str]]] = None,
    force: bool = False,
) -> List[str]: ...
def hurt_mobs(
    entity_id_list: List[str],
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
) -> None: ...
def aoe_damage(
    radius: float,
    pos: FTuple3,
    dim: int,
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    before_hurt_callback: Optional[Callable[[str, str, str], Optional[str]]] = None,
    after_hurt_callback: Optional[Callable[[str, str, str], Optional[str]]] = None,
    force: bool = False,
) -> List[str]: ...
def sector_aoe_damage(
    sector_radius: float,
    sector_angle: float,
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    force: bool = False,
) -> List[str]: ...
def rectangle_aoe_damage(
    min_vertex: FTuple3,
    max_vertex: FTuple3,
    dim: int,
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    hurt_attacker: bool = False,
    hurt_child: bool = False,
    ent_filter: Optional[Callable[[str], bool]] = None,
    force: bool = False,
) -> List[str]: ...
def hurt_by_set_health(entity_id: str, damage: int) -> None: ...
def hurt(
    entity_id: str,
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
) -> None: ...
def percent_damage(
    entity_id: str,
    percent: float,
    type_name: str,
    cause: str = ActorDamageCause.EntityAttack,
    attacker: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
) -> None: ...
