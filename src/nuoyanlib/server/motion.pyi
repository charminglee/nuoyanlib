# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-2-10
#  ⠀
# =================================================


from ..core._types._typing import FTuple3, FTuple2, TimeEaseFuncType
from ..common.enum import TimeEaseFunc


def set_motion(entity_id: str, motion: FTuple3) -> None: ...
def start_mover(entity_id: str, mover_id: int) -> None: ...
def move_entity(
    entity_id: str,
    direction: FTuple3,
    dist: float,
    time: float,
    is_throughable: bool = False,
    ease_func: TimeEaseFuncType = TimeEaseFunc.LINEAR,
) -> None: ...
def entity_plunge(entity_id1: str, entity_id2: str, speed: float) -> None: ...
def entity_plunge_by_dir(entity_id: str, direction: FTuple3, speed: float) -> None: ...
def entity_plunge_by_rot(entity_id: str, rot: FTuple2, speed: float) -> None: ...
