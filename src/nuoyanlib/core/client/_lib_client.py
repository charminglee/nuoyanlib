# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


from collections import defaultdict
import itertools
import random
import mod.client.extraClientApi as c_api
from mod.client.system.clientSystem import ClientSystem
from ... import config
from ...common.time_ease import TimeEase
from .. import _const, _logging
from ..system import NuoyanLibBaseSystem
from .comp import CF, LvComp


class NuoyanLibClientSystem(NuoyanLibBaseSystem, ClientSystem):
    _instance = None

    def __init__(self, namespace, system_name):
        ClientSystem.__init__(self, namespace, system_name)
        NuoyanLibBaseSystem.__init__(self)
        NuoyanLibClientSystem._instance = self
        self.unsync_query = []
        self.callback_data = {}
        self.gse_data = {}
        self.gse_counter = itertools.count()

        ns, sys_name = c_api.GetEngineNamespace(), c_api.GetEngineSystemName()
        self.native_listen(ns, sys_name, "AddEntityClientEvent", self.AddEntityClientEvent)
        self.native_listen(ns, sys_name, "RemoveEntityClientEvent", self.RemoveEntityClientEvent)
        self.native_listen(ns, sys_name, "UiInitFinished", self.UiInitFinished)
        if config.GSE_USE_RENDER_TICK:
            self.native_listen(ns, sys_name, "GameRenderTickEvent", self.GameRenderTickEvent)

        ns, sys_name_c, sys_name_s = _env.LIB_NAME, _env.LIB_CLIENT_NAME, _env.LIB_SERVER_NAME
        self.native_listen(ns, sys_name_s, "_SetQueryVar", self._SetQueryVar)
        self.native_listen(ns, sys_name_c, "_NuoyanLibCall", self._NuoyanLibCall)
        self.native_listen(ns, sys_name_s, "_NuoyanLibCall", self._NuoyanLibCall)
        self.native_listen(ns, sys_name_c, "_NuoyanLibCallReturn", self._NuoyanLibCallReturn)
        self.native_listen(ns, sys_name_s, "_NuoyanLibCallReturn", self._NuoyanLibCallReturn)
        self.native_listen(ns, sys_name_s, "_NuoyanLibVisualizeArea", self._NuoyanLibVisualizeArea)

        if not config.ENABLED_MODSDK_LOG:
            _logging.disable_modsdk_loggers()
        _logging.info("NuoyanLibClientSystem inited")

    def Destroy(self):
        NuoyanLibBaseSystem.Destroy(self)
        from ..listener import unlisten_all_events
        for _, system in _env.CLIENT_SYSTEMS.items():
            unlisten_all_events(system)

    # region Events ====================================================================================================

    def AddEntityClientEvent(self, args):
        if args['engineTypeStr'] == _shared.GSE_IDENTIFIER:
            entity_id = args['id']
            cf = CF(entity_id)
            self.gse_data[entity_id] = {
                'inited': False,
                'attr_comp': cf.ModAttr,
                'render_comp': cf.ActorRender,
                'te': None,
                'geo_name': None,
                'pos': (args['posX'], args['posY'], args['posZ']),
            }

    def RemoveEntityClientEvent(self, args):
        entity_id = args['id']
        if entity_id in CF._cache:
            del CF._cache[entity_id]
        if entity_id in self.gse_data:
            del self.gse_data[entity_id]

    def UiInitFinished(self, args):
        self.NotifyToServer("UiInitFinished", {})

    if config.GSE_USE_RENDER_TICK:
        def GameRenderTickEvent(self, args):
            self._on_gse_update()
    else:
        def Update(self):
            self._on_gse_update()

    # endregion

    # region Broadcast =================================================================================================

    def broadcast_to_all_client(
            self,
            event_name,
            event_data,
            ns=_env.LIB_NAME,
            sys_name=_env.LIB_CLIENT_NAME,
    ):
        self.NotifyToServer("_BroadcastToAllClient", {
            'event_name': event_name,
            'event_data': event_data,
            'ns': ns,
            'sys_name': sys_name,
        })

    def notify_to_multi_clients(
            self,
            player_ids,
            event_name,
            event_data,
            ns=_env.LIB_NAME,
            sys_name=_env.LIB_CLIENT_NAME,
    ):
        if not player_ids:
            return
        self.NotifyToServer("_NotifyToMultiClients", {
            'player_ids': player_ids,
            'event_name': event_name,
            'event_data': event_data,
            'ns': ns,
            'sys_name': sys_name,
        })

    def notify_to_client(
            self,
            player_id,
            event_name,
            event_data,
            ns=_env.LIB_NAME,
            sys_name=_env.LIB_CLIENT_NAME,
    ):
        self.NotifyToServer("_NotifyToClient", {
            'player_id': player_id,
            'event_name': event_name,
            'event_data': event_data,
            'ns': ns,
            'sys_name': sys_name,
        })

    # endregion

    # region set_query_mod_var =========================================================================================

    def _SetQueryVar(self, args):
        for entity_id, query_list in args.items():
            comp = CF(entity_id).QueryVariable
            for name, value in query_list:
                if comp.Get(name) == -1.0:
                    comp.Register(name, 0.0)
                comp.Set(name, value)

    def set_query_mod_var(self, entity_id, name, value, sync):
        self.unsync_query.append((entity_id, name, value))

        comp = CF(entity_id).QueryVariable
        if comp.Get(name) == -1.0:
            comp.Register(name, 0.0)
        comp.Set(name, value)

        if sync:
            self.sync_query_mod_var()

    def sync_query_mod_var(self):
        args = defaultdict(list)
        while self.unsync_query:
            entity_id, name, value = self.unsync_query.pop()
            args[entity_id].append((name, value))
        if args:
            self.NotifyToServer("_SetQueryVar", args)

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
        if uuid:
            def callback(*cb_args):
                ret_args = {'uuid': uuid, 'cb_args': cb_args}
                if player_id:
                    self.notify_to_client(player_id, "_NuoyanLibCallReturn", ret_args)
                else:
                    self.NotifyToServer("_NuoyanLibCallReturn", ret_args)
        else:
            callback = None
        from ...common.communicate import _call_local
        _call_local(ns, sys_name, method, callback, delay_ret, call_args, call_kwargs)

    def _NuoyanLibCallReturn(self, args):
        uuid = args['uuid']
        cb_args = args['cb_args']
        from ...common.communicate import _call_callback
        _call_callback(uuid, -1, cb_args)

    # endregion

    # region spawn_ground_shatter_effect ===============================================================================

    def spawn_one_gse(self, pos, block, args):
        entity_id = self.CreateClientEntityByTypeStr(_shared.GSE_IDENTIFIER, pos, (0, 0))
        if entity_id:
            cf = CF(entity_id)
            cf.Model.SetEntityShadowShow(False)
            data = {
                'inited': False,
                'attr_comp': None,
                'render_comp': cf.ActorRender,
                'te': None,
                'geo_name': None,
                'pos': pos,
                'block': block,
            }
            data.update(args)
            self.gse_data[entity_id] = data
            self._init_gse(data)
        return entity_id

    def destroy_one_gse(self, entity_id):
        self.DestroyClientEntity(entity_id)
        self.gse_data.pop(entity_id, None)

    def _init_gse(self, data):
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
        geo_name = "nyl_gse_%d" % next(self.gse_counter)
        LvComp.BlockGeometry.CombineBlockPaletteToGeometry(palette, geo_name)
        tilt_angle = data['tilt_angle']
        rot = tuple(random.uniform(-tilt_angle, tilt_angle) for _ in range(3))
        data['render_comp'].AddActorBlockGeometry(geo_name, (0, -1.01, 0), rot)
        data['geo_name'] = geo_name

        final_height = random.uniform(data['min_height'], data['max_height'])
        out_te = TimeEase(
            final_height,
            final_height - data['out_dist'],
            data['out_time'],
            hold_on_last_frame=True,
            ease_func=data.get('out_ease', config.GSE_OUT_FUNC),
        )
        static_te = TimeEase.static(
            final_height,
            data['time'] - data['in_time'] - data['out_time'],
            next_te=out_te,
        )
        in_te = TimeEase(
            final_height - data['in_dist'],
            final_height,
            data['in_time'],
            ease_func=data.get('in_ease', config.GSE_IN_FUNC),
            next_te=static_te,
        )
        data['te'] = in_te

        data['inited'] = True
        self._update_gse_offset(data)

    def _update_gse_offset(self, data):
        y = next(data['te'])
        data['render_comp'].SetActorBlockGeometryOffset(data['geo_name'], (0, -1.01 + y, 0))

    def _on_gse_update(self):
        if not self.gse_data:
            return
        for data in self.gse_data.values():
            if data['inited']:
                self._update_gse_offset(data)
            elif data['attr_comp']:
                args = data['attr_comp'].GetAttr(_shared.GSE_ARGS)
                if args:
                    data.update(args)
                    self._init_gse(data)

    # endregion

    # region _visualize_area ===========================================================================================

    def _NuoyanLibVisualizeArea(self, args):
        # todo
        area_type = args['area_type']
        args = args['args']
        dim = args[0]
        if dim != LvComp.Game.GetCurrentDimension():
            return
        shape = None
        if area_type == "sphere":
            r, pos = args[1:]
            shape = LvComp.Drawing.AddSphereShape(pos, r)
        elif area_type == "cylinder":
            r, pos1, pos2 = args[1:]
        if shape:
            LvComp.Game.AddTimer(5, shape.Remove)

    # endregion


def instance():
    if not NuoyanLibClientSystem._instance:
        NuoyanLibClientSystem._instance = c_api.GetSystem(_env.LIB_NAME, _env.LIB_CLIENT_NAME)
    return NuoyanLibClientSystem._instance

















