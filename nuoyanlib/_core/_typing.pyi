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
#   Last Modified : 2025-01-29
#
# ====================================================


from typing import Tuple, Dict, Optional, Union, TypedDict, List, Callable
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.common.utils.mcmath import Vector3


ItemDict = Optional[dict]
ItemCellPos = Tuple[str, int]
ItemCell = Union[str, ItemCellPos]
ItemGridKeys = Union[str, Tuple[str, ...], None]
class ItemSelectedData(TypedDict):
    item_dict: dict
    cell_path: str
    cell_pos: ItemCellPos
class ItemHeapData(TypedDict):
    item_dict: dict
    cell_path: str
    cell_pos: ItemCellPos
    selected_count: int
    animating: bool
    bar_ctrl: ProgressBarUIControl


PyBasicTypes = Union[str, int, float, list, tuple, dict, None]
FTuple2 = Tuple[float, float]
FTuple3 = Tuple[float, float, float]
Vector = Union[FTuple3, List[float], Vector3]
VectorNotList = Union[FTuple3, Vector3]
Matrix = List[List[float]]
EventArgs = Dict[str, PyBasicTypes]


UiControl = Union[str, BaseUIControl]
EntFilter = Optional[Callable[[str], bool]]

