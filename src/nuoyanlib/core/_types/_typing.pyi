# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-11
|
| ====================================================
"""


import sys
from typing import TypeVar, Tuple, Dict, Optional, Union, TypedDict, List, Callable, Any, ParamSpec
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ...client.ui.nyc import *


T = TypeVar("T")
P = ParamSpec("P")
F = TypeVar("F", bound=Callable[..., Any])
FuncDecorator = Callable[[F], F]
__T_type = TypeVar("__T_type", bound=type)
ClassDecorator = Callable[[__T_type], __T_type]
if sys.version_info >= (3, 11):
    from typing_extensions import Self as _Self
    Self = _Self
else:
    Self = T


PyBasicTypes = Union[str, int, float, list, tuple, dict, None]
SupportNeteaseApi = Union[str, int, float, list, tuple, dict, None, long, set, frozenset]
FTuple = Tuple[float, ...]
FTuple2 = Tuple[float, float]
FTuple3 = Tuple[float, float, float]
FTuple4 = Tuple[float, float, float, float]
ITuple = Tuple[int, ...]
ITuple2 = Tuple[int, int]
ITuple3 = Tuple[int, int, int]
STuple = Tuple[str, ...]
Matrix = List[List[float]]
Args = Tuple[Any, ...]
Kwargs = Dict[str, Any]


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
UserData = Dict[str, Any]


ArgsDict = Dict[str, PyBasicTypes]
EntFilter = Optional[Callable[[str], bool]]


UiPathOrControl = Union[str, BaseUIControl]
UiPathOrNyControl = Union[str, BaseUIControl, NyControl]
UiControl = Union[BaseUIControl, NyControl]
NyControlTypes = Union[
    NyButton,
    NyComboBox,
    NyControl,
    NyEditBox,
    NyGrid,
    NyImage,
    NyInputPanel,
    NyItemRenderer,
    NyLabel,
    NyMiniMap,
    NyPaperDoll,
    NyProgressBar,
    NyScrollView,
    NySelectionWheel,
    NySlider,
    NyStackPanel,
    NyToggle,
]


TimeEaseFuncType = Callable[[float], float]
