# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-10
#  ⠀
#  ================================================


import sys
from typing import Generic, Type, Callable, ClassVar, TypedDict, Any, Literal, NoReturn, Dict, Optional, List, Union
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ....core._types._typing import UiPathOrNyControl, FTuple2, STuple, T, NyScreenBaseT
from ....core._types._checker import args_type_check
from ....core._utils import cached_property
from . import *
from ..screen_node import NyScreenBase


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
__AllowedApplyAttrs = Literal[
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
]


class InteractableControl(object):
    _callbacks: Dict[int, List[Callable]]
    _callback_setters: Dict[int, Union[tuple, Callable]]
    def __init__(self, callback_setters: Dict[int, Union[tuple, Callable]]) -> None: ...
    def __ui_destroy__(self) -> None: ...
    def _exec_callbacks(self, cb_type: int, *args: Any) -> None: ...
    def set_callback(self, func: Callable, *cb_types: int) -> None: ...
    def remove_callback(self, func: Callable, *cb_types: int) -> None: ...


class NyControlMeta(type):
    def __call__(cls: Type[T], ny_screen_node, path, **kwargs) -> T: ...


class NyControl(object):
    _ALLOWED_APPLY_ATTRS: ClassVar[STuple]
    _screen_node: ScreenNode
    _base_control: BaseUIControl
    _kwargs: Dict[str, Any]
    ny_screen_node: NyScreenBase
    """ 持有该控件的 ``NyScreenNode`` 或 ``NyScreenProxy`` 实例。 """
    def __init__(self, ny_screen_node: NyScreenBase, path: str) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __ui_destroy__(self) -> None: ...
    def __repr__(self) -> str: ...
    @cached_property
    def name(self) -> str: ...
    @cached_property
    def path(self) -> str: ...
    @cached_property
    def full_path(self) -> str: ...
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
    def clear_pos_data(self) -> bool: ...
    def save_pos(self) -> bool: ...
    def reset_pos(self) -> bool: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    def apply_attr(self, attr: __AllowedApplyAttrs, value: Any, level: int = 1) -> None: ...
    def has_child(self, path: str) -> bool: ...
    def get_child(self, path: str) -> Optional[NyControl]: ...
    def add_child(self, def_name: str, child_name: str, force_update: bool = True) -> Optional[NyControl]: ...
    def clone_to(
        self: T,
        parent: UiPathOrNyControl,
        name: str = "",
        sync_refresh: bool = True,
        force_update: bool = True,
    ) -> Optional[T]: ...
    def clone_from(
        self,
        control: UiPathOrNyControl,
        name: str = "",
        sync_refresh: bool = True,
        force_update: bool = True,
    ) -> Optional[NyControl]: ...
    def children(self, level: int = 1) -> List[NyControl]: ...
    def children_path(self, level: int = 1) -> List[str]: ...
    def destroy(self) -> None: ...
    def to_button(self, *, touch_event_params: Optional[dict] = None) -> NyButton: ...
    def to_image(self) -> NyImage: ...
    def to_label(self) -> NyLabel: ...
    def to_input_panel(self) -> NyInputPanel: ...
    def to_stack_panel(self) -> NyStackPanel: ...
    def to_edit_box(self) -> NyEditBox: ...
    def to_paper_doll(self) -> NyPaperDoll: ...
    def to_item_renderer(self) -> NyItemRenderer: ...
    def to_scroll_view(self) -> NyScrollView: ...
    def to_grid(
        self,
        *,
        is_stack_grid: bool = False,
        template_name: str = "",
        cell_visible_binding: str = "",
        collection_name: str = "",
    ) -> NyGrid: ...
    def to_progress_bar(self) -> NyProgressBar: ...
    def to_toggle(self) -> NyToggle: ...
    def to_slider(self) -> NySlider: ...
    def to_selection_wheel(self) -> NySelectionWheel: ...
    def to_combo_box(self) -> NyComboBox: ...
    def to_mini_map(self) -> NyMiniMap: ...
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
    set_touch_enable = BaseUIControl.SetTouchEnable
    reset_animation = BaseUIControl.resetAnimation
    pause_animation = BaseUIControl.PauseAnimation
    play_animation = BaseUIControl.PlayAnimation
    stop_animation = BaseUIControl.StopAnimation
    set_animation = BaseUIControl.SetAnimation
    remove_animation = BaseUIControl.RemoveAnimation
    set_anim_end_callback = BaseUIControl.SetAnimEndCallback
    remove_anim_end_callback = BaseUIControl.RemoveAnimEndCallback
    is_anim_end_callback_registered = BaseUIControl.IsAnimEndCallbackRegistered


if sys.version_info <= (2, 7):
    class NyControl(NyControl, Generic[NyScreenBaseT]):
        __metaclass__ = NyControlMeta
        ny_screen_node: NyScreenBaseT
        def __init__(self, ny_screen_node: NyScreenBaseT, path: str) -> None: ...
else:
    class NyControl(NyControl, Generic[NyScreenBaseT], metaclass=NyControlMeta):
        ny_screen_node: NyScreenBaseT
        def __init__(self, ny_screen_node: NyScreenBaseT, path: str) -> None: ...

