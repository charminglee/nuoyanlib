# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


import mod.server.extraServerApi as server_api
from ._comp import ServerSystem
from .._const import LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH, __version__
from .._listener import ServerEventProxy, lib_sys_event
from .._sys import NuoyanLibBaseSystem
from .._logging import info
from .._utils import singleton
from ...utils.communicate import call_local, call_callback


def instance():
    if not NuoyanLibServerSystem.instance:
        NuoyanLibServerSystem.instance = server_api.GetSystem(LIB_NAME, LIB_SERVER_NAME)
    return NuoyanLibServerSystem.instance


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    @staticmethod
    def register():
        if not server_api.GetSystem(LIB_NAME, LIB_SERVER_NAME):
            server_api.RegisterSystem(LIB_NAME, LIB_SERVER_NAME, LIB_SERVER_PATH)

    def __init__(self, namespace, system_name):
        super(NuoyanLibServerSystem, self).__init__(namespace, system_name)
        self.query_cache = {}
        info("NuoyanLibServerSystem inited, ver: %s" % __version__)

    # General ==========================================================================================================

    @lib_sys_event
    def _ButtonCallbackTrigger(self, args):
        func_name = args['name']
        func_args = args['args']
        func_args['__id__'] = args['__id__']
        func = getattr(self, func_name, None)
        if func:
            func(func_args)

    def UiInitFinished(self, event):
        if self.query_cache:
            self.NotifyToClient(event.__id__, "_SetQueryCache", self.query_cache)

    # BroadcastToAllClient =============================================================================================

    @lib_sys_event
    def _BroadcastToAllClient(self, args):
        event_name = args['event_name']
        event_data = args['event_data']
        namespace = args['namespace']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        ServerSystem(namespace, sys_name).BroadcastToAllClient(event_name, event_data)

    # NotifyToMultiClients =============================================================================================

    @lib_sys_event
    def _NotifyToMultiClients(self, args):
        player_ids = args['player_ids']
        event_name = args['event_name']
        event_data = args['event_data']
        namespace = args['namespace']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        ServerSystem(namespace, sys_name).NotifyToMultiClients(player_ids, event_name, event_data)

    # set_query_mod_var ================================================================================================

    @lib_sys_event
    def _SetQueryVar(self, args):
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        self.query_cache.setdefault(entity_id, {})[name] = value
        self.BroadcastToAllClient("_SetQueryVar", args)

    # call =============================================================================================================

    @lib_sys_event
    def _NuoyanLibCall(self, args):
        namespace = args['namespace']
        system_name = args['system_name']
        method = args['method']
        delay_ret = args['delay_ret']
        call_args = args['args']
        call_kwargs = args['kwargs']
        uuid = args['uuid']
        playerId = args['__id__']
        target_sys = server_api.GetSystem(namespace, system_name)
        def callback(cb_args):
            self.NotifyToClient(playerId, "_NuoyanLibCallReturn", {'uuid': uuid, 'cb_args': cb_args})
        call_local(target_sys, method, callback, delay_ret, call_args, call_kwargs)

    @lib_sys_event
    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        call_callback(uuid, **cb_args)





















