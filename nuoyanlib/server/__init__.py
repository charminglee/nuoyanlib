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
#   Last Modified : 2023-09-06
#
# ====================================================


from serverComps import (
    SERVER_ENGINE_NAMESPACE,
    SERVER_ENGINE_SYSTEM_NAME,
    ServerSystem,
    ServerCompFactory,
    LEVEL_ID,
    ServerLevelComps,
)
from structure import (
    place_large_structure,
)
from entity import (
    clear_effects,
    bounce_entities,
    attract_entities,
    is_mob,
    all_mob,
    has_mob,
    entity_filter,
    is_entity_type,
    sort_entity_list_by_dist,
    launch_projectile,
    entity_plunge,
    entity_plunge_by_dir,
    entity_plunge_by_rot,
    get_all_entities,
    get_entities_by_name,
    get_entities_by_type,
    get_entities_in_area,
    get_entities_by_locking,
    get_nearest_entity,
    attack_nearest_mob,
    has_effect,
)
from hurt import (
    explode_hurt,
    aoe_damage,
    sector_aoe_damage,
    rectangle_aoe_damage,
    hurt_by_set_health,
    hurt,
    percent_damage,
    line_damage,
)
from inv import (
    deduct_inv_item,
    clear_items,
    get_item_pos,
    change_item_count,
)
from nuoyanServerSystem import (
    server_listener,
    ALL_SERVER_ENGINE_EVENTS,
    NuoyanServerSystem,
)


__all__ = [
    "SERVER_ENGINE_NAMESPACE",
    "SERVER_ENGINE_SYSTEM_NAME",
    "ServerSystem",
    "ServerCompFactory",
    "LEVEL_ID",
    "ServerLevelComps",
    "place_large_structure",
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
    "explode_hurt",
    "aoe_damage",
    "sector_aoe_damage",
    "rectangle_aoe_damage",
    "hurt_by_set_health",
    "hurt",
    "percent_damage",
    "line_damage",
    "deduct_inv_item",
    "clear_items",
    "get_item_pos",
    "change_item_count",
    "server_listener",
    "ALL_SERVER_ENGINE_EVENTS",
    "NuoyanServerSystem",
]
