# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-13
|
| ====================================================
"""


from typing import List, Tuple, Iterator, TypedDict, ClassVar, Optional, overload, Any, Dict, Type, Generator, Callable, Union
from mod.client.ui.screenNode import ScreenNode
from mod.client.system.clientSystem import ClientSystem
from ...core._types._typing import Self, FTuple2, Args, Kwargs, UiPathOrControl, NyControlTypes, ArgsDict, T, FuncDecorator
from .nyc import *
from ...utils.enum import ButtonCallbackType


class __FrameAnimData(TypedDict):
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


class ScreenNodeExtension(object):
    ROOT_PANEL_PATH: ClassVar[str]
    """
    基类画布的根面板（root_screen_panel）路径。
    """
    _nyc_cache_map: Dict[str, NyControlTypes]
    _ui_pos_data_key: str
    _screen_node: ScreenNode
    _frame_anim_data: Dict[str, __FrameAnimData]
    _binging_data: Dict[Callable, Callable]
    cs: Union[ClientSystem, Any]
    """
    创建该UI的客户端实例。
    """
    root_panel: NyControl
    """
    当前界面根面板的 ``NyControl`` 实例。
    
    当界面继承基类画布时，根面板为 ``root_screen_panel`` ，路径为 ``"/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"`` 。
    否则根面板为画布本身，路径为空字符串 ``""`` 。
    """
    has_created: bool
    """
    UI界面是否已创建完成。
    
    若 ``has_created`` 为True，此时UI界面的 ``.Create()`` 或 ``.OnCreate()`` 方法已执行完毕。
    """
    is_base_screen: bool
    """
    是否是基类画布。
    """
    @overload
    def __init__(self: Self, namespace: str, name: str, param: Optional[dict] = None, /) -> None: ...
    @overload
    def __init__(self: Self, screen_name: str, screen_node: ScreenNode, /) -> None: ...
    def __create__(self): ...
    def __destroy__(self): ...
    def _OnRenderTick(self, args: ArgsDict) -> None: ...
    def build_binding(self, func: Callable, flag: int, binding_name: str = "", collection_name: str = "") -> bool: ...
    def unbuild_binding(self, func: Callable) -> bool: ...
    def _create_binding_proxy(
        self,
        func: Callable,
        flag: int,
        binding_name: str = "",
        collection_name: str = "",
    ) -> Callable: ...
    def create_ny_control(self, path_or_control: UiPathOrControl) -> Optional[NyControl]: ...
    def create_ny_button(
        self,
        path_or_control: UiPathOrControl,
        *,
        touch_event_params: Optional[dict] = None
    ) -> Optional[NyButton]: ...
    def create_ny_combo_box(self, path_or_control: UiPathOrControl) -> Optional[NyComboBox]: ...
    def create_ny_edit_box(self, path_or_control: UiPathOrControl) -> Optional[NyEditBox]: ...
    def create_ny_grid(
        self,
        path_or_control: UiPathOrControl,
        *,
        is_stack_grid: bool = False,
        template_name: str = "",
        cell_visible_binding: str = "",
        collection_name: str = "",
    ) -> Optional[NyGrid]: ...
    def create_ny_image(self, path_or_control: UiPathOrControl) -> Optional[NyImage]: ...
    def create_ny_input_panel(self, path_or_control: UiPathOrControl) -> Optional[NyInputPanel]: ...
    def create_ny_item_renderer(self, path_or_control: UiPathOrControl) -> Optional[NyItemRenderer]: ...
    def create_ny_label(self, path_or_control: UiPathOrControl) -> Optional[NyLabel]: ...
    def create_ny_mini_map(self, path_or_control: UiPathOrControl) -> Optional[NyMiniMap]: ...
    def create_ny_paper_doll(self, path_or_control: UiPathOrControl) -> Optional[NyPaperDoll]: ...
    def create_ny_progress_bar(self, path_or_control: UiPathOrControl) -> Optional[NyProgressBar]: ...
    def create_ny_scroll_view(self, path_or_control: UiPathOrControl) -> Optional[NyScrollView]: ...
    def create_ny_selection_wheel(self, path_or_control: UiPathOrControl) -> Optional[NySelectionWheel]: ...
    def create_ny_slider(self, path_or_control: UiPathOrControl) -> Optional[NySlider]: ...
    def create_ny_stack_panel(self, path_or_control: UiPathOrControl) -> Optional[NyStackPanel]: ...
    def create_ny_toggle(self, path_or_control: UiPathOrControl) -> Optional[NyToggle]: ...
    CreateNyControl = create_ny_control
    CreateNyButton = create_ny_button
    CreateNyComboBox = create_ny_combo_box
    CreateNyEditBox = create_ny_edit_box
    CreateNyGrid = create_ny_grid
    CreateNyImage = create_ny_image
    CreateNyInputPanel = create_ny_input_panel
    CreateNyItemRenderer = create_ny_item_renderer
    CreateNyLabel = create_ny_label
    CreateNyMiniMap = create_ny_mini_map
    CreateNyPaperDoll = create_ny_paper_doll
    CreateNyProgressBar = create_ny_progress_bar
    CreateNyScrollView = create_ny_scroll_view
    CreateNySelectionWheel = create_ny_selection_wheel
    CreateNySlider = create_ny_slider
    CreateNyStackPanel = create_ny_stack_panel
    CreateNyToggle = create_ny_toggle
    def _create_nyc(self, path_or_control: UiPathOrControl, typ: Type[T] = NyControl, **kwargs: Any) -> T: ...
    def _destroy_nyc(self, nyc: NyControl) -> None: ...
    @staticmethod
    def button_callback(
        btn_path: str,
        *callback_types: ButtonCallbackType,
        touch_event_params: Optional[dict] = None,
    ) -> FuncDecorator: ...
    def _process_button_callback(self) -> None: ...
    def _expend_path(self, path: str) -> Generator[str]: ...
    def clear_all_pos_data(self) -> bool: ...
    def save_all_pos_data(self) -> bool: ...
    ClearAllPosData = clear_all_pos_data
    SaveAllPosData = save_all_pos_data
    def _save_ui_pos_data(self, data: Dict[str, List[Tuple[str, FTuple2]]]) -> bool: ...
    def _get_ui_pos_data(self) -> Dict[str, List[Tuple[str, FTuple2]]]: ...
    def _recover_ui_pos(self) -> None: ...
    def _play_frame_anim(
        self,
        ny_image: NyImage,
        tex_path: str,
        frame_count: int,
        frame_rate: int,
        stop_frame: int = -1,
        loop: bool = False,
        callback: Optional[Callable] = None,
        args: Optional[Args] = None,
        kwargs: Optional[Kwargs] = None,
    ) -> None: ...
    def _pause_frame_anim(self, ny_image: NyImage) -> None: ...
    def _stop_frame_anim(self, ny_image: NyImage) -> None: ...
    def _OnGridSizeChanged(self, args: ArgsDict) -> None: ...
    def _is_control_exist(self, path: str) -> bool: ...
