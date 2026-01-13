# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


from threading import local
import sys
from types import MethodType
from typing import Generic, Hashable, List, Callable, Any, Dict, Type, Union, Tuple, Optional, Generator, overload
from ._types._typing import Self, ITuple, T, F, TypeT
from ._types._checker import args_type_check


VOID: object


class DefaultLocal(Generic[T]):
    _default_factory: Callable[[], T]
    _local: local
    def __init__(self: Self, default_factory: Callable[[], T] = lambda: None) -> None: ...
    def __getattribute__(self, name: str) -> Union[T, Any]: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...


def get_file_path(index: int = -2) -> str: ...
@overload
def parse_indices(index: slice, length: int, cls: type, op: Callable[[int], T]) -> List[T]: ...
@overload
def parse_indices(index: slice, length: int, cls: type) -> int: ...
@overload
def parse_indices(index: int, length: int, cls: type, op: Callable[[int], T]) -> T: ...
@overload
def parse_indices(index: int, length: int, cls: type) -> int: ...
@overload
def parse_indices_generator(index: Union[slice, int], length: int, cls: type, op: Callable[[int], T]) -> Generator[T]: ...
@overload
def parse_indices_generator(index: Union[slice, int], length: int, cls: type) -> Generator[int]: ...
def inject_is_client(func: F) -> F: ...


class __Universal(object):
    pass
UNIVERSAL_OBJECT: __Universal


def client_api(func: F) -> F: ...
def server_api(func: F) -> F: ...


if sys.version_info <= (2, 7):
    from types import DictProxyType
    MappingProxy = DictProxyType
else:
    from types import MappingProxyType
    MappingProxy = MappingProxyType


_KWARGS_MARK: Tuple[object]
def _lru_key(args: tuple, kwargs: dict) -> Hashable: ...


class lru_cache(object):
    size: int
    full: bool
    root: List[list, list, Hashable, Any]
    hits: int
    misses: int
    @args_type_check(int, is_method=True)
    def __init__(self: Self, size: int = 128) -> None: ...
    def __call__(self, func_or_cls: T) -> T: ...


@overload
def singleton(init_once: bool = True) -> Callable[[TypeT], TypeT]: ...
@overload
def singleton(init_once: TypeT) -> TypeT: ...


class cached_property(object):
    __doc__: Optional[str]
    getter: Callable[[Any], Any]
    def __init__(self: Self, getter: Callable[[Any], Any]) -> None: ...
    def __get__(self, ins: Any, cls: type) -> Any: ...


def kwargs_defaults(**kwargs: Any) -> Callable[[F], F]: ...
def try_exec(func: Callable, *args: Any, **kwargs: Any) -> Union[Any, Exception]: ...
def iter_obj_attrs(obj: Any) -> Generator[Any]: ...
def get_func(cls: type, module: ITuple, func: ITuple) -> Optional[Callable]: ...
def assert_error(
    func: Callable,
    args: Tuple[Any, ...] = (),
    kwargs: Dict[str, Any] = None,
    exc: Union[Type[Exception], Tuple[Type[Exception], ...]] = (),
) -> None: ...
def join_chr(*seq: int) -> str: ...
def hook_method(
    org_method: MethodType,
    before_hook: Optional[Callable] = None,
    after_hook: Optional[Callable] = None,
) -> None: ...
# def is_inv36_key(k: str) -> bool: ...
# def is_inv27_key(k: str) -> bool: ...
# def is_shortcut_key(k: str) -> bool: ...
# def is_inv_key(k: str) -> bool: ...
# def is_not_inv_key(k: str) -> bool: ...
