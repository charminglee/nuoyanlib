# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from typing import Dict, List, Tuple, Optional, Union, Set, Callable
from ..core._types._typing import FTuple3, FTuple2


def set_query_mod_var(entity_id: str, name: str, value: float) -> None: ...
def clear_effects(entity_id: str) -> None: ...
def bounce_entities(
    pos: FTuple3,
    dim: int,
    radius: float,
    power: float,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    filter_abiotic: bool =False,
) -> List[str]: ...
def attract_entities(
    pos: FTuple3,
    dim: int,
    radius: float,
    power: float,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    filter_abiotic: bool =False,
) -> List[str]: ...
def is_mob(entity_id: str) -> bool: ...
def all_mob(entity_id_list: List[str]) -> bool: ...
def any_mob(entity_id_list: List[str]) -> bool: ...
def entity_filter(
    entity_list: List[str],
    *args: Union[Tuple[FTuple3, float], int, List[str], List[int], Set[int], Set[str]],
) -> List[str]: ...
def is_entity_type(entity_id: str, etype: Union[int, str]) -> bool: ...
def sort_entity_list_by_dist(entity_list: List[str], pos: FTuple3) -> None: ...
def launch_projectile(
    projectile_name: str,
    spawner_id: str,
    power: Optional[float] = None,
    damage: Optional[int] = None,
    position: Optional[FTuple3] = None,
    direction: Optional[FTuple3] = None,
    gravity: Optional[float] = None,
    target_id: str = "",
    damage_owner: bool = False,
) -> str: ...
def entity_plunge(entity_id1: str, entity_id2: str, speed: float) -> None: ...
def entity_plunge_by_dir(entity_id: str, direction: FTuple3, speed: float) -> None: ...
def entity_plunge_by_rot(entity_id: str, rot: FTuple2, speed: float) -> None: ...
def get_all_entities(ent_filter: Optional[Callable[[str], bool]] = None) -> List[str]: ...
def get_entities_in_area(
    pos: FTuple3,
    radius: float,
    dimension: int = 0,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    filter_abiotic: bool = False,
) -> List[str]: ...
def get_entities_by_type(
    type_id: int,
    pos: Optional[FTuple3] = None,
    dimension: int = 0,
    radius: float = 0.0,
) -> List[str]: ...
def get_entities_by_name(name: str) -> List[str]: ...
def get_entities_by_locking(
    entity_id: str,
    dist: float = -1.0,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
) -> List[str]: ...
def get_nearest_entity(
    obj: Union[str, FTuple3],
    count: int = 1,
    dim: int = 0,
    radius: float = -1.0,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_abiotic: bool = False,
) -> Union[str, List[str], None]: ...
def attack_nearest_mob(
    entity_id: str,
    r: float = 15.0,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
) -> Optional[str]: ...
def has_effect(entity_id: str, effect_id: str) -> bool: ...
def get_entities_by_ray(
    start_pos: FTuple3,
    direction: FTuple3,
    length: float,
    dimension: int = 0,
    count: int = 0,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    filter_abiotic: bool = False,
) -> List[Dict[str, Union[str, tuple]]]: ...
