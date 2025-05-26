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
#   Last Modified : 2025-05-23
#
# ====================================================


import mod.server.extraServerApi as _server_api
from . import _comp
from .. import _listener, _sys, _utils, _logging, _const
from ...utils import communicate as _communicate


def instance():
    if not NuoyanLibServerSystem.instance:
        NuoyanLibServerSystem.instance = _server_api.GetSystem(_const.LIB_NAME, _const.LIB_SERVER_NAME)
    return NuoyanLibServerSystem.instance


@_utils.singleton
class NuoyanLibServerSystem(_sys.NuoyanLibBaseSystem, _listener.ServerEventProxy, _comp.ServerSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibServerSystem, self).__init__(namespace, system_name)
        self.query_cache = {}
        self.first_player_id = "-1"
        _logging.log("Inited, ver: %s" % _const.__version__, NuoyanLibServerSystem)

    # General ==========================================================================================================

    def AddServerPlayerEvent(self, args):
        player_id = args['id']
        if self.first_player_id == "-1":
            self.first_player_id = player_id

    @_listener.lib_sys_event
    def _ButtonCallbackTrigger(self, args):
        func_name = args['name']
        func_args = args['args']
        func_args['__id__'] = args['__id__']
        func = getattr(self, func_name, None)
        if func:
            func(func_args)

    def UiInitFinished(self, args):
        player_id = args['__id__']
        if self.query_cache:
            self.NotifyToClient(player_id, "_SetQueryCache", self.query_cache)

    # BroadcastToAllClient =============================================================================================

    @_listener.lib_sys_event
    def _BroadcastToAllClient(self, args):
        event_name = args['event_name']
        event_data = args['event_data']
        namespace = args['namespace']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        _comp.ServerSystem(namespace, sys_name).BroadcastToAllClient(event_name, event_data)

    # NotifyToMultiClients =============================================================================================

    @_listener.lib_sys_event
    def _NotifyToMultiClients(self, args):
        player_ids = args['player_ids']
        event_name = args['event_name']
        event_data = args['event_data']
        namespace = args['namespace']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        _comp.ServerSystem(namespace, sys_name).NotifyToMultiClients(player_ids, event_name, event_data)

    # set_query_mod_var ================================================================================================

    @_listener.lib_sys_event
    def _SetQueryVar(self, args):
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        self.query_cache.setdefault(entity_id, {})[name] = value
        self.BroadcastToAllClient("_SetQueryVar", args)

    # call =============================================================================================================

    @_listener.lib_sys_event
    def _NuoyanLibCall(self, args):
        namespace = args['namespace']
        system_name = args['system_name']
        method = args['method']
        delay_ret = args['delay_ret']
        call_args = args['args']
        call_kwargs = args['kwargs']
        uuid = args['uuid']
        playerId = args['__id__']
        target_sys = _server_api.GetSystem(namespace, system_name)
        def callback(cb_args):
            self.NotifyToClient(playerId, "_NuoyanLibCallReturn", {'uuid': uuid, 'cb_args': cb_args})
        _communicate.call_local(target_sys, method, callback, delay_ret, call_args, call_kwargs)

    @_listener.lib_sys_event
    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        _communicate.call_callback(uuid, **cb_args)





















