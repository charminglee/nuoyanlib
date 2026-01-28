# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-19
#  ⠀
# =================================================


from typing import Literal, TypeVar, Union, Any, Callable, Tuple, Optional, overload
from ..core._types._typing import FTuple2, ITuple3, FTuple3
from ..core._utils import singleton, lru_cache, cached_property, try_exec, iter_obj_attrs


__DictT = TypeVar("__DictT", bound=dict)


singleton = singleton
lru_cache = lru_cache
cached_property = cached_property
try_exec = try_exec
iter_obj_attrs = iter_obj_attrs


def rgb2hex(
    rgb_color: Union[FTuple3, ITuple3],
    mc_rgb: bool = True ,
    with_sign: bool = True,
    upper: bool = True,
) -> str: ...
@overload
def hex2rgb(hex_color: str, mc_rgb: Literal[True]) -> FTuple3: ...
@overload
def hex2rgb(hex_color: str) -> FTuple3: ...
@overload
def hex2rgb(hex_color: str, mc_rgb: Literal[False]) -> ITuple3: ...
@overload
def hex2rgb(hex_color: str, mc_rgb: bool = True) -> Union[FTuple3, ITuple3]: ...
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
def check_string(string: str, *check: str) -> bool: ...
def convert_dict_value_to_tuple(dct: __DictT) -> __DictT: ...
def convert_list_to_tuple(lst: list) -> tuple: ...
def translate_time(
    sec: int,
    separator: str = "",
    unit: Optional[Tuple[str, str, str]] = ("h", "m", "s"),
    zfill: bool = False,
) -> str: ...
