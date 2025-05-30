# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2025-05-30
#
# ====================================================


from typing import List, Optional, Callable, Dict, Tuple
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from ..._core._types._typing import UiControl, FTuple2
from ...utils import Enum


def to_button(screen_node: ScreenNode, control: UiControl) -> Optional[ButtonUIControl]: ...
def to_path(control: UiControl) -> str: ...
def to_control(screen_node: ScreenNode, path: UiControl) -> Optional[BaseUIControl]: ...
def save_ui_pos_data(key: str, data: Dict[str, List[Tuple[str, FTuple2]]]) -> bool: ...
def get_ui_pos_data(key: str) -> Dict[str, List[Tuple[str, FTuple2]]]: ...


class UIControlType:
    All: int
    Button: int
    Custom: int
    CollectionPanel: int
    Dropdown: int
    EditBox: int
    Factory: int
    Grid: int
    Image: int
    InputPanel: int
    Label: int
    Panel: int
    Screen: int
    ScrollbarBox: int
    ScrollTrack: int
    ScrollView: int
    SelectionWheel: int
    Slider: int
    SliderBox: int
    StackPanel: int
    Toggle: int
    ImageCycler: int
    LabelCycler: int
    GridPageIndicator: int
    Combox: int
    Layout: int
    StackGrid: int
    Joystick: int
    RichText: int
    SixteenNineLayout: int
    MulLinesEdit: int
    AminProcessBar: int
    Unknown: int


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


def get_all_children_path_by_level(control: UiControl, screen_node: ScreenNode, level: int = 1) -> List[str]: ...
def get_parent_path(control: UiControl) -> Optional[str]: ...
def get_parent_control(control: UiControl, screen_node: ScreenNode) -> Optional[BaseUIControl]: ...
def is_ui_out_of_screen(control: UiControl, screen_node: Optional[ScreenNode] = None) -> bool: ...
def notify_server(func: Callable) -> Callable: ...
