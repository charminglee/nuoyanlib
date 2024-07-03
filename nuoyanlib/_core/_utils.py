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
#   Last Modified : 2024-07-02
#
# ====================================================


from ._const import (
    SHORTCUT as _SHORTCUT,
    INV27 as _INV27,
    INV36 as _INV36,
)
from ..config import SYSTEM_BINDINGS as _SYSTEM_BINDINGS


__all__ = [
    "is_inv36_key",
    "is_inv27_key",
    "is_shortcut_key",
    "is_inv_key",
    "is_not_inv_key",
    "get_opposite_system",
]


def is_inv36_key(k):
    return k.endswith(_INV36)


def is_inv27_key(k):
    return k.endswith(_INV27)


def is_shortcut_key(k):
    return k.endswith(_SHORTCUT)


def is_inv_key(k):
    return is_inv36_key(k) or is_inv27_key(k) or is_shortcut_key(k)


def is_not_inv_key(k):
    return not is_inv_key(k)


def get_opposite_system(sys_name):
    for sys1, sys2 in _SYSTEM_BINDINGS:
        if sys1 == sys_name:
            return sys2
        if sys2 == sys_name:
            return sys1







