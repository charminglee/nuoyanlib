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
#   Last Modified : 2025-05-28
#
# ====================================================


"""
nuoyanlib工具库。
"""


from .mc_math import (
    pos_block_facing,
    to_polar_coordinate,
    to_cartesian_coordinate,
    probability_true_i,
    probability_true_f,
    pos_distance_to_line,
    pos_floor,
    pos_distance,
    to_relative_pos,
    to_screen_pos,
    pos_rotate,
    midpoint,
    camera_rot_p2p,
    pos_entity_facing,
    pos_forward_rot,
    n_quantiles_index_list,
    cube_center,
    cube_longest_side_len,
    is_in_sector,
    is_in_cube,
    rot_diff,
    ray_aabb_intersection,
)
from .enum import (
    Enum,
    search_data,
    ITEM_LIST,
    BLOCK_LIST,
    STRUCTURE_DICT,
    BIOME_DICT,
    EFFECT_DICT,
    ENTITY_ID_DICT,
    ATTACKABLE_MOB_LIST,
    HOSTILE_MOB_LIST,
    FRIENDLY_MOB_LIST,
    MOB_LIST,
    ENTITY_LIST,
)
from .item import (
    deepcopy_item_dict,
    gen_item_dict,
    get_item_count,
    set_namespace,
    is_same_item,
    is_empty_item,
    are_same_item,
    get_max_stack,
)
from .mc_random import (
    random_pos,
    random_string,
    random_even_poses,
)
# from .mc_timer import *
from .utils import (
    add_condition_to_func,
    remove_condition_to_func,
    all_indexes,
    check_string,
    check_string2,
    turn_dict_value_to_tuple,
    turn_list_to_tuple,
    is_method_overridden,
    translate_time,
)
from .vector import (
    is_zero_vec,
    set_vec_length,
    vec_orthogonal_decomposition,
    vec_entity_left,
    vec_entity_right,
    vec_entity_front,
    vec_entity_back,
    vec_normalize,
    vec_rot_p2p,
    vec_p2p,
    vec_length,
    vec_angle,
    vec_euler_rotate,
    vec_rotate_around,
    outgoing_vec,
    vec_composite,
    vec_scale,
)
from .time_ease import (
    TimeEaseFunc,
    TimeEase,
)
from .communicate import (
    Caller,
    broadcast_to_all_systems,
    call,
)
from .pos_gen import (
    gen_line_pos,
    gen_circle_pos,
    gen_sphere_pos,
    gen_cube_pos,
    gen_spiral_pos,
)
