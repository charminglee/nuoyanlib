# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-13
|
| ==============================================
"""


import mod.server.extraServerApi as server_api
from .comp import ServerSystem
from .. import _const, _logging
from ..listener import ServerEventProxy
from .._sys import NuoyanLibBaseSystem
from .._utils import singleton
from ... import config


__all__ = []


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibServerSystem, self).__init__(namespace, system_name)
        self.__lib_flag__ = 0
        self.query_cache = {}
        self.callback_data = {}
        ln = _const.LIB_NAME
        lsn = _const.LIB_SERVER_NAME
        lcn = _const.LIB_CLIENT_NAME
        self.native_listen(ln, lcn, "_ButtonCallbackTrigger", self._ButtonCallbackTrigger)
        self.native_listen(ln, lcn, "_BroadcastToAllClient", self._BroadcastToAllClient)
        self.native_listen(ln, lcn, "_NotifyToMultiClients", self._NotifyToMultiClients)
        self.native_listen(ln, lcn, "_SetQueryVar", self._SetQueryVar)
        self.native_listen(ln, lcn, "_NuoyanLibCall", self._NuoyanLibCall)
        self.native_listen(ln, lcn, "_NuoyanLibCallReturn", self._NuoyanLibCallReturn)
        if config.ENABLED_MCP_MOD_LOG_DUMPING:
            server_api.SetMcpModLogCanPostDump(True)
        _logging.info(
            "NuoyanLibServerSystem inited (ver: %s, script: %s)"
            % (_const.__version__, self.__class__.__module__.split(".")[0])
        )

    @classmethod
    def register(cls):
        system = server_api.GetSystem(_const.LIB_NAME, _const.LIB_SERVER_NAME)
        if not system:
            path = cls.__module__ + "." + cls.__name__
            server_api.RegisterSystem(_const.LIB_NAME, _const.LIB_SERVER_NAME, path)
            system = server_api.GetSystem(_const.LIB_NAME, _const.LIB_SERVER_NAME)
        return system

    def get_lib_dict(self):
        from ... import server
        return server.__dict__

    # General ==========================================================================================================

    def _ButtonCallbackTrigger(self, args):
        func_name = args['name']
        func_args = args['args']
        func_args['__id__'] = args['__id__']
        func = getattr(self, func_name, None)
        if func:
            func(func_args)

    def UiInitFinished(self, args):
        if self.query_cache:
            self.NotifyToClient(args.__id__, "_SetQueryCache", self.query_cache)

    # BroadcastToAllClient =============================================================================================

    def _BroadcastToAllClient(self, args):
        event_name = args['event_name']
        event_data = args['event_data']
        ns = args['ns']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        ServerSystem(ns, sys_name).BroadcastToAllClient(event_name, event_data)

    # NotifyToMultiClients =============================================================================================

    def _NotifyToMultiClients(self, args):
        player_ids = args['player_ids']
        event_name = args['event_name']
        event_data = args['event_data']
        ns = args['ns']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        ServerSystem(ns, sys_name).NotifyToMultiClients(player_ids, event_name, event_data)

    # set_query_mod_var ================================================================================================

    def _SetQueryVar(self, args):
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        self.query_cache.setdefault(entity_id, {})[name] = value
        self.BroadcastToAllClient("_SetQueryVar", args)

    # call =============================================================================================================

    def _NuoyanLibCall(self, args):
        ns = args['ns']
        sys_name = args['sys_name']
        method = args['method']
        delay_ret = args['delay_ret']
        call_args = args['args']
        call_kwargs = args['kwargs']
        uuid = args['uuid']
        playerId = args['__id__']
        target_sys = server_api.GetSystem(ns, sys_name)
        def callback(cb_args):
            ret_args = {'uuid': uuid, 'cb_args': cb_args, 'method': method}
            self.NotifyToClient(playerId, "_NuoyanLibCallReturn", ret_args)
        from ...utils.communicate import call_local
        call_local(target_sys, method, callback, delay_ret, call_args, call_kwargs)

    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        method = args['method']
        from ...utils.communicate import call_callback
        call_callback(uuid, **cb_args)


def instance():
    if not NuoyanLibServerSystem.__instance__:
        NuoyanLibServerSystem.__instance__ = server_api.GetSystem(_const.LIB_NAME, _const.LIB_SERVER_NAME)
    return NuoyanLibServerSystem.__instance__




















