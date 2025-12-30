# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-30
#  ⠀
# =================================================


import sys
from typing import Protocol, Iterator, TypeVar, Tuple, Dict, Optional, Union, TypedDict, List, Callable, Any, ParamSpec
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ...client.ui.nyc import *


T = TypeVar("T")
T2 = TypeVar("T2")
P = ParamSpec("P")
F = TypeVar("F", bound=Callable[..., Any])
TypeT = TypeVar("TypeT", bound=type)
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
ArgsDict = Dict[str, PyBasicTypes]
EntFilter = Optional[Callable[[str], bool]]
TimeEaseFuncType = Callable[[float], float]


if sys.version_info <= (2, 7):
    Number = Union[float, int, long]
else:
    Number = Union[float, int]
NumberT = TypeVar("NumberT", bound=Number)


Pos = Union[FTuple3, FTuple2]
PosT = TypeVar("PosT", bound=Pos)


if sys.version_info <= (2, 7):
    Scalar = Union[float, int, long]
else:
    Scalar = Union[float, int]
class VectorLike(Protocol):
    def __iter__(self) -> Iterator[float]: ...
    def __getitem__(self, i: int) -> float: ...
    def __len__(self) -> int: ...
GeneralVector = Union[FTuple3, FTuple2]
VectorLikeT = TypeVar("VectorLikeT", bound=VectorLike)


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


