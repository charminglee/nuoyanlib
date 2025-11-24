# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-24
|
| ====================================================
"""


from typing import List
from ..core._types._typing import EntFilter


def get_entities_within_view(
    world_dist: float = 50,
    screen_dist: float = 100,
    ent_filter: EntFilter = None,
) -> List[str]: ...
