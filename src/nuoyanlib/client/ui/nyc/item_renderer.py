# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-11-30
|
| ====================================================
"""


from ....core import error
from ....utils.enum import ControlType
from .control import NyControl


__all__ = [
    "NyItemRenderer",
]


class NyItemRenderer(NyControl):
    """
    物品渲染器控件类。

    -----

    :param ScreenNodeExtension screen_node_ex: 物品渲染器所在UI类的实例（需继承ScreenNodeExtension）
    :param ItemRendererUIControl item_renderer_control: 通过asItemRenderer()等方式获取的ItemRendererUIControl实例
    """

    CONTROL_TYPE = ControlType.ITEM_RENDERER

    def __init__(self, screen_node_ex, item_renderer_control, **kwargs):
        NyControl.__init__(self, screen_node_ex, item_renderer_control)

    def __destroy__(self):
        NyControl.__destroy__(self)

    # region Properties ================================================================================================

    @property
    def item_name(self):
        """
        [可读写属性]

        ItemRenderer显示的物品的identifier。

        :rtype: str
        """
        return self._base_control.GetUiItem().get('itemName', "")

    @item_name.setter
    def item_name(self, val):
        """
        [可读写属性]

        ItemRenderer显示的物品的identifier。

        :type val: str
        """
        self._base_control.SetUiItem(val, self.item_aux, self.is_enchanted)

    @property
    def item_aux(self):
        """
        [可读写属性]

        ItemRenderer显示的物品的特殊值。

        :rtype: int
        """
        return self._base_control.GetUiItem().get('auxValue', 0)

    @item_aux.setter
    def item_aux(self, val):
        """
        [可读写属性]

        ItemRenderer显示的物品的特殊值。

        :type val: int
        """
        self._base_control.SetUiItem(self.item_name, val, self.is_enchanted)

    @property
    def is_enchanted(self):
        """
        [可读写属性]

        ItemRenderer显示的物品是否附魔。

        :rtype: bool
        """
        return self._base_control.GetUiItem().get('isEnchanted', False)

    @is_enchanted.setter
    def is_enchanted(self, val):
        """
        [可读写属性]

        ItemRenderer显示的物品是否附魔。

        :type val: bool
        """
        self._base_control.SetUiItem(self.item_name, self.item_aux, val)

    @property
    def user_data(self):
        """
        [只写属性]

        设置ItemRenderer显示的物品的UserData。

        :rtype: None
        """
        raise error.GetPropertyError("user_data")

    @user_data.setter
    def user_data(self, val):
        """
        [只写属性]

        设置ItemRenderer显示的物品的UserData。

        :type val: dict|None
        """
        self._base_control.SetUiItem(self.item_name, self.item_aux, self.is_enchanted, val)

    # endregion











