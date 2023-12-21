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
#   Last Modified : 2023-11-30
#
# ====================================================


from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.imageUIControl import ImageUIControl
from mod.client.ui.controls.labelUIControl import LabelUIControl
from mod.common.utils.timer import CallLater


_PATH: str
_NAMESPACE: str
_UI_NAME_ITEM_TIPS_BOX: str
_UI_PATH_ITEM_TIPS_BOX: str
_UI_DEF_ITEM_TIPS_BOX: str
_UI_PATH_TIPS_IMAGE: str
_UI_PATH_TIPS: str
_UI_PATH_TIPS_LABEL: str


class ItemTipsBox(ScreenNode):
    _item_tips_box_node: _ItemTipsBoxUI
    def __init__(self, namespace: str, name: str, param: dict) -> None: ...
    def __register(self) -> None: ...
    def ShowItemHoverTipsBox(self, item_dict: dict) -> None: ...
    def ShowTipsBox(self, text: str) -> None: ...
    def HideTipsBox(self) -> None: ...


class _ItemTipsBoxUI(ScreenNode):
    alpha_tick: int
    tips_img: ImageUIControl
    tips_panel: BaseUIControl
    tips_label: LabelUIControl
    timer1: CallLater
    timer2: CallLater
    def __init__(self, namespace: str, name: str, param: dict) -> None: ...
    def Create(self) -> None: ...
    def Update(self) -> None: ...
    def ShowItemHoverTipsBox(self, item_dict: dict) -> None: ...
    def ShowTipsBox(self, text: str) -> None: ...
    def HideTipsBox(self) -> None: ...














