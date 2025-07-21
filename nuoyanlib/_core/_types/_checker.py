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
from ... import config


__all__ = []


if config.ENABLED_TYPE_CHECKING:
    def args_type_check(*typ, **kwargs):
        is_method = kwargs.get('is_method', False)
        typ = tuple(
            (t if isinstance(t, tuple) else (t,))
            for t in typ
        )
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for i, a in enumerate(args):
                    if is_method and i == 0:
                        continue
                    idx = i - 1 if is_method else i
                    a_type = type(a)
                    expect_types = typ[idx]
                    if a_type not in expect_types:
                        types = "/".join(t.__name__ for t in expect_types)
                        raise TypeError(
                            "the %dth argument of %s() should be '%s', got '%s'"
                            % (i + 1, func.__name__, types, a_type.__name__)
                        )
                return func(*args, **kwargs)
            return wrapper
        return decorator
else:
    def args_type_check(*typ, **kwargs):
        def decorator(func):
            return func
        return decorator


def __test__():
    from .._utils import assert_error
    @args_type_check(int, (int, str), tuple)
    def test(a, b, c):
        return True
    assert test(1, 2, (3, 4))
    assert test(1, "2", (3, 4))
    assert_error(test, (1, [], (3, 4)), TypeError)










