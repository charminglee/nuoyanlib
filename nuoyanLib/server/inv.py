# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-07-02
#
# ====================================================


import mod.server.extraServerApi as _serverApi
from mod.common.minecraftEnum import ItemPosType as _ItemPosType, GameType as _GameType
from ..utils.item import is_empty_item as _is_empty_item


__all__ = [
    "clear_items",
    "get_item_pos",
    "change_player_item_count",
]


_LEVEL_ID = _serverApi.GetLevelId()
_ServerCompFactory = _serverApi.GetEngineCompFactory()
_LevelGameComp = _ServerCompFactory.CreateGame(_LEVEL_ID)


_ITEM_POS_SIZE = (36, 1, 1, 4)


def clear_items(playerId, itemPosType=_ItemPosType.INVENTORY, pos=-1):
    # type: (str, int, int) -> None
    """
    清空玩家指定位置的物品。
    -----------------------------------------------------------
    【playerId: str】 玩家的实体ID
    【itemPosType: int】 槽位类型，ItemPosType枚举，默认为背包
    【pos: int】 槽位编号，默认为-1，表示清空全部物品
    -----------------------------------------------------------
    NoReturn
    """
    comp = _ServerCompFactory.CreateItem(playerId)
    if pos == -1:
        comp.SetPlayerAllItems({(itemPosType, i): None for i in range(_ITEM_POS_SIZE[itemPosType])})
    else:
        comp.SetPlayerAllItems({(itemPosType, pos): None})


def get_item_pos(entityId, posType, itemId, itemAux=-1, count=1):
    # type: (str, int, str, int, int) -> list[int]
    """
    获取物品所在槽位。
    -----------------------------------------------------------
    【entityId: str】 生物的实体ID
    【posType: int】 ItemPosType枚举
    【itemId: str】 物品ID
    【itemAux: int = -1】 物品特殊值，-1表示任意特殊值
    【count: int = 1】 返回数量，比如1表示只返回第一个搜索到的物品的槽位
    -----------------------------------------------------------
    return: List[int] -> 物品所在槽位的列表
    """
    isPlayer = (_ServerCompFactory.CreateEngineType(entityId).GetEngineTypeStr() == "minecraft:player")
    itemComp = _ServerCompFactory.CreateItem(entityId)
    num = 1 if posType == 1 or posType == 2 else (4 if posType == 3 else 36)
    result = []
    for i in range(num):
        if len(result) >= count:
            break
        itemDict = itemComp.GetPlayerItem(posType, i) if isPlayer else itemComp.GetEntityItem(posType, i)
        if itemDict and itemDict['newItemName'] == itemId and (itemAux == -1 or itemDict['newAuxValue'] == itemAux):
            result.append(i)
    return result


def change_player_item_count(playerId, posType=_ItemPosType.CARRIED, pos=0, change=-1):
    # type: (str, int, int, int) -> None
    """
    改变玩家指定槽位物品的数量。（创造模式下不生效）
    示例：
    change_player_item_count(playerId)     # 玩家手持物品数量-1
    -----------------------------------------------------------
    【playerId: str】 玩家实体ID
    【posType: int = ItemPosType.CARRIED】 槽位类型
    【pos: int = 0】 槽位
    【change: int = -1】 改变量
    -----------------------------------------------------------
    NoReturn
    """
    if _LevelGameComp.GetPlayerGameType(playerId) == _GameType.Creative:
        return
    itemComp = _ServerCompFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(posType, pos)
    item['count'] += change
    if item['count'] <= 0:
        item = None
    itemComp.SetPlayerAllItems({(posType, pos): item})


def cal_item_count(playerId, name, aux=-1):
    """
    计算玩家背包中指定物品的总数量。
    -----------------------------------------------------------
    【playerId: str】 玩家的实体ID
    【name: str】 物品名称
    【aux: int = -1】 物品特殊值（-1表示任意特殊值）
    -----------------------------------------------------------
    return: int -> 指定物品在背包中的总数
    """
    count = 0
    items = _ServerCompFactory.CreateItem(playerId).GetPlayerAllItems(_ItemPosType.INVENTORY)
    for item in items:
        if _is_empty_item(item):
            continue
        if item['newItemName'] == name and (aux == -1 or item['newAuxValue'] == aux):
            count += item['count']
    return count


def deduct_item(playerId, name, aux, count):
    """
    从玩家背包中扣除指定数量的物品。
    -----------------------------------------------------------
    【playerId: str】 玩家的实体ID
    【name: str】 物品名称
    【aux: int】 物品特殊值（-1表示任意特殊值）
    【count: int】 扣除数量
    -----------------------------------------------------------
    return: 扣除成功返回True，扣除失败（如物品数量不足）返回False
    """
    totalCount = cal_item_count(playerId, name, aux)
    if totalCount < count:
        return False
    comp = _ServerCompFactory.CreateItem(playerId)
    items = comp.GetPlayerAllItems(_ItemPosType.INVENTORY)
    for i, item in enumerate(items[:]):
        if _is_empty_item(item) or item['newItemName'] != name or item['newAuxValue'] != aux:
            continue
        c = item['count']
        item['count'] -= count
        count -= c
        if item['count'] <= 0:
            items[i] = None
        if count <= 0:
            break
    comp.SetPlayerAllItems({
        (_ItemPosType.INVENTORY, i): item for i, item in enumerate(items)
    })
    return True













