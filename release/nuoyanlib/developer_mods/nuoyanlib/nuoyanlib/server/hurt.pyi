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
#   Last Modified : 2024-04-28
#
# ====================================================


from typing import Tuple, List, Optional, Callable
from mod.common.minecraftEnum import ActorDamageCause


def explode_hurt(
    radius: float,
    pos: Tuple[float, float, float],
    source_id: str,
    dim: int,
    fire: bool = False,
    breaks: bool = True,
    tile_drops: bool = True,
    mob_loot: bool = True,
    hurt_source: bool = False,
) -> None: ...
def line_damage(
    damage: int,
    radius: float,
    start_pos: Tuple[float, float, float],
    end_pos: Tuple[float, float, float],
    dim: int,
    attacker_id: str = "",
    child_id: str = "",
    cause: str = ActorDamageCause.NONE,
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
    damage: int,
    attacker_id: str = "",
    child_id: str = "",
    cause: str = ActorDamageCause.NONE,
    knocked: bool = True,
    force: bool = False,
) -> None: ...
def aoe_damage(
    damage: int,
    radius: float,
    pos: Tuple[float, float, float],
    dim: int,
    attacker_id: str = "",
    child_id: str = "",
    cause: str = ActorDamageCause.NONE,
    knocked: bool = True,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    before_hurt_callback: Optional[Callable[[str, str, str], Optional[str]]] = None,
    after_hurt_callback: Optional[Callable[[str, str, str], Optional[str]]] = None,
    force: bool = False,
) -> List[str]: ...
def sector_aoe_damage(
    attacker_id: str,
    sector_radius: float,
    sector_angle: float,
    damage: int,
    knocked: bool = True,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    force: bool = False,
) -> List[str]: ...
def rectangle_aoe_damage(
    top_pos1: Tuple[float, float, float],
    top_pos2: Tuple[float, float, float],
    dim: int,
    damage: int,
    attacker_id: str = "",
    knocked: bool = True,
    filter_ids: Optional[List[str]] = None,
    filter_types: Optional[List[int]] = None,
    force: bool = False,
) -> List[str]: ...
def hurt_by_set_health(entity_id: str, damage: int) -> None: ...
def hurt(
    entity_id: str,
    damage: int,
    cause: str = ActorDamageCause.NONE,
    attacker: str = "",
    child_id: str = "",
    knocked: bool = True,
    force: bool = False,
) -> None: ...
def percent_damage(
    entity_id: str,
    percent: float,
    type_name: str,
    cause: str = ActorDamageCause.NONE,
    attacker: str = "",
    child_id: str = "",
    knocked: bool = True,
    force: bool = False,
) -> None: ...
