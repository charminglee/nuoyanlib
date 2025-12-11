# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-05
|
| ====================================================
"""


from typing import Tuple, Callable, ClassVar, TypedDict, Any, Literal, NoReturn, Dict, Optional, Type, List
from types import MethodType
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ....core._types._typing import Self, UiPathOrNyControl, FTuple2, STuple, T
from ....core._types._checker import args_type_check
from ....core._utils import cached_property
from ..screen_node import ScreenNodeExtension
from . import *
from ....utils.enum import Enum


__Anchor = Literal[
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
class __FullPositionParams(TypedDict, total=False):
    followType: Literal["none", "parent", "maxChildren", "maxSibling", "children", "x", "y"]
    relativeValue: float
    absoluteValue: float
class __FullSizeParams(TypedDict, total=False):
    fit: bool
    followType: Literal["none", "parent", "maxChildren", "maxSibling", "children", "x", "y"]
    relativeValue: float
    absoluteValue: float
__UiPropertyNamesAll = Literal[
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
__UiPropertyNames = Literal[
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


class InteractableControl(object):
    CALLBACK_TYPE: ClassVar[Type[Enum]]
    callbacks: Dict[str, List[Callable]]
    _callback_flag: List[str]
    _callback_func_map: Dict[str, Tuple[MethodType, MethodType]]
    def __init__(self: Self, callback_func_map: Dict[str, Tuple[MethodType, MethodType]]) -> None: ...
    def __destroy__(self) -> None: ...
    def _exec_callbacks(self, cb_type: str, *args: Any) -> None: ...
    def set_callback(self, func: Callable, cb_type: str = None) -> bool: ...
    def remove_callback(self, func: Callable, cb_type: str = None) -> bool: ...


class NyControl(object):
    CONTROL_TYPE: ClassVar[str]
    _ALLOWED_APPLY_ATTRS: ClassVar[STuple]
    _screen_node: ScreenNode
    ui_node: ScreenNodeExtension
    """
    控件所在UI类的实例。
    """
    _base_control: BaseUIControl
    _kwargs: Dict[str, Any]
    def __init__(
        self: Self,
        screen_node_ex: ScreenNodeExtension,
        control: BaseUIControl,
        **kwargs: Any
    ) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __destroy__(self) -> None: ...
    def __repr__(self) -> str: ...
    @cached_property
    def name(self) -> str: ...
    @cached_property
    def path(self) -> str: ...
    @cached_property
    def parent_path(self) -> str: ...
    @cached_property
    def parent(self) -> Optional[NyControl]: ...
    @property
    def position(self) -> FTuple2: ...
    @position.setter
    def position(self, val: FTuple2) -> None: ...
    @property
    def anchor_from(self) -> __Anchor: ...
    @anchor_from.setter
    def anchor_from(self, val: __Anchor) -> None: ...
    @property
    def anchor_to(self) -> __Anchor: ...
    @anchor_to.setter
    def anchor_to(self, val: __Anchor) -> None: ...
    @property
    def clip_offset(self) -> FTuple2: ...
    @clip_offset.setter
    def clip_offset(self, val: FTuple2) -> None: ...
    @property
    def clip_children(self) -> bool: ...
    @clip_children.setter
    def clip_children(self, val: bool) -> None: ...
    @property
    def full_position_x(self) -> __FullPositionParams: ...
    @full_position_x.setter
    def full_position_x(self, val: __FullPositionParams) -> None: ...
    @property
    def full_position_y(self) -> __FullPositionParams: ...
    @full_position_y.setter
    def full_position_y(self, val: __FullPositionParams) -> None: ...
    @property
    def full_size_x(self) -> __FullSizeParams: ...
    @full_size_x.setter
    def full_size_x(self, val: __FullSizeParams) -> None: ...
    @property
    def full_size_y(self) -> __FullSizeParams: ...
    @full_size_y.setter
    def full_size_y(self, val: __FullSizeParams) -> None: ...
    @property
    def global_position(self) -> FTuple2: ...
    @global_position.setter
    def global_position(self, val: FTuple2) -> None: ...
    @property
    def max_size(self) -> FTuple2: ...
    @max_size.setter
    def max_size(self, val: FTuple2) -> None: ...
    @property
    def min_size(self) -> FTuple2: ...
    @min_size.setter
    def min_size(self, val: FTuple2) -> None: ...
    @property
    def size(self) -> FTuple2: ...
    @size.setter
    def size(self, val: FTuple2) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, val: bool) -> None: ...
    @property
    def alpha(self) -> NoReturn: ...
    @alpha.setter
    def alpha(self, val: float) -> None: ...
    @property
    def layer(self) -> int: ...
    @layer.setter
    def layer(self, val: int) -> None: ...
    @property
    def touch_enable(self) -> NoReturn: ...
    @touch_enable.setter
    def touch_enable(self, val: bool) -> None: ...
    @property
    def property_bag(self) -> Optional[Dict[str, Any]]: ...
    @property_bag.setter
    def property_bag(self, val: Dict[str, Any]) -> None: ...
    @args_type_check(str, is_method=True)
    def __truediv__(self, other: str) -> Optional[NyControl]: ...
    __div__ = __truediv__
    def apply_attr(
        self,
        attr: Literal[
            "position",
            "anchor_from",
            "anchor_to",
            "clip_offset",
            "clip_children",
            "full_position_x",
            "full_position_y",
            "full_size_x",
            "full_size_y",
            "global_position",
            "max_size",
            "min_size",
            "size",
            "visible",
            "alpha",
            "layer",
            "touch_enable",
            "property_bag",
        ],
        value: Any,
        level: int = 1,
    ) -> None: ...
    def add_child(self, def_name: str, child_name: str, force_update: bool = True) -> Optional[NyControl]: ...
    def clone_to(
        self: T,
        parent: UiPathOrNyControl,
        name: str = "",
        sync_refresh: bool = True,
        force_update: bool = True,
    ) -> T: ...
    def clone_from(
        self,
        control: UiPathOrNyControl,
        name: str = "",
        sync_refresh: bool = True,
        force_update: bool = True,
    ) -> Optional[NyControl]: ...
    def children(self, level: int = 1) -> List[NyControl]: ...
    def children_path(self, level: int = 1) -> List[str]: ...
    @classmethod
    def from_path(
        cls: Type[T],
        screen_node_ex: ScreenNodeExtension,
        path: str,
        **kwargs: Any,
    ) -> T: ...
    @classmethod
    def from_control(
        cls: Type[T],
        screen_node_ex: ScreenNodeExtension,
        control: BaseUIControl,
        **kwargs: Any,
    ) -> T: ...
    def destroy(self) -> None: ...
    ApplyAttr = apply_attr
    AddChild = add_child
    CloneTo = clone_to
    CloneFrom = clone_from
    Children = children
    ChildrenPath = children_path
    FromPath = from_path
    FromControl = from_control
    Destroy = destroy
    def to_button(self, *, touch_event_params: Optional[dict] = None) -> Optional[NyButton]: ...
    def to_image(self) -> Optional[NyImage]: ...
    def to_label(self) -> Optional[NyLabel]: ...
    def to_input_panel(self) -> Optional[NyInputPanel]: ...
    def to_stack_panel(self) -> Optional[NyStackPanel]: ...
    def to_edit_box(self) -> Optional[NyEditBox]: ...
    def to_paper_doll(self) -> Optional[NyPaperDoll]: ...
    def to_item_renderer(self) -> Optional[NyItemRenderer]: ...
    def to_scroll_view(self) -> Optional[NyScrollView]: ...
    def to_grid(
        self,
        *,
        is_stack_grid: bool = False,
        template_name: str = "",
        cell_visible_binding: str = "",
        collection_name: str = "",
    ) -> Optional[NyGrid]: ...
    def to_progress_bar(self) -> Optional[NyProgressBar]: ...
    def to_toggle(self) -> Optional[NyToggle]: ...
    def to_slider(self) -> Optional[NySlider]: ...
    def to_selection_wheel(self) -> Optional[NySelectionWheel]: ...
    def to_combo_box(self) -> Optional[NyComboBox]: ...
    def to_mini_map(self) -> Optional[NyMiniMap]: ...
    ToButton = to_button
    ToImage = to_image
    ToLabel = to_label
    ToInputPanel = to_input_panel
    ToStackPanel = to_stack_panel
    ToEditBox = to_edit_box
    ToPaperDoll = to_paper_doll
    ToItemRenderer = to_item_renderer
    ToScrollView = to_scroll_view
    ToGrid = to_grid
    ToProgressBar = to_progress_bar
    ToToggle = to_toggle
    ToSlider = to_slider
    ToSelectionWheel = to_selection_wheel
    ToComboBox = to_combo_box
    ToMiniMap = to_mini_map
    SetPosition = BaseUIControl.SetPosition
    SetFullSize = BaseUIControl.SetFullSize
    GetFullSize = BaseUIControl.GetFullSize
    SetFullPosition = BaseUIControl.SetFullPosition
    GetFullPosition = BaseUIControl.GetFullPosition
    SetAnchorFrom = BaseUIControl.SetAnchorFrom
    GetAnchorFrom = BaseUIControl.GetAnchorFrom
    SetAnchorTo = BaseUIControl.SetAnchorTo
    GetAnchorTo = BaseUIControl.GetAnchorTo
    SetClipOffset = BaseUIControl.SetClipOffset
    GetClipOffset = BaseUIControl.GetClipOffset
    SetClipsChildren = BaseUIControl.SetClipsChildren
    GetClipsChildren = BaseUIControl.GetClipsChildren
    SetMaxSize = BaseUIControl.SetMaxSize
    GetMaxSize = BaseUIControl.GetMaxSize
    SetMinSize = BaseUIControl.SetMinSize
    GetMinSize = BaseUIControl.GetMinSize
    GetPosition = BaseUIControl.GetPosition
    GetGlobalPosition = BaseUIControl.GetGlobalPosition
    SetSize = BaseUIControl.SetSize
    GetSize = BaseUIControl.GetSize
    SetVisible = BaseUIControl.SetVisible
    GetVisible = BaseUIControl.GetVisible
    SetTouchEnable = BaseUIControl.SetTouchEnable
    SetAlpha = BaseUIControl.SetAlpha
    SetLayer = BaseUIControl.SetLayer
    GetPath = BaseUIControl.GetPath
    GetChildByName = BaseUIControl.GetChildByName
    GetChildByPath = BaseUIControl.GetChildByPath
    resetAnimation = BaseUIControl.resetAnimation
    PauseAnimation = BaseUIControl.PauseAnimation
    PlayAnimation = BaseUIControl.PlayAnimation
    StopAnimation = BaseUIControl.StopAnimation
    SetAnimation = BaseUIControl.SetAnimation
    RemoveAnimation = BaseUIControl.RemoveAnimation
    SetAnimEndCallback = BaseUIControl.SetAnimEndCallback
    RemoveAnimEndCallback = BaseUIControl.RemoveAnimEndCallback
    IsAnimEndCallbackRegistered = BaseUIControl.IsAnimEndCallbackRegistered
    GetPropertyBag = BaseUIControl.GetPropertyBag
    SetPropertyBag = BaseUIControl.SetPropertyBag