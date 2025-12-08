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


from typing import Optional, Union, List, Any, overload, Literal
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
from ...core._types._typing import UiPathOrNyControl
from ...utils.enum import ControlType


class _UIControlType:
    ALL: int
    BUTTON: int
    CUSTOM: int
    COLLECTION_PANEL: int
    DROPDOWN: int
    EDIT_BOX: int
    FACTORY: int
    GRID: int
    IMAGE: int
    INPUT_PANEL: int
    LABEL: int
    PANEL: int
    SCREEN: int
    SCROLLBAR_BOX: int
    SCROLL_TRACK: int
    SCROLL_VIEW: int
    SELECTION_WHEEL: int
    SLIDER: int
    SLIDER_BOX: int
    STACK_PANEL: int
    TOGGLE: int
    IMAGE_CYCLER: int
    LABEL_CYCLER: int
    GRID_PAGE_INDICATOR: int
    COMBOX: int
    LAYOUT: int
    STACK_GRID: int
    JOYSTICK: int
    RICH_TEXT: int
    SIXTEEN_NINE_LAYOUT: int
    MUL_LINES_EDIT: int
    AMIN_PROCESS_BAR: int
    UNKNOWN: int


def create_ui(
    namespace: str,
    ui_key: str,
    cls_path: str,
    screen_def: str = "",
    register: bool = True,
    param: Optional[dict] = None,
    push: bool = False,
    client_system: Optional[ClientSystem] = None
) -> Union[ScreenNode, Any]: ...
def to_path(control: UiPathOrNyControl) -> str: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["BaseControl", "Panel", "PaperDoll", "GradientRenderer"]) -> BaseUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["Label"]) -> LabelUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["Button"]) -> ButtonUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["Image"]) -> ImageUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["Grid"]) -> GridUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["ScrollView"]) -> ScrollViewUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["SwitchToggle"]) -> SwitchToggleUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["TextEditBox"]) -> TextEditBoxUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["ProgressBar"]) -> ProgressBarUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["NeteasePaperDoll"]) -> NeteasePaperDollUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["MiniMap"]) -> MiniMapUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["Slider"]) -> SliderUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["ItemRenderer"]) -> ItemRendererUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["NeteaseComboBox"]) -> NeteaseComboBoxUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["InputPanel"]) -> InputPanelUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["StackPanel"]) -> StackPanelUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal["SelectionWheel"]) -> SelectionWheelUIControl: ...
@overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: str = ControlType.BASE_CONTROL) -> BaseUIControl: ...
def get_children_path_by_level(
    control: UiPathOrNyControl,
    screen_node: ScreenNode,
    level: int = 1,
) -> List[str]: ...
def get_children_by_level(
    control: UiPathOrNyControl,
    screen_node: ScreenNode,
    level: int = 1,
) -> List[BaseUIControl]: ...
def get_parent_path(control: UiPathOrNyControl) -> Optional[str]: ...
def get_parent(control: UiPathOrNyControl, screen_node: ScreenNode) -> Optional[BaseUIControl]: ...
def is_out_of_screen(control: UiPathOrNyControl, screen_node: Optional[ScreenNode] = None) -> bool: ...
