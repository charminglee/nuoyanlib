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
#   Last Modified : 2023-09-06
#
# ====================================================


from mod.common.minecraftEnum import (
    ItemPosType as _ItemPosType,
    GameType as _GameType,
)
from ..utils.item import is_empty_item as _is_empty_item
from serverComps import (
    ServerCompFactory as _ServerCompFactory,
    ServerLevelComps as _ServerLevelComps,
)


__all__ = [
    "deduct_inv_item",
    "clear_items",
    "get_item_pos",
    "change_item_count",
]


_ITEM_POS_SIZE = (36, 1, 1, 4)


def clear_items(playerId, itemPosType, pos):
    """
    清空玩家指定位置的物品，并返回该位置被清除前的物品信息字典。

    -----

    :param str playerId: 玩家的实体ID
    :param int itemPosType: 槽位类型，ItemPosType枚举
    :param int pos: 槽位编号

    :return: 该位置被清除前的物品信息字典
    :rtype: dict
    """
    comp = _ServerCompFactory.CreateItem(playerId)
    item = comp.GetPlayerItem(itemPosType, pos, True)
    comp.SetPlayerAllItems({(itemPosType, pos): None})
    return item


def get_item_pos(entityId, posType, itemId, itemAux=-1, count=1):
    """
    获取物品所在槽位。

    -----

    :param str entityId: 生物的实体ID
    :param int posType: ItemPosType枚举
    :param str itemId: 物品ID
    :param int itemAux: 物品特殊值，默认为-1，表示任意特殊值
    :param int count: 返回数量，比如1表示只返回第一个搜索到的物品的槽位，默认为1

    :return: 物品所在槽位的列表，获取不到返回空列表
    :rtype: list[int]
    """
    isPlayer = (_ServerCompFactory.CreateEngineType(entityId).GetEngineTypeStr() == "minecraft:player")
    itemComp = _ServerCompFactory.CreateItem(entityId)
    num = _ITEM_POS_SIZE[posType - 1]
    result = []
    for i in range(num):
        if len(result) >= count:
            break
        itemDict = itemComp.GetPlayerItem(posType, i) if isPlayer else itemComp.GetEntityItem(posType, i)
        if (
                itemDict
                and itemDict['newItemName'] == itemId
                and (itemAux == -1 or itemDict['newAuxValue'] == itemAux)
        ):
            result.append(i)
    return result


def change_item_count(playerId, posType=_ItemPosType.CARRIED, pos=0, change=-1):
    """
    改变玩家指定槽位物品的数量。（创造模式下不生效）

    -----

    【示例】

    玩家手持物品数量减1：

    >>> change_item_count(playerId)

    玩家背包槽位10的物品数量加2：

    >>> change_item_count(playerId, ItemPosType.INVENTORY, 10, 2)

    -----

    :param str playerId: 玩家实体ID
    :param int posType: 槽位类型，默认为ItemPosType.CARRIED
    :param int pos: 槽位，默认为0
    :param int change: 改变量，默认为-1

    :return: 无
    :rtype: None
    """
    if _ServerLevelComps.Game.GetPlayerGameType(playerId) == _GameType.Creative:
        return
    itemComp = _ServerCompFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(posType, pos)
    item['count'] += change
    if item['count'] <= 0:
        item = None
    itemComp.SetPlayerAllItems({(posType, pos): item})


def deduct_inv_item(playerId, name, aux=-1, count=1):
    """
    从玩家背包中扣除指定数量的物品。

    该函数无需传入物品所在位置，而是自动从背包中寻找指定物品，找到了则扣除指定数量。

    -----

    :param str playerId: 玩家的实体ID
    :param str name: 物品名称
    :param int aux: 物品特殊值，默认为-1，表示任意特殊值
    :param int count: 扣除数量，默认为1

    :return: 扣除成功返回True，扣除失败（如物品数量不足）返回False
    :rtype: bool
    """
    comp = _ServerCompFactory.CreateItem(playerId)
    items = comp.GetPlayerAllItems(_ItemPosType.INVENTORY, True)
    itemsDictMap = {}
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
        itemsDictMap[(_ItemPosType.INVENTORY, i)] = item
        if count <= 0:
            break
    else:
        return False
    if itemsDictMap:
        comp.SetPlayerAllItems(itemsDictMap)
    return True













