# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-5
#  ⠀
#  ================================================


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


