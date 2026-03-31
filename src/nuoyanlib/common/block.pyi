# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-28
#  ⠀
# =================================================


from typing import overload, Set
from ..core._types._typing import ITuple3


_AIR_BLOCKS: Set[str]
@overload
def is_air(pos: ITuple3, dim: int) -> bool: ...
@overload
def is_air(pos: ITuple3) -> bool: ...
