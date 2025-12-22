# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


if 0:
    from typing import Any
    from mod.client.system.clientSystem import ClientSystem
    from mod.server.system.serverSystem import ServerSystem


import traceback
from uuid import uuid4
import mod.client.extraClientApi as c_api
from ..core._sys import get_api, is_client, get_lv_comp, get_lib_system
from ..core.error import SystemNotFoundError


__all__ = [
    "Caller",
    "broadcast_to_all_systems",
    "call",
]


# todo
class Caller(object):
    def __init__(self, ns, sys_name, method=""):
        self.ns = ns
        self.sys_name = sys_name
        self.method = method

    def __call__(self, args=None, kwargs=None, method="", player_id=None, callback=None, delay_ret=-1):
        method = method or self.method
        return call(self.ns, self.sys_name, method, args, kwargs, player_id, callback, delay_ret)


# todo
def call_func(func_path, args=None, kwargs=None, callback=None, delay_ret=-1):
    pass


def broadcast_to_all_systems(event_name, event_args, from_system):
    """
    广播事件到所有系统，包括服务端和所有玩家的客户端。

    注：监听该事件时使用 ``from_system`` 的命名空间和系统名称即可。

    -----

    :param str event_name: 事件名
    :param Any event_args: 事件参数
    :param ClientSystem|ServerSystem from_system: 事件来源系统的实例

    :return: 无
    :rtype: None

    :raise SystemNotFoundError: from_system不存在时抛出
    """
    if is_client():
        get_lib_system(True).broadcast_to_all_client(
            event_name, event_args, from_system.namespace, from_system.systemName
        )
        from_system.NotifyToServer(event_name, event_args)
    else:
        from_system.BroadcastToAllClient(event_name, event_args)
        from_system.BroadcastEvent(event_name, event_args)


def _call_callback(cb_or_uuid, delay_ret, cb_args):
    lib_sys = get_lib_system()
    if isinstance(cb_or_uuid, str):
        data = lib_sys.callback_data[cb_or_uuid]
        callback = data['callback']
        data['count'] -= 1
        if data['count'] <= 0:
            del lib_sys.callback_data[cb_or_uuid]
    else:
        callback = cb_or_uuid
    if delay_ret >= 0:
        get_lv_comp().Game.AddTimer(delay_ret, callback, *cb_args)
    else:
        callback(*cb_args)


def _call_local(ns, sys_name, method, cb_or_uuid, delay_ret, args, kwargs):
    target_sys = get_api().GetSystem(ns, sys_name)
    if not target_sys:
        raise SystemNotFoundError(ns, sys_name)

    try:
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        ret = getattr(target_sys, method)(*args, **kwargs)
        success = True
    except:
        ret = None
        success = False
        traceback.print_exc()

    if cb_or_uuid:
        if is_client():
            cb_args = (success, ret, c_api.GetLocalPlayerId())
        else:
            cb_args = (success, ret)
        _call_callback(cb_or_uuid, delay_ret, cb_args)


def _call_remote(ns, sys_name, method, player_id, callback, delay_ret, args, kwargs):
    lib_sys = get_lib_system()
    if callback:
        uuid = uuid4().hex
        lib_sys.callback_data[uuid] = {'callback': callback, 'count': len(player_id) if player_id else 1}
    else:
        uuid = None
    notify_args = {
        'ns': ns,
        'sys_name': sys_name,
        'method': method,
        'uuid': uuid,
        'delay_ret': delay_ret,
        'args': args,
        'kwargs': kwargs,
    }
    if is_client():
        if player_id:
            lib_sys.notify_to_multi_clients(player_id, "_NuoyanLibCall", notify_args)
        else:
            lib_sys.NotifyToServer("_NuoyanLibCall", notify_args)
    else:
        if len(player_id) == 1:
            lib_sys.NotifyToClient(player_id[0], "_NuoyanLibCall", notify_args)
        else:
            lib_sys.NotifyToMultiClients(player_id, "_NuoyanLibCall", notify_args)


def call(ns, sys_name, method, args=None, kwargs=None, player_id=None, callback=None, delay_ret=-1):
    """
    调用指定客户端或服务端系统的函数，可以通过回调函数获取调用结果。

    回调函数的三个参数说明如下：

    - ``success`` -- bool，表示调用是否成功
    - ``ret`` -- 被调用函数的返回值
    - ``player_id`` -- str，仅当调用客户端时存在该参数，表示触发回调函数的玩家实体ID

    -----

    :param str ns: 被调用函数所在系统的命名空间
    :param str sys_name: 被调用函数所在系统的名称
    :param str method: 被调用函数名
    :param tuple args: 位置参数元组，展开后传入被调用函数；默认为None
    :param dict[str,Any] kwargs: 关键字参数字典，展开后传入被调用函数；默认为None
    :param str|list[str]|None player_id: 调用客户端时，需指定玩家实体ID；传入玩家实体ID/玩家实体ID列表表示单个/多个玩家，传入"*"（星号）表示所有玩家；调用服务端时忽略该参数即可
    :param function|None callback: 回调函数，参数说明见上方；默认为None
    :param float delay_ret: 延迟返回时间，单位为秒；若设置了该值，则callback触发前会延迟给定时间；由于跨端调用本身存在不可避免的网络延迟，因此实际的延迟时间会大于此处给定的值；默认为-1，即无延迟

    :return: 无
    :rtype: None
    """
    api = get_api()
    if player_id == "*":
        player_id = api.GetPlayerList()
    elif isinstance(player_id, str):
        player_id = [player_id]
    elif isinstance(player_id, (list, tuple)):
        player_id = list(player_id)

    if is_client():
        # c2c
        if player_id:
            local_plr = api.GetLocalPlayerId()
            if local_plr in player_id:
                _call_local(ns, sys_name, method, callback, delay_ret, args, kwargs)
                player_id.remove(local_plr)
            if player_id:
                _call_remote(ns, sys_name, method, player_id, callback, delay_ret, args, kwargs)
        # c2s
        else:
            _call_remote(ns, sys_name, method, player_id, callback, delay_ret, args, kwargs)
    else:
        # s2c
        if player_id:
            _call_remote(ns, sys_name, method, player_id, callback, delay_ret, args, kwargs)
        # s2s
        else:
            _call_local(ns, sys_name, method, callback, delay_ret, args, kwargs)










