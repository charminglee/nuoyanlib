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
#   Last Modified : 2024-04-30
#
# ====================================================


"""

itemGridManager
===============
该模块提供了物品网格的Python实现。将自定义UI类继承 ``ItemGridManager`` ，即可轻松实现一个功能完备的背包UI。

-----

【名词解释】

* 网格：即Grid控件，一种能够对模板控件多次克隆并排列成网状的控件。
* 方格：即网格的单个子控件，也称为网格的元素，本质上是个按钮控件。
* 网格的key：在 ``ItemGridManager`` 中，每个网格都有一个唯一的key，数据类型为字符串，可自定义，或使用预设的key来启用特定功能。
* 方格索引：类似于物品栏槽位，从0开始，网格的第一个方格的索引为0，第二个为1，以此类推，从左到右从上到下递增。
* 方格位置元组：用于表示指定方格，由两个元素组成：(方格所在网格的key, 方格索引)。
* 方格路径：即方格控件的UI路径。
* 分堆数据字典：保存了当前物品分堆数据的字典。

+---------------+----------------------+--------------------+
|     字典键     |         数据类型       |         解释       |
+===============+======================+====================+
|    item_dict   |          dict        |     物品信息字典     |
+---------------+----------------------+--------------------+
| selected_count |          int         | 当前分堆选中的物品数量 |
+---------------+----------------------+--------------------+
|   animating   |         bool         | 分堆进度条动画是否运行 |
+---------------+----------------------+--------------------+
|    bar_ctrl    | ProgressBarUIControl |  分堆进度条控件实例   |
+---------------+----------------------+--------------------+

* 选中物品数据字典：保存了当前选中物品的数据的字典。

+----------+--------+--------------------+
|  字典键   | 数据类型 |        解释         |
+==========+========+====================+
| item_dict |  dict  |     物品信息字典     |
+----------+--------+--------------------+
|    bp    |  str   |    选中方格的路径     |
+----------+--------+--------------------+

-----

【使用方法】

| 1、将您的服务端继承 ``NuoyanServerSystem`` ，此后无需再继承 ``ServerSystem`` 。
| 2、将您的UI类继承 ``ItemGridManager`` ，此后无需再继承 ``ScreenNode`` ，然后正常注册与创建您的UI。
| 3、在UI类的 ``__init__`` 或 ``Create`` 方法里使用接口 ``self.RegisterItemGrid`` 注册一个物品网格。
| 4、网格第一次显示时，调用 ``self.InitItemGrids`` 对网格进行初始化，第二次显示时无需再次调用该接口。网格何时第一次显示取决于您的设置，如果您的网格在创建UI时就立即显示，则在 ``Create`` 方法内执行上述初始化操作即可。
| 5、完成上述步骤后您就可以调用其他接口对网格进行操作，如设置网格所有物品、设置指定位置物品的数量等。

-----

【注意事项】

| 1、如果您的UI类重写了 ``Update`` 方法，请在该方法内调用一次父类同名方法，例如： ``super(你的UI类, self).Update()`` 或 ``ItemGridManager.Update()`` 。

"""


from functools import wraps as _wraps
import mod.client.extraClientApi as _client_api
from mod.common.minecraftEnum import ItemPosType as _ItemPosType
from ...utils.item import (
    is_same_item as _is_same_item,
    is_empty_item as _is_empty_item,
    get_max_stack as _get_max_stack
)
from item_fly_anim import ItemFlyAnim as _ItemFlyAnim
from item_tips_box import ItemTipsBox as _ItemTipsBox
from screen_node import (
    ui_listener as _ui_listener,
    NuoyanScreenNode as _NuoyanScreenNode,
)
from ui_utils import get_direct_children_path as _get_direct_children_path
from ..comp import (
    LvComp as _LvComp,
    CLIENT_ENGINE_NAMESPACE as _CLIENT_ENGINE_NAMESPACE,
    CLIENT_ENGINE_SYSTEM_NAME as _CLIENT_ENGINE_SYSTEM_NAME,
    PLAYER_ID as _PLAYER_ID,
)
from ...config import (
    MOD_NAME as _MOD_NAME,
    CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME,
)


__all__ = [
    "ItemGridManager",
]


_IMAGE_PATH_ITEM_CELL_SELECTED = "textures/ui/recipe_book_button_borderless_lightpressed"
_IMAGE_PATH_ITEM_CELL_DEFAULT = "textures/ui/item_cell"
_UI_NAME_COUNT = "count"
_UI_NAME_ITEM_RENDERER = "item_renderer"
_UI_NAME_DURABILITY = "durability"
_UI_NAME_DEFAULT = "default"
_UI_NAME_HEAP = "heap"
_UI_NAME_ITEM_BG = "item_bg"


_SHORTCUT = "shortcut"
_INV27 = "inv27"
_INV36 = "inv36"
_RESERVED_KEYS = (_SHORTCUT, _INV27, _INV36)


def _deepcopy(obj):
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            if k == 'userData':
                new[k] = v.copy() if v is not None else None
            else:
                new[k] = _deepcopy(v)
    elif isinstance(obj, list):
        new = [_deepcopy(i) for i in obj]
    else:
        new = obj
    return new


def _listen_item_changes(func):
    @_wraps(func)
    def wrapper(self, *args, **kwargs):
        old = _deepcopy(self._grid_items_data)
        res = func(self, *args, **kwargs)
        new = _deepcopy(self._grid_items_data)
        changes = _analyze_changes(old, new)
        if changes:
            _update_changes(self._ItemGridManager__changes, changes)
            self.OnItemGridChanged({'changes': self._ItemGridManager__changes})
            self._ItemGridManager__changes = {}
        return res
    return wrapper


