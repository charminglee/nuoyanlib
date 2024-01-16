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
#   Last Modified : 2024-01-15
#
# ====================================================


from ...utils.item import is_empty_item as _is_empty_item
from ..comp import (
    ScreenNode as _ScreenNode,
    ViewBinder as _ViewBinder,
    LvComp as _LvComp,
)


__all__ = [
    "ItemFlyAnim",
]


_ITEM_FLY_PANEL_NAME = "ny_item_fly_panel"
_UI_NAME_ITEM_FLY_PANEL = "NyItemFlyAnim." + _ITEM_FLY_PANEL_NAME
_UI_PATH_FLY_ITEM_0 = "/%s/0" % _UI_NAME_ITEM_FLY_PANEL


class ItemFlyAnim(_ScreenNode):
    """
    为原版ScreenNode提供物品飞行动画支持。
    """

    def __init__(self, namespace, name, param):
        # noinspection PySuperArguments
        super(ItemFlyAnim, self).__init__(namespace, name, param)
        self._item_fly_queue = {}
        self._fly_ir = []

    def Create(self):
        """
        *[event]*

        UI生命周期函数，当UI创建成功时调用。

        若重写了该方法，请调用一次父类的同名方法，否则部分功能将不可用。如：

        >>> class MyUI(ItemFlyAnim):
        ...     def Create(self):
        ...         super(MyUI, self).Create()

        -----

        :return: 无
        :rtype: None
        """
        # noinspection PySuperArguments
        super(ItemFlyAnim, self).Create()
        panel = self.CreateChildControl(_UI_NAME_ITEM_FLY_PANEL, _ITEM_FLY_PANEL_NAME)
        self._fly_ir.append(panel.GetChildByName("0").asItemRenderer())
        self._fly_ir.append(panel.GetChildByName("1").asItemRenderer())

    @_ViewBinder.binding(_ViewBinder.BF_BindString, "#main.gametick")
    def _OnGameTick(self):
        # 物品飞行动画
        for k, data in self._item_fly_queue.items():
            x = data['x_off']
            y = data['y_off']
            ui_ctrl = data['ui_ctrl']
            pos = ui_ctrl.GetPosition()
            ui_ctrl.SetPosition((pos[0] + x, pos[1] + y))
            data['tick'] -= 1
            # 动画结束
            if data['tick'] <= 0:
                ui_ctrl.SetVisible(False)
                del self._item_fly_queue[k]

    def _clone_new_ir(self):
        name = str(len(self._fly_ir))
        if self.Clone(_UI_PATH_FLY_ITEM_0, "/" + _ITEM_FLY_PANEL_NAME, name):
            ir = self.GetBaseUIControl("/%s/%s" % (_ITEM_FLY_PANEL_NAME, name)).asItemRenderer()
            self._fly_ir.append(ir)
            return ir

    def _get_idle_ir_index(self):
        for i in range(len(self._fly_ir)):
            if i not in self._item_fly_queue:
                return i

    def SetOneItemFlyAnim(self, item_dict, from_pos, to_pos, ui_size):
        """
        设置单个物品飞行动画。

        -----

        :param dict item_dict: 物品信息字典
        :param tuple[float,float] from_pos: 动画起点坐标
        :param tuple[float,float] to_pos: 动画终点坐标
        :param float|tuple[float,float] ui_size: 物品图标尺寸，传入float时，图标长宽均设置为该值，传入tuple时，图标长宽设置为该元组对应值

        :return: 无
        :rtype: None
        """
        if _is_empty_item(item_dict, False):
            return
        # ItemRenderer不够用时克隆出新的ItemRenderer，否则使用空闲的ItemRenderer
        queue_len = len(self._item_fly_queue)
        ui_count = len(self._fly_ir)
        if queue_len >= ui_count:
            ir = self._clone_new_ir()
            if not ir:
                return
            index = ui_count
        else:
            index = self._get_idle_ir_index()
            if index is None:
                return
            ir = self._fly_ir[index]
        # 配置ItemRenderer
        item_name = item_dict['newItemName']
        aux = item_dict.get('newAuxValue', 0)
        enchanted = bool(item_dict.get('enchantData') or item_dict.get('modEnchantData'))
        user_data = item_dict.get('userData')
        ir.SetUiItem(item_name, aux, enchanted, user_data)
        ir.SetVisible(True)
        ir.SetPosition(from_pos)
        ir.SetSize(ui_size if isinstance(ui_size, tuple) else (ui_size, ui_size))
        # 动画持续帧数
        dur = int(_LvComp.Game.GetFps() * 0.175)
        # x轴上每帧的偏移量
        x_off = (to_pos[0] - from_pos[0]) / dur
        # y轴上每帧的偏移量
        y_off = (to_pos[1] - from_pos[1]) / dur
        # 添加进动画执行队列
        self._item_fly_queue[index] = {
            'x_off': x_off,
            'y_off': y_off,
            'tick': dur,
            'ui_ctrl': ir,
        }

    def SetItemsFlyAnim(self, data):
        """
        设置多个物品飞行动画。

        -----

        :param list[dict[str,Any]] data: 动画数据列表，列表每个元素为一个字典，字典的key分别为item_dict、from_pos、to_pos、ui_size，对应的value的含义与SetOneItemFlyAnim方法中的参数相同。

        :return: 无
        :rtype: None
        """
        for d in data:
            self.SetOneItemFlyAnim(**d)














