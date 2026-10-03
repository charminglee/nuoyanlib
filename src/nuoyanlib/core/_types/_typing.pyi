# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-17
#  ⠀
#  ================================================


from typing import ClassVar, Protocol, Iterator, TypeVar, Tuple, Dict, Optional, Union, TypedDict, List, Callable, Any, ParamSpec
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from ...client.ui.screen_node import NyScreenBase
from ...client.ui.nyc.control import NyControl
from ...client.ui.nyc.button import NyButton
from ...client.ui.nyc.combo_box import NyComboBox
from ...client.ui.nyc.edit_box import NyEditBox
from ...client.ui.nyc.grid import NyGrid
from ...client.ui.nyc.image import NyImage
from ...client.ui.nyc.input_panel import NyInputPanel
from ...client.ui.nyc.item_renderer import NyItemRenderer
from ...client.ui.nyc.label import NyLabel
from ...client.ui.nyc.mini_map import NyMiniMap
from ...client.ui.nyc.paper_doll import NyPaperDoll
from ...client.ui.nyc.progress_bar import NyProgressBar
from ...client.ui.nyc.scroll_view import NyScrollView
from ...client.ui.nyc.selection_wheel import NySelectionWheel
from ...client.ui.nyc.slider import NySlider
from ...client.ui.nyc.stack_panel import NyStackPanel
from ...client.ui.nyc.toggle import NyToggle


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)
T2 = TypeVar("T2")
P = ParamSpec("P")
F = TypeVar("F", bound=Callable[..., Any])
TypeT = TypeVar("TypeT", bound=type)


NyScreenBaseT = TypeVar("NyScreenBaseT", bound=NyScreenBase)
NyControlT = TypeVar("NyControlT", bound=NyControl)
NyControlT_co = TypeVar("NyControlT_co", bound=NyControl, covariant=True)


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
EasingFuncType = Callable[[float], float]


Number = Union[float, int]
Scalar = Union[float, int]
NumberT = TypeVar("NumberT", bound=Number, covariant=True)


Pos = Union[FTuple3, FTuple2]
PosT = TypeVar("PosT", bound=Pos)


class VectorLike(Protocol):
    def __getitem__(self, i: int, /) -> Number: ...
    def __iter__(self) -> Iterator[Number]: ...
    def __len__(self) -> int: ...


GeneralVector = Union[FTuple3, FTuple2]


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
