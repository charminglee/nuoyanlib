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
#   Last Modified : 2024-07-05
#
# ====================================================


from .._core._const import LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH
import mod.server.extraServerApi as server_api
if not server_api.GetSystem(LIB_NAME, LIB_SERVER_NAME):
    server_api.RegisterSystem(LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH)
del server_api, LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH


from .._core._server._comp import *
from .._core._server._listener import (
    event,
)
from .server_system import *
from .entity import *
from .hurt import *
from .inv import *
from .structure import *


__all__ = [
    # _comp
    "SERVER_ENGINE_NAMESPACE",
    "SERVER_ENGINE_SYSTEM_NAME",
    "ServerSystem",
    "CompFactory",
    "LEVEL_ID",
    "LvComp",
    # _listener
    "event",
    # server_system
    "NuoyanServerSystem",
    # entity
    "set_query_mod_var",
    "clear_effects",
    "bounce_entities",
    "attract_entities",
    "is_mob",
    "all_mob",
    "any_mob",
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
    # hurt
    "explode_hurt",
    "aoe_damage",
    "sector_aoe_damage",
    "rectangle_aoe_damage",
    "hurt_by_set_health",
    "hurt",
    "percent_damage",
    "line_damage",
    # inv
    "set_items_to_item_grid",
    "get_items_from_item_grid",
    "update_item_grids",
    "deduct_inv_item",
    "clear_items",
    "get_item_pos",
    "change_item_count",
    # structure
    "place_large_structure",
]
