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


from functools import wraps
from . import _const


__all__ = [
    "try_exec",
    "iter_obj_attrs",
    "cached_property",
    "CachedObject",
    "hook_method",
    "cached_method",
    "cached_func",
    "singleton",
]


def try_exec(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except:
        import traceback
        traceback.print_exc()


def iter_obj_attrs(obj):
    for name in dir(obj):
        try:
            attr = getattr(obj, name)
        except AttributeError:
            continue
        yield attr


def get_func(cls, module, func):
    g = cls.__init__.__func__.__globals__
    m = join_chr(*module)
    f = join_chr(*func)
    try:
        return getattr(g[m], f)
    except (AttributeError, KeyError):
        return lambda *_, **__: None


def assert_error(func, args, *error):
    try:
        func(*args)
    except error:
        assert True
    except:
        assert False


class cached_property(object):
    def __init__(self, getter):
        self.getter = getter
        self.__doc__ = getattr(getter, '__doc__', "")

    def __get__(self, ins, cls):
        value = self.getter(ins)
        setattr(ins, self.getter.__name__, value)
        return value


def join_chr(*seq):
    return "".join(chr(i) for i in seq)


class _CachedObjectMeta(type):
    def __new__(metacls, name, bases, dct):
        cls = type.__new__(metacls, name, bases, dct)
        if name != "CachedObject":
            cls.__cache__ = {}
        return cls


class CachedObject(object):
    """
    ::

        class A(CachedObject):
            @classmethod
            def __cache_key__(cls, a, b, c):   # 自定义缓存key获取方式
                return a, c

            def __init__(self, a, b, c):
                ...
    """

    __metaclass__ = _CachedObjectMeta

    def __new__(cls, *args, **kwargs):
        key = cls.__cache_key__(*args, **kwargs)
        if key not in cls.__cache__:
            cls.__cache__[key] = object.__new__(cls)
        return cls.__cache__[key]

    @classmethod
    def __cache_key__(cls, *args, **kwargs):
        return args


def hook_method(org_method, my_method):
    ins = org_method.__self__
    org_name = org_method.__name__
    @wraps(org_method.__func__)
    def wrapper(self, *args, **kwargs):
        try_exec(my_method, *args, **kwargs)
        org_method(*args, **kwargs)
    from types import MethodType
    wrapper = MethodType(wrapper, ins)
    setattr(ins, org_name, wrapper)


def cached_method(method):
    cache_dct = {}
    @wraps(method)
    def wrapper(self, *args):
        if args in cache_dct:
            return cache_dct[args]
        ret = method(self, *args)
        if ret is not None:
            cache_dct[args] = ret
        return ret
    return wrapper


def cached_func(func):
    cache_dct = {}
    @wraps(func)
    def wrapper(*args):
        if args in cache_dct:
            return cache_dct[args]
        ret = func(*args)
        if ret is not None:
            cache_dct[args] = ret
        return ret
    return wrapper


def singleton(init_once=True):
    def decorator(cls):
        cls.__instance__ = None
        cls.__inited__ = False
        org_new = cls.__new__
        org_init = cls.__init__
        def new_new(*args, **kwargs):
            return cls.__instance__ or org_new(*args, **kwargs)
        def new_init(self, *args, **kwargs):
            if cls.__instance__ is None:
                cls.__instance__ = self
            if not cls.__inited__ or not _init_once:
                org_init(self, *args, **kwargs)
                cls.__inited__ = True
        cls.__new__ = staticmethod(new_new)
        cls.__init__ = new_init
        return cls
    if isinstance(init_once, bool):
        _init_once = init_once
        return decorator
    else:
        _init_once = False
        return decorator(init_once)


def is_inv36_key(k):
    return k.endswith(_const.INV36)


def is_inv27_key(k):
    return k.endswith(_const.INV27)


def is_shortcut_key(k):
    return k.endswith(_const.SHORTCUT)


def is_inv_key(k):
    return is_inv36_key(k) or is_inv27_key(k) or is_shortcut_key(k)


def is_not_inv_key(k):
    return not is_inv_key(k)


def __test__():
    a = [0]
    class T(object):
        @cached_property
        def prop1(self):
            a[0] += 1
            return "a" + "b"
        @cached_property
        def prop2(self):
            a[0] += 1
            return "c" + "d"
    t = T()
    assert t.prop1 == "ab"
    assert t.prop1 == "ab"
    assert t.prop2 == "cd"
    assert t.prop2 == "cd"
    assert a[0] == 2

    n = [0]
    @singleton(False)
    class A(object):
        def __init__(self):
            n[0] += 1
    a1 = A()
    a2 = A()
    assert a1 == a2
    assert n[0] == 2
    @singleton(True)
    class A(object):
        def __init__(self):
            n[0] += 1
    A()
    A()
    assert n[0] == 3









