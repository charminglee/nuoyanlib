# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


from nuoyanlib.core._types._checker import args_type_check
from nuoyanlib.core._utils import assert_error


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
