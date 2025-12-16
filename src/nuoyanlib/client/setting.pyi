# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


def save_setting(name: str, data_dict: dict, is_global: bool = True) -> bool: ...
def read_setting(name: str, is_global: bool = True) -> dict: ...
def check_setting(name: str, item_list: list, is_global: bool = True) -> list: ...

















