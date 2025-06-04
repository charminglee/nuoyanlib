# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from typing import Tuple, Dict, Optional, Union, TypedDict, List, Callable, Literal, Any
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.common.utils.mcmath import Vector3


PyBasicTypes = Union[str, int, float, list, tuple, dict, None]
FTuple = Tuple[float, ...]
FTuple2 = Tuple[float, float]
FTuple3 = Tuple[float, float, float]
ITuple = Tuple[int, ...]
ITuple2 = Tuple[int, int]
ITuple3 = Tuple[int, int, int]
STuple = Tuple[str, ...]
Vector = Union[FTuple3, List[float], Vector3]
VectorNoList = Union[FTuple3, Vector3]
Matrix = List[List[float]]


class ItemDict(TypedDict, total=False):
    newItemName: str
    newAuxValue: str
    count: int
    itemName: str
    auxValue: int
    showInHand: bool
    enchantData: List[ITuple2]
    modEnchantData: List[ITuple2]
    customTips: str
    extraId: str
    userData: Dict[str, Any]
    durability: int
ItemCellPos = Tuple[str, int]
ItemCell = Union[str, ItemCellPos]
ItemGridKeys = Union[str, STuple, None]
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


ArgsDict = Dict[str, PyBasicTypes]
EntFilter = Optional[Callable[[str], bool]]


UiPathOrControl = Union[str, BaseUIControl]
Anchor = Literal[
    "top_left",
    "top_middle",
    "top_right",
    "left_middle",
    "center",
    "right_middle",
    "bottom_left",
    "bottom_middle",
    "bottom_right",
]
class FullPositionDict(TypedDict, total=False):
    followType: Literal["none", "parent", "maxChildren", "maxSibling", "children", "x", "y"]
    relativeValue: float
    absoluteValue: float
class FullSizeDict(TypedDict, total=False):
    fit: bool
    followType: Literal["none", "parent", "maxChildren", "maxSibling", "children", "x", "y"]
    relativeValue: float
    absoluteValue: float
UiPropertyNameAll = Literal[
    "all",
    "size",
    "offset",
    "alpha",
    "clip",
    "color",
    "flip_book",
    "aseprite_flip_book",
    "uv",
    "wait",
]
UiPropertyName = Literal[
    "size",
    "offset",
    "alpha",
    "clip",
    "color",
    "flip_book",
    "aseprite_flip_book",
    "uv",
    "wait",
]
