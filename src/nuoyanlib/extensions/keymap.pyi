# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-14
|
| ==============================================
"""


from typing import Callable, Optional, Any


def bind_key(
    key: int,
    on_up: Optional[Callable[[], Any]] = None,
    on_down: Optional[Callable[[], Any]] = None,
    cond: Optional[Callable[[], bool]] = None,
    multi_binding: bool = False,
) -> bool: ...
