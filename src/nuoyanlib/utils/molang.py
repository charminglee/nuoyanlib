# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-23
#  ⠀
# =================================================


from ..core._sys import get_lib_system


__all__ = [
    "set_query_mod_var",
]


def set_query_mod_var(entity_id, name, value, sync=True):
    """
    设置实体 ``query.mod`` 变量的值。

    将 ``sync`` 参数设为 ``True`` 可进行全局同步（即通过服务端广播给所有客户端设置变量的值），无需再手动实现同步逻辑。
    当 ``sync`` 为 ``True`` 时，会一次性将之前未同步的变量进行同步。因此若同时设置多个变量，只需在最后一次再将 ``sync`` 设为 ``True`` 。

    新玩家加入时，「nuoyanlib」会将所有设置过的变量的最新值同步给该玩家的客户端。

    说明
    ----

    若设置的变量未注册，会自动进行注册。

    -----

    :param str entity_id: 实体ID
    :param str name: 变量名
    :param float value: 设置的值
    :param bool sync: 是否进行全局同步；默认为 True

    :return: 无
    :rtype: None
    """
    get_lib_system().set_query_mod_var(entity_id, name, value, sync)














