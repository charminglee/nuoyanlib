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


from collections import defaultdict
import mod.server.extraServerApi as s_api
from .. import _const, _logging
from .._utils import singleton
from .._sys import NuoyanLibBaseSystem, load_extensions
from ..listener import ServerEventProxy, _lib_sys_event
from .comp import ServerSystem, CF


@singleton
class NuoyanLibServerSystem(ServerEventProxy, NuoyanLibBaseSystem, ServerSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibServerSystem, self).__init__(namespace, system_name)
        self.query_cache = defaultdict(dict)
        self.unsync_query = []
        self.callback_data = {}
        _logging.info("NuoyanLibServerSystem inited")

    # region Events ====================================================================================================

    def EntityRemoveEvent(self, args):
        entity_id = args.id
        if entity_id in CF._cache:
            del CF._cache[entity_id]

    def UiInitFinished(self, args):
        player_id = args.__id__
        if self.query_cache:
            query_args = {
                eid: query_dict.items()
                for eid, query_dict in self.query_cache.items()
            }
            self.NotifyToClient(player_id, "_SetQueryVar", query_args)
        self.sync_all(player_id)

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
        player_id = args['__id__']
        del args['__id__']

        for entity_id, query_list in args.items():
            for name, value in query_list:
                self.query_cache[entity_id][name] = value

        players = s_api.GetPlayerList()
        players.remove(player_id)
        self.NotifyToMultiClients(players, "_SetQueryVar", args)

    def set_query_mod_var(self, entity_id, name, value, sync):
        self.unsync_query.append((entity_id, name, value))
        if sync:
            self.sync_query_mod_var()

    def sync_query_mod_var(self):
        args = defaultdict(list)
        while self.unsync_query:
            entity_id, name, value = self.unsync_query.pop()
            args[entity_id].append((name, value))
            self.query_cache[entity_id][name] = value
        if args:
            self.BroadcastToAllClient("_SetQueryVar", args)

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
    if not NuoyanLibServerSystem._instance:
        NuoyanLibServerSystem._instance = s_api.GetSystem(_const.LIB_NAME, _const.LIB_SERVER_NAME)
    return NuoyanLibServerSystem._instance




















