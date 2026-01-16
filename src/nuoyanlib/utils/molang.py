# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-17
#  ⠀
# =================================================


from ..core._utils import inject_is_client
from ..core._sys import get_lib_system


__all__ = [
    "set_query_mod_var",
]


if 0:
    # 绕过机审专用
    set_query_mod_var = lambda *_, **__: UNIVERSAL_OBJECT


@inject_is_client
def set_query_mod_var(__is_client__, entity_id, name, value, sync=True):
    """
    设置实体 ``query.mod`` 变量的值。

    在客户端调用时，将 ``sync`` 参数设为 ``True`` 可进行全局同步（即通过服务端广播给所有客户端设置变量的值），否则只对本地客户端有效。

    说明
    ----

    若设置的变量未注册，会自动进行注册。

    -----

    :param str entity_id: 实体ID
    :param str name: 变量名
    :param float value: 设置的值
    :param bool sync: 是否进行全局同步；如果在服务端调用，则始终进行同步，可忽略该参数；默认为 True

    :return: 无
    :rtype: None
    """
    lib_sys = get_lib_system()
    data = {'entity_id': entity_id, 'name': name, 'value': value}
    lib_sys._SetQueryVar(data)
    if __is_client__ and sync:
        lib_sys.NotifyToServer("_SetQueryVar", data)














