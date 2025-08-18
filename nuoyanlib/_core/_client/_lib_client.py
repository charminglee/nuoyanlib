# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-19
|
| ==============================================
"""


from random import uniform
import mod.client.extraClientApi as client_api
from .comp import ClientSystem, CF, PLAYER_ID, LvComp
from .. import _const, _logging
from ..listener import ClientEventProxy
from .._sys import NuoyanLibBaseSystem, load_extensions
from .._utils import singleton
from ... import config
from ...utils.time_ease import TimeEase


__all__ = []


@singleton
class NuoyanLibClientSystem(ClientEventProxy, NuoyanLibBaseSystem, ClientSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibClientSystem, self).__init__(namespace, system_name)
        self.__lib_flag__ = 0
        self.callback_data = {}
        self._ground_shatter_data = {}
        ln = _const.LIB_NAME
        lsn = _const.LIB_SERVER_NAME
        lcn = _const.LIB_CLIENT_NAME
        self.native_listen(ln, lsn, "_SetQueryCache", self._SetQueryCache)
        self.native_listen(ln, lsn, "_SetQueryVar", self._SetQueryVar)
        self.native_listen(ln, lcn, "_NuoyanLibCall", self._NuoyanLibCall)
        self.native_listen(ln, lsn, "_NuoyanLibCall", self._NuoyanLibCall)
        self.native_listen(ln, lcn, "_NuoyanLibCallReturn", self._NuoyanLibCallReturn)
        self.native_listen(ln, lsn, "_NuoyanLibCallReturn", self._NuoyanLibCallReturn)
        if config.DISABLED_MODSDK_LOG:
            _logging.disable_modsdk_loggers()
        if config.ENABLED_MCP_MOD_LOG_DUMPING:
            client_api.SetMcpModLogCanPostDump(True)
        _logging.info("NuoyanLibClientSystem inited")

    @classmethod
    def register(cls):
        system = client_api.GetSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME)
        if not system:
            path = cls.__module__ + "." + cls.__name__
            client_api.RegisterSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME, path)
            system = client_api.GetSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME)
        return system

    def get_lib_dict(self):
        from ... import client
        return client.__dict__

    # region General ===================================================================================================

    if config.GSE_USE_RENDER_TICK:
        def GameRenderTickEvent(self, args):
            self._update_ground_shatter_effect()
    else:
        def Update(self):
            NuoyanLibBaseSystem.Update(self)
            self._update_ground_shatter_effect()

    def UiInitFinished(self, args):
        self.NotifyToServer("UiInitFinished", {})

    def LoadClientAddonScriptsAfter(self, args):
        load_extensions()

    def broadcast_to_all_client(self, event_name, event_data, ns="", sys_name=""):
        if not ns:
            ns = _const.LIB_NAME
        if not sys_name:
            sys_name = _const.LIB_CLIENT_NAME
        self.NotifyToServer("_BroadcastToAllClient", {
            'event_name': event_name,
            'event_data': event_data,
            'ns': ns,
            'sys_name': sys_name,
        })

    def notify_to_multi_clients(self, player_ids, event_name, event_data, ns="", sys_name=""):
        if not ns:
            ns = _const.LIB_NAME
        if not sys_name:
            sys_name = _const.LIB_CLIENT_NAME
        self.NotifyToServer("_NotifyToMultiClients", {
            'player_ids': player_ids,
            'event_name': event_name,
            'event_data': event_data,
            'ns': ns,
            'sys_name': sys_name,
        })

    # endregion

    # region set_query_mod_var =========================================================================================

    def _SetQueryCache(self, args):
        for entity_id, queries in args.items():
            comp = CF(entity_id).QueryVariable
            for name, value in queries.items():
                if comp.Get(name) == -1.0:
                    comp.Register(name, 0.0)
                comp.Set(name, value)

    def _SetQueryVar(self, args):
        if args.get('__id__') == PLAYER_ID:
            return
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        comp = CF(entity_id).QueryVariable
        if comp.Get(name) == -1.0:
            comp.Register(name, 0.0)
        comp.Set(name, value)

    # endregion

    # region call ======================================================================================================

    def _NuoyanLibCall(self, args):
        ns = args['ns']
        sys_name = args['sys_name']
        method = args['method']
        uuid = args['uuid']
        delay_ret = args['delay_ret']
        call_args = args['args']
        call_kwargs = args['kwargs']
        player_id = args.get('__id__')
        target_sys = client_api.GetSystem(ns, sys_name)
        def callback(cb_args):
            ret_args = {'uuid': uuid, 'cb_args': cb_args, 'method': method}
            if player_id:
                self.notify_to_multi_clients([player_id], "_NuoyanLibCallReturn", ret_args)
            else:
                self.NotifyToServer("_NuoyanLibCallReturn", ret_args)
        from ...utils.communicate import call_local
        call_local(target_sys, method, callback, delay_ret, call_args, call_kwargs)

    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        method = args['method']
        from ...utils.communicate import call_callback
        call_callback(uuid, **cb_args)

    # endregion

    # region spawn_ground_shatter_effect ===============================================================================

    def AddEntityClientEvent(self, args):
        if args.engineTypeStr == _const.TypeStr.GROUND_SHATTER_EFFECT:
            entity_id = args.id
            cf = CF(entity_id)
            self._ground_shatter_data[entity_id] = {
                'inited': False,
                'attr_comp': cf.ModAttr,
                'render_comp': cf.ActorRender,
                'te': None,
                'geo_name': None,
                'pos': (args.posX, args.posY, args.posZ),
            }

    def RemoveEntityClientEvent(self, args):
        entity_id = args.id
        if entity_id in self._ground_shatter_data:
            del self._ground_shatter_data[entity_id]

    def _init_ground_shatter_effect(self, data):
        palette = LvComp.Block.GetBlankBlockPalette()
        palette.DeserializeBlockPalette(
            {
                'extra': {},
                'void': False,
                'actor': {},
                'volume': (1, 1, 1),
                'common': {data['block']: [0]},
                'eliminateAir': True,
            }
        )
        geo_name = str(id(palette))
        LvComp.BlockGeometry.CombineBlockPaletteToGeometry(palette, geo_name)
        tilt_angle = data['tilt_angle']
        rot = tuple(uniform(-tilt_angle, tilt_angle) for _ in range(3))
        data['render_comp'].AddActorBlockGeometry(geo_name, (0, -1.01, 0), rot)
        data['geo_name'] = geo_name

        final_height = uniform(data['min_height'], data['max_height'])
        out_te = TimeEase(
            final_height,
            final_height - data['out_dist'],
            data['out_time'],
            hold_on_last_frame=True,
            ease_func=config.GSE_OUT_FUNC,
        )
        keep_te = TimeEase(
            final_height,
            final_height,
            data['time'] - data['in_time'] - data['out_time'],
            next_te=out_te,
        )
        in_te = TimeEase(
            final_height - data['in_dist'],
            final_height,
            data['in_time'],
            ease_func=config.GSE_IN_FUNC,
            next_te=keep_te,
        )
        data['te'] = in_te

    def _update_ground_shatter_effect(self):
        if not self._ground_shatter_data:
            return
        for data in self._ground_shatter_data.values():
            if not data['inited']:
                args = data['attr_comp'].GetAttr(_const.GSE_ATTR)
                if args:
                    data.update(args)
                    self._init_ground_shatter_effect(data)
                    data['inited'] = True
            if data['inited']:
                n = next(data['te'])
                data['render_comp'].SetActorBlockGeometryOffset(data['geo_name'], (0, -1.01 + n, 0))

    # endregion


def instance():
    if not NuoyanLibClientSystem.__instance__:
        NuoyanLibClientSystem.__instance__ = client_api.GetSystem(_const.LIB_NAME, _const.LIB_CLIENT_NAME)
    return NuoyanLibClientSystem.__instance__

















