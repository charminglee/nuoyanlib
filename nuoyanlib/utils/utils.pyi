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
#   Last Modified : 2024-07-02
#
# ====================================================


from typing import Sequence, Any, List, Callable


def add_condition_to_func(cond: Callable[[], bool], func: Callable[[bool], Any], interval: int = 1) -> int: ...
def remove_condition_to_func(cond_id: int) -> bool: ...
def all_indexes(seq: Sequence, *elements: Any) -> List[int]: ...
def check_string(string: str, *check: str) -> bool: ...
def check_string2(string: str, *check: str) -> bool: ...
def turn_dict_value_to_tuple(orig_dict: dict) -> None: ...
def turn_list_to_tuple(lst: list) -> tuple: ...
def is_method_overridden(subclass: Any, father: Any, method: str) -> bool: ...
def translate_time(sec: int) -> str: ...
