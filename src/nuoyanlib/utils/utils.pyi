# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


from typing import TypeVar, Sequence, Any, List, Callable, Tuple, Optional
from ..core._types._typing import FTuple2


_T_type = TypeVar("_T_type", bound=type)


def get_time() -> float: ...
def timeit(
    func: Callable,
    n: int = 100000,
    print_res: bool = False,
    args: Optional[Any] = None,
    kwargs: Optional[Any] = None,
) -> FTuple2: ...
def notify_error(player_id: Optional[str] = None) -> None: ...
def call_interval(interval: float) -> Callable: ...
def add_condition_to_func(cond: Callable[[], bool], func: Callable[[bool], Any], freq: int = 1) -> int: ...
def rm_condition_to_func(cond_id: int) -> bool: ...
def all_indexes(seq: Sequence, *elements: Any) -> List[int]: ...
def check_string(string: str, *check: str) -> bool: ...
def check_string2(string: str, *check: str) -> bool: ...
def turn_dict_value_to_tuple(orig_dict: dict) -> None: ...
def turn_list_to_tuple(lst: list) -> tuple: ...
def is_method_overridden(subclass: Any, father: Any, method: str) -> bool: ...
def translate_time(
    sec: int,
    separator: str = "",
    unit: Optional[Tuple[str, str, str]] = ("h", "m", "s"),
    zfill: bool = False,
) -> str: ...
