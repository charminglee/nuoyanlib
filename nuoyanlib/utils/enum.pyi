# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-07-22
|
| ==============================================
"""


from typing import Dict, List, Tuple, Any, Optional, Iterator, Union, overload, Type
from _typeshed import Self
from .._core._types._typing import STuple


class EnumMeta(type):
    __flag__: int
    __members__: Dict[str, Any]
    _restrict_type: Optional[type]
    def __new__(
        metacls: Type[Self],
        name: str,
        bases: Tuple[type, ...],
        dct: Dict[str, Any],
        restrict_type: Optional[type] = None,
    ) -> Self: ...
    def __setattr__(cls, name: str, value: Any) -> None: ...
    def __delattr__(cls, name: str) -> None: ...
    def __contains__(cls, member: Any) -> bool: ...
    def __len__(cls) -> int: ...
    def __iter__(cls: Type[Self]) -> Iterator[Self]: ...
    @overload
    def __getitem__(cls, item: type) -> Type[Enum]: ...
    @overload
    def __getitem__(cls, item: str) -> Any: ...
    def __gen_auto_value__(cls, name: Optional[str] = None) -> Union[str, int]: ...


class Enum(metaclass=EnumMeta):
    __name: str
    __value: Any
    __hash: int
    class auto(object): ...
    def __init__(self, name: str, value: Any) -> None: ...
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> Any: ...


class ComboBoxCallbackType(Enum[str]):
    OPEN: str
    CLOSE: str
    SELECT: str


class ButtonCallbackType(Enum[str]):
    UP: str
    DOWN: str
    CANCEL: str
    MOVE: str
    MOVE_IN: str
    MOVE_OUT: str
    DOUBLE_CLICK: str
    LONG_CLICK: str
    HOVER_IN: str
    HOVER_OUT: str
    SCREEN_EXIT: str


class UiControlType(Enum[int]):
    all: int
    button: int
    custom: int
    collection_panel: int
    dropdown: int
    edit_box: int
    factory: int
    grid: int
    image: int
    input_panel: int
    label: int
    panel: int
    screen: int
    scrollbar_box: int
    scroll_track: int
    scroll_view: int
    selection_wheel: int
    slider: int
    slider_box: int
    stack_panel: int
    toggle: int
    image_cycler: int
    label_cycler: int
    grid_page_indicator: int
    combox: int
    layout: int
    stack_grid: int
    joystick: int
    rich_text: int
    sixteen_nine_layout: int
    mul_lines_edit: int
    amin_process_bar: int
    unknown: int


class ControlType(Enum[str]):
    base_control: str
    button: str
    image: str
    label: str
    panel: str
    input_panel: str
    stack_panel: str
    edit_box: str
    paper_doll: str
    netease_paper_doll: str
    item_renderer: str
    gradient_renderer: str
    scroll_view: str
    grid: str
    progress_bar: str
    toggle: str
    slider: str
    selection_wheel: str
    combo_box: str
    mini_map: str
    _not_special: STuple


def search_data(data: Any, lst: list) -> bool: ...


ENTITY_LIST: List[Optional[int, str, str, int]]
MOB_LIST: List[Tuple[int, str, str, int, bool]]
FRIENDLY_MOB_LIST: List[Tuple[int, str, str, int]]
HOSTILE_MOB_LIST: List[Tuple[int, str, str, int]]
ATTACKABLE_MOB_LIST: List[Tuple[int, str, str, int]]
ENTITY_ID_DICT: Dict[int, int]
EFFECT_DICT: Dict[str, str]
BIOME_DICT: Dict[str, str]
STRUCTURE_DICT: Dict[int, Tuple[str, str]]
BLOCK_LIST: List[str]
ITEM_LIST: List[str]
