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
#   Last Modified : 2024-06-19
#
# ====================================================


from typing import Tuple, Union, Optional, List, Dict
from mod.common.minecraftEnum import Facing


def pos_block_facing(
    pos: Tuple[float, float, float],
    face: int = Facing.North,
    dist: float = 1.0
) -> Optional[Tuple[float, float, float]]: ...
def to_polar_coordinate(
    coordinate: Tuple[float, float],
    rad: bool = False,
    origin: Tuple[float, float] = (0, 0),
) -> Tuple[float, float]: ...
def to_cartesian_coordinate(
    coordinate: Tuple[float, float],
    rad: bool = False,
    origin: Tuple[float, float] = (0, 0),
) -> Tuple[float, float]: ...
def probability_true_i(n: int, d: int) -> bool: ...
def probability_true_f(f: float) -> bool: ...
def pos_distance_to_line(
    pos: Tuple[float, float, float],
    line_pos1: Tuple[float, float, float],
    line_pos2: Tuple[float, float, float],
) -> float: ...
def pos_floor(pos: Tuple[float, float, float]) -> Tuple[int, int, int]: ...
def pos_distance(
    first_point: Tuple[float, ...],
    second_point: Tuple[float, ...],
) -> float: ...
def to_relative_pos(
    entity_pos1: Tuple[float, float, float],
    entity_pos2: Tuple[float, float, float],
) -> Optional[Tuple[float, float, float]]: ...
def to_screen_pos(
    entity_pos: Tuple[float, float, float],
    center_pos: Tuple[float, float, float],
    screen_size: int,
    max_distance: int,
    ui_size: int,
    player_rot: float,
) -> Optional[Tuple[float, float]]: ...
def pos_rotate(angle: float, pos: Tuple[float, float]) -> Optional[Tuple[float, float]]: ...
def straight_pos_list(
    pos1: Tuple[float, float, float],
    pos2: Tuple[float, float, float],
    count: int,
    only: int=-1,
) -> List[Tuple[float, float, float]]: ...
def midpoint(first_point: Tuple[float, ...], second_point: Tuple[float, ...]) -> Tuple[float, ...]: ...
def camera_rot_p2p(
    pos1: Tuple[float, float, float],
    pos2: Tuple[float, float, float],
) -> Optional[Tuple[float, float]]: ...
def circle_pos_list(
    center_pos: Tuple[float, float, float],
    radius: float, density: int,
) -> List[Tuple[float, float, float]]: ...
def pos_entity_facing(
    entity_id: str,
    dis: float,
    use_0yaw: bool = False,
    height_offset: float = 0.0,
) -> Optional[Tuple[float, float, float]]: ...
def pos_forward_rot(
    pos: Tuple[float, float, float],
    rot: Tuple[float, float],
    dis: float,
) -> Optional[Tuple[float, float, float]]: ...
def n_quantiles_index_list(n: int, data: Union[tuple, list, set]) -> List[int]: ...
def cube_center(
    start_pos: Tuple[float, float, float],
    end_pos: Tuple[float, float, float],
) -> Optional[Tuple[float, float, float]]: ...
def cube_longest_side_len(
    start_pos: Tuple[float, float, float],
    end_pos: Tuple[float, float, float],
) -> float: ...
def is_in_sector(
    test_pos: Tuple[float, float, float],
    vertex_pos: Tuple[float, float, float],
    radius: float,
    sector_angle: float,
    sector_bisector_angle: float,
) -> bool: ...
def sphere_pos_list(
    center_pos: Tuple[float, float, float],
    radius: float,
    density: int,
) -> List[Tuple[float, float, float]]: ...
def cube_pos_list(
    pos1: Tuple[float, float, float],
    pos2: Tuple[float, float, float],
    step: int = 1,
) -> List[Tuple[float, float, float]]: ...
def spiral_pos_list(
    start_pos: Tuple[float, float, float],
    iterations: int,
) -> List[Tuple[float, float, float]]: ...
def is_in_cube(
    obj: Union[str, Tuple[float, float, float]],
    pos1: Tuple[float, float, float],
    pos2: Tuple[float, float, float],
    ignore_y: bool = False,
) -> bool: ...
def rot_diff(r1: float, r2: float) -> float: ...
def ray_aabb_intersection(
    ray_start_pos: Tuple[float, float, float],
    ray_dir: Tuple[float, float, float],
    length: float,
    cube_center_pos: Tuple[float, float, float],
    cube_size: Tuple[float, float, float],
) -> Optional[Tuple[float, float, float]]: ...
def get_blocks_by_ray(
    start_pos: Tuple[float, float, float],
    direction: Tuple[float, float, float],
    length: float,
    dimension: int = 0,
    count: int = 0,
    filter_blocks: Optional[List[str]] = None,
) -> List[Dict[str, Union[str, int, tuple]]]: ...
