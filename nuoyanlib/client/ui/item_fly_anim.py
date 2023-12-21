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

itemFlyAnim
===========

该模块提供了物品飞行动画的Python实现。通过ItemFlyAnim，您可以轻松实现一个像原版一样丝滑的物品飞行动画。

"""


import mod.client.extraClientApi as api
from ...utils.item import is_empty_item as _is_empty_item
from ..comp import (
    ScreenNode as _ScreenNode,
    ViewBinder as _ViewBinder,
    LvComp as _LvComp,
)


__all__ = [
    "ItemFlyAnim",
]


_PATH = __file__.replace(".py", "").replace("/", ".")
_NAMESPACE = "NuoyanLib"
_UI_NAME_ITEM_FLY_ANIM = "NyItemFlyAnim"
_UI_PATH_ITEM_FLY_ANIM = _PATH + "._ItemFlyAnimUI"
_UI_DEF_ITEM_FLY_ANIM = "NyItemFlyAnim.main"
_UI_PATH_FLY_ITEM_1 = "/item_fly_panel/item_renderer1"
_UI_PATH_FLY_ITEM_2 = "/item_fly_panel/item_renderer2"


class ItemFlyAnim(_ScreenNode):
    """
    为原版ScreenNode提供物品飞行动画支持。
    """

    def __init__(self, namespace, name, param):
        # noinspection PySuperArguments
        super(ItemFlyAnim, self).__init__(namespace, name, param)
        self._item_fly_anim_node = None
        self.__register()

    def __register(self):
        node = api.GetUI(_NAMESPACE, _UI_NAME_ITEM_FLY_ANIM)
        if node:
            self._item_fly_anim_node = node
        else:
            api.RegisterUI(
                _NAMESPACE, _UI_NAME_ITEM_FLY_ANIM, _UI_PATH_ITEM_FLY_ANIM, _UI_DEF_ITEM_FLY_ANIM
            )
            self._item_fly_anim_node = api.CreateUI(
                _NAMESPACE, _UI_NAME_ITEM_FLY_ANIM, {'isHud': 1, '__cs__': self}
            )

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
        self._item_fly_anim_node.SetOneItemFlyAnim(item_dict, from_pos, to_pos, ui_size)

    def SetItemsFlyAnim(self, data):
        """
        设置多个物品飞行动画。

        -----

        :param list[dict[str,Any]] data: 动画数据列表，列表每个元素为一个字典，字典的key分别为item_dict、from_pos、to_pos、ui_size，对应的value的含义与SetOneItemFlyAnim方法中的参数相同。

        :return: 无
        :rtype: None
        """
        self._item_fly_anim_node.SetItemsFlyAnim(data)


class _ItemFlyAnimUI(_ScreenNode):
    def __init__(self, namespace, name, param):
        super(_ItemFlyAnimUI, self).__init__(namespace, name, param)
        self.item_fly_queue = {}
        self.fly_ir = []

    def Create(self):
        self.fly_ir.append(self.GetBaseUIControl(_UI_PATH_FLY_ITEM_1).asItemRenderer())
        self.fly_ir.append(self.GetBaseUIControl(_UI_PATH_FLY_ITEM_2).asItemRenderer())

    # ====================================== System Event Callback =====================================================

    @_ViewBinder.binding(_ViewBinder.BF_BindString, "#main.gametick")
    def OnGameTick(self):
        # 物品飞行动画
        for k, data in self.item_fly_queue.items():
            x = data['x_off']
            y = data['y_off']
            ui_ctrl = data['ui_ctrl']
            pos = ui_ctrl.GetPosition()
            ui_ctrl.SetPosition((pos[0] + x, pos[1] + y))
            data['tick'] -= 1
            # 动画结束
            if data['tick'] <= 0:
                ui_ctrl.SetVisible(False)
                del self.item_fly_queue[k]

    # ========================================== Basic Function ========================================================

    def _clone_new_ir(self):
        name = str(len(self.fly_ir))
        if self.Clone(_UI_PATH_FLY_ITEM_1, "/item_fly_panel", name):
            ir = self.GetBaseUIControl("/item_fly_panel/" + name).asItemRenderer()
            self.fly_ir.append(ir)
            return ir

    def _get_idle_ir_index(self):
        for i in range(len(self.fly_ir)):
            if i not in self.item_fly_queue:
                return i

    def SetOneItemFlyAnim(self, item_dict, from_pos, to_pos, ui_size):
        if _is_empty_item(item_dict, False):
            return
        # ItemRenderer不够用时克隆出新的ItemRenderer，否则使用空闲的ItemRenderer
        queue_len = len(self.item_fly_queue)
        ui_count = len(self.fly_ir)
        if queue_len >= ui_count:
            ir = self._clone_new_ir()
            if not ir:
                return
            index = ui_count
        else:
            index = self._get_idle_ir_index()
            if index is None:
                return
            ir = self.fly_ir[index]
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
        self.item_fly_queue[index] = {
            'x_off': x_off,
            'y_off': y_off,
            'tick': dur,
            'ui_ctrl': ir,
        }

    def SetItemsFlyAnim(self, data):
        for d in data:
            self.SetOneItemFlyAnim(**d)