def _analyze_changes(old, new):
    changes = {}
    if old == new:
        return {}
    for key, item_list in old.items():
        for i, old_item in enumerate(item_list):
            new_item = new[key][i]
            if old_item != new_item:
                changes[(key, i)] = {'old': old_item, 'new': new_item}
    return changes


def _update_changes(old_changes, new_changes):
    for k, d in new_changes.items():
        if k not in old_changes:
            old_changes[k] = d
        else:
            old_changes[k]['new'] = d['new']
    for k, d in old_changes.items():
        if d['new'] == d['old']:
            del old_changes[k]


class ItemGridManager(_ItemFlyAnim, _ItemTipsBox, _NuoyanScreenNode):
    """
    物品网格管理器，实现了类似于原版背包的诸多物品功能。
    """

    def __init__(self, namespace, name, param):
        super(ItemGridManager, self).__init__(namespace, name, param)
        self._cs = _client_api.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        self.__screen_node = param['_screen_node'] if param and '_screen_node' in param else self
        self._grid_items_data = {}
        self._item_heap_data = {}
        self._selected_item = {}
        self._grid_paths = {}
        self._grid_keys = []
        self._cell_paths = {}
        self._cell_poses = {}
        self._cell_ui_ctrls = {}
        self.__changes = {}
        self._locked_cells = set()
        self._locked_grids = set()
        self.__move_in_grid_list = []
        self.__org_item = {}
        self._inited_keys = []
        self.__tick = 0
        self.__namespace = _MOD_NAME + "_" + self.__class__.__name__

    # ======================================= System Event Callback ====================================================

    def Destroy(self):
        """
        *[event]*

        | UI生命周期函数，当UI销毁时调用。
        | 若重写了该方法，请调用一次父类的同名方法。如：
        ::

            class MyUI(ItemGridManager):
                def Destroy(self):
                    super(MyUI, self).Destroy()

        -----

        :return: 无
        :rtype: None
        """
        super(ItemGridManager, self).Destroy()
        self._cs.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "GetEntityByCoordReleaseClientEvent",
            self, self._GetEntityByCoordReleaseClientEvent1
        )
        self._cs.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "InventoryItemChangedClientEvent",
            self, self._InventoryItemChangedClientEvent
        )
        self._cs.UnListenForEvent(
            "NuoyanLib", "_TransitServerSystem", "_SyncItems", self, self._SyncItems
        )

    def Update(self):
        """
        *[tick]* *[event]*

        | 客户端每帧调用。
        | 若重写了该方法，请调用一次父类的同名方法，否则部分功能将不可用。如：
        ::

            class MyUI(ItemGridManager):
                def Update(self):
                    super(MyUI, self).Update()

        -----

        :return: 无
        :rtype: None
        """
        super(ItemGridManager, self).Update()
        # 物品分堆
        self.__tick += 1
        if self._item_heap_data and self._item_heap_data['animating']:
            count = self._item_heap_data['item_dict']['count']
            if count > 1:
                tick = round(45.0 / (count - 1))
                if tick < 1:
                    tick = 1
                if not self.__tick % tick and self._item_heap_data['selected_count'] < count:
                    self._item_heap_data['selected_count'] += 1
                    bar_ctrl = self._item_heap_data['bar_ctrl']
                    bar_ctrl.SetValue(float(self._item_heap_data['selected_count']) / count)

    @_ui_listener("GetEntityByCoordReleaseClientEvent")
    def _GetEntityByCoordReleaseClientEvent1(self, args):
        if len(self.__move_in_grid_list) >= 2:
            self.SetSelectedItem(self._selected_item['bp'], False)
        self.__move_in_grid_list = []
        self.__org_item = {}

    @_ui_listener("InventoryItemChangedClientEvent")
    def _InventoryItemChangedClientEvent(self, args):
        player_id = args['playerId']
        slot = args['slot']
        item_dict = args['newItemDict']
        # 背包物品变化时同步更新UI
        if player_id != _PLAYER_ID:
            return
        if _INV36 in self._inited_keys:
            self._grid_items_data[_INV36][slot] = _deepcopy(item_dict)
            self._set_cell_ui_item((_INV36, slot), item_dict)
        if _INV27 in self._inited_keys and slot >= 9:
            self._grid_items_data[_INV27][slot - 9] = _deepcopy(item_dict)
            self._set_cell_ui_item((_INV27, slot - 9), item_dict)
        if _SHORTCUT in self._inited_keys and slot <= 8:
            self._grid_items_data[_SHORTCUT][slot] = _deepcopy(item_dict)
            self._set_cell_ui_item((_SHORTCUT, slot), item_dict)

    # ========================================== New Event Callback ====================================================

    def OnMoveItemsBefore(self, args):
        """
        | 物品发生移动前触发。

        -----

        | 【from_path: str】 起始位置的方格路径
        | 【to_path: str】 终点位置的方格路径
        | 【from_pos: Tuple[str, int]】 起始位置的方格位置元组
        | 【to_pos: Tuple[str, int]】 终点位置的方格位置元组
        | 【$move_count: int】 移动数量，可修改
        | 【$sync: bool】 是否将物品数据同步到服务端，设置为False则不会同步
        | 【$fly_anim: bool】 是否播放物品飞行动画，设置为False则不会显示物品飞行动画
        | 【$force: bool】 是否强制移动，若设置为True，则本次移动会用起始位置的物品覆盖终点位置的物品，否则交换两个位置的物品
        | 【$cancel: bool】 是否取消本次移动，设置为True即可取消

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnMoveItemsAfter(self, args):
        """
        | 物品发生移动后触发。

        -----

        | 【from_path: str】 起始位置的方格路径
        | 【to_path: str】 终点位置的方格路径
        | 【from_pos: Tuple[str, int]】 起始位置的方格位置元组
        | 【to_pos: Tuple[str, int]】 终点位置的方格位置元组
        | 【move_count: int】 移动数量
        | 【sync: bool】 本次移动的物品数据是否同步到服务端
        | 【fly_anim: bool】 是否播放物品飞行动画
        | 【force: bool】 是否强制移动

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnReceiveItemsDataFromServerBefore(self, args):
        """
        | 从服务端接收到物品数据，网格刷新物品数据前触发。

        -----

        | 【data: Dict[str, List[dict]]】 物品数据字典，字典键为网格的key，值为该网格所有物品的物品信息字典列表

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnItemGridChanged(self, args):
        """
        | 网格内的物品发生改变时触发。

        -----

        | 【changes: Dict[Tuple[str, int], Dict[str, dict]]】 字典，结构如下，其中(key, index)为发生变化的网格key和物品所在方格的索引，'old'为变化前的物品信息字典，'new'为变化后的物品信息字典
        ::

            {
                (key, index): {'old': dict, 'new': dict},
                ...
            }

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnItemGridSelectedItem(self, args):
        """
        | 网格内的物品被选中时触发。

        -----

        | 【item_dict: dict】 物品信息字典
        | 【cell_path: str】 方格路径
        | 【cell_pos: Tuple[str, int]】 方格位置元组
        | 【$cancel: bool】 是否取消选中

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    # ============================================ UI Callback =========================================================

    def OnItemCellTouchUp(self, args):
        """
        | 方格抬起时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _on_item_cell_touch_up(self, args):
        self.OnItemCellTouchUp(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        item_dict = self.GetItemCellItem(bp)
        if self._selected_item:
            from_path = self._selected_item['bp']
            count = self._item_heap_data['selected_count'] if self._item_heap_data else -1
            self.MoveItems(from_path, bp, count)
            self.SetSelectedItem(from_path, False)
        elif not _is_empty_item(item_dict):
            self.SetSelectedItem(bp, True)
        self.PauseItemHeapProgressBar()

    def OnItemCellTouchMoveIn(self, args):
        """
        | 手指移动到方格内时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _on_item_cell_touch_move_in(self, args):
        self.OnItemCellTouchMoveIn(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        if self._item_heap_data or not self._selected_item:
            return
        from_path = self._selected_item['bp']
        item_dict = self.GetItemCellItem(bp)
        if bp == from_path or not _is_empty_item(item_dict):
            return
        if not self.__move_in_grid_list:
            self.__org_item = self._selected_item['item_dict']
        if bp not in self.__move_in_grid_list:
            self.__move_in_grid_list.append(bp)
        if len(self.__move_in_grid_list) >= 2:
            self.SeparateItemsEvenly(from_path, self.__org_item, self.__move_in_grid_list)

    def OnItemCellDoubleClick(self, args):
        """
        | 双击方格触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _on_item_cell_double_click(self, args):
        self.OnItemCellDoubleClick(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        if self._item_heap_data:
            return
        item_dict = self.GetItemCellItem(bp)
        if _is_empty_item(item_dict):
            return
        name = item_dict['newItemName']
        aux = item_dict.get('newAuxValue', 0)
        max_stack = _LvComp.Item.GetItemBasicInfo(name, aux)['maxStackSize']
        if item_dict['count'] < max_stack:
            self.MergeItems(bp)
        self.SetSelectedItem(bp, False)

    def OnItemCellLongClick(self, args):
        """
        | 长按方格触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _on_item_cell_long_click(self, args):
        self.OnItemCellLongClick(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        item_dict = self.GetItemCellItem(bp)
        if self._selected_item:
            self.SetSelectedItem(self._selected_item['bp'], False)
        if not _is_empty_item(item_dict) and item_dict['count'] >= 2:
            self.SetItemHeapData(bp, 1)
            self.StartItemHeapProgressBar()

    def OnItemCellTouchDown(self, args):
        """
        | 方格按下时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _on_item_cell_touch_down(self, args):
        self.OnItemCellTouchDown(args)
        bp = args['ButtonPath']
        item_dict = self.GetItemCellItem(bp)
        self.ShowItemHoverTipsBox(item_dict)

    def OnItemCellTouchMove(self, args):
        """
        | 手指在方格上移动时每帧触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def OnItemCellTouchMoveOut(self, args):
        """
        | 手指移出方格时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def OnItemCellTouchCancel(self, args):
        """
        | 方格取消按下时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    # ============================================== UI操作 =============================================================

    def GetAllItemCellUIControls(self, key):
        """
        | 获取指定网格中所有方格的 ``ButtonUIControl`` 实例。

        -----

        :param str key: 网格的key

        :return: 网格中所有方格的ButtonUIControl实例的列表，获取不到时返回空列表
        :rtype: list[ButtonUIControl]
        """
        return self._cell_ui_ctrls.get(key, [])

    def GetItemCellUIControl(self, cell):
        """
        | 获取指定方格的 ``ButtonUIControl`` 。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 指定方格的ButtonUIControl实例，获取不到时返回None
        :rtype: ButtonUIControl|None
        """
        pos = self.GetItemCellPos(cell)
        return self._cell_ui_ctrls[pos[0]][pos[1]] if pos else None

    def SetItemCellDurabilityBar(self, cell, item_dict=None, auto=False):
        """
        | 设置指定方格的物品耐久显示。该接口仅改变UI显示，并不实际改变该方格内物品的耐久。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict item_dict: 物品信息字典，默认为None
        :param bool auto: 是否自动设置，默认为False，设置为True时将忽略item_dict参数，根据方格的物品数据进行设置

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        dur_ctrl = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_DURABILITY).asProgressBar()
        if auto:
            item_dict = self.GetItemCellItem(cell)
        if _is_empty_item(item_dict):
            dur_ctrl.SetVisible(False)
            return True
        durability = item_dict.get('durability', 0)
        item_name = item_dict['newItemName']
        aux = item_dict.get('newAuxValue', 0)
        is_enchanted = bool(item_dict.get('enchantData') or item_dict.get('modEnchantData'))
        basic_info = _LvComp.Item.GetItemBasicInfo(item_name, aux, is_enchanted)
        max_durability = basic_info['maxDurability']
        if durability <= 0 or durability >= max_durability:
            dur_ctrl.SetVisible(False)
        else:
            dur_ctrl.SetVisible(True)
            dur_ctrl.SetValue(float(durability) / max_durability)
        return True

    def SetItemCellRenderer(self, cell, item_dict=None, auto=False):
        """
        | 设置指定方格的物品渲染器显示物品。该接口仅改变UI显示，并不实际改变该方格内物品。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict item_dict: 物品信息字典，默认为None
        :param bool auto: 是否自动设置，默认为False，设置为True时将忽略item_dict参数，根据方格的物品数据进行设置

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        cell = self.GetItemCellUIControl(cell)
        item_renderer = cell.GetChildByName(_UI_NAME_ITEM_RENDERER).asItemRenderer()
        item_bg = cell.GetChildByName(_UI_NAME_ITEM_BG)
        if auto:
            item_dict = self.GetItemCellItem(cell)
        if not _is_empty_item(item_dict):
            item_renderer.SetVisible(True)
            name = item_dict['newItemName']
            aux = item_dict.get('newAuxValue', 0)
            is_enchanted = bool(item_dict.get('enchantData') or item_dict.get('modEnchantData'))
            user_data = item_dict.get('userData')
            item_renderer.SetUiItem(name, aux, is_enchanted, user_data)
            item_bg.SetVisible(False)
        else:
            item_renderer.SetVisible(False)
            item_bg.SetVisible(True)
        return False

    def SetItemCellCountLabel(self, cell, item_dict=None, auto=False):
        """
        | 设置指定方格的物品数量文本。该接口仅改变UI显示，并不实际改变该方格内物品的数量，如需设置物品数量，请使用 ``SetItemCellCount`` 。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict item_dict: 物品信息字典，默认为None
        :param bool auto: 是否自动设置，默认为False，设置为True时将忽略item_dict参数，根据方格的物品数据进行设置

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        label = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_COUNT).asLabel()
        if auto:
            item_dict = self.GetItemCellItem(cell)
        count = item_dict.get('count', 1) if not _is_empty_item(item_dict) else 0
        if count >= 2:
            label.SetVisible(True)
            label.SetText(str(int(count)))
        else:
            label.SetVisible(False)
        return True

    def UpdateAndSyncItemGrids(self, keys=None):
        """
        | 刷新网格并向服务端同步物品数据。

        -----

        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格

        :return: 是否成功
        :rtype: bool
        """
        if not keys:
            keys = self._grid_keys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return False
        data = {}
        for k in keys:
            items = self._grid_items_data[k]
            self.SetItemGridItems(items, k, False)
            data[k] = items
        self._cs.NotifyToServer("_UpdateItemsData", {'data': data, 'namespace': self.__namespace})
        return True

    def ClearItemGridState(self):
        """
        | 清除网格状态（包括物品选中状态和长按分堆状态）。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if self._selected_item:
            bp = self._selected_item['bp']
            default_img = self.GetItemCellUIControl(bp).GetChildByName(_UI_NAME_DEFAULT).asImage()
            default_img.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
            self._selected_item = {}
        if self._item_heap_data:
            self._item_heap_data['bar_ctrl'].SetVisible(False)
            self._item_heap_data = {}
        return True

    def _set_item_fly_anim(self, item_dict, from_cell, to_cell):
        from_ui = self.GetItemCellUIControl(from_cell)
        from_pos = from_ui.GetGlobalPosition()
        ui_size = from_ui.GetSize()
        to_pos = self.GetItemCellUIControl(to_cell).GetGlobalPosition()
        self.SetOneItemFlyAnim(item_dict, from_pos, to_pos, ui_size)

    def StartItemHeapProgressBar(self):
        """
        | 启动物品分堆进度条动画。需要先调用 ``SetItemHeapData`` 设置物品分堆数据后才有效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._item_heap_data:
            return False
        self._item_heap_data['bar_ctrl'].SetVisible(True)
        self._item_heap_data['animating'] = True
        self.__tick = 0
        return True

    def PauseItemHeapProgressBar(self):
        """
        | 暂停物品分堆进度条动画。需要先调用 ``SetItemHeapData`` 设置物品分堆数据后才有效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._item_heap_data:
            return False
        self._item_heap_data['animating'] = False
        return True

    def LockItemGrid(self, key, lock):
        """
        | 锁定或解锁指定网格，锁定后该网格内的所有方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。

        -----

        :param str key: 网格的key
        :param bool lock: 是否锁定

        :return: 是否成功
        :rtype: bool
        """
        if not self.AllItemGridsInited(key):
            return False
        if lock:
            self._locked_grids.add(key)
        else:
            self._locked_grids.discard(key)
        return True

    def IsItemGridLocked(self, key):
        """
        | 获取指定网格是否被锁定。

        -----

        :param str key: 网格的key

        :return: 是否被锁定，是则返回True，否则返回False
        :rtype: bool
        """
        return key in self._locked_grids

    def LockItemCell(self, cell, lock):
        """
        | 锁定或解锁指定方格，锁定后该方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param bool lock: 是否锁定

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        pos = self.GetItemCellPos(cell)
        if lock:
            self._locked_cells.add(pos)
        else:
            self._locked_cells.discard(pos)
        return True

    def IsItemCellLocked(self, cell):
        """
        | 获取指定方格是否被锁定。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 是否被锁定，是则返回True，否则返回False
        :rtype: bool
        """
        pos = self.GetItemCellPos(cell)
        return pos and (pos in self._locked_cells or pos[0] in self._locked_grids)

    # ============================================== 物品操作 ============================================================

    def _is_cell_exist(self, *cell):
        return all(self.GetItemCellPos(c) in self._cell_paths for c in cell)

    @_listen_item_changes
    def _set_cell_ui_item(self, cell, item_dict):
        self.SetItemCellRenderer(cell, item_dict)
        self.SetItemCellCountLabel(cell, item_dict)
        self.SetItemCellDurabilityBar(cell, item_dict)

    def SetItemGridItems(self, item_dict_list, key, sync=True):
        """
        | 将物品一键设置到网格的每个方格上。

        -----

        :param list[dict] item_dict_list: 物品信息字典列表
        :param str key: 网格的key
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self.AllItemGridsInited(key):
            return False
        for i, item_dict in enumerate(item_dict_list):
            self._set_cell_ui_item((key, i), item_dict)
        if sync:
            self.UpdateAndSyncItemGrids(key)
        return True

    def GetItemGridItems(self, key):
        """
        | 获取网格内的所有物品。

        -----

        :param str key: 网格的key

        :return: 物品信息字典列表，获取不到时返回空列表
        :rtype: list[dict|None]
        """
        return _deepcopy(self._grid_items_data[key]) if key in self._grid_items_data else []

    def SetItemCellItem(self, cell, item_dict, sync=True):
        """
        | 将物品设置到指定方格上。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict item_dict: 物品信息字典
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        self._set_cell_ui_item(cell, item_dict)
        if sync:
            self.UpdateAndSyncItemGrids(self.GetItemGridKey(cell))
        return True

    def GetItemCellItem(self, cell):
        """
        | 获取方格的物品信息字典。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 物品信息字典，获取不到返回None
        :rtype: dict|None
        """
        pos = self.GetItemCellPos(cell)
        return _deepcopy(self._grid_items_data[pos[0]][pos[1]]) if pos else None

    def MoveItems(self, from_cell, to_cell, move_count=-1, sync=True, fly_anim=True, force=False):
        """
        | 移动物品。
        | 当起始位置为空气时，本次移动无效。
        | 当终点位置有物品且 ``force`` 参数为 ``False`` 时，会发生物品交换，有两次物品移动操作，第一次为起始位置物品→终点位置，第二次为终点位置物品→起始位置。第二次移动本质上是第一次移动的“副作用”，不会触发 ``OnMoveItemsBefore`` 和 ``OnMoveItemsAfter`` 事件。

        -----

        :param str|tuple[str,int] from_cell: 起始位置的方格路径或方格位置元组
        :param str|tuple[str,int] to_cell: 终点位置的方格路径或方格位置元组
        :param int move_count: 移动数量，默认为-1，表示移动全部数量
        :param bool sync: 是否将物品数据同步到服务端，默认为True
        :param bool fly_anim: 是否播放物品飞行动画，默认为True
        :param bool force: 是否强制移动，默认为False；若强制移动，该接口会用起始位置的物品覆盖终点位置的物品，否则交换两个位置的物品

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(from_cell, to_cell):
            return False
        from_item = self.GetItemCellItem(from_cell)
        to_item = self.GetItemCellItem(to_cell)
        if _is_empty_item(from_item):
            return False
        args = {
            'from_path': self.GetItemCellPath(from_cell),
            'to_path': self.GetItemCellPath(to_cell),
            'from_pos': self.GetItemCellPos(from_cell),
            'to_pos': self.GetItemCellPos(to_cell),
            'move_count': move_count,
            'sync': sync,
            'fly_anim': fly_anim,
            'force': force,
            'cancel': False,
        }
        self.OnMoveItemsBefore(args)
        if args['cancel']:
            return False
        move_count = args['move_count']
        sync = args['sync']
        fly_anim = args['fly_anim']
        force = args['force']
        if move_count <= -1:
            move_count = from_item['count']
        if force or _is_empty_item(to_item):
            self._move_items_to_empty(from_cell, to_cell, move_count)
        elif _is_same_item(from_item, to_item):
            if from_cell != to_cell:
                self._move_items_to_same(from_cell, to_cell, move_count)
        else:
            self._exchange_items(from_cell, to_cell)
            if fly_anim:
                self._set_item_fly_anim(to_item, to_cell, from_cell)
        if sync:
            self.UpdateAndSyncItemGrids()
        if fly_anim:
            self._set_item_fly_anim(from_item, from_cell, to_cell)
        del args['cancel']
        self.OnMoveItemsAfter(args)
        return True

    def _exchange_items(self, from_cell, to_cell):
        from_item = self.GetItemCellItem(from_cell)
        to_item = self.GetItemCellItem(to_cell)
        self._set_cell_ui_item(from_cell, to_item)
        self._set_cell_ui_item(to_cell, from_item)

    def _move_items_to_empty(self, from_cell, to_cell, count):
        from_item = self.GetItemCellItem(from_cell)
        from_new_count = from_item['count'] - count
        from_item['count'] = count
        self._set_cell_ui_item(to_cell, from_item)
        from_item['count'] = from_new_count
        if from_item['count'] <= 0:
            from_item = None
        self._set_cell_ui_item(from_cell, from_item)

    def _move_items_to_same(self, from_cell, to_cell, count):
        overflow_count = self.SetItemCellCount(to_cell, +count, sync=False)
        self.SetItemCellCount(from_cell, -count + overflow_count, sync=False)

    def MergeItems(self, to_cell, sync=True, fly_anim=True):
        """
        | 将所有其他同类物品与指定物品进行合堆。

        -----

        :param str|tuple[str,int] to_cell: 要合堆的方格路径或方格位置元组
        :param bool sync: 是否将物品数据同步到服务端，默认为True
        :param bool fly_anim: 是否播放物品飞行动画，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(to_cell):
            return False
        to_cell = self.GetItemCellPos(to_cell)
        to_item = self.GetItemCellItem(to_cell)
        if _is_empty_item(to_item):
            return False
        max_stack = _get_max_stack(to_item)
        for from_key, from_all_items in self._grid_items_data.items():
            if to_item['count'] == max_stack:
                break
            for from_index, from_item in enumerate(from_all_items):
                if to_item['count'] == max_stack:
                    break
                from_cell = (from_key, from_index)
                if self.IsItemCellLocked(from_cell):
                    continue
                if from_cell == to_cell:
                    continue
                if _is_empty_item(from_item) or not _is_same_item(from_item, to_item):
                    continue
                from_count = from_item['count']
                if from_count == max_stack:
                    continue
                self._move_items_to_same(from_cell, to_cell, from_count)
                if fly_anim:
                    self._set_item_fly_anim(from_item, from_cell, to_cell)
        if sync:
            self.UpdateAndSyncItemGrids()
        return True

    @_listen_item_changes
    def SeparateItemsEvenly(self, from_cell, from_org_item, to_cell_list, sync=True):
        """
        | 物品均分。

        -----

        :param str|tuple[str,int] from_cell: 要进行均分的方格路径或方格位置元组
        :param dict from_org_item: 均分前的物品信息字典
        :param list[str|tuple[str,int]] to_cell_list: 均分后位置的方格路径或方格位置元组的列表
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(from_cell):
            return False
        if _is_empty_item(from_org_item):
            return False
        from_key, from_index = self.GetItemCellPos(from_cell)
        from_all_items = self._grid_items_data[from_key]
        from_count = from_org_item['count']
        grid_count = len(to_cell_list)
        to_count = from_count / grid_count
        if to_count <= 0:
            return False
        for to_cell in to_cell_list:
            to_key, to_index = self.GetItemCellPos(to_cell)
            to_all_items = self._grid_items_data[to_key]
            to_all_items[to_index] = _deepcopy(from_org_item)
            to_all_items[to_index]['count'] = to_count
        remain_count = from_count % grid_count
        if remain_count >= 1:
            from_all_items[from_index] = _deepcopy(from_org_item)
            from_all_items[from_index]['count'] = remain_count
        else:
            from_all_items[from_index] = None
        if sync:
            self.UpdateAndSyncItemGrids()
        return True

    @_listen_item_changes
    def SetItemCellCount(self, cell, count, absolute=0, sync=True):
        """
        | 设置指定方格内的物品的数量。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param int count: 数量
        :param int absolute: 传0或1，0表示在原数量的基础上增加count（正数表示增加，负数表示减少），1表示将物品数量直接设置为count，默认为0
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 溢出数量，即设置数量后超过最大堆叠数的数量
        :rtype: int
        """
        if not self._is_cell_exist(cell):
            return 0
        key, index = self.GetItemCellPos(cell)
        item = self._grid_items_data[key][index]
        if _is_empty_item(item):
            return 0
        max_stack = _get_max_stack(item)
        if absolute:
            item['count'] = count
        else:
            item['count'] += count
        overflow_count = 0
        if item['count'] > max_stack:
            overflow_count = item['count'] - max_stack
            item['count'] = max_stack
        if item['count'] <= 0:
            self._grid_items_data[key][index] = None
        if sync:
            self.UpdateAndSyncItemGrids()
        return overflow_count

    def GetItemCellCount(self, cell):
        """
        | 获取指定方格内的物品的数量。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 物品数量，没有物品时返回0
        :rtype: int
        """
        item = self.GetItemCellItem(cell)
        return item['count'] if not _is_empty_item(item) else 0

    def ReturnItemsToInv(self, keys=None):
        """
        | 将所有背包外的物品返还给背包。必须注册了key为"inv36"的网格或同时注册了key为"inv27"和"shortcut"的网格才有效。

        -----

        :param str|tuple[str,...]|None keys: 指定要将哪些网格的物品返还给背包，多个网格可使用元组，也可不传该参数，表示所有已注册网格

        :return: 是否返还成功
        :rtype: bool
        """
        if not keys:
            keys = self._grid_keys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return False
        if _INV36 not in self._grid_keys and (_SHORTCUT not in self._grid_keys or _INV27 not in self._grid_keys):
            return False
        put_keys = _INV36 if _INV36 in self._grid_keys else (_SHORTCUT, _INV27)
        update = False
        for key in keys:
            if key in _RESERVED_KEYS:
                continue
            item_list = self._grid_items_data[key]
            for i, item in enumerate(item_list):
                if _is_empty_item(item):
                    continue
                if self.PutItemToGrids((key, i), put_keys, False):
                    update = True
        if update:
            self.UpdateAndSyncItemGrids()
        return True

    @_listen_item_changes
    def PutItemToGrids(self, put_item, keys=None, sync=True, fly_anim=True):
        """
        | 将物品放入指定网格。
        | 优先与未达到最大堆叠的同种物品进行合堆，若没有同种物品或合堆后仍有剩余则放入空格子，若没有空格子则丢弃到世界（或尝试放入下一个网格）。

        -----

        :param dict|str|tuple[str,int] put_item: 放入的物品，可传入物品信息字典、方格路径或方格位置元组
        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格
        :param bool sync: 是否将物品数据同步到服务端，默认为True，若同时执行多次物品操作，建议前几次设置sync为False，只在最后一次设置为True
        :param bool fly_anim: 是否播放物品飞行动画，默认为True

        :return: 物品放入后所在方格位置元组的列表，放入失败返回空列表
        :rtype: list[tuple[str,int]]
        """
        if not keys:
            keys = self._grid_keys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return []
        if isinstance(put_item, dict):
            put_item_dict = _deepcopy(put_item)
        else:
            put_item_dict = self.GetItemCellItem(put_item)
            self._set_cell_ui_item(put_item, None)
        put_poses = []
        for key in keys:
            poses = self._put_item(put_item_dict, key)
            put_poses.extend(poses)
            if put_item_dict['count'] <= 0:
                break
        else:
            self.ThrowItem(put_item_dict, sync=False)
        if fly_anim and isinstance(put_item, (str, tuple)):
            for to_pos in put_poses:
                self._set_item_fly_anim(put_item_dict, put_item, to_pos)
        if sync and put_poses:
            self.UpdateAndSyncItemGrids()
        return put_poses

    def _put_item(self, put_item, key):
        put_poses = []
        max_stack = _get_max_stack(put_item)
        empty_index = []
        if key not in self._grid_items_data:
            return []
        item_list = self._grid_items_data[key]
        # 寻找同种物品放入
        for index, item in enumerate(item_list):
            if _is_empty_item(item):
                empty_index.append((key, index))
                continue
            count = item['count']
            if not _is_same_item(item, put_item) or count == max_stack:
                continue
            can_put_count = max_stack - count
            if put_item['count'] <= can_put_count:
                item['count'] += put_item['count']
                put_item['count'] = 0
            else:
                item['count'] = max_stack
                put_item['count'] -= can_put_count
            put_poses.append((key, index))
            if put_item['count'] <= 0:
                break
        else:
            # 没有同种物品则放入空格
            for key, index in empty_index:
                count = max_stack if put_item['count'] > max_stack else put_item['count']
                new_item = _deepcopy(put_item)
                new_item['count'] = count
                put_item['count'] -= count
                item_list[index] = new_item
                put_poses.append((key, index))
                if put_item['count'] <= 0:
                    break
        return put_poses

    def ThrowItem(self, what, count=-1, sync=True):
        """
        | 将物品丢弃到世界。

        -----

        :param dict|str|tuple[str,int] what: 丢弃的物品，可传入物品信息字典、方格路径或方格位置元组
        :param int count: 丢弃数量，默认为-1，表示丢弃全部
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 是否丢弃成功
        :rtype: bool
        """
        if isinstance(what, dict):
            item = _deepcopy(what)
            if _is_empty_item(item):
                return False
        else:
            item = self.GetItemCellItem(what)
            if _is_empty_item(item):
                return False
            self.SetItemCellCount(
                what,
                -count if count >= 0 else 0,
                0 if count >= 0 else 1,
                sync,
            )
        if count >= 0:
            item['count'] = count
        self._cs.NotifyToServer("_ThrowItem", item)
        return True

    def SyncAllItemsFromServer(self, keys=None):
        """
        | 从服务端同步所有物品数据到客户端，并刷新网格。

        -----

        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格

        :return: 是否同步成功
        :rtype: bool
        """
        if not keys:
            keys = self._grid_keys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return False
        self._cs.NotifyToServer("_SyncItems", {'namespace': self.__namespace, 'keys': keys})
        return True

    @_ui_listener(namespace="NuoyanLib", system_name="_TransitServerSystem")
    def _SyncItems(self, args):
        data = args['data']
        namespace = args['namespace']
        if namespace != self.__namespace:
            return
        self.OnReceiveItemsDataFromServerBefore({'data': data})
        for key, item_list in data.items():
            self.SetItemGridItems(item_list, key, False)

    def SetSelectedItem(self, cell, selected=True):
        """
        | 设置指定物品的选中状态。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param bool selected: 是否选中，默认为True

        :return: 是否设置成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        default_img = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_DEFAULT).asImage()
        if selected:
            bp = self.GetItemCellPath(cell)
            pos = self.GetItemCellPos(cell)
            item_dict = self.GetItemCellItem(cell)
            args = {
                'item_dict': item_dict,
                'cell_path': bp,
                'cell_pos': pos,
                'cancel': False,
            }
            self.OnItemGridSelectedItem(args)
            if not args['cancel']:
                default_img.SetSprite(_IMAGE_PATH_ITEM_CELL_SELECTED)
                self._selected_item = {'item_dict': item_dict, 'bp': bp}
            else:
                return False
        else:
            default_img.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
            self.ClearItemGridState()
        return True

    def GetSelectedItem(self):
        """
        | 获取当前选中的物品的数据。

        -----

        :return: 选中物品数据字典，没有选中物品时返回空字典
        :rtype: dict[str,dict|str]
        """
        return self._selected_item

    def SetItemHeapData(self, cell, count):
        """
        | 设置物品分堆数据。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param int count: 分堆数量

        :return: 设置成功时返回分堆数据字典，失败时返回None
        :rtype: dict[str,dict|int|bool|ProgressBarUIControl]|None
        """
        if not self._is_cell_exist(cell):
            return
        item_dict = self.GetItemCellItem(cell)
        heap_bar = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_HEAP).asProgressBar()
        heap_bar.SetVisible(True)
        heap_bar.SetValue(float(count) / item_dict['count'])
        self._item_heap_data = {
            'item_dict': item_dict,
            'selected_count': count,
            'animating': False,
            'bar_ctrl': heap_bar,
        }
        return self._item_heap_data

    def GetItemHeapData(self):
        """
        | 获取物品分堆数据。

        -----

        :return: 分堆数据字典，没有分堆数据时返回空字典
        :rtype: dict[str,dict|int|bool|ProgressBarUIControl]
        """
        return self._item_heap_data

    # ========================================== Basic Function ========================================================

    def RegisterItemGrid(self, key, path, is_single=False):
        """
        | 注册网格或注册单个方格按钮。如果注册的是单个方格按钮，则该方格按钮将被视为只有一个元素的网格。
        | 当网格的key为"shortcut"、"inv27"或"inv36"时，将获得以下特殊功能：
        * 该网格将与本地玩家的背包进行绑定，"shortcut"表示快捷栏，"inv27"表示除快捷栏以外的物品栏，"inv36"表示整个物品栏。
        * 该网格会自动获取本地玩家背包物品数据，并显示物品。
        * 在该网格进行的任何物品操作会自动与本地玩家的背包进行同步。

        -----

        :param str key: 网格的key
        :param str path: 网格的UI路径
        :param bool is_single: 是否是单个方格按钮，默认为False

        :return: 是否注册成功
        :rtype: bool
        """
        if key in self._grid_keys:
            return False
        self._grid_paths[key] = (path, is_single)
        self._grid_keys.append(key)
        self._grid_items_data[key] = []
        return True

    def InitItemGrids(self, keys=None, callback=None, *args, **kwargs):
        """
        | 初始化网格。
        | 初始化前请先使用 ``RegisterItemGrid`` 注册网格。
        | 仅在网格显示时调用才有效。

        -----

        :param str|list[str]|None keys: 网格的key，多个网格可使用列表，传入None时表示所有已注册网格；默认为None
        :param function|None callback: 初始化完成后调用的函数，默认为None
        :param Any args: 传入callback的变长参数
        :param Any kwargs: 传入callback的字典变长参数

        :return: 是否初始化成功
        :rtype: bool
        """
        if not keys:
            keys = self._grid_keys
        else:
            if isinstance(keys, str):
                keys = [keys]
            if not all((i in self._grid_keys) for i in keys):
                return False
        _LvComp.Game.AddTimer(0, self._init_item_grids, keys, callback, args, kwargs)
        return True

    def _init_item_grids(self, keys, callback, args, kwargs):
        for key in keys:
            self._cell_ui_ctrls[key] = []
            # 获取网格所有元素的路径
            gp, is_single = self._grid_paths[key]
            if is_single:
                all_children = [gp]
            else:
                all_children = _get_direct_children_path(gp, self.__screen_node)
            # 初始化操作
            for i, path in enumerate(all_children):
                pos = (key, i)
                self._cell_poses[path] = pos
                self._cell_paths[pos] = path
                self._grid_items_data[key].append(None)
                btn = self.__screen_node.GetBaseUIControl(path).asButton()
                btn.AddTouchEventParams()
                btn.SetButtonTouchMoveInCallback(self._on_item_cell_touch_move_in)
                btn.SetButtonTouchMoveCallback(self.OnItemCellTouchMove)
                btn.GetChildByName("heap").SetVisible(False)
                self.SetButtonDoubleClickCallback(path, self._on_item_cell_double_click, self._on_item_cell_touch_up)
                self.SetButtonLongClickCallback(
                    path,
                    self._on_item_cell_long_click,
                    self._on_item_cell_touch_up,
                    self.OnItemCellTouchMoveOut,
                    self._on_item_cell_touch_down,
                    self.OnItemCellTouchCancel,
                )
                self._cell_ui_ctrls[key].append(btn)
                self.SetItemCellRenderer(pos, None)
                self.SetItemCellCountLabel(pos, None)
                self.SetItemCellDurabilityBar(pos, None)
            # 显示背包物品
            if key in _RESERVED_KEYS:
                invItems = _LvComp.Item.GetPlayerAllItems(_ItemPosType.INVENTORY, True)
                if key == _INV36:
                    items = invItems
                elif key == _INV27:
                    items = invItems[9:]
                else:
                    items = invItems[:9]
                self.SetItemGridItems(items, key, False)
            self._inited_keys.append(key)
        if callback:
            callback(*args, **kwargs)

    def AllItemGridsInited(self, keys=None):
        """
        | 判断网格是否完成初始化。

        -----

        :param str|list[str]|None keys: 网格的key，多个网格可使用列表，传入None时表示所有已注册网格；默认为None

        :return: 网格均已完成初始化时返回True，否则返回False
        :rtype: bool
        """
        if not keys:
            keys = self._grid_keys
        elif isinstance(keys, str):
            keys = [keys]
        return all((key in self._inited_keys) for key in keys)

    def GetItemGridKey(self, cell):
        """
        | 获取方格所在网格的key。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 方格所在网格的key，获取不到返回None
        :rtype: str|None
        """
        if isinstance(cell, tuple):
            return cell[0]
        for (key, _), path in self._cell_paths.items():
            if cell == path:
                return key

    def GetItemCellPath(self, cell):
        """
        | 根据方格位置元组获取方格路径。若传入方格路径，则返回其本身。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 方格路径，获取不到返回None
        :rtype: str|None
        """
        if isinstance(cell, str):
            return cell
        return self._cell_paths.get(cell)

    def GetItemCellPos(self, cell):
        """
        | 根据方格路径获取方格位置元组。若传入方格位置元组，则返回其本身。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 方格位置元组，获取不到返回None
        :rtype: tuple[str,int]|None
        """
        if isinstance(cell, tuple):
            return cell
        return self._cell_poses.get(cell)



















