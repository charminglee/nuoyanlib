# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from typing import Optional
from .._core._types._typing import FTuple3


def play_custom_sound(
    sound_name: str,
    pos: FTuple3 = (0, 0, 0),
    volume: float = 1.0,
    speed: float = 1.0,
    is_loop: bool = False,
    entity_id: Optional[str] = None,
) -> str: ...
def stop_custom_sound(sound_id: str, fade_out_time: float = 0.0) -> bool: ...

















