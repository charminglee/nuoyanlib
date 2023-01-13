# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-14
#
# ====================================================


import mod.server.extraServerApi as _serverApi
from mod.common.minecraftEnum import ItemPosType as _ItemPosType, GameType as _GameType


_LEVEL_ID = _serverApi.GetLevelId()
_ServerCompFactory = _serverApi.GetEngineCompFactory()
_LevelGameComp = _ServerCompFactory.CreateGame(_LEVEL_ID)


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
    return -> None
    """
    if _LevelGameComp.GetPlayerGameType(playerId) == _GameType.Creative:
        return
    itemComp = _ServerCompFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(posType, pos)
    item['count'] += change
    if item['count'] <= 0:
        item = None
    itemComp.SetPlayerAllItems({(posType, pos): item})
















