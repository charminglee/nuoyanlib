# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-12
|
| ==============================================
"""


from typing import TypeVar, Tuple, Dict, Optional, Union, TypedDict, List, Callable, Any, Iterator
from types import InstanceType
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.common.utils.mcmath import Vector3
from ...client.ui.nyc import *


_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Any])


PyBasicTypes = Union[str, int, float, list, tuple, dict, None]
FTuple = Tuple[float, ...]
FTuple2 = Tuple[float, float]
FTuple3 = Tuple[float, float, float]
FTuple4 = Tuple[float, float, float, float]
ITuple = Tuple[int, ...]
ITuple2 = Tuple[int, int]
ITuple3 = Tuple[int, int, int]
STuple = Tuple[str, ...]
Vector = Union[FTuple3, List[float], Vector3]
VectorNoList = Union[FTuple3, Vector3]
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
EventCallbackFunc = Callable[[ArgsDict], Any]
EventCallbackMethod = Callable[[InstanceType, ArgsDict], Any]


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
class FrameAnimData(TypedDict):
    control: NyImage
    tex_path: str
    frame_time: float
    stop_frame: int
    loop: bool
    last_time: float
    indexes: Iterator[int]
    is_pausing: bool
    callback: Callable
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
class BtnTouchCallbackDict(TypedDict):
    #collection_name
    #collection_index
    ButtonState: int
    TouchEvent: int
    PrevButtonDownID: int
    TouchPosX: float
    TouchPosY: float
    ButtonPath: str
    AddTouchEventParams: dict
class BtnHoverCallbackDict(TypedDict):
    isHoverIn: int
    PrevButtonDownID: int
    ButtonPath: str
    AddHoverEventParams: dict


TimeEaseFuncType = Callable[[float], float]
