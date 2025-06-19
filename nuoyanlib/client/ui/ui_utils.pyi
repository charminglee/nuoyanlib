# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-10
|
| ==============================================
"""


from typing import List, Optional, Callable, Dict, Tuple, Union, Generator
from typing_extensions import deprecated
from mod.client.system.clientSystem import ClientSystem
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.labelUIControl import LabelUIControl
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.imageUIControl import ImageUIControl
from mod.client.ui.controls.gridUIControl import GridUIControl
from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from mod.client.ui.controls.progressBarUIControl import ProgressBarUIControl
from mod.client.ui.controls.neteasePaperDollUIControl import NeteasePaperDollUIControl
from mod.client.ui.controls.minimapUIControl import MiniMapUIControl
from mod.client.ui.controls.sliderUIControl import SliderUIControl
from mod.client.ui.controls.itemRendererUIControl import ItemRendererUIControl
from mod.client.ui.controls.neteaseComboBoxUIControl import NeteaseComboBoxUIControl
from mod.client.ui.controls.inputPanelUIControl import InputPanelUIControl
from mod.client.ui.controls.stackPanelUIControl import StackPanelUIControl
from mod.client.ui.controls.selectionWheelUIControl import SelectionWheelUIControl
from ..._core._types._typing import UiPathOrControl, FTuple2, STuple
from ...utils import Enum


def create_ui(
    namespace: str,
    ui_key: str,
    cls_path: str,
    screen_def: str,
    register: bool = True,
    param: Optional[dict] = None,
    push: bool = False,
    client_system: Optional[ClientSystem] = None
) -> Optional[ScreenNode]: ...


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


def to_path(control: UiPathOrControl) -> str: ...
def to_control(
    screen_node: ScreenNode,
    path: UiPathOrControl,
    control_type: str = ControlType.base_control,
) -> Union[
    BaseUIControl,
    LabelUIControl,
    ButtonUIControl,
    ImageUIControl,
    GridUIControl,
    ScrollViewUIControl,
    SwitchToggleUIControl,
    TextEditBoxUIControl,
    ProgressBarUIControl,
    NeteasePaperDollUIControl,
    MiniMapUIControl,
    SliderUIControl,
    ItemRendererUIControl,
    NeteaseComboBoxUIControl,
    InputPanelUIControl,
    StackPanelUIControl,
    SelectionWheelUIControl,
    None,
]: ...
def save_ui_pos_data(key: str, data: Dict[str, List[Tuple[str, FTuple2]]]) -> bool: ...
def get_ui_pos_data(key: str) -> Dict[str, List[Tuple[str, FTuple2]]]: ...


class ButtonCallback(Enum[int]):
    touch_up: int
    touch_down: int
    touch_cancel: int
    touch_move: int
    touch_move_in: int
    touch_move_out: int
    double_click: int
    long_click: int
    hover_in: int
    hover_out: int
    screen_exit: int


def get_children_path_by_level(
    control: UiPathOrControl,
    screen_node: ScreenNode,
    level: int = 1,
) -> Generator[str, None, None]: ...
def get_children_control_by_level(
    control: UiPathOrControl,
    screen_node: ScreenNode,
    level: int = 1,
) -> Generator[BaseUIControl, None, None]: ...
def get_parent_path(control: UiPathOrControl) -> Optional[str]: ...
def get_parent_control(control: UiPathOrControl, screen_node: ScreenNode) -> Optional[BaseUIControl]: ...
def is_ui_out_of_screen(control: UiPathOrControl, screen_node: Optional[ScreenNode] = None) -> bool: ...
@deprecated("已废弃，将在未来版本中移除。")
def notify_server(func: Callable) -> Callable: ...
