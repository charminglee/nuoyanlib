# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-29
|
| ==============================================
"""


from typing import Union, Optional, List, Dict
from mod.common.minecraftEnum import Facing
from .._core._types._typing import FTuple2, FTuple3, FTuple, ITuple


def pos_distance_square(pos1: FTuple, pos2: FTuple) -> float: ...
def clamp(x: float, min_value: float, max_value: float) -> float: ...
def pos_block_facing(pos: FTuple3, face: int = Facing.North, dist: float = 1.0) -> Optional[FTuple3]: ...
def to_polar_coordinate(coordinate: FTuple2, rad: bool = False, origin: FTuple2 = (0, 0)) -> FTuple2: ...
def to_cartesian_coordinate(coordinate: FTuple2, rad: bool = False, origin: FTuple2 = (0, 0)) -> FTuple2: ...
def probability_true_i(n: int, d: int) -> bool: ...
def probability_true_f(f: float) -> bool: ...
def pos_distance_to_line(pos: FTuple3, line_pos1: FTuple3, line_pos2: FTuple3) -> float: ...
def pos_floor(pos: FTuple) -> ITuple: ...
def pos_distance(first_point: FTuple, second_point: FTuple) -> float: ...
def to_relative_pos(entity_pos1: FTuple3, entity_pos2: FTuple3) -> Optional[FTuple3]: ...
def to_screen_pos(
    entity_pos: FTuple3,
    center_pos: FTuple3,
    screen_size: int,
    max_distance: int,
    ui_size: int,
    player_rot: float,
) -> Optional[FTuple2]: ...
def pos_rotate(angle: float, pos: FTuple2) -> Optional[FTuple2]: ...
def midpoint(first_point: FTuple, second_point: FTuple) -> FTuple: ...
def camera_rot_p2p(pos1: FTuple3, pos2: FTuple3) -> Optional[FTuple2]: ...
def pos_entity_facing(
    entity_id: str,
    dis: float,
    use_0yaw: bool = False,
    height_offset: float = 0.0,
) -> Optional[FTuple3]: ...
def pos_forward_rot(pos: FTuple3, rot: FTuple2, dis: float) -> Optional[FTuple3]: ...
def n_quantiles_index_list(n: int, data: Union[tuple, list, set]) -> List[int]: ...
def cube_center(start_pos: FTuple3, end_pos: FTuple3) -> Optional[FTuple3]: ...
def cube_longest_side_len(start_pos: FTuple3, end_pos: FTuple3) -> float: ...
def is_in_sector(
    test_pos: FTuple3,
    vertex_pos: FTuple3,
    radius: float,
    sector_angle: float,
    sector_bisector_angle: float,
) -> bool: ...
def is_in_cube(obj: Union[str, FTuple3], pos1: FTuple3, pos2: FTuple3, ignore_y: bool = False) -> bool: ...
def rot_diff(r1: float, r2: float) -> float: ...
def ray_aabb_intersection(
    ray_start_pos: FTuple3,
    ray_dir: FTuple3,
    length: float,
    cube_center_pos: FTuple3,
    cube_size: FTuple3,
) -> Optional[FTuple3]: ...
def get_blocks_by_ray(
    start_pos: FTuple3,
    direction: FTuple3,
    length: float,
    dimension: int = 0,
    count: int = 0,
    filter_blocks: Optional[List[str]] = None,
) -> List[Dict[str, Union[str, int, tuple]]]: ...
