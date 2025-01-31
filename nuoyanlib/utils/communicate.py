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
#   Last Modified : 2025-01-26
#
# ====================================================


from uuid import uuid4 as _uuid4
from traceback import format_exc as _format_exc
from .._core._sys import (
    get_api as _get_api,
    is_client as _is_client,
    get_comp_factory as _get_comp_factory,
    LEVEL_ID as _LEVEL_ID,
)


__all__ = [
    "call_callback",
    "call_local",
    "call",
]


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
        _get_comp_factory().CreateGame(_LEVEL_ID).AddTimer(delay_ret, callback, cb_args)
    else:
        callback(cb_args)


def call_local(target_sys, method, cb_or_uuid, delay_ret, args, kwargs):
    player_id = _get_api().GetLocalPlayerId() if _is_client() else ""
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


def _notify_call(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs):
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
    if _is_client():
        from .._core._client._lib_client import get_lib_system
        lib_sys = get_lib_system()
        if player_id is None:
            lib_sys.NotifyToServer("_NuoyanLibCall", notify_args)
        else:
            lib_sys.notify_to_multi_clients(player_id, "_NuoyanLibCall", notify_args)
    else:
        from .._core._server._lib_server import get_lib_system
        get_lib_system().NotifyToMultiClients(player_id, "_NuoyanLibCall", notify_args)


def call(
        namespace,
        system_name,
        method,
        player_id=None,
        callback=None,
        delay_ret=-1,
        timeout=3.0, # todo
        args=None,
        kwargs=None,
):
    """
    | 调用指定客户端或服务端系统的函数，可以通过回调函数获取被调用函数的返回值。
    | 回调函数的参数字典说明如下：
    - ``success`` – bool，表示调用是否成功
    - ``ret`` – 被调用函数的返回值
    - ``error`` – str，若调用时出现异常，异常信息将通过该参数给出
    - ``player_id`` – str，调用客户端时，该参数表示该客户端的玩家实体ID
    | 由于ModSDK接口限制，跨端调用时，被调用函数返回的数据类型和传入被调用函数的参数的类型仅支持python基本数据类型（str，int，float，list，tuple，dict）。

    -----

    :param str namespace: 被调用函数所在系统的命名空间
    :param str system_name: 被调用函数所在系统的名称
    :param str method: 被调用函数名
    :param str|list[str]|None player_id: 当被调用方为客户端时，可以指定玩家实体ID，传入玩家实体ID列表即可指定多个玩家，或用单字符"*"表示所有玩家；默认为None，表示被调用方为服务端
    :param function|None callback: 回调函数，默认为None；接受一个带有三个参数的字典，参数说明见上方
    :param float delay_ret: 延迟返回时间，单位为秒，若设置了该值，则callback触发前会延迟给定时间；但由于跨端调用本身存在不可避免的网络延迟，实际的延迟时间会大于此处给定的值；默认为-1，即无延迟
    :param float timeout: 超时时间，单位为秒，若超时时间内未收到被调用函数的返回值，将判定为调用失败，默认为3.0
    :param tuple args: 位置参数元组，展开后传入被调用函数中
    :param dict[str,Any] kwargs: 关键字参数字典，展开后传入被调用函数中

    :return: 无
    :rtype: None
    """
    api = _get_api()
    target_sys = api.GetSystem(namespace, system_name)
    if player_id == "*":
        player_id = api.GetPlayerList()
    elif isinstance(player_id, str):
        player_id = [player_id]
    elif isinstance(player_id, list):
        player_id = player_id[:]
    if _is_client():
        # c to s
        if not target_sys and not player_id:
            _notify_call(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs)
        # c to c
        else:
            local_plr = api.GetLocalPlayerId()
            if local_plr in player_id:
                call_local(target_sys, method, callback, delay_ret, args, kwargs)
                player_id.remove(local_plr)
            if player_id:
                _notify_call(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs)
    else:
        # s to s
        if target_sys:
            call_local(target_sys, method, callback, delay_ret, args, kwargs)
        elif not player_id:
            call_callback(callback, delay_ret, False)
        # s to c
        else:
            _notify_call(namespace, system_name, method, player_id, callback, delay_ret, args, kwargs)










