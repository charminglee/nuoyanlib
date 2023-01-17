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
#   Last Modified : 2023-01-15
#
# ====================================================


_AIR = ["minecraft:air", "air"]


def complete_item_namespace(name):
    # type: (str) -> str
    """
    在物品名称开头补充minecraft命名空间。如果已存在命名空间则返回原物品名称。
    示例：
    complete_item_namespace("apple")
    # "minecraft:apple"
    complete_item_namespace("minecraft:apple")
    # "minecraft:apple"
    -----------------------------------------------------------
    【name: str】 物品名称
    -----------------------------------------------------------
    return: str -> 补全后的物品名称
    """
    if ":" in name:
        return name
    return "minecraft:" + name


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
    newItemData1 = [itemDict1.get('newItemName'), itemDict1.get('newAuxValue', 0)]
    newItemData2 = [itemDict2.get('newItemName'), itemDict2.get('newAuxValue', 0)]
    itemData1 = [itemDict1.get('itemName'), itemDict1.get('auxValue', 0)]
    itemData2 = [itemDict2.get('itemName'), itemDict2.get('auxValue', 0)]
    newItemData1[0] = complete_item_namespace(newItemData1[0])
    newItemData2[0] = complete_item_namespace(newItemData2[0])
    itemData1[0] = complete_item_namespace(itemData1[0])
    itemData2[0] = complete_item_namespace(itemData2[0])
    if (not newItemData1[0] and not itemData1[0]) or (not newItemData2[0] and not itemData2[0]):
        return False
    if newItemData1[0] and newItemData2[0] and newItemData1 == newItemData2:
        return True
    if itemData1[0] and itemData2[0] and itemData1 == itemData2:
        return True
    if newItemData1[0] and itemData2[0] and newItemData1 == itemData2:
        return True
    if itemData1[0] and newItemData2[0] and itemData1 == newItemData2:
        return True
    return False


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
    return ('newItemName' not in itemDict and 'itemName' not in itemDict) \
           or (zeroCountIsEmp and itemDict.get('count', 1) <= 0) \
           or itemDict.get('newItemName') in _AIR  \
           or itemDict.get('itemName') in _AIR


if __name__ == "__main__":
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
    print complete_item_namespace("apple")  # "minecraft:apple"
    print complete_item_namespace("minecraft:apple")  # "minecraft:apple"

















