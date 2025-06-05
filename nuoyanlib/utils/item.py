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


from mod.common.minecraftEnum import ItemPosType as _ItemPosType
from .._core import _sys


__all__ = [
    "deepcopy_item_dict",
    "gen_item_dict",
    "get_item_count",
    "set_namespace",
    "is_same_item",
    "is_empty_item",
    "are_same_item",
    "get_max_stack",
]


def deepcopy_item_dict(item_dict):
    """
    | 对物品信息字典进行深拷贝。比标准库的 ``deepcopy`` 效率更高。
    | 注：该函数进行的深拷贝为伪深拷贝，只会对字典中的字典、列表进行递归深拷贝，其他不可变对象（如元组、字符串等）仍保留原引用。

    -----

    :param dict|None item_dict: 物品信息字典

    :return: 新的物品信息字典
    :rtype: dict|None
    """
    if isinstance(item_dict, dict):
        new = {}
        for k, v in item_dict.items():
            if k == 'userData':
                # todo: 优化此处的copy
                new[k] = v.copy() if v is not None else None
            else:
                new[k] = deepcopy_item_dict(v)
        return new
    elif isinstance(item_dict, list):
        return [deepcopy_item_dict(i) for i in item_dict]
    else:
        return item_dict


def gen_item_dict(
        newItemName,
        newAuxValue=0,
        count=1,
        showInHand=True,
        enchantData=None,
        modEnchantData=None,
        customTips="",
        extraId="",
        userData=None,
        durability=0,
        itemName="",
        auxValue=0,
):
    """
    | 构造物品信息字典。
    | 利用IDE的参数提示编写物品信息字典，省去了翻阅文档的麻烦。该函数返回的物品信息字典可直接传入接口使用。

    -----

    :param str newItemName: 必须设置，物品的identifier，即"命名空间:物品名"
    :param int newAuxValue: 可选，物品附加值，默认为0
    :param int count: 可选，物品数量，设置为0时为空物品，默认为1
    :param bool showInHand: 可选，是否显示在手上，默认为True
    :param list[tuple[int,int]]|None enchantData: 可选，附魔数据，类型为列表，列表中每个元素为元组：( `附魔类型 <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EnchantType.html>`_, 附魔等级)
    :param list[tuple[str,int]]|None modEnchantData: 可选，自定义附魔数据，类型为列表，列表中每个元素为元组：(自定义附魔id, 自定义附魔等级)
    :param str customTips: 可选，物品的自定义tips，修改该内容后会覆盖实例的组件 `netease:customtips <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/15-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%89%A9%E5%93%81/1-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%BA%E7%A1%80%E7%89%A9%E5%93%81.html?key=netease%3Acustomtips&docindex=1&type=0>`_ 的内容
    :param str extraId: 可选，物品自定义标识符，可以用于保存数据，区分物品
    :param dict|None userData: 可选，物品userData，用于灾厄旗帜、旗帜等物品，请勿随意设置该值
    :param int durability: 可选，物品耐久度，不存在耐久概念的物品默认值为0
    :param str itemName: （废弃）1.22及以前版本的旧identifier，详见 `1.23版本物品id变更 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-1.23%E7%89%88%E6%9C%AC%E7%89%A9%E5%93%81id%E5%8F%98%E6%9B%B4.html>`_
    :param str auxValue: （废弃）1.22及以前版本的旧物品附加值，详见 `1.23版本物品id变更 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/20-%E7%8E%A9%E6%B3%95%E5%BC%80%E5%8F%91/13-%E6%A8%A1%E7%BB%84SDK%E7%BC%96%E7%A8%8B/2-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-1.23%E7%89%88%E6%9C%AC%E7%89%A9%E5%93%81id%E5%8F%98%E6%9B%B4.html>`_

    :return: 物品信息字典
    :rtype: dict
    """
    if not newItemName or count == 0:
        return None
    if not itemName:
        del itemName, auxValue
    if not enchantData:
        enchantData = []
    if not modEnchantData:
        modEnchantData = []
    return locals()


def get_item_count(player_id, name, aux=-1):
    """
    | 获取玩家背包中指定物品的总数量。

    -----

    :param str player_id: 玩家的实体ID
    :param str name: 物品名称
    :param int aux: 物品特殊值（-1表示任意特殊值），默认为-1

    :return: 指定物品在背包中的总数
    :rtype: int
    """
    count = 0
    items = _sys.get_comp_factory().CreateItem(player_id).GetPlayerAllItems(_ItemPosType.INVENTORY)
    for item in items:
        if is_empty_item(item):
            continue
        if item['newItemName'] == name and (aux == -1 or item['newAuxValue'] == aux):
            count += item['count']
    return count


