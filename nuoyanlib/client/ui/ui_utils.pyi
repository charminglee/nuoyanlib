# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-20
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
from ..._core._types._typing import UiPathOrControl, FTuple2
from ...utils.enum import ControlType


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
