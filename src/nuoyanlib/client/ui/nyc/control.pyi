# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


from typing import Generic, Type, Callable, ClassVar, TypedDict, Any, Literal, NoReturn, Dict, Optional, List, Union
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ....core._types._typing import FTuple2, STuple, T, NyScreenBaseT
from ....core._types._checker import args_type_check
from ....core._utils import cached_property
from ..screen_node import NyScreenBase
from .button import NyButton
from .combo_box import NyComboBox
from .edit_box import NyEditBox
from .grid import NyGrid
from .image import NyImage
from .input_panel import NyInputPanel
from .item_renderer import NyItemRenderer
from .label import NyLabel
from .mini_map import NyMiniMap
from .paper_doll import NyPaperDoll
from .progress_bar import NyProgressBar
from .scroll_view import NyScrollView
from .selection_wheel import NySelectionWheel
from .slider import NySlider
from .stack_panel import NyStackPanel
from .toggle import NyToggle


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
    def exec_callbacks(self, cb_type: int, *args: Any) -> None: ...
    def set_callback(self, func: Callable, *cb_types: int) -> None: ...
    def remove_callback(self, func: Callable, *cb_types: int) -> None: ...


class NyControlMeta(type):
    def __call__(cls: Type[T], ny_screen_node: NyScreenBase, path: str, **kwargs: Any) -> T: ...


