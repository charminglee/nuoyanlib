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
#   Last Modified : 2024-05-31
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
    PlrComp as _PlrComp,
)
from _listener import (
    listen_custom as _listen_custom,
    listen_for as _listen_for,
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
        self._old_carried_item = ("minecraft:air", 0)
        _LvComp.Game.AddTimer(0, _listen_custom, self)

    # General ==========================================================================================================

    @_listen_for("UiInitFinished")
    def _on_ui_init_finished(self, args):
        self.NotifyToServer("UiInitFinished", {})
        _LvComp.Game.AddTimer(0, self._on_carried_item_changed, {'itemDict': _PlrComp.Item.GetCarriedItem()})

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

    # Auto Show Ui =====================================================================================================

    @_listen_for("OnCarriedNewItemChangedClientEvent")
    def _on_carried_item_changed(self, args):
        item_dict = args['itemDict']
        item_name = item_dict['newItemName'] if item_dict else "minecraft:air"
        item_aux = item_dict['newAuxValue'] if item_dict else 0
        item = (item_name, item_aux)
        self._set_ui_visible(self._old_carried_item, False)
        self._set_ui_visible(item, True)
        self._old_carried_item = item

    def _set_ui_visible(self, item, visible):
        name = item[0]
        func_list = []
        if item in self._auto_show_ui:
            func_list += self._auto_show_ui[item]
        if (name, -1) in self._auto_show_ui:
            func_list += self._auto_show_ui[(name, -1)]
        for func in func_list:
            func(visible)

    def register_auto_show_ui(self, item_name, ui_node=None, func=None, item_aux=-1):
        if not ui_node and not func:
            return False
        if item_name is None:
            item_name = "minecraft:air"
        if not func:
            func = getattr(ui_node, "SetScreenVisible", None)
        if not func:
            return False
        self._auto_show_ui.setdefault((item_name, item_aux), []).append(func)
        return True

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


def get_lib_system():
    return _client_api.GetSystem(_LIB_NAME, _LIB_CLIENT_NAME)
















