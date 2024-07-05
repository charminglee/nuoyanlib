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


from typing import Tuple


def set_query_mod_var(entity_id: str, name: str, value: float, sync: bool = True) -> bool: ...
def add_player_render_resources(player_id: str, rebuild: bool, *res_tuple: Tuple[str, str]) -> Tuple[bool, ...]: ...
def add_entity_render_resources(entity_id: str, rebuild: bool, *res_tuple: Tuple[str, str]) -> Tuple[bool, ...]: ...
