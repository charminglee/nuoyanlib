# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-03-25
#  ⠀
# =================================================


from typing import Callable, Any, Optional, overload, Hashable
from ..core._types._typing import F
from ..core._utils import DefaultLocal


_timers: DefaultLocal[dict]


def _add_timer(
    t: float,
    is_repeat: bool,
    key: Optional[Hashable],
    func: Callable,
    *args: Any,
    **kwargs: Any,
) -> None: ...
@overload
def delay(t: float = 0, key: Optional[Hashable] = None) -> Callable[[F], F]: ...
@overload
def delay(t: F, key: Optional[Hashable] = None) -> F: ...
@overload
def repeat(t: float = 0, key: Optional[Hashable] = None, exec_now: bool = False) -> Callable[[F], F]: ...
@overload
def repeat(t: F, key: Optional[Hashable] = None, exec_now: bool = False) -> F: ...
