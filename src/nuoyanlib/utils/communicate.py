# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-12
#  ⠀
# =================================================


import traceback
from uuid import uuid4
import mod.client.extraClientApi as c_api
from ..core._sys import get_api, is_client, get_lv_comp, get_lib_system
from ..core._utils import try_exec
from ..core.error import SystemNotFoundError


if 0:
    from typing import Any
    from mod.client.system.clientSystem import ClientSystem
    from mod.server.system.serverSystem import ServerSystem


__all__ = [
    "SyncData",
    "Caller",
    "broadcast_to_all_systems",
    "call",
]


class SyncData(object):
    """
    跨端同步数据类。

    实现了跨端数据同步逻辑，其中一端修改数据后，会自动且安全地同步至另一端。
    支持多人联机环境，开发者无需关注玩家加入/退出的情况。

    说明
    ----

    目前仅支持从服务端同步至客户端。

    数据键和数据按 MCP 进行隔离，因此不同 MCP 中的相同键名不会造成冲突。（MCP 指每个包含 ``modMain.py`` 脚本的文件夹所构成的代码模块）

    示例
    ----

    服务端使用 ``SyncData()`` 定义一个同步数据对象，并设置默认值 ``IsRaining()`` 。

    >>> class MyServerSystem(nyl.ServerEventProxy, nyl.ServerSystem):
    ...     def __init__(self, namespace, system_name):
    ...         super(MyServerSystem, self).__init__(namespace, system_name)
    ...         self.is_raining = nyl.SyncData("is_raining", nyl.LvComp.Weather.IsRaining())
    ...         # 若键名已存在，则抛出 KeyError
    ...         # self.is_raining2 = nyl.SyncData("is_raining")
    ...
    ...     def OnRainLevelChangeServerEvent(self, args):
    ...         # 下雨等级变化时，设置同步数据的值，并同步至客户端
    ...         # args.newLevel > 0 表示正在下雨
    ...         self.is_raining.set(args.newLevel > 0, True)
    ...

    客户端使用 ``SyncData.from_server()`` 定义一个绑定到服务端的同步数据对象，服务端设置数据值时，客户端会实时收到更新。

    >>> class MyClientSystem(nyl.ClientEventProxy, nyl.ClientSystem):
    ...     def __init__(self, namespace, system_name):
    ...         super(MyClientSystem, self).__init__(namespace, system_name)
    ...         self.is_raining = nyl.SyncData.from_server("is_raining", False, self.on_is_raining_update)
    ...         # 允许通过 .from_server() 定义多个相同键名的同步数据对象
    ...         # self.is_raining2 = nyl.SyncData.from_server("is_raining", False)
    ...
    ...     def on_is_raining_update(self, key, old_value, new_value):
    ...         # 收到服务端数据更新时触发
    ...         print "is_raining: %s -> %s" % (old_value, new_value)
    ...

    客户端/服务端获取 ``is_raining`` 的值。

    >>> self.is_raining.get() # 或 self.is_raining.value

    -----

    :param str key: 数据键名
    :param Any|None default: 数据默认值；默认为 None

    :raise KeyError: 键名冲突时抛出
    """

    __slots__ = ('key', 'value', '_flag', '_on_sync', '_player_id', '_is_dirty')

    F_SOURCE = -1
    F_FROM_CLIENT = 0
    F_FROM_SERVER = 1

    def __init__(self, key, default=None, **kwargs):
        self.key = key
        self.value = default
        self._flag = kwargs.get('flag', self.F_SOURCE)
        self._on_sync = kwargs.get('on_sync')
        self._player_id = kwargs.get('player_id')
        self._is_dirty = False
        get_lib_system().register_sd(self)

    @classmethod
    def from_client(cls, player_id, key, default=None, on_sync=None):
        """
        [类方法]

        创建一个跨端同步数据，同步自客户端。

        -----

        :param str player_id: 玩家实体ID
        :param str key: 数据键名
        :param Any|None default: 数据默认值；仅当客户端数据未创建时使用该默认值；默认为 None
        :param function|None on_sync: 收到客户端数据更新时触发的回调函数，该函数接受四个参数：player_id（玩家实体ID）、key（数据键名）、old_value（旧数据值）和 new_value（新数据值）；默认为 None

        :return: SyncData 对象
        :rtype: SyncData
        """
        # return cls(key, default, flag=cls.F_FROM_CLIENT, player_id=player_id, on_sync=on_sync) # noqa
        # todo

    @classmethod
    def from_server(cls, key, default=None, on_sync=None):
        """
        [类方法]

        创建一个跨端同步数据，同步自服务端。

        -----

        :param str key: 数据键名
        :param Any|None default: 数据默认值；仅当服务端数据未创建时使用该默认值；默认为 None
        :param function|None on_sync: 收到服务端数据更新时触发的回调函数，该函数接受三个参数：key（数据键名）、old_value（旧数据值）和 new_value（新数据值）；默认为 None

        :return: SyncData 对象
        :rtype: SyncData
        """
        return cls(key, default, flag=cls.F_FROM_SERVER, on_sync=on_sync) # noqa

    def __repr__(self):
        if self._flag == self.F_FROM_SERVER:
            return "SyncData.from_server(key=%r, value=%r)" % (self.key, self.value)
        elif self._flag == self.F_FROM_CLIENT:
            return "SyncData.from_client(player_id=%r, key=%r, value=%r)" % (self._player_id, self.key, self.value)
        else:
            return "SyncData(key=%r, value=%r)" % (self.key, self.value)

    def set(self, value, sync=False):
        """
        设置数据值。

        注意：由 ``.from_client()`` 或 ``.from_server()`` 创建的 ``SyncData`` 对象不支持设置。

        -----

        :param Any value: 数据值
        :param bool sync: 是否立即进行同步；默认为 False

        :return: 无
        :rtype: None

        :raise RuntimeError: 若 SyncData 对象由 .from_client() 或 .from_server() 创建，则抛出该异常
        """
        if self._flag == self.F_FROM_CLIENT:
            raise RuntimeError("cannot call .set() method on the SyncData object which created by .from_client()")
        if self._flag == self.F_FROM_SERVER:
            raise RuntimeError("cannot call .set() method on the SyncData object which created by .from_server()")
        if self.value == value:
            return
        self.value = value
        self._is_dirty = True
        if sync:
            self.sync()

    def get(self):
        """
        获取数据值。

        -----

        :return: 数据值
        :rtype: Any
        """
        return self.value

    def sync(self):
        """
        立即将数据同步至另一端。

        注意：由 ``.from_client()`` 或 ``.from_server()`` 创建的 ``SyncData`` 对象不支持同步。

        -----

        :return: 无
        :rtype: None

        :raise RuntimeError: 若 SyncData 对象由 .from_client() 或 .from_server() 创建，则抛出该异常
        """
        if self._flag == self.F_FROM_CLIENT:
            raise RuntimeError("cannot call .sync() method on the SyncData object which created by .from_client()")
        if self._flag == self.F_FROM_SERVER:
            raise RuntimeError("cannot call .sync() method on the SyncData object which created by .from_server()")
        get_lib_system().sync(self.key)
        self._is_dirty = False

    @staticmethod
    def sync_all():
        """
        [静态方法]

        立即将所有已创建的 ``SyncData`` 对象的数据同步至另一端。

        -----

        :return: 无
        :rtype: None
        """
        get_lib_system().sync_all()

    def _on_engine_sync(self, new_value):
        old_value = self.value
        self.value = new_value
        if self._on_sync:
            if self._flag == self.F_FROM_CLIENT:
                try_exec(self._on_sync, self._player_id, self.key, old_value, new_value)
            elif self._flag == self.F_FROM_SERVER:
                try_exec(self._on_sync, self.key, old_value, new_value)


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
    """
    if is_client():
        get_lib_system().broadcast_to_all_client(
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










