# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-18
#  ⠀
# =================================================


from functools import wraps
from .._utils import get_arg_names
from ... import config


if config.ENABLED_TYPE_CHECKING:
    def args_type_check(*types):
        types = tuple(
            t if type(t) is tuple else (t,)
            for t in types
        )

        def decorator(func):
            arg_names = get_arg_names(func)
            is_method = arg_names and arg_names[0] == "self"

            @wraps(func)
            def wrapper(*args, **kwargs):
                for i, arg in enumerate(args):
                    if is_method and i == 0:
                        continue
                    if is_method:
                        i -= 1
                    if i >= len(types):
                        break
                    typ = callable if callable(arg) else type(arg)
                    expect_types = types[i]
                    if typ not in expect_types:
                        raise TypeError(
                            "argument %d must be %s, not %s"
                            % (i + 1, "/".join(t.__name__ for t in expect_types), typ.__name__)
                        )
                return func(*args, **kwargs)

            return wrapper
        return decorator

else:
    def args_type_check(*types):
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
    assert_error(test, (1, [], (3,)), exc=TypeError)
    @args_type_check((int, callable))
    def test2(a):
        return True
    assert test2(1)
    assert test2(test)
    assert_error(test2, ("",), exc=TypeError)










