# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-24
|
| ==============================================
"""


from functools import wraps
from ... import config


__all__ = []


if config.ENABLED_TYPE_CHECKING:
    def args_type_check(*types, **kwargs):
        is_method = kwargs.get('is_method', False)
        types = tuple(
            (t if isinstance(t, tuple) else (t,))
            for t in types
        )
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **_kwargs):
                for i, arg in enumerate(args):
                    if is_method and i == 0:
                        continue
                    idx = i - 1 if is_method else i
                    if idx >= len(types):
                        break
                    typ = type(arg)
                    expect_types = types[idx]
                    if typ not in expect_types:
                        raise TypeError(
                            "argument %d must be %s, not %s"
                            % (i + 1, "/".join(t.__name__ for t in expect_types), typ.__name__)
                        )
                return func(*args, **_kwargs)
            return wrapper
        return decorator
else:
    def args_type_check(*types, **kwargs):
        def decorator(func):
            return func
        return decorator


def __test__():
    from .._utils import assert_error
    @args_type_check(int, (int, str), tuple)
    def test(a, b, c, d):
        return True
    assert test(1, 2, (3,), 114514)
    assert test(1, "2", (3,), 114514)
    assert_error(test, (1, [], (3,)), TypeError)










