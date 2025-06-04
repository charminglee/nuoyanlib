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


from typing import Callable, Any, Optional
from threading import Timer


class McTimer(object):
    type: str
    sec: float
    func: Optional[Callable]
    args: Any
    kwargs: Any
    _pause: bool
    _cancel: bool
    __timer: Optional[Timer]
    def __init__(self: ..., ttype: str, sec: float, func: Callable, *args: Any, **kwargs: Any): ...
    def _execute(self) -> Any: ...
    def __func(self) -> None: ...
    def Start(self) -> McTimer: ...
    def Cancel(self) -> None: ...
    def _release(self) -> None: ...
    def Pause(self, sec: Optional[float] = None) -> McTimer: ...
    def Continue(self) -> McTimer: ...
    def Execute(self) -> Any: ...
    def IsCanceled(self) -> bool: ...
    def IsPaused(self) -> bool: ...
