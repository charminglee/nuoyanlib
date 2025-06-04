# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from uuid import uuid4 as _uuid4
from traceback import format_exc as _format_exc
from .._core import _sys


__all__ = [
    "Caller",
    "call",
    "broadcast_to_all_systems"
]


# todo
class Caller(object):
    def __init__(self, namespace, system_name, method=""):
        self.namespace = namespace
        self.system_name = system_name
        self.method = method

    def __call__(self, args=None, kwargs=None, method="", player_id=None, callback=None, delay_ret=-1):
        method = method or self.method
        return call(self.namespace, self.system_name, method, args, kwargs, player_id, callback, delay_ret)


# todo
def call_func(func_path, args=None, kwargs=None, callback=None, delay_ret=-1):
    pass


def broadcast_to_all_systems(event_name, event_args, from_system):
    """
    | 广播事件到所有系统，包括服务端和所有玩家的客户端。
    | 监听该事件时使用 ``from_system`` 的命名空间和系统名称即可。

    -----

    :param str event_name: 事件名
    :param Any event_args: 事件参数
    :param ClientSystem|ServerSystem|tuple[str,str] from_system: 事件来源系统，可传入系统实例或元组：(命名空间, 系统名称)

    :return: 无
    :rtype: None
    """
    api = _sys.get_api()
    if _sys.is_client():
        from .._core._client._lib_client import instance
        lib_sys = instance()
        if isinstance(from_system, tuple):
            lib_sys.broadcast_to_all_client(event_name, event_args, *from_system)
            from_system = api.GetSystem(*from_system)
            if not from_system:
                from mod.client.system.clientSystem import ClientSystem
                from_system = ClientSystem(*from_system)
        else:
            lib_sys.broadcast_to_all_client(
                event_name, event_args, from_system.namespace, from_system.systemName # NOQA
            )
        from_system.NotifyToServer(event_name, event_args)
    else:
        if isinstance(from_system, tuple):
            from_system = api.GetSystem(*from_system)
            if not from_system:
                from mod.server.system.serverSystem import ServerSystem
                from_system = ServerSystem(*from_system)
        from_system.BroadcastToAllClient(event_name, event_args)
        from_system.BroadcastEvent(event_name, event_args)


_callback_data = {}


def call_callback(cb_or_uuid, delay_ret=-1, success=True, ret=None, error="", player_id=""):
    if isinstance(cb_or_uuid, str):
        data = _callback_data[cb_or_uuid]
        callback = data['callback']
        data['count'] -= 1
        if data['count'] <= 0:
            del _callback_data[cb_or_uuid]
    else:
        callback = cb_or_uuid
    if not callback:
        return
    cb_args = {'success': success, 'ret': ret, 'error': error, 'player_id': player_id}
    if delay_ret >= 0:
        _sys.get_comp_factory().CreateGame(_sys.LEVEL_ID).AddTimer(delay_ret, callback, cb_args)
    else:
        callback(cb_args)


def call_local(target_sys, method, cb_or_uuid, delay_ret, args, kwargs):
    player_id = _sys.get_api().GetLocalPlayerId() if _sys.is_client() else ""
    if not target_sys:
        call_callback(cb_or_uuid, delay_ret, False, player_id=player_id)
    else:
        try:
            if args is None:
                args = ()
            if kwargs is None:
                kwargs = {}
            ret = getattr(target_sys, method)(*args, **kwargs)
        except:
            call_callback(cb_or_uuid, delay_ret, False, error=_format_exc(), player_id=player_id)
        else:
            call_callback(cb_or_uuid, delay_ret, True, ret, player_id=player_id)


def _notify(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs):
    uuid = str(_uuid4())
    notify_args = {
        'namespace': namespace,
        'system_name': system_name,
        'method': method,
        'uuid': uuid,
        'delay_ret': delay_ret,
        'args': args,
        'kwargs': kwargs,
    }
    _callback_data[uuid] = {'callback': callback, 'count': len(player_id) if player_id else 1}
    if _sys.is_client():
        from .._core._client._lib_client import instance
        lib_sys = instance()
        if player_id is None:
            lib_sys.NotifyToServer("_NuoyanLibCall", notify_args)
        else:
            lib_sys.notify_to_multi_clients(player_id, "_NuoyanLibCall", notify_args)
    else:
        from .._core._server._lib_server import instance
        instance().NotifyToMultiClients(player_id, "_NuoyanLibCall", notify_args)


def call(
        namespace,
        system_name,
        method,
        args=None,
        kwargs=None,
        player_id=None,
        callback=None,
        delay_ret=-1,
):
    """
    | 调用指定客户端或服务端系统的函数，可以通过回调函数获取被调用函数的返回值。
    | 回调函数的参数字典说明如下：
    - ``success`` -- bool，表示调用是否成功
    - ``ret`` -- 被调用函数的返回值
    - ``error`` -- str，若调用时出现异常，异常信息将通过该参数给出
    - ``player_id`` -- str，调用客户端时，该参数表示该客户端的玩家实体ID
    | 由于ModSDK接口限制，跨端调用时，被调用函数返回的数据类型和传入被调用函数的参数的类型仅支持python基本数据类型（str，int，float，list，tuple，dict）。

    -----

    :param str namespace: 被调用函数所在系统的命名空间
    :param str system_name: 被调用函数所在系统的名称
    :param str method: 被调用函数名
    :param tuple args: 位置参数元组，展开后传入被调用函数中
    :param dict[str,Any] kwargs: 关键字参数字典，展开后传入被调用函数中
    :param str|list[str]|None player_id: 当被调用方为客户端时，可以指定玩家实体ID，传入玩家实体ID列表即可指定多个玩家，或用单字符"*"表示所有玩家；默认为None，表示被调用方为服务端
    :param function|None callback: 回调函数，默认为None；接受一个带有四个参数的字典，参数说明见上方
    :param float delay_ret: 延迟返回时间，单位为秒，若设置了该值，则callback触发前会延迟给定时间；但由于跨端调用本身存在不可避免的网络延迟，实际的延迟时间会大于此处给定的值；默认为-1，即无延迟

    :return: 无
    :rtype: None
    """
    api = _sys.get_api()
    target_sys = api.GetSystem(namespace, system_name)
    if player_id == "*":
        player_id = api.GetPlayerList()
    elif isinstance(player_id, str):
        player_id = [player_id]
    elif isinstance(player_id, list):
        player_id = player_id[:]
    if _sys.is_client():
        # c to s
        if not target_sys and not player_id:
            _notify(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs)
        # c to c
        else:
            local_plr = api.GetLocalPlayerId()
            if local_plr in player_id:
                call_local(target_sys, method, callback, delay_ret, args, kwargs)
                player_id.remove(local_plr)
            if player_id:
                _notify(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs)
    else:
        # s to s
        if target_sys:
            call_local(target_sys, method, callback, delay_ret, args, kwargs)
        elif not player_id:
            call_callback(callback, delay_ret, False)
        # s to c
        else:
            _notify(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs)










