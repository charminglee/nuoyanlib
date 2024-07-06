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
#   Last Modified : 2024-07-06
#
# ====================================================


import mod.client.extraClientApi as _client_api
from .._const import (
    LIB_NAME as _LIB_NAME,
    LIB_CLIENT_NAME as _LIB_CLIENT_NAME,
)
from ._comp import (
    PLAYER_ID as _PLAYER_ID,
    ClientSystem as _ClientSystem,
    CompFactory as _CompFactory,
    LvComp as _LvComp,
)
from ._listener import (
    listen_custom as _listen_custom,
    event as _event,
    lib_sys_event as _lib_sys_event,
)
from .._utils import (
    is_not_inv_key as _is_not_inv_key,
)
from .._sys import (
    NuoyanLibBaseSystem as _NuoyanLibBaseSystem,
)
from .._logging import log as _log


__all__ = [
    "NuoyanLibClientSystem",
    "get_lib_system",
]


class NuoyanLibClientSystem(_NuoyanLibBaseSystem, _ClientSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibClientSystem, self).__init__(namespace, system_name)
        self.item_grid_path = {}
        self.item_grid_size = {}
        self.item_grid_items = {}
        self.registered_keys = {}
        _LvComp.Game.AddTimer(0, _listen_custom, self)
        _log("Inited", NuoyanLibClientSystem)

    # General ==========================================================================================================

    @_event("UiInitFinished")
    def _on_ui_init_finished(self, args):
        self.NotifyToServer("UiInitFinished", {})

    @_lib_sys_event("_SetQueryCache")
    def _on_set_query_cache(self, args):
        for entity_id, queries in args.items():
            for name, value in queries.items():
                comp = _CompFactory.CreateQueryVariable(entity_id)
                if comp.Get(name) == -1.0:
                    comp.Register(name, 0.0)
                comp.Set(name, value)

    @_lib_sys_event("_SetQueryVar")
    def on_set_query_var(self, args):
        if args.get('__id__') == _PLAYER_ID:
            return
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        comp = _CompFactory.CreateQueryVariable(entity_id)
        if comp.Get(name) == -1.0:
            comp.Register(name, 0.0)
        comp.Set(name, value)

    # Item Grid ========================================================================================================

    @_lib_sys_event("_UpdateItemGrids")
    def _on_update_item_grids(self, args):
        data = args['data']
        self.item_grid_items.update(data)
        _log("Updated item grids: %s" % data.keys(), NuoyanLibClientSystem)

    def register_item_grid(self, key, cls_path, path, size, is_single):
        if key in self.item_grid_path:
            _log("Register item grid failed: key '%s' already exists" % key, level="ERROR")
            return False
        self.registered_keys.setdefault(cls_path, []).append(key)
        self.item_grid_path[key] = (path, is_single)
        self.item_grid_size[key] = size
        if _is_not_inv_key(key):
            self.item_grid_items[key] = [None] * size
            self.NotifyToServer("_RegisterItemGrid", {'key': key, 'size': size})
        return True


_lib_sys = None


def get_lib_system():
    global _lib_sys
    if not _lib_sys:
        _lib_sys = _client_api.GetSystem(_LIB_NAME, _LIB_CLIENT_NAME)
    if not _lib_sys:
        _log("Get client lib system failed!", level="ERROR")
    return _lib_sys



















