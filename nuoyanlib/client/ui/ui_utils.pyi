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
#   Last Modified : 2025-02-03
#
# ====================================================


from typing import List, Optional
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ..._core._typing import UiControl


def register_item_grid(
    key: str,
    ui_cls_path: str,
    grid_path: str,
    grid_size: int = 1,
    is_single: bool = False,
) -> bool: ...
def __get_path(control: UiControl) -> str: ...
def get_direct_children_path(control: UiControl, ui_ins: ScreenNode) -> List[str]: ...
def get_parent_path(control: UiControl) -> Optional[str]: ...
def get_parent_control(control: UiControl, ui_ins: ScreenNode) -> Optional[BaseUIControl]: ...















