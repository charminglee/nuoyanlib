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


from operator import itemgetter as _itemgetter
from types import MethodType as _MethodType
from functools import wraps as _wraps
try:
    from . import _const
    from ..config import ENABLED_TYPE_CHECKING as _ENABLED_TYPE_CHECKING
except:
    _ENABLED_TYPE_CHECKING = True


class cache_property(object):
    def __init__(self, getter):
        self.getter = getter
        self.prop_name = getter.__name__
        self.cached_data = None

    def __get__(self, obj, typ=None):
        if not self.cached_data:
            self.cached_data = self.getter(obj)
        return self.cached_data

    def __set__(self, obj, value):
        raise AttributeError("can't set property '%s'" % self.prop_name)

    def __delete__(self, obj):
        raise AttributeError("can't delete property '%s'" % self.prop_name)


def join_chr(*seq):
    return "".join(chr(i) for i in seq)


class _CacheObjectMeta(type):
    def __new__(metacls, name, bases, dct):
        cls = type.__new__(metacls, name, bases, dct)
        if name != "CacheObject":
            cls.__cache__ = {}
        return cls


class CacheObject(object):
    __metaclass__ = _CacheObjectMeta
    __cache_key_idx__ = None

    def __new__(cls, *args):
        key = _itemgetter(cls.__cache_key_idx__)(args) if cls.__cache_key_idx__ else args
        if key not in cls.__cache__:
            cls.__cache__[key] = object.__new__(cls)
        return cls.__cache__[key]


def hook_method(ins, org_method_name, my_method):
    org_method = getattr(ins, org_method_name)
    @_wraps(org_method.__func__)
    def wrapper(self, *args, **kwargs):
        my_method(*args, **kwargs)
        org_method(*args, **kwargs)
    wrapper = _MethodType(wrapper, ins)
    setattr(ins, org_method_name, wrapper)


if _ENABLED_TYPE_CHECKING:
    def args_type_check(*typ, **kwargs):
        is_method = kwargs.get('is_method', False)
        typ = tuple(
            (t if isinstance(t, tuple) else (t,))
            for t in typ
        )
        def decorator(func):
            @_wraps(func)
            def wrapper(*args):
                for i, a in enumerate(args):
                    if is_method and i == 0:
                        continue
                    idx = i - 1 if is_method else i
                    if type(a) not in typ[idx]:
                        expect_type = "/".join(t.__name__ for t in typ[idx])
                        raise TypeError(
                            "the %dth argument of %s() should be %s, got %s"
                            % (i + 1, func.__name__, expect_type, type(a).__name__)
                        )
                return func(*args)
            return wrapper
        return decorator
else:
    def args_type_check(*typ, **kwargs):
        def decorator(func):
            return func
        return decorator


def method_cache(method):
    cache_dct = {}
    @_wraps(method)
    def wrapper(self, *args):
        if args in cache_dct:
            return cache_dct[args]
        ret = method(self, *args)
        if ret is not None:
            cache_dct[args] = ret
        return ret
    return wrapper


def func_cache(func):
    cache_dct = {}
    @_wraps(func)
    def wrapper(*args):
        if args in cache_dct:
            return cache_dct[args]
        ret = func(*args)
        if ret is not None:
            cache_dct[args] = ret
        return ret
    return wrapper


def singleton(cls):
    org_new = cls.__new__
    org_init = cls.__init__
    def new_new(*args, **kwargs):
        return cls.instance or org_new(*args, **kwargs)
    def new_init(self, *args, **kwargs):
        if cls.instance is None:
            cls.instance = self
        org_init(self, *args, **kwargs)
    cls.__new__ = staticmethod(new_new)
    cls.__init__ = new_init
    cls.instance = None
    return cls


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


if __name__ == "__main__":
    class T(object):
        @cache_property
        def prop1(self):
            print("prop1")
            return "a" + "b"
        @cache_property
        def prop2(self):
            print("prop2")
            return "c" + "d"
    t = T()
    print(t.prop1)
    print(t.prop1)
    print(t.prop2)
    print(t.prop2)
    # t.prop1 = 1
    # del t.prop1
    # @args_type_check(int, (int, str), tuple)
    # def test(a, b, c):
    #     return True
    # print test(1, 2, (3, 4))
    # print test(1, "2", (3, 4))
    # print test(1, [], (3, 4))









