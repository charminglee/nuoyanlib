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


from typing import List
from .._core._types._typing import EntFilter


def get_entities_within_view(
    world_dist: float = 50,
    screen_dist: float = 100,
    ent_filter: EntFilter = None,
) -> List[str]: ...
