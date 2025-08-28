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
#
#
# import mod.server.extraServerApi as _server_api
# from mod.common.minecraftEnum import (
#     ItemPosType as _ItemPosType
# )
# from ..server import (
#     CF as _CompFactory,
#     ServerSystem as _ServerSystem,
#     LvComp as _LvComp,
# )
# from .._core._logging import log as _log
# from ..utils import (
#     is_empty_item as _is_empty_item,
#     deepcopy_item_dict as _deepcopy_item_dict,
# )
# from .._core._utils import (
#     is_inv36_key as _is_inv36_key,
#     is_inv27_key as _is_inv27_key,
#     is_shortcut_key as _is_shortcut_key,
#     is_inv_key as _is_inv_key,
#     is_not_inv_key as _is_not_inv_key,
#     singleton as _singleton,
# )
# from .._core._listener import (
#     lib_sys_event as _lib_sys_event,
#     ServerEventProxy as _ServerEventProxy,
# )
#
#
# _DATA_KEY_ITEMS_DATA = "_nuoyanlib_item_grid_data"
# _INV_POS_TYPE = _ItemPosType.INVENTORY
#
#
# @_singleton
# class ItemGridServer(_ServerEventProxy, _ServerSystem):
#     def __init__(self, namespace, system_name):
#         super(ItemGridServer, self).__init__(namespace, system_name)
#         self.item_grid_items = _LvComp.ExtraData.GetExtraData(_DATA_KEY_ITEMS_DATA) or {}
#
#     def Destroy(self):
#         res = _LvComp.ExtraData.SetExtraData(_DATA_KEY_ITEMS_DATA, self.item_grid_items)
#         _log("Saved item grid data (%s)" % res, ItemGridServer, "INFO" if res else "ERROR")
#
#     @_lib_sys_event
#     def _RegisterItemGrid(self, args):
#         player_id = args['__id__']
#         key = args['key']
#         size = args['size']
#         data = self.item_grid_items.setdefault(player_id, {})
#         if key not in data:
#             data[key] = [None] * size
#
#     @_lib_sys_event
#     def _OnClientItemGridInitFinished(self, args):
#         player_id = args['__id__']
#         keys = args['keys']
#         not_inv_keys = filter(_is_not_inv_key, keys)
#         self._UpdateItemGrids({'__id__': player_id, 'keys': not_inv_keys})
#
#     @_lib_sys_event
#     def _UpdateItemGrids(self, args):
#         player_id = args['__id__']
#         keys = args['keys']
#         if player_id not in self.item_grid_items:
#             return False
#         data = {
#             key: items
#             for key, items in self.item_grid_items[player_id].items()
#             if key in keys
#         }
#         update_inv = filter(_is_inv_key, keys)
#         self.NotifyToClient(player_id, "_UpdateItemGrids", {'data': data, 'update_inv': update_inv})
#         return True
#
#     @_lib_sys_event
#     def _ThrowItem(self, args):
#         player_id = args['__id__']
#         del args['__id__']
#         item_dict = args
#         dim = _CompFactory.CreateDimension(player_id).GetEntityDimensionId()
#         pos = _CompFactory.CreatePos(player_id).GetPos()
#         if not pos:
#             return
#         item_ent = self.CreateEngineItemEntity(item_dict, dim, pos)
#         if item_ent:
#             rot = _CompFactory.CreateRot(player_id).GetRot()
#             rot = (-15, rot[1])
#             direction = _server_api.GetDirFromRot(rot)
#             motion = tuple(i * 0.3 for i in direction)
#             _CompFactory.CreateActorMotion(item_ent).SetMotion(motion)
#
#     @_lib_sys_event
#     def _SyncItemOperation(self, args):
#         player_id = args['__id__']
#         op = args['op']
#         op_args = args['args']
#         getattr(self, "_" + op)(player_id, op_args)
#
#     def _set_grid(self, player_id, args):
#         key, item_dict_list = args
#         self.set_all_items(player_id, key, item_dict_list)
#
#     def _set_cell(self, player_id, args):
#         pos, item_dict = args
#         self.set_item(player_id, pos, item_dict)
#
#     def _exchange(self, player_id, args):
#         from_pos, to_pos = (from_key, from_index), (to_key, to_index) = args
#         if _is_inv_key(from_key) and _is_inv_key(to_key):
#             if _is_inv27_key(from_key):
#                 from_index += 9
#             if _is_inv27_key(to_key):
#                 to_index += 9
#             _CompFactory.CreateItem(player_id).SetInvItemExchange(from_index, to_index)
#         else:
#             from_item = self.get_item(player_id, from_pos)
#             to_item = self.get_item(player_id, to_pos)
#             self.set_item(player_id, [from_pos, to_pos], [to_item, from_item])
#
#     def _move(self, player_id, args):
#         from_pos, to_pos, count = args
#         from_item = self.get_item(player_id, from_pos)
#         to_item = _deepcopy_item_dict(from_item)
#         from_item['count'] -= count
#         to_item['count'] = count
#         self.set_item(player_id, [from_pos, to_pos], [from_item, to_item])
#
#     def _divide(self, player_id, args):
#         from_item, from_pos, to_pos_list, override, to_count, remain_count = args
#         pos_list = to_pos_list + [from_pos]
#         to_item = _deepcopy_item_dict(from_item)
#         to_item['count'] = to_count
#         item_dict_list = [to_item] * len(to_pos_list)
#         if remain_count >= 1:
#             from_item['count'] = remain_count
#             item_dict_list.append(from_item)
#         else:
#             item_dict_list.append(None)
#         self.set_item(player_id, pos_list, item_dict_list)
#
#     def _set_count(self, player_id, args):
#         pos, _ = (key, index), count = args
#         if _is_shortcut_key(key) or _is_inv36_key(key):
#             _CompFactory.CreateItem(player_id).SetInvItemNum(index, count)
#         elif _is_inv27_key(key):
#             _CompFactory.CreateItem(player_id).SetInvItemNum(index + 9, count)
#         else:
#             item = self.get_item(player_id, pos)
#             item['count'] = count
#             self.set_item(player_id, pos, item)
#
#     def _ret_items(self, player_id, args):
#         keys = args[0]
#         items_data = self.item_grid_items[player_id]
#         for key, items in items_data.items():
#             if key not in keys:
#                 continue
#             for item in items:
#                 if _is_empty_item(item):
#                     continue
#                 _LvComp.Item.SpawnItemToPlayerInv(item, player_id)
#             items_data[key] = [None] * len(items_data[key])
#         self._UpdateItemGrids({'__id__': player_id, 'keys': keys})
#
#     def set_all_items(self, player_id, key, item_dict_list, deepcopy=False):
#         res = []
#         for i, item_dict in enumerate(item_dict_list):
#             pos = (key, i)
#             if self._broadcast_item_grid_changed(player_id, pos, item_dict):
#                 res.append(False)
#                 continue
#             res.append(self._set_item(player_id, pos, item_dict, deepcopy))
#         self._UpdateItemGrids({'__id__': player_id, 'keys': (key,)})
#         return res
#
#     def set_item(self, player_id, pos_list, item_dict_list, deepcopy=False):
#         if not isinstance(pos_list, list):
#             pos_list = [pos_list]
#         if not isinstance(item_dict_list, list):
#             item_dict_list = [item_dict_list]
#         keys = tuple(pos[0] for pos in pos_list)
#         cancel = False
#         for pos, item_dict in zip(pos_list, item_dict_list):
#             if self._broadcast_item_grid_changed(player_id, pos, item_dict):
#                 cancel = True
#         if not cancel:
#             for pos, item_dict in zip(pos_list, item_dict_list):
#                 self._set_item(player_id, pos, item_dict, deepcopy)
#         self._UpdateItemGrids({'__id__': player_id, 'keys': keys})
#         return not cancel
#
#     def _set_item(self, player_id, pos, item_dict, deepcopy=False):
#         key, index = pos
#         if _is_empty_item(item_dict):
#             item_dict = None
#         if _is_shortcut_key(key) or _is_inv36_key(key):
#             res = _CompFactory.CreateItem(player_id).SetPlayerAllItems({(_INV_POS_TYPE, index): item_dict})
#             return res.values()[0]
#         elif _is_inv27_key(key):
#             res = _CompFactory.CreateItem(player_id).SetPlayerAllItems({(_INV_POS_TYPE, index + 9): item_dict})
#             return res.values()[0]
#         else:
#             if (
#                     player_id not in self.item_grid_items
#                     or key not in self.item_grid_items[player_id]
#                     or index >= len(self.item_grid_items[player_id][key])
#             ):
#                 return False
#             if deepcopy:
#                 item_dict = _deepcopy_item_dict(item_dict)
#             self.item_grid_items[player_id][key][index] = item_dict
#             return True
#
#     def _broadcast_item_grid_changed(self, player_id, pos, new_item):
#         old_item = self.get_item(player_id, pos)
#         args = {
#             'player_id': player_id,
#             'pos': pos,
#             'old_item': old_item,
#             'new_item': _deepcopy_item_dict(new_item),
#             'cancel': False,
#         }
#         self.BroadcastEvent("ItemGridChangedServerEvent", args)
#         return args['cancel']
#
#     def get_all_items(self, player_id, key):
#         comp = _CompFactory.CreateItem(player_id)
#         if _is_inv36_key(key):
#             items = comp.GetPlayerAllItems(_INV_POS_TYPE, True)
#         elif _is_inv27_key(key):
#             items = comp.GetPlayerAllItems(_INV_POS_TYPE, True)[9:]
#         elif _is_shortcut_key(key):
#             items = comp.GetPlayerAllItems(_INV_POS_TYPE, True)[:9]
#         else:
#             items = self._get_not_inv_items(player_id, key)
#         return [None if _is_empty_item(i) else i for i in items] if items else []
#
#     def get_item(self, player_id, pos):
#         key, index = pos
#         comp = _CompFactory.CreateItem(player_id)
#         if _is_shortcut_key(key) or _is_inv36_key(key):
#             item = comp.GetPlayerItem(_INV_POS_TYPE, index, True)
#         elif _is_inv27_key(key):
#             item = comp.GetPlayerItem(_INV_POS_TYPE, index + 9, True)
#         else:
#             item = self._get_not_inv_items(player_id, key, index)
#         return None if _is_empty_item(item) else item
#
#     def _get_not_inv_items(self, player_id, key, index=-1):
#         if player_id not in self.item_grid_items or key not in self.item_grid_items[player_id]:
#             return
#         items = self.item_grid_items[player_id][key]
#         if index == -1:
#             return _deepcopy_item_dict(items)
#         elif index < len(items):
#             return _deepcopy_item_dict(items[index])
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
