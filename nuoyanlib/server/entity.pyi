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
#   Last Modified : 2023-11-26
#
# ====================================================


from typing import Dict, List, Tuple, Optional, Union


def clear_effects(entity_id: str) -> None: ...
def bounce_entities(
    pos: Tuple[float, float, float],
    dim: int,
    radius: float,
    power: float,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    filter_abiotic: bool =False,
) -> List[str]: ...
def attract_entities(
    pos: Tuple[float, float, float],
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
def any_mob(entity_id_list: List[str]) -> bool:
def entity_filter(
    entity_list: List[str],
    *args: Union[Tuple[Tuple[float, float, float], float], int, List[str], List[int]],
) -> List[str]: ...
def is_entity_type(entity_id: str, etype: Union[int, str]) -> bool: ...
def sort_entity_list_by_dist(entity_list: List[str], pos: Tuple[float, float, float]) -> None: ...
def launch_projectile(
    projectile_name: str,
    spawner_id: str,
    power: Optional[float] = None,
    damage: Optional[int] = None,
    position: Optional[Tuple[float, float, float]] = None,
    direction: Optional[Tuple[float, float, float]] = None,
    gravity: Optional[float] = None,
    target_id: str = "",
    damage_owner: bool = False,
) -> str: ...
def entity_plunge(entity_id1: str, entity_id2: str, speed: float) -> None: ...
def entity_plunge_by_dir(entity_id: str, direction: Tuple[float, float, float], speed: float) -> None: ...
def entity_plunge_by_rot(entity_id: str, rot: Tuple[float, float], speed: float) -> None: ...
def get_all_entities() -> List[str]: ...
def get_entities_in_area(
    pos: Tuple[float, float, float],
    radius: float,
    dimension: int = 0,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    filter_abiotic: bool = False,
) -> List[str]: ...
def get_entities_by_type(
    type_id: int,
    pos: Optional[Tuple[float, float, float]] = None,
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
    obj: Union[str, Tuple[float, float, float]],
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
    start_pos: Tuple[float, float, float],
    direction: Tuple[float, float, float],
    length: float,
    dimension: int = 0,
    count: int = 0,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    filter_type_str: Optional[List[str]] = None,
    filter_abiotic: bool = False,
) -> List[Dict[str, Union[str, tuple]]]: ...
def entity_distance(ent1: str, ent2: str) -> float: ...