def set_namespace(name, namespace="minecraft"):
    """
    | 设置物品的命名空间。

    -----

    :param str name: 物品名称
    :param str namespace: 命名空间，默认为"minecraft"

    :return: 新的物品名称
    :rtype: str
    """
    if not name:
        return ""
    name_lst = name.split(":")
    if ":" not in name:
        name_lst.insert(0, "")
    name_lst[0] = namespace
    return ":".join(name_lst)


def _same(what1, what2):
    return (not what1 and not what2) or what1 == what2


def is_same_item(item_dict1, item_dict2):
    """
    | 判断两个物品是否是同种物品。

    -----

    :param dict item_dict1: 物品信息字典1
    :param dict item_dict2: 物品信息字典2

    :return: 相同则返回True，否则返回False
    :rtype: bool
    """
    is_emp1 = is_empty_item(item_dict1)
    is_emp2 = is_empty_item(item_dict2)
    if is_emp1 != is_emp2:
        return False
    if is_emp1 and is_emp2:
        return True
    if 'newItemName' in item_dict1:
        item_data1 = [item_dict1['newItemName'], item_dict1.get('newAuxValue', 0)]
    else:
        item_data1 = [item_dict1['itemName'], item_dict1.get('auxValue', 0)]
    if 'newItemName' in item_dict2:
        item_data2 = [item_dict2['newItemName'], item_dict2.get('newAuxValue', 0)]
    else:
        item_data2 = [item_dict2['itemName'], item_dict2.get('auxValue', 0)]
    item_data1[0] = set_namespace(item_data1[0])
    item_data2[0] = set_namespace(item_data2[0])
    extra_id1, extra_id2 = item_dict1.get('extraId'), item_dict2.get('extraId')
    user_data1, user_data2 = item_dict1.get('userData'), item_dict2.get('userData')
    if not _same(extra_id1, extra_id2) or not _same(user_data1, user_data2):
        return False
    return item_data1 == item_data2


def are_same_item(item, *other_item):
    """
    | 判断多个物品是否是同种物品。

    -----

    :param dict item: 物品信息字典
    :param dict other_item: 物品信息字典

    :return: 相同则返回True，否则返回False
    :rtype: bool
    """
    for it in other_item:
        if not is_same_item(item, it):
            return False
    return True


_AIR = ("minecraft:air", "air")


def is_empty_item(item, zero_is_emp=True):
    """
    | 判断物品是否是空物品。

    -----

    :param dict item: 物品信息字典
    :param bool zero_is_emp: 是否把数量为0的物品视为空物品，默认为是

    :return: 空物品则返回True，否则返回False
    :rtype: bool
    """
    return (
        not item
        or ('newItemName' not in item and 'itemName' not in item)
        or (zero_is_emp and item.get('count', 1) <= 0)
        or item.get('newItemName') in _AIR
        or item.get('itemName') in _AIR
    )


def get_max_stack(item):
    """
    | 获取物品最大堆叠数量。

    -----

    :param dict item: 物品信息字典

    :return: 最大堆叠数量，获取不到返回-1
    :rtype: int
    """
    name = item['newItemName']
    aux = item.get('newAuxValue', 0)
    if aux == -1:
        aux = 0
    comp = _sys.get_comp_factory().CreateItem(_sys.LEVEL_ID)
    try:
        return comp.GetItemBasicInfo(name, aux)['maxStackSize']
    except KeyError:
        return -1


if __name__ == "__main__":
    item1 = {'newItemName': "minecraft:apple"}
    item2 = {'itemName': "minecraft:apple"}
    item3 = {'newItemName': "minecraft:apple", 'newAuxValue': 1}
    item4 = {'itemName': "minecraft:apple", 'auxValue': 1}
    item5 = {'newItemName': "minecraft:apple"}
    item6 = {'itemName': "minecraft:apple"}
    print("-" * 50)
    print(is_same_item(item1, item2))  # True
    print(is_same_item(item3, item4))  # True
    print(is_same_item(item1, item3))  # False
    print(is_same_item(item2, item4))  # False
    print(is_same_item(item1, item4))  # False
    print(are_same_item(item1, item2, item3, item4))  # False
    print(are_same_item(item1, item2, item5, item6))  # True
    print("-" * 50)
    emp1 = {'newItemName': "minecraft:air"}
    emp2 = {'newItemName': "minecraft:apple", 'count': 0}
    emp3 = {}
    emp4 = {'itemName': "air"}
    print(is_empty_item(emp1))  # True
    print(is_empty_item(emp2))  # True
    print(is_empty_item(emp3))  # True
    print(is_empty_item(emp4))  # True
    print(is_empty_item(item1))  # False
    print(is_empty_item(item2))  # False
    print(is_empty_item(item3))  # False
    print(is_empty_item(item4))  # False
    print("-" * 50)
    print(set_namespace("apple"))  # "minecraft:apple"
    print(set_namespace("minecraft:apple", "nuoyan"))  # "nuoyan:apple"