class NyControl(Generic[NyScreenBaseT], metaclass=NyControlMeta):
    __metaclass__ = NyControlMeta
    CONTROL_TYPE: ClassVar[int]
    ALLOWED_APPLY_ATTRS: ClassVar[STuple]
    _screen_node: ScreenNode
    _base_control: BaseUIControl
    _kwargs: Dict[str, Any]
    ny_screen_node: NyScreenBaseT
    """ 持有该控件的 ``NyScreenNode`` 或 ``NyScreenProxy`` 实例。 """
    def __init__(self, ny_screen_node: NyScreenBaseT, path: str) -> None: ...
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
    def parent(self) -> Optional[NyControl[NyScreenBaseT]]: ...
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
    def __truediv__(self, other: str) -> NyControl[NyScreenBaseT]: ...
    __div__ = __truediv__
    def apply_attr(self, attr: __AllowedApplyAttrs, value: Any, level: int = 1) -> None: ...
    def has_child(self, path: str) -> bool: ...
    def get_child(self, path: str) -> Optional[NyControl[NyScreenBaseT]]: ...
    def add_child(
        self,
        def_name: str,
        child_name: str,
        force_update: bool = True,
    ) -> Optional[NyControl[NyScreenBaseT]]: ...
    def clone_to(
        self: T,
        parent: Union[str, NyControl[NyScreenBaseT]],
        name: str = "",
        sync_refresh: bool = True,
        force_update: bool = True,
    ) -> Optional[T]: ...
    def clone_from(
        self,
        control: Union[str, NyControl[NyScreenBaseT]],
        name: str = "",
        sync_refresh: bool = True,
        force_update: bool = True,
    ) -> Optional[NyControl[NyScreenBaseT]]: ...
    def children(self, level: int = 1) -> List[NyControl[NyScreenBaseT]]: ...
    def children_path(self, level: int = 1) -> List[str]: ...
    def destroy(self) -> None: ...
    @classmethod
    def auto(cls, ny_screen_node: T, path: str) -> NyControl[T]: ...
    def _try_convert(self, base_control: BaseUIControl) -> BaseUIControl: ...
    def to_button(self, *, touch_event_params: Optional[dict] = None) -> NyButton[NyScreenBaseT]: ...
    def to_image(self) -> NyImage[NyScreenBaseT]: ...
    def to_label(self) -> NyLabel[NyScreenBaseT]: ...
    def to_input_panel(self) -> NyInputPanel[NyScreenBaseT]: ...
    def to_stack_panel(self) -> NyStackPanel[NyScreenBaseT]: ...
    def to_edit_box(self) -> NyEditBox[NyScreenBaseT]: ...
    def to_paper_doll(self) -> NyPaperDoll[NyScreenBaseT]: ...
    def to_item_renderer(self) -> NyItemRenderer[NyScreenBaseT]: ...
    def to_scroll_view(self) -> NyScrollView[NyScreenBaseT]: ...
    def to_grid(
        self,
        *,
        is_stack_grid: bool = False,
        template_name: str = "",
        cell_visible_binding: str = "",
        collection_name: str = "",
    ) -> NyGrid[NyScreenBaseT]: ...
    def to_progress_bar(self) -> NyProgressBar[NyScreenBaseT]: ...
    def to_toggle(self) -> NyToggle[NyScreenBaseT]: ...
    def to_slider(self) -> NySlider[NyScreenBaseT]: ...
    def to_selection_wheel(self) -> NySelectionWheel[NyScreenBaseT]: ...
    def to_combo_box(self) -> NyComboBox[NyScreenBaseT]: ...
    def to_mini_map(self) -> NyMiniMap[NyScreenBaseT]: ...
    set_position = SetPosition = BaseUIControl.SetPosition
    set_full_size = SetFullSize = BaseUIControl.SetFullSize
    get_full_size = GetFullSize = BaseUIControl.GetFullSize
    set_full_position = SetFullPosition = BaseUIControl.SetFullPosition
    get_full_position = GetFullPosition = BaseUIControl.GetFullPosition
    set_anchor_from = SetAnchorFrom = BaseUIControl.SetAnchorFrom
    get_anchor_from = GetAnchorFrom = BaseUIControl.GetAnchorFrom
    set_anchor_to = SetAnchorTo = BaseUIControl.SetAnchorTo
    get_anchor_to = GetAnchorTo = BaseUIControl.GetAnchorTo
    set_clip_offset = SetClipOffset = BaseUIControl.SetClipOffset
    get_clip_offset = GetClipOffset = BaseUIControl.GetClipOffset
    set_clips_children = SetClipsChildren = BaseUIControl.SetClipsChildren
    get_clips_children = GetClipsChildren = BaseUIControl.GetClipsChildren
    set_max_size = SetMaxSize = BaseUIControl.SetMaxSize
    get_max_size = GetMaxSize = BaseUIControl.GetMaxSize
    set_min_size = SetMinSize = BaseUIControl.SetMinSize
    get_min_size = GetMinSize = BaseUIControl.GetMinSize
    get_position = GetPosition = BaseUIControl.GetPosition
    get_global_position = GetGlobalPosition = BaseUIControl.GetGlobalPosition
    set_size = SetSize = BaseUIControl.SetSize
    get_size = GetSize = BaseUIControl.GetSize
    set_visible = SetVisible = BaseUIControl.SetVisible
    get_visible = GetVisible = BaseUIControl.GetVisible
    set_touch_enable = SetTouchEnable = BaseUIControl.SetTouchEnable
    set_alpha = SetAlpha = BaseUIControl.SetAlpha
    set_layer = SetLayer = BaseUIControl.SetLayer
    get_path = GetPath = BaseUIControl.GetPath
    get_child_by_name = GetChildByName = BaseUIControl.GetChildByName
    get_child_by_path = GetChildByPath = BaseUIControl.GetChildByPath
    reset_animation = resetAnimation = BaseUIControl.resetAnimation
    pause_animation = PauseAnimation = BaseUIControl.PauseAnimation
    play_animation = PlayAnimation = BaseUIControl.PlayAnimation
    stop_animation = StopAnimation = BaseUIControl.StopAnimation
    set_animation = SetAnimation = BaseUIControl.SetAnimation
    remove_animation = RemoveAnimation = BaseUIControl.RemoveAnimation
    set_anim_end_callback = SetAnimEndCallback = BaseUIControl.SetAnimEndCallback
    remove_anim_end_callback = RemoveAnimEndCallback = BaseUIControl.RemoveAnimEndCallback
    is_anim_end_callback_registered = IsAnimEndCallbackRegistered = BaseUIControl.IsAnimEndCallbackRegistered
    get_property_bag = GetPropertyBag = BaseUIControl.GetPropertyBag
    set_property_bag = SetPropertyBag = BaseUIControl.SetPropertyBag
