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
#   Last Modified : 2024-04-28
#
# ====================================================


from mod.common.minecraftEnum import (
    ItemPosType as _ItemPosType,
    GameType as _GameType,
)
from ..utils.item import is_empty_item as _is_empty_item
from comp import (
    CompFactory as _CompFactory,
    LvComp as _LvComp,
)


__all__ = [
    "deduct_inv_item",
    "clear_items",
    "get_item_pos",
    "change_item_count",
]


_ITEM_POS_SIZE = (36, 1, 1, 4)


def clear_items(player_id, item_pos_type, pos):
    """
    | 清空玩家指定位置的物品，并返回该位置被清除前的物品信息字典。

    -----

    :param str player_id: 玩家的实体ID
    :param int item_pos_type: 槽位类型，ItemPosType枚举
    :param int pos: 槽位编号

    :return: 该位置被清除前的物品信息字典
    :rtype: dict
    """
    comp = _CompFactory.CreateItem(player_id)
    item = comp.GetPlayerItem(item_pos_type, pos, True)
    comp.SetPlayerAllItems({(item_pos_type, pos): None})
    return item


def get_item_pos(entity_id, pos_type, item_id, item_aux=-1, count=1):
    """
    | 获取物品所在槽位。

    -----

    :param str entity_id: 生物的实体ID
    :param int pos_type: ItemPosType枚举
    :param str item_id: 物品ID
    :param int item_aux: 物品特殊值，默认为-1，表示任意特殊值
    :param int count: 返回数量，比如1表示只返回第一个搜索到的物品的槽位，默认为1

    :return: 物品所在槽位的列表，获取不到返回空列表
    :rtype: list[int]
    """
    is_player = (_CompFactory.CreateEngineType(entity_id).GetEngineTypeStr() == "minecraft:player")
    item_comp = _CompFactory.CreateItem(entity_id)
    num = _ITEM_POS_SIZE[pos_type - 1]
    result = []
    for i in range(num):
        if len(result) >= count:
            break
        if is_player:
            item_dict = item_comp.GetPlayerItem(pos_type, i)
        else:
            item_dict = item_comp.GetEntityItem(pos_type, i)
        if (
                item_dict
                and item_dict['newItemName'] == item_id
                and (item_aux == -1 or item_dict['newAuxValue'] == item_aux)
        ):
            result.append(i)
    return result


def change_item_count(player_id, pos_type=_ItemPosType.CARRIED, pos=0, change=-1):
    """
    | 改变玩家指定槽位物品的数量。（创造模式下不生效）

    -----

    :param str player_id: 玩家实体ID
    :param int pos_type: 槽位类型，默认为ItemPosType.CARRIED
    :param int pos: 槽位，默认为0
    :param int change: 改变量，默认为-1

    :return: 无
    :rtype: None
    """
    if _LvComp.Game.GetPlayerGameType(player_id) == _GameType.Creative:
        return
    item_comp = _CompFactory.CreateItem(player_id)
    item = item_comp.GetPlayerItem(pos_type, pos, True)
    item['count'] += change
    if item['count'] <= 0:
        item = None
    item_comp.SetPlayerAllItems({(pos_type, pos): item})


def deduct_inv_item(player_id, name, aux=-1, count=1):
    """
    | 从玩家背包中扣除指定数量的物品。
    | 该函数无需传入物品所在位置，而是自动从背包中寻找指定物品，找到了则扣除指定数量。

    -----

    :param str player_id: 玩家的实体ID
    :param str name: 物品名称
    :param int aux: 物品特殊值，默认为-1，表示任意特殊值
    :param int count: 扣除数量，默认为1

    :return: 扣除成功返回True，扣除失败（如物品数量不足）返回False
    :rtype: bool
    """
    comp = _CompFactory.CreateItem(player_id)
    items = comp.GetPlayerAllItems(_ItemPosType.INVENTORY, True)
    items_dict_map = {}
    for i, item in enumerate(items):
        if _is_empty_item(item):
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
        items_dict_map[(_ItemPosType.INVENTORY, i)] = item
        if count <= 0:
            break
    else:
        return False
    if items_dict_map:
        comp.SetPlayerAllItems(items_dict_map)
    return True













