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


from typing import Dict, Optional, Union, List, Any
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
from ...core._types._typing import UiPathOrNyControl
from .nyc import NyControl


def is_top_ui(screen_name: str) -> bool: ...
def pop_to_hud() -> None: ...


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


def _is_ui_registered(ui_key: str) -> bool: ...
@deprecated("已废弃，请使用 ``@screen`` 装饰器创建UI")
def create_ui(
    namespace: str,
    ui_key: str,
    cls_path: str,
    screen_def: str = "",
    param: Optional[Dict[str, Any]] = None,
    client_system: Optional[ClientSystem] = None
) -> Union[ScreenNode, Any]: ...
@deprecated("已废弃，请使用 ``@screen`` 装饰器创建UI")
def push_ui(
    namespace: str,
    ui_key: str,
    cls_path: str,
    screen_def: str = "",
    param: Optional[dict] = None,
    client_system: Optional[ClientSystem] = None
) -> Union[ScreenNode, Any]: ...
def to_path(control: UiPathOrNyControl) -> str: ...
# @overload
def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: int = NyControl.BASE_CONTROL) -> Optional[BaseUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.BASE_CONTROL, NyControl.PANEL, NyControl.PAPER_DOLL, NyControl.GRADIENT_RENDERER]) -> Optional[BaseUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.LABEL]) -> Optional[LabelUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.BUTTON]) -> Optional[ButtonUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.IMAGE]) -> Optional[ImageUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.GRID]) -> Optional[GridUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.SCROLL_VIEW]) -> Optional[ScrollViewUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.TOGGLE]) -> Optional[SwitchToggleUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.EDIT_BOX]) -> Optional[TextEditBoxUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.PROGRESS_BAR]) -> Optional[ProgressBarUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.NETEASE_PAPER_DOLL]) -> Optional[NeteasePaperDollUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.MINI_MAP]) -> Optional[MiniMapUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.SLIDER]) -> Optional[SliderUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.ITEM_RENDERER]) -> Optional[ItemRendererUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.COMBO_BOX]) -> Optional[NeteaseComboBoxUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.INPUT_PANEL]) -> Optional[InputPanelUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.STACK_PANEL]) -> Optional[StackPanelUIControl]: ...
# @overload
# def to_control(screen_node: ScreenNode, path: UiPathOrNyControl, control_type: Literal[NyControl.SELECTION_WHEEL]) -> Optional[SelectionWheelUIControl]: ...
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
