# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-05-20
#
# ====================================================


from functools import wraps as _wraps
from . import _const


def param_type_check(*typ):
    def decorator(func):
        @_wraps(func)
        def wrapper(*args):
            for i, a in enumerate(args):
                if type(a) is not typ[i]:
                    raise TypeError(
                        "The %dth parameter of '%s' should be %s, got %s."
                        % (i + 1, func.__name__, typ[i].__name__, type(a).__name__)
                    )
            func(*args)
        return wrapper
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







