# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-12-03
|
| ==============================================
"""


from types import MethodType
from typing import Hashable, List, _F, TypeVar, Callable, Any, Dict, Union, Tuple, Optional, _T, Generator, overload
from ._types._typing import ITuple
from ._types._checker import args_type_check


__T_type = TypeVar("__T_type", bound=type)


_KWARGS_MARK: Tuple[object]


def _lru_key(args: tuple, kwargs: dict) -> Hashable: ...


class lru_cache(object):
    size: int
    full: bool
    root: List[list, list, Hashable, Any]
    @args_type_check(int, is_method=True)
    def __init__(self: ..., size: int = 128) -> None: ...
    def __call__(self, func: _F) -> _F: ...


def client_api(func: _F) -> _F: ...
def server_api(func: _F) -> _F: ...
@overload
def singleton(init_once: bool = True) -> Callable[[__T_type], __T_type]: ...
@overload
def singleton(cls: __T_type, /) -> __T_type: ...


class cached_property(object):
    __doc__: Optional[str]
    getter: Callable[[Any], Any]
    def __init__(self: ..., getter: Callable[[Any], Any]) -> None: ...
    def __get__(self, ins: Any, cls: type) -> Any: ...


def kwargs_setter(**kwargs: Any) -> Callable[[_T], _T]: ...
def try_exec(func: Callable, *args: Any, **kwargs: Any) -> Union[Any, Exception]: ...
def iter_obj_attrs(obj: Any) -> Generator[Any]: ...
def get_func(cls: type, module: ITuple, func: ITuple) -> Optional[Callable]: ...
def assert_error(
    func: Callable,
    args: Tuple[Any, ...] = (),
    kwargs: Dict[str, Any] = None,
    exc: Union[Exception, Tuple[Exception, ...]] = (),
) -> None: ...
def join_chr(*seq: int) -> str: ...
def hook_method(org_method: MethodType, my_method: MethodType) -> None: ...
# def is_inv36_key(k: str) -> bool: ...
# def is_inv27_key(k: str) -> bool: ...
# def is_shortcut_key(k: str) -> bool: ...
# def is_inv_key(k: str) -> bool: ...
# def is_not_inv_key(k: str) -> bool: ...
