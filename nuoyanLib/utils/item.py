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
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-02-26
#
# ====================================================


try:
    import mod.client.extraClientApi as _clientApi
    import mod.server.extraServerApi as _serverApi
except:
    pass


__all__ = [
    "set_namespace",
    "is_same_item",
    "is_empty_item",
    "are_same_item",
    "get_max_stack",
]


_AIR = ["minecraft:air", "air"]


def set_namespace(name, namespace="minecraft"):
    # type: (str, str) -> str
    """
    设置物品的命名空间。
    示例：
    set_namespace("apple")     # "minecraft:apple"
    set_namespace("apple", "nuoyan")     # "nuoyan:apple"
    set_namespace("minecraft:apple", "nuoyan")     # "nuoyan:apple"
    -----------------------------------------------------------
    【name: str】 物品名称
    【namespace: str = "minecraft"】 命名空间
    -----------------------------------------------------------
    return: str -> 新的物品名称
    """
    if not name:
        return ""
    nameLst = name.split(":")
    if ":" not in name:
        nameLst.insert(0, "")
    nameLst[0] = namespace
    return ":".join(nameLst)


def is_same_item(itemDict1, itemDict2):
    # type: (dict, dict) -> bool
    """
    判断两个物品是否是同种物品。
    -----------------------------------------------------------
    【itemDict1: dict】 物品信息字典1
    【itemDict2: dict】 物品信息字典2
    -----------------------------------------------------------
    return: bool -> 相同则返回True，否则返回False
    """
    isEmp1 = is_empty_item(itemDict1)
    isEmp2 = is_empty_item(itemDict2)
    if (isEmp1 and not isEmp2) or (not isEmp1 and isEmp2):
        return False
    if isEmp1 and isEmp2:
        return True
    newItemData1 = [itemDict1.get('newItemName', ""), itemDict1.get('newAuxValue', 0)]
    newItemData2 = [itemDict2.get('newItemName', ""), itemDict2.get('newAuxValue', 0)]
    itemData1 = [itemDict1.get('itemName', ""), itemDict1.get('auxValue', 0)]
    itemData2 = [itemDict2.get('itemName', ""), itemDict2.get('auxValue', 0)]
    newItemData1[0] = set_namespace(newItemData1[0])
    newItemData2[0] = set_namespace(newItemData2[0])
    itemData1[0] = set_namespace(itemData1[0])
    itemData2[0] = set_namespace(itemData2[0])
    extraId1, extraId2 = itemDict1.get('extraId'), itemDict2.get('extraId')
    userData1, userData2 = itemDict1.get('userData'), itemDict2.get('userData')
    if not _same(extraId1, extraId2) or not _same(userData1, userData2):
        return False
    if (not newItemData1[0] and not itemData1[0]) or (not newItemData2[0] and not itemData2[0]):
        return False
    if newItemData1 == newItemData2:
        return True
    if itemData1 == itemData2:
        return True
    if newItemData1 == itemData2:
        return True
    if itemData1 == newItemData2:
        return True
    return False


def _same(what1, what2):
    return (not what1 and not what2) or what1 == what2


def are_same_item(item, *otherItem):
    # type: (dict, dict) -> bool
    """
    判断多个物品是否是同种物品。
    -----------------------------------------------------------
    【item: dict】 物品信息字典
    【*otherItem: dict】 物品信息字典
    -----------------------------------------------------------
    return: bool -> 相同则返回True，否则返回False
    """
    for it in otherItem:
        if not is_same_item(item, it):
            return False
    return True


def is_empty_item(itemDict, zeroCountIsEmp=True):
    # type: (dict, bool) -> bool
    """
    判断物品是否是空物品。
    -----------------------------------------------------------
    【itemDict: dict】 物品信息字典
    【zeroCountIsEmp: bool = True】 是否把数量为0的物品视为空物品
    -----------------------------------------------------------
    return: bool -> 空物品则返回True，否则返回False
    """
    return not itemDict \
           or ('newItemName' not in itemDict and 'itemName' not in itemDict) \
           or (zeroCountIsEmp and itemDict.get('count', 1) <= 0) \
           or itemDict.get('newItemName') in _AIR  \
           or itemDict.get('itemName') in _AIR


def _get_level_id():
    return _clientApi.GetLevelId() or _serverApi.GetLevelId()


def _is_server():
    return _clientApi.GetLocalPlayerId() == "-1"


def get_max_stack(itemDict):
    """
    获取物品最大堆叠数量。
    -----------------------------------------------------------
    【itemDict: dict】 物品信息字典
    -----------------------------------------------------------
    return: int -> 最大堆叠数量，获取不到返回-1
    """
    name = itemDict['newItemName']
    aux = itemDict.get('newAuxValue', 0)
    if aux == -1:
        aux = 0
    if _is_server():
        comp = _serverApi.GetEngineCompFactory().CreateItem(_get_level_id())
    else:
        comp = _clientApi.GetEngineCompFactory().CreateItem(_get_level_id())
    try:
        return comp.GetItemBasicInfo(name, aux)['maxStackSize']
    except KeyError:
        return -1


def _test():
    item1 = {'newItemName': "minecraft:apple"}
    item2 = {'itemName': "minecraft:apple"}
    item3 = {'newItemName': "minecraft:apple", 'newAuxValue': 1}
    item4 = {'itemName': "minecraft:apple", 'auxValue': 1}
    item5 = {'newItemName': "minecraft:apple"}
    item6 = {'itemName': "minecraft:apple"}
    print "-" * 50
    print is_same_item(item1, item2)  # True
    print is_same_item(item3, item4)  # True
    print is_same_item(item1, item3)  # False
    print is_same_item(item2, item4)  # False
    print is_same_item(item1, item4)  # False
    print are_same_item(item1, item2, item3, item4)  # False
    print are_same_item(item1, item2, item5, item6)  # True
    print "-" * 50
    emp1 = {'newItemName': "minecraft:air"}
    emp2 = {'newItemName': "minecraft:apple", 'count': 0}
    emp3 = {}
    emp4 = {'itemName': "air"}
    print is_empty_item(emp1)  # True
    print is_empty_item(emp2)  # True
    print is_empty_item(emp3)  # True
    print is_empty_item(emp4)  # True
    print is_empty_item(item1)  # False
    print is_empty_item(item2)  # False
    print is_empty_item(item3)  # False
    print is_empty_item(item4)  # False
    print "-" * 50
    print set_namespace("apple")  # "minecraft:apple"
    print set_namespace("minecraft:apple", "nuoyan")  # "nuoyan:apple"

















