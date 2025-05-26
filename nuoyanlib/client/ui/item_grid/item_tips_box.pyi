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
#   Last Modified : 2024-05-31
#
# ====================================================


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
