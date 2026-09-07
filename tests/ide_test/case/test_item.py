# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


from nuoyanlib.common.item import is_same_item, is_empty_item, set_namespace


item1 = {'newItemName': "minecraft:apple"}
item2 = {'newItemName': "minecraft:apple", 'newAuxValue': 1}
item3 = {'newItemName': "minecraft:apple", 'newAuxValue': 2}
item4 = {'newItemName': "minecraft:apple", 'newAuxValue': 0, 'userData': None, 'extraId': None}
item5 = {'newItemName': "minecraft:apple", 'userData': {'a': 1}}
item6 = {'newItemName': "minecraft:apple", 'extraId': "a"}
assert not is_same_item(item1, item2, item3)
assert is_same_item(item1, item4)
assert not is_same_item(item1, item5)
assert not is_same_item(item1, item6)


emp1 = {'newItemName': "minecraft:air"}
emp2 = {'newItemName': "minecraft:apple", 'count': 0}
emp3 = {}
assert is_empty_item(emp1)
assert is_empty_item(emp2)
assert is_empty_item(emp3)
assert not is_empty_item(item1)
assert not is_empty_item(item3)


assert set_namespace("apple") == "minecraft:apple"
assert set_namespace("minecraft:apple", "nuoyan") == "nuoyan:apple"
