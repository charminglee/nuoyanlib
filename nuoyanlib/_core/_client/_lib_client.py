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
#   Last Modified : 2024-06-16
#
# ====================================================


import mod.client.extraClientApi as _client_api
from .._const import (
    LIB_NAME as _LIB_NAME,
    LIB_CLIENT_NAME as _LIB_CLIENT_NAME,
)
from _comp import (
    PLAYER_ID as _PLAYER_ID,
    ClientSystem as _ClientSystem,
    CompFactory as _CompFactory,
    LvComp as _LvComp,
)
from _listener import (
    listen_custom as _listen_custom,
    event as _event,
    listen_for_lib_sys as _listen_for_lib_sys,
)
from .._utils import (
    is_not_inv_key as _is_not_inv_key,
)


__all__ = [
    "NuoyanLibClientSystem",
    "get_lib_system",
]


class NuoyanLibClientSystem(_ClientSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibClientSystem, self).__init__(namespace, system_name)
        self.item_grid_path = {}
        self.item_grid_size = {}
        self.item_grid_items = {}
        self.registered_keys = {}
        self._auto_show_ui = {}
        self._ui_display_state = {}
        _LvComp.Game.AddTimer(0, _listen_custom, self)

    # General ==========================================================================================================

    @_event("UiInitFinished")
    def _on_ui_init_finished(self, args):
        self.NotifyToServer("UiInitFinished", {})

    @_event("OnScriptTickClient")
    def _on_script_tick(self):
        for ui, lst in self._auto_show_ui.items():
            cond, display_func = lst
            if not display_func:
                ui_node = _client_api.GetUI(*ui)
                if ui_node:
                    display_func = lst[1] = ui_node.SetScreenVisible
                else:
                    continue
            to_display = bool(cond())
            state = self._ui_display_state[ui]
            if to_display != state:
                display_func(to_display)
                self._ui_display_state[ui] = to_display

    @_listen_for_lib_sys("_SetQueryCache")
    def _on_set_query_cache(self, args):
        for entity_id, queries in args.items():
            for name, value in queries.items():
                comp = _CompFactory.CreateQueryVariable(entity_id)
                if comp.Get(name) == -1.0:
                    comp.Register(name, 0.0)
                comp.Set(name, value)

    @_listen_for_lib_sys("_SetQueryVar")
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

    def register_auto_show_ui(self, namespace, ui_key, cond, display_func):
        key = (namespace, ui_key)
        self._auto_show_ui[key] = [cond, display_func]
        self._ui_display_state.setdefault(key, None)

    # Item Grid ========================================================================================================

    @_listen_for_lib_sys("_UpdateItemGrids")
    def _on_update_item_grids(self, args):
        data = args['data']
        self.item_grid_items.update(data)

    def register_item_grid(self, key, cls_path, path, size, is_single):
        if key in self.item_grid_path:
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
    return _lib_sys
















