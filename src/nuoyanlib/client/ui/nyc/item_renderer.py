# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


if bool(0):
    from ..screen_node import NyScreenNode, NyScreenProxy


from ....core import error
from ..ui_utils import _UIControlType
from .control import NyControl


__all__ = [
    "NyItemRenderer",
]


class NyItemRenderer(NyControl):
    """
    物品渲染器控件类。

    -----

    :param NyScreenNode|NyScreenProxy ny_screen_node: 持有该物品渲染器控件的 NyScreenNode 或 NyScreenProxy 实例
    :param str path: 控件路径
    """

    CONTROL_TYPE = _UIControlType.ITEM_RENDERER

    def __init__(self, ny_screen_node, path, **kwargs):
        NyControl.__init__(self, ny_screen_node, path)

    def __ui_destroy__(self):
        NyControl.__ui_destroy__(self)

    # region Properties ================================================================================================

    @property
    def item_name(self):
        """
        [可读写属性]

        ItemRenderer 显示的物品的 identifier。

        :rtype: str
        """
        return self._base_control.GetUiItem().get('itemName', "")

    @item_name.setter
    def item_name(self, val):
        """
        [可读写属性]

        ItemRenderer 显示的物品的 identifier。

        :type val: str
        """
        self._base_control.SetUiItem(val, self.item_aux, self.is_enchanted)

    @property
    def item_aux(self):
        """
        [可读写属性]

        ItemRenderer 显示的物品的特殊值。

        :rtype: int
        """
        return self._base_control.GetUiItem().get('auxValue', 0)

    @item_aux.setter
    def item_aux(self, val):
        """
        [可读写属性]

        ItemRenderer 显示的物品的特殊值。

        :type val: int
        """
        self._base_control.SetUiItem(self.item_name, val, self.is_enchanted)

    @property
    def is_enchanted(self):
        """
        [可读写属性]

        物品渲染器显示的物品是否附魔。

        :rtype: bool
        """
        return self._base_control.GetUiItem().get('isEnchanted', False)

    @is_enchanted.setter
    def is_enchanted(self, val):
        """
        [可读写属性]

        物品渲染器显示的物品是否附魔。

        :type val: bool
        """
        self._base_control.SetUiItem(self.item_name, self.item_aux, val)

    @property
    def user_data(self):
        """
        [只写属性]

        设置物品渲染器显示的物品的 UserData 。

        :rtype: None
        """
        raise error.GetPropertyError("user_data")

    @user_data.setter
    def user_data(self, val):
        """
        [只写属性]

        设置物品渲染器显示的物品的 UserData 。

        :type val: dict|None
        """
        self._base_control.SetUiItem(self.item_name, self.item_aux, self.is_enchanted, val)

    # endregion

    # region Compatibility =============================================================================================

    set_ui_item = SetUiItem = lambda s, *a, **k: s._base_control.SetUiItem(*a, **k)
    get_ui_item = GetUiItem = lambda s, *a, **k: s._base_control.GetUiItem(*a, **k)

    # endregion





