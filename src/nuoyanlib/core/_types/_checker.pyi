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


from typing import Tuple, Callable, Union
from ._typing import _F


def args_type_check(
    *types: Union[type, Tuple[type, ...]],
    is_method: bool = False,
) -> Callable[[_F], _F]: ...
