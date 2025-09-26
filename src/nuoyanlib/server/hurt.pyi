# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-26
|
| ==============================================
"""


from contextlib import contextmanager
from typing import List, Optional, Callable, ContextManager, Literal, Any
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


__BasicPos = Literal["foot_pos", "center"]


def hurt(
    entity_id: str,
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
) -> bool: ...
def hurt_mobs(
    entities: List[str],
    damage: float,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
    hurt_attacker: bool = False,
    hurt_child: bool = False,
    ent_filter: Optional[Callable[[str], bool]] = None,
    on_hurt_before: Optional[Callable[[str], Optional[str]]] = None,
    on_hurt_after: Optional[Callable[[str], Optional[str]]] = None,
) -> List[str]: ...
def explode_damage(
    r: float,
    pos: FTuple3,
    source_id: str,
    dim: int,
    fire: bool = False,
    breaks: bool = True,
    tile_drops: bool = True,
    mob_loot: bool = True,
    hurt_source: bool = False,
) -> None: ...
def _visualize_area(area_type: str, *args: Any) -> None: ...
def _get_basic_pos(entity_id: str, base: __BasicPos) -> FTuple3: ...
def cylinder_damage(
    damage: float,
    r: float,
    pos1: FTuple3,
    pos2: FTuple3,
    dim: int,
    *,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
    hurt_attacker: bool = False,
    hurt_child: bool = False,
    ent_filter: Optional[Callable[[str], bool]] = None,
    on_hurt_before: Optional[Callable[[str], Optional[str]]] = None,
    on_hurt_after: Optional[Callable[[str], Optional[str]]] = None,
    visualize: bool = False,
    basic_pos: __BasicPos = "foot_pos",
) -> List[str]: ...
def sphere_damage(
    damage: float,
    r: float,
    pos: FTuple3,
    dim: int,
    *,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
    hurt_attacker: bool = False,
    hurt_child: bool = False,
    ent_filter: Optional[Callable[[str], bool]] = None,
    on_hurt_before: Optional[Callable[[str], Optional[str]]] = None,
    on_hurt_after: Optional[Callable[[str], Optional[str]]] = None,
    visualize: bool = False,
    basic_pos: __BasicPos = "foot_pos",
) -> List[str]: ...
def sector_damage(
    damage: float,
    r: float,
    angle: float,
    center: FTuple3,
    direction: FTuple3,
    dim: int,
    *,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
    hurt_attacker: bool = False,
    hurt_child: bool = False,
    ent_filter: Optional[Callable[[str], bool]] = None,
    on_hurt_before: Optional[Callable[[str], Optional[str]]] = None,
    on_hurt_after: Optional[Callable[[str], Optional[str]]] = None,
    visualize: bool = False,
    basic_pos: __BasicPos = "foot_pos",
) -> List[str]: ...
def rectangle_damage(
    damage: float,
    pos1: FTuple3,
    pos2: FTuple3,
    dim: int,
    *,
    cause: str = ActorDamageCause.EntityAttack,
    attacker_id: Optional[str] = None,
    child_id: Optional[str] = None,
    knocked: bool = True,
    force: bool = False,
    hurt_attacker: bool = False,
    hurt_child: bool = False,
    ent_filter: Optional[Callable[[str], bool]] = None,
    on_hurt_before: Optional[Callable[[str], Optional[str]]] = None,
    on_hurt_after: Optional[Callable[[str], Optional[str]]] = None,
    visualize: bool = False,
    basic_pos: __BasicPos = "foot_pos",
) -> List[str]: ...
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
