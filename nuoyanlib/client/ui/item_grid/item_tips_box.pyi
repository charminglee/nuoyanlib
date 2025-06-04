# -*- coding: utf-8 -*-
"""
| ===================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ===================================
"""


from typing import Optional
from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.imageUIControl import ImageUIControl
from mod.client.ui.controls.labelUIControl import LabelUIControl


_NAMESPACE: str
_TIPS_PANEL_NAME: str
_UI_NAME_ITEM_TIPS_BOX: str
_ANIM_NAME: str
_UI_PATH_TIPS_BG: str
_UI_PATH_TIPS_LABEL: str


class ItemTipsBox(object):
    __screen_node: ScreenNode
    item_tips_bg: Optional[ImageUIControl]
    item_tips_panel: Optional[BaseUIControl]
    item_tips_label: Optional[LabelUIControl]
    __follow: bool
    def __init__(self: ..., screen_node: ScreenNode) -> None: ...
    def Create(self) -> None: ...
    def Update(self) -> None: ...
    def ShowItemHoverTipsBox(
        self,
        item_dict: dict,
        show_category: bool = True,
        show_user_data: bool = True,
        follow: bool = False,
    ) -> bool: ...
    def ShowHoverTipsBox(self, text: str, follow: bool = False) -> bool: ...
    def HideHoverTipsBox(self) -> None: ...
    def _update_pos(self) -> None: ...
