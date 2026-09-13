# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-9
#  ⠀
#  ================================================


import sys
from typing import ClassVar, Protocol, Iterator, TypeVar, Tuple, Dict, Optional, Union, TypedDict, List, Callable, Any, ParamSpec
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ...client.ui.screen_node import NyScreenBase
from ...client.ui.nyc import (
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
)


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
T2 = TypeVar("T2")
P = ParamSpec("P")
F = TypeVar("F", bound=Callable[..., Any])
TypeT = TypeVar("TypeT", bound=type)
NyScreenBaseT = TypeVar("NyScreenBaseT", bound=NyScreenBase)


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
SlotsType = ClassVar[STuple]


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


UiPathOrNyControl = Union[str, NyControl]
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


