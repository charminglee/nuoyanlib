# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-22
|
| ==============================================
"""


from typing import Tuple, Callable, Union


def args_type_check(
    *typ: Union[type, Tuple[type, ...]],
    is_method: bool = False,
) -> Callable[[Callable], Callable]: ...
