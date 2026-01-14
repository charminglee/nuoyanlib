# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
#  ⠀
# =================================================


from mod.common.minecraftEnum import ItemPosType, GameType
from ..core.server.comp import CF, LvComp
from ..utils.item import is_empty_item


__all__ = [
    # "set_items_to_item_grid",
    # "get_items_from_item_grid",
    # "update_item_grids",
    "deduct_inv_item",
    "clear_items",
    "get_item_pos",
    "change_item_count",
]


# def set_items_to_item_grid(player_id, key, item_dict_list):
#     """
#     设置物品网格的所有物品。
#
#     -----
#
#     :param str player_id: 玩家实体ID
#     :param str key: 网格的key
#     :param list[dict|None] item_dict_list: 物品信息字典列表
#
#     :return: 返回一个列表，列表元素为布尔值，对应item_dict_list中各物品是否设置成功
#     :rtype: list[bool]
#     """
#     lib_sys = _lib_server.instance()
#     if not lib_sys:
#         return False
#     return lib_sys.set_all_items(player_id, key, item_dict_list, True)
#
#
# def get_items_from_item_grid(player_id, key):
#     """
#     获取物品网格的所有物品。
#
#     -----
#
#     :param str player_id: 玩家实体ID
#     :param str key: 网格的key
#
#     :return: 物品信息字典列表，获取不到返回空列表
#     :rtype: list[dict|None]
#     """
#     lib_sys = _lib_server.instance()
#     if not lib_sys:
#         return []
#     return lib_sys.get_all_items(player_id, key)


# def update_item_grids(player_id, keys):
#     """
#     立即同步一次玩家的物品数据给客户端的物品网格。
#
#     以“_shortcut”、“_inv27”或“_inv36”结尾的网格无需使用此接口进行同步。
#
#     -----
#
#     :param str player_id: 玩家的实体ID
#     :param str|tuple[str] keys: 网格的key，多个网格请使用元组
#
#     :return: 是否成功
#     :rtype: bool
#     """
#     lib_sys = _lib_server.instance()
#     if not lib_sys:
#         return False
#     if isinstance(keys, str):
#         keys = (keys,)
#     return lib_sys.on_update_item_grids({'__id__': player_id, 'keys': keys})


def clear_items(player_id, item_pos_type, pos=0):
    """
    清空玩家指定位置的物品，并返回该位置被清除前的物品信息字典。

    -----

    :param str player_id: 玩家的实体ID
    :param int item_pos_type: 槽位类型，ItemPosType 枚举
    :param int pos: 槽位索引；默认为 0

    :return: 该位置被清除前的物品信息字典
    :rtype: dict
    """
    comp = CF(player_id).Item
    item = comp.GetPlayerItem(item_pos_type, pos, True)
    comp.SetPlayerAllItems({(item_pos_type, pos): None})
    return item


_ITEM_POS_SIZE = (36, 1, 1, 4)


def get_item_pos(entity_id, pos_type, item_id, item_aux=-1, count=1):
    """
    获取物品所在槽位。

    -----

    :param str entity_id: 生物的实体ID
    :param int pos_type: ItemPosType 枚举
    :param str item_id: 物品ID
    :param int item_aux: 物品特殊值；默认为 -1，表示任意特殊值
    :param int count: 返回数量，比如 1 表示只返回第一个搜索到的物品的槽位；默认为 1

    :return: 物品所在槽位的列表，获取不到返回空列表
    :rtype: list[int]
    """
    cf = CF(entity_id)
    is_player = (cf.EngineType.GetEngineTypeStr() == "minecraft:player")
    result = []
    for i in xrange(_ITEM_POS_SIZE[pos_type]):
        if len(result) >= count:
            break
        if is_player:
            item_dict = cf.Item.GetPlayerItem(pos_type, i)
        else:
            item_dict = cf.Item.GetEntityItem(pos_type, i)
        if (
                item_dict
                and item_dict['newItemName'] == item_id
                and (item_aux == -1 or item_dict['newAuxValue'] == item_aux)
        ):
            result.append(i)
    return result


def change_item_count(player_id, pos_type=ItemPosType.CARRIED, pos=0, change=-1):
    """
    改变玩家指定槽位物品的数量。（创造模式下不生效）

    -----

    :param str player_id: 玩家实体ID
    :param int pos_type: 槽位类型；默认为 ItemPosType.CARRIED
    :param int pos: 槽位；默认为 0
    :param int change: 改变量；默认为 -1

    :return: 无
    :rtype: None
    """
    if LvComp.Game.GetPlayerGameType(player_id) == GameType.Creative:
        return
    item_comp = CF(player_id).Item
    item = item_comp.GetPlayerItem(pos_type, pos, True)
    item['count'] += change
    if item['count'] <= 0:
        item = None
    item_comp.SetPlayerAllItems({(pos_type, pos): item})


def deduct_inv_item(player_id, name, aux=-1, count=1, include_creative=False):
    """
    从玩家背包中扣除指定数量的物品。

    说明
    ----

    该函数无需传入物品所在位置，而是自动从背包中寻找指定物品，找到了则扣除指定数量。

    -----

    :param str player_id: 玩家的实体ID
    :param str name: 物品名称
    :param int aux: 物品特殊值；默认为 -1，表示任意特殊值
    :param int count: 扣除数量；默认为 1
    :param bool include_creative: 创造模式下是否扣除；默认为 False

    :return: 扣除成功返回 True，扣除失败（如物品数量不足）返回 False
    :rtype: bool
    """
    if not include_creative and LvComp.Game.GetPlayerGameType(player_id) == GameType.Creative:
        return False
    comp = CF(player_id).Item
    items = comp.GetPlayerAllItems(ItemPosType.INVENTORY, True)
    items_dict_map = {}
    for i, item in enumerate(items):
        if is_empty_item(item):
            continue
        if item['newItemName'] != name:
            continue
        if aux != -1 and item['newAuxValue'] != aux:
            continue
        c = item['count']
        item['count'] -= count
        count -= c
        if item['count'] <= 0:
            item = None
        items_dict_map[(ItemPosType.INVENTORY, i)] = item
        if count <= 0:
            break
    else:
        return False
    if items_dict_map:
        comp.SetPlayerAllItems(items_dict_map)
        return True
    return False














