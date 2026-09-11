# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-11
#  ⠀
#  ================================================


from typing import Dict, Optional, Union, List, Any
from typing_extensions import deprecated
from mod.client.system.clientSystem import ClientSystem
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from ...core._types._typing import UiPathOrNyControl
from .screen_node import NyScreenBase


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
    NETEASE_PAPER_DOLL: int
    ITEM_RENDERER: int
    PROGRESS_BAR: int
    COMBO_BOX: int
    MINI_MAP: int


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
def _to_path(control: UiPathOrNyControl) -> str: ...
def get_children_path_by_level(
    control: UiPathOrNyControl,
    ny_screen_node: NyScreenBase,
    level: int = 1,
) -> List[str]: ...
def get_children_by_level(
    control: UiPathOrNyControl,
    ny_screen_node: NyScreenBase,
    level: int = 1,
) -> List[BaseUIControl]: ...
def get_parent_path(control: UiPathOrNyControl) -> Optional[str]: ...
def get_parent(control: UiPathOrNyControl, ny_screen_node: NyScreenBase) -> Optional[BaseUIControl]: ...
def is_out_of_screen(control: UiPathOrNyControl, ny_screen_node: Optional[NyScreenBase] = None) -> bool: ...
