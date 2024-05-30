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


import mod.server.extraServerApi as _server_api
from mod.common.minecraftEnum import (
    ItemPosType as _ItemPosType
)
from .._const import (
    LIB_NAME as _LIB_NAME,
    LIB_SERVER_NAME as _LIB_SERVER_NAME,
)
from _comp import (
    CompFactory as _CompFactory,
    ServerSystem as _ServerSystem,
    LvComp as _LvComp,
)
from _listener import (
    listen_custom as _listen_custom,
    listen_for_lib_sys as _listen_for_lib_sys,
)
from .._utils import (
    is_inv36_key as _is_inv36_key,
    is_inv27_key as _is_inv27_key,
    is_shortcut_key as _is_shortcut_key,
    is_inv_key as _is_inv_key,
    is_not_inv_key as _is_not_inv_key,
)
from ...utils.item import (
    is_empty_item as _is_empty_item,
    deepcopy_item_dict as _deepcopy_item_dict,
)


__all__ = [
    "NuoyanLibServerSystem",
    "get_lib_system",
]


_DATA_KEY_ITEMS_DATA = "_nuoyanlib_item_grid_data"
_INV_POS_TYPE = _ItemPosType.INVENTORY


class NuoyanLibServerSystem(_ServerSystem):
    def __init__(self, namespace, system_name):
        super(NuoyanLibServerSystem, self).__init__(namespace, system_name)
        self._query_cache = {}
        self._item_grid_items = _LvComp.ExtraData.GetExtraData(_DATA_KEY_ITEMS_DATA) or {}
        _LvComp.Game.AddTimer(0, _listen_custom, self)

    def Destroy(self):
        _LvComp.ExtraData.SetExtraData(_DATA_KEY_ITEMS_DATA, self._item_grid_items)

    # General ==========================================================================================================

    @_listen_for_lib_sys("_SetQueryVar")
    def on_set_query_var(self, args):
        entity_id = args['entity_id']
        name = args['name']
        value = args['value']
        self._query_cache.setdefault(entity_id, {})[name] = value
        self.BroadcastToAllClient("_SetQueryVar", args)

    @_listen_for_lib_sys("_BroadcastToAllClient")
    def _on_broadcast_to_all_client(self, args):
        event_name = args['event_name']
        event_data = args['event_data']
        namespace = args['namespace']
        sys_name = args['sys_name']
        if isinstance(event_data, dict) and '__id__' in args:
            event_data['__id__'] = args['__id__']
        _ServerSystem(namespace, sys_name).BroadcastToAllClient(event_name, event_data)

    @_listen_for_lib_sys("UiInitFinished")
    def _on_ui_init_finished(self, args):
        player_id = args['__id__']
        if self._query_cache:
            self.NotifyToClient(player_id, "_SetQueryCache", self._query_cache)

    # Item Grid ========================================================================================================

    @_listen_for_lib_sys("_RegisterItemGrid")
    def _on_register_item_grid(self, args):
        player_id = args['__id__']
        key = args['key']
        size = args['size']
        data = self._item_grid_items.setdefault(player_id, {})
        if key not in data:
            data[key] = [None] * size

    @_listen_for_lib_sys("_OnClientItemGridInitFinished")
    def _on_item_grid_init_finished(self, args):
        player_id = args['__id__']
        keys = args['keys']
        not_inv_keys = filter(_is_not_inv_key, keys)
        self.on_update_item_grids({'__id__': player_id, 'keys': not_inv_keys})

    @_listen_for_lib_sys("_UpdateItemGrids")
    def on_update_item_grids(self, args):
        player_id = args['__id__']
        keys = args['keys']
        if player_id not in self._item_grid_items:
            return False
        data = {
            key: items
            for key, items in self._item_grid_items[player_id].items()
            if key in keys
        }
        update_inv = filter(_is_inv_key, keys)
        self.NotifyToClient(player_id, "_UpdateItemGrids", {'data': data, 'update_inv': update_inv})
        return True

    @_listen_for_lib_sys("_ThrowItem")
    def _on_throw_item(self, args):
        player_id = args['__id__']
        del args['__id__']
        item_dict = args
        dim = _CompFactory.CreateDimension(player_id).GetEntityDimensionId()
        pos = _CompFactory.CreatePos(player_id).GetPos()
        if not pos:
            return
        item_ent = self.CreateEngineItemEntity(item_dict, dim, pos)
        if item_ent:
            rot = _CompFactory.CreateRot(player_id).GetRot()
            rot = (-15, rot[1])
            direction = _server_api.GetDirFromRot(rot)
            motion = tuple(i * 0.3 for i in direction)
            _CompFactory.CreateActorMotion(item_ent).SetMotion(motion)

    @_listen_for_lib_sys("_SyncItemOperation")
    def _on_sync_item_operation(self, args):
        player_id = args['__id__']
        op = args['op']
        op_args = args['args']
        getattr(self, "_" + op)(player_id, op_args)

    def _set_grid(self, player_id, args):
        key, item_dict_list = args
        self.set_all_items(player_id, key, item_dict_list)

    def _set_cell(self, player_id, args):
        pos, item_dict = args
        self.set_item(player_id, pos, item_dict)

    def _exchange(self, player_id, args):
        from_pos, to_pos = (from_key, from_index), (to_key, to_index) = args
        if _is_inv_key(from_key) and _is_inv_key(to_key):
            if _is_inv27_key(from_key):
                from_index += 9
            if _is_inv27_key(to_key):
                to_index += 9
            _CompFactory.CreateItem(player_id).SetInvItemExchange(from_index, to_index)
        else:
            from_item = self.get_item(player_id, from_pos)
            to_item = self.get_item(player_id, to_pos)
            self.set_item(player_id, [from_pos, to_pos], [to_item, from_item])

    def _move(self, player_id, args):
        from_pos, to_pos, count = args
        from_item = self.get_item(player_id, from_pos)
        to_item = _deepcopy_item_dict(from_item)
        from_item['count'] -= count
        to_item['count'] = count
        self.set_item(player_id, [from_pos, to_pos], [from_item, to_item])

    def _divide(self, player_id, args):
        from_item, from_pos, to_pos_list, override, to_count, remain_count = args
        pos_list = to_pos_list + [from_pos]
        to_item = _deepcopy_item_dict(from_item)
        to_item['count'] = to_count
        item_dict_list = [to_item] * len(to_pos_list)
        if remain_count >= 1:
            from_item['count'] = remain_count
            item_dict_list.append(from_item)
        else:
            item_dict_list.append(None)
        self.set_item(player_id, pos_list, item_dict_list)

    def _set_count(self, player_id, args):
        pos, _ = (key, index), count = args
        if _is_shortcut_key(key) or _is_inv36_key(key):
            _CompFactory.CreateItem(player_id).SetInvItemNum(index, count)
        elif _is_inv27_key(key):
            _CompFactory.CreateItem(player_id).SetInvItemNum(index + 9, count)
        else:
            item = self.get_item(player_id, pos)
            item['count'] = count
            self.set_item(player_id, pos, item)

    def _ret_items(self, player_id, args):
        keys = args[0]
        items_data = self._item_grid_items[player_id]
        for key, items in items_data.items():
            if key not in keys:
                continue
            for item in items:
                if _is_empty_item(item):
                    continue
                _LvComp.Item.SpawnItemToPlayerInv(item, player_id)
            items_data[key] = [None] * len(items_data[key])
        self.on_update_item_grids({'__id__': player_id, 'keys': keys})

    def set_all_items(self, player_id, key, item_dict_list, deepcopy=False):
        res = []
        for i, item_dict in enumerate(item_dict_list):
            pos = (key, i)
            if self._broadcast_item_grid_changed(player_id, pos, item_dict):
                res.append(False)
                continue
            res.append(self._set_item(player_id, pos, item_dict, deepcopy))
        self.on_update_item_grids({'__id__': player_id, 'keys': (key,)})
        return res

    def set_item(self, player_id, pos_list, item_dict_list, deepcopy=False):
        if not isinstance(pos_list, list):
            pos_list = [pos_list]
        if not isinstance(item_dict_list, list):
            item_dict_list = [item_dict_list]
        keys = tuple(pos[0] for pos in pos_list)
        cancel = False
        for pos, item_dict in zip(pos_list, item_dict_list):
            if self._broadcast_item_grid_changed(player_id, pos, item_dict):
                cancel = True
        if not cancel:
            for pos, item_dict in zip(pos_list, item_dict_list):
                self._set_item(player_id, pos, item_dict, deepcopy)
        self.on_update_item_grids({'__id__': player_id, 'keys': keys})
        return not cancel

    def _set_item(self, player_id, pos, item_dict, deepcopy=False):
        key, index = pos
        if _is_empty_item(item_dict):
            item_dict = None
        if _is_shortcut_key(key) or _is_inv36_key(key):
            res = _CompFactory.CreateItem(player_id).SetPlayerAllItems({(_INV_POS_TYPE, index): item_dict})
            return res.values()[0]
        elif _is_inv27_key(key):
            res = _CompFactory.CreateItem(player_id).SetPlayerAllItems({(_INV_POS_TYPE, index + 9): item_dict})
            return res.values()[0]
        else:
            if (
                    player_id not in self._item_grid_items
                    or key not in self._item_grid_items[player_id]
                    or index >= len(self._item_grid_items[player_id][key])
            ):
                return False
            if deepcopy:
                item_dict = _deepcopy_item_dict(item_dict)
            self._item_grid_items[player_id][key][index] = item_dict
            return True

    def _broadcast_item_grid_changed(self, player_id, pos, new_item):
        old_item = self.get_item(player_id, pos)
        args = {
            'player_id': player_id,
            'pos': pos,
            'old_item': old_item,
            'new_item': _deepcopy_item_dict(new_item),
            'cancel': False,
        }
        self.BroadcastEvent("ItemGridChangedServerEvent", args)
        return args['cancel']

    def get_all_items(self, player_id, key):
        comp = _CompFactory.CreateItem(player_id)
        if _is_inv36_key(key):
            items = comp.GetPlayerAllItems(_INV_POS_TYPE, True)
        elif _is_inv27_key(key):
            items = comp.GetPlayerAllItems(_INV_POS_TYPE, True)[9:]
        elif _is_shortcut_key(key):
            items = comp.GetPlayerAllItems(_INV_POS_TYPE, True)[:9]
        else:
            items = self._get_not_inv_items(player_id, key)
        return [None if _is_empty_item(i) else i for i in items] if items else []

    def get_item(self, player_id, pos):
        key, index = pos
        comp = _CompFactory.CreateItem(player_id)
        if _is_shortcut_key(key) or _is_inv36_key(key):
            item = comp.GetPlayerItem(_INV_POS_TYPE, index, True)
        elif _is_inv27_key(key):
            item = comp.GetPlayerItem(_INV_POS_TYPE, index + 9, True)
        else:
            item = self._get_not_inv_items(player_id, key, index)
        return None if _is_empty_item(item) else item

    def _get_not_inv_items(self, player_id, key, index=-1):
        if player_id not in self._item_grid_items or key not in self._item_grid_items[player_id]:
            return
        items = self._item_grid_items[player_id][key]
        if index == -1:
            return _deepcopy_item_dict(items)
        elif index < len(items):
            return _deepcopy_item_dict(items[index])


def get_lib_system():
    return _server_api.GetSystem(_LIB_NAME, _LIB_SERVER_NAME)


















