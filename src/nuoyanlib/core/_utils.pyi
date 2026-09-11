# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-9
#  ⠀
#  ================================================


from threading import local
import sys
from typing import TypeVar, Generic, Hashable, List, Callable, Any, Type, Union, Tuple, Optional, Generator, overload, Dict
from ._types._typing import ITuple, T, F, Args, Kwargs, STuple, T_co
from ._types._checker import args_type_check


__CallableT = TypeVar("__CallableT", bound=Callable)


if sys.version_info >= (3, 10):
    from typing import ParamSpec, Concatenate
    __P = ParamSpec("__P")
    __R_co = TypeVar("__R_co", covariant=True)
    class dualmethod(Generic[T, __P, __R_co]):
        func: Callable[Concatenate[T, __P], __R_co]
        def __init__(self, func: Callable[Concatenate[T, __P], __R_co]) -> None: ...
        def __get__(self, instance: Any, owner: Optional[Type[T]] = None) -> Callable[__P, __R_co]: ...
else:
    class dualmethod(object):
        func: Callable
        def __init__(self, func: Callable) -> None: ...
        def __get__(self, instance: T, owner: Optional[Type[T]] = None) -> Callable: ...


def get_arg_names(func: Callable) -> STuple: ...
def get_module(*args: int) -> Any: ...


class DefaultLocal(Generic[T]):
    _default_factory: Callable[[], T]
    _local: local
    def __init__(self, default_factory: Callable[[], T] = lambda: None) -> None: ...
    def __getattribute__(self, name: str) -> Union[T, Any]: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...


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


def _lru_key(args: Args, kwargs: Kwargs) -> Hashable: ...
class lru_cache(object):
    size: int
    full: bool
    root: List[list, list, Hashable, Any]
    hits: int
    misses: int
    @args_type_check(int)
    def __init__(self, size: int = 128) -> None: ...
    def __call__(self, func_or_cls: T) -> T: ...


class SingletonMeta(type):
    _instance: Optional[Any]
    def __new__(metacls: Type[T], name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> T: ...
    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T: ...
if sys.version_info <= (2, 7):
    class Singleton(object):
        __metaclass__ = SingletonMeta
        _instance: Optional[Any]
else:
    class Singleton(metaclass=SingletonMeta):
        _instance: Optional[Any]
class ArgsSingletonMeta(type):
    _instances: Dict[tuple, Any]
    _unhashable_instances: List[Tuple[tuple, Any]]
    def __call__(cls: Type[T], *args: Any, **kwargs: Any) -> T: ...
if sys.version_info <= (2, 7):
    class ArgsSingleton(object):
        __metaclass__ = ArgsSingletonMeta
        _instances: Dict[tuple, Any]
        _unhashable_instances: List[Tuple[tuple, Any]]
else:
    class ArgsSingleton(metaclass=ArgsSingletonMeta):
        _instances: Dict[tuple, Any]
        _unhashable_instances: List[Tuple[tuple, Any]]


if sys.version_info >= (3, 8):
    from functools import cached_property
    cached_property = cached_property
else:
    class cached_property(Generic[T_co]):
        func: Callable[[Any], T_co]
        attrname: str
        __doc__: Optional[str]
        def __init__(self, func: Callable[[Any], T_co]) -> None: ...
        @overload
        def __get__(self: T, instance: None, owner: Optional[type] = None) -> T: ...
        @overload
        def __get__(self, instance: object, owner: Optional[type] = None) -> T_co: ...
        def __set__(self, instance: object, value: T_co) -> None: ...


def kwargs_defaults(**kwargs: Any) -> Callable[[F], F]: ...
def try_exec(func: Callable, *args: Any, **kwargs: Any) -> Union[Any, Exception]: ...
def iter_obj_attrs(obj: Any) -> Generator[Any]: ...
def get_func(cls: type, module: ITuple, func: ITuple) -> Optional[Callable]: ...
def assert_error(
    func: Callable,
    args: Args = (),
    kwargs: Optional[Kwargs] = None,
    exc: Union[Type[Exception], Tuple[Type[Exception], ...]] = (),
) -> None: ...
def join_chr(*seq: int) -> str: ...
@overload
def hook_method(
    obj: object,
    func_name: str,
    before_hook: __CallableT,
    after_hook: __CallableT,
) -> __CallableT: ...
@overload
def hook_method(
    obj: object,
    func_name: str,
    before_hook: __CallableT,
    after_hook: None = None,
) -> __CallableT: ...
@overload
def hook_method(
    obj: object,
    func_name: str,
    *,
    after_hook: __CallableT,
) -> __CallableT: ...
@overload
def hook_method(
    obj: object,
    func_name: str,
) -> Callable: ...
# def is_inv36_key(k: str) -> bool: ...
# def is_inv27_key(k: str) -> bool: ...
# def is_shortcut_key(k: str) -> bool: ...
# def is_inv_key(k: str) -> bool: ...
# def is_not_inv_key(k: str) -> bool: ...
