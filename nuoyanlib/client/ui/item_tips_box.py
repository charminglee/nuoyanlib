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


"""

itemTipsBox
===========

该模块提供了物品悬浮文本框的Python实现，即打开背包后点击物品出现的文本框。通过ItemTipsBox，您可以在任何位置任何时候显示与原版几乎一模一样的物品悬浮文本框。

-----

【使用方法】

1、将NyItemTipsBox.json放到资源包的ui文件夹内，然后在_ui_def.json中填入"ui/NyItemTipsBox.json"。

2、将您的UI类继承ItemTipsBox，此后无需再继承ScreenNode，例如：class MyUi(ItemTipsBox)，然后正常注册与创建您的UI。

3、通过调用相关接口即可显示物品悬浮文本框。

-----

【注意事项】

1、目前暂不支持通过堆栈管理方式创建的UI。

"""


import mod.client.extraClientApi as api
from ...utils.item import is_empty_item as _is_empty_item
from ..comp import (
    LvComp as _LvComp,
    ScreenNode as _ScreenNode,
)


__all__ = [
    "ItemTipsBox",
]


_PATH = __file__.replace(".py", "").replace("/", ".")
_NAMESPACE = "NuoyanLib"
_UI_NAME_ITEM_TIPS_BOX = "NyItemTipsBox"
_UI_PATH_ITEM_TIPS_BOX = _PATH + "._ItemTipsBoxUI"
_UI_DEF_ITEM_TIPS_BOX = "NyItemTipsBox.main"
_UI_PATH_TIPS_IMAGE = "/tips_panel/image"
_UI_PATH_TIPS = "/tips_panel"
_UI_PATH_TIPS_LABEL = "/tips_panel/image/label"


class ItemTipsBox(_ScreenNode):
    """
    为原版ScreenNode提供物品悬浮文本显示支持。
    """

    def __init__(self, namespace, name, param):
        # noinspection PySuperArguments
        super(ItemTipsBox, self).__init__(namespace, name, param)
        self._item_tips_box_node = None
        self.__register()

    def __register(self):
        node = api.GetUI(_NAMESPACE, _UI_NAME_ITEM_TIPS_BOX)
        if node:
            self._item_tips_box_node = node
        else:
            api.RegisterUI(
                _NAMESPACE, _UI_NAME_ITEM_TIPS_BOX, _UI_PATH_ITEM_TIPS_BOX, _UI_DEF_ITEM_TIPS_BOX
            )
            self._item_tips_box_node = api.CreateUI(
                _NAMESPACE, _UI_NAME_ITEM_TIPS_BOX, {'isHud': 1, '__cs__': self}
            )

    def ShowItemHoverTipsBox(self, item_dict):
        """
        显示物品悬浮文本框。

        -----

        :param dict item_dict: 物品信息字典

        :return: 无
        :rtype: None
        """
        self._item_tips_box_node.ShowItemHoverTipsBox(item_dict)

    def ShowTipsBox(self, text):
        """
        显示自定义内容的悬浮文本框。

        -----

        :param str text: 文本内容

        :return: 无
        :rtype: None
        """
        self._item_tips_box_node.ShowTipsBox(text)

    def HideTipsBox(self):
        """
        隐藏悬浮文本框。

        -----

        :return: 无
        :rtype: None
        """
        self._item_tips_box_node.HideTipsBox()


class _ItemTipsBoxUI(_ScreenNode):
    def __init__(self, namespace, name, param):
        super(_ItemTipsBoxUI, self).__init__(namespace, name, param)
        self.alpha_tick = 0
        self.tips_img = None
        self.tips_panel = None
        self.tips_label = None
        self.timer1 = None
        self.timer2 = None

    def Create(self):
        self.tips_label = self.GetBaseUIControl(_UI_PATH_TIPS_LABEL).asLabel()
        self.tips_panel = self.GetBaseUIControl(_UI_PATH_TIPS)
        self.tips_img = self.GetBaseUIControl(_UI_PATH_TIPS_IMAGE).asImage()
        self.SetScreenVisible(False)

    def Update(self):
        # tips透明度动画
        if self.alpha_tick:
            self.alpha_tick -= 1
            alpha = self.alpha_tick / 30.0
            self.tips_img.SetAlpha(alpha)
            self.tips_label.SetAlpha(alpha)

    # ========================================= Basic Function =========================================================

    def ShowItemHoverTipsBox(self, item_dict):
        if _is_empty_item(item_dict):
            return
        name = item_dict['newItemName']
        aux = item_dict.get('newAuxValue', 0)
        if aux == -1:
            aux = 0
        user_data = item_dict.get('userData')
        text = _LvComp.Item.GetItemFormattedHoverText(name, aux, True, user_data)
        self.ShowTipsBox(text)

    def ShowTipsBox(self, text):
        # 显示文本框
        self.SetScreenVisible(True)
        self.alpha_tick = 0
        self.tips_img.SetAlpha(1.0)
        self.tips_label.SetAlpha(1.0)
        self.tips_label.SetText(text)
        # 取消正在执行的timer
        if self.timer1:
            _LvComp.Game.CancelTimer(self.timer1)
        if self.timer2:
            _LvComp.Game.CancelTimer(self.timer2)
        # 一秒后执行渐出动画
        def func1():
            self.alpha_tick = 30
            self.timer1 = None
        self.timer1 = _LvComp.Game.AddTimer(1, func1)
        # 两秒后隐藏文本框并恢复初始状态
        def func2():
            self.HideTipsBox()
            self.timer2 = None
        self.timer2 = _LvComp.Game.AddTimer(2, func2)

    def HideTipsBox(self):
        if self.timer1:
            _LvComp.Game.CancelTimer(self.timer1)
            self.timer1 = None
        if self.timer2:
            _LvComp.Game.CancelTimer(self.timer2)
            self.timer2 = None
        self.alpha_tick = 0
        self.tips_img.SetAlpha(1.0)
        self.tips_label.SetAlpha(1.0)
        self.SetScreenVisible(False)

















