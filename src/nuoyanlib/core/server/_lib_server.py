# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-02
|
| ====================================================
"""


import mod.server.extraServerApi as s_api
from .. import _const, _logging
from .._utils import singleton
from .._sys import NuoyanLibBaseSystem
from ..listener import ServerEventProxy, _lib_sys_event
from .comp import ServerSystem
from ... import config


__all__ = []


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibServerSystem, self).__init__(namespace, system_name)
        self.query_cache = {}
        self.callback_data = {}
        if config.ENABLED_MCP_MOD_LOG_DUMPING:
            s_api.SetMcpModLogCanPostDump(True)
        _logging.info("NuoyanLibServerSystem inited")

    # region General ===================================================================================================

    @_lib_sys_event
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

    # def LoadServerAddonScriptsAfter(self, args):
    #     load_extensions()

    # endregion

    # region Broadcast =================================================================================================

    @_lib_sys_event
    def _BroadcastToAllClient(self, args):
        event_name = args['event_name']
        event_data = args['event_data']
        ns = args['ns']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        ServerSystem(ns, sys_name).BroadcastToAllClient(event_name, event_data)

    @_lib_sys_event
    def _NotifyToMultiClients(self, args):
        player_ids = args['player_ids']
        event_name = args['event_name']
        event_data = args['event_data']
        ns = args['ns']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        ServerSystem(ns, sys_name).NotifyToMultiClients(player_ids, event_name, event_data)

    @_lib_sys_event
    def _NotifyToClient(self, args):
        player_id = args['player_id']
        event_name = args['event_name']
        event_data = args['event_data']
        ns = args['ns']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        ServerSystem(ns, sys_name).NotifyToClient(player_id, event_name, event_data)

    # endregion

    # region set_query_mod_var =========================================================================================

    @_lib_sys_event
    def _SetQueryVar(self, args):
        player_id = args.get('__id__')
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        self.query_cache.setdefault(entity_id, {})[name] = value
        player_lst = s_api.GetPlayerList()
        if player_id:
            player_lst.remove(player_id)
        self.NotifyToMultiClients(player_lst, "_SetQueryVar", args)

    # endregion

    # region call ======================================================================================================

    @_lib_sys_event
    def _NuoyanLibCall(self, args):
        ns = args['ns']
        sys_name = args['sys_name']
        method = args['method']
        delay_ret = args['delay_ret']
        call_args = args['args']
        call_kwargs = args['kwargs']
        uuid = args['uuid']
        player_id = args['__id__']
        if uuid:
            def callback(*cb_args):
                ret_args = {'uuid': uuid, 'cb_args': cb_args}
                self.NotifyToClient(player_id, "_NuoyanLibCallReturn", ret_args)
        else:
            callback = None
        from ...utils.communicate import _call_local
        _call_local(ns, sys_name, method, callback, delay_ret, call_args, call_kwargs)

    @_lib_sys_event
    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        from ...utils.communicate import _call_callback
        _call_callback(uuid, -1, cb_args)

    # endregion


def instance():
    if not NuoyanLibServerSystem.__instance__:
        NuoyanLibServerSystem.__instance__ = s_api.GetSystem(_const.LIB_NAME, _const.LIB_SERVER_NAME)
    return NuoyanLibServerSystem.__instance__




















