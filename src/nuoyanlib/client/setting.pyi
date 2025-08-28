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


def save_setting(name: str, data_dict: dict, is_global: bool = True) -> bool: ...
def read_setting(name: str, is_global: bool = True) -> dict: ...
def check_setting(name: str, item_list: list, is_global: bool = True) -> list: ...

















