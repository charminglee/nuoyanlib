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
#   Last Modified : 2024-04-20
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
|    itemDict   |          dict        |     物品信息字典     |
+---------------+----------------------+--------------------+
| selectedCount |          int         | 当前分堆选中的物品数量 |
+---------------+----------------------+--------------------+
|   animating   |         bool         | 分堆进度条动画是否运行 |
+---------------+----------------------+--------------------+
|    barCtrl    | ProgressBarUIControl |  分堆进度条控件实例   |
+---------------+----------------------+--------------------+

* 选中物品数据字典：保存了当前选中物品的数据的字典。

+----------+--------+--------------------+
|  字典键   | 数据类型 |        解释         |
+==========+========+====================+
| itemDict |  dict  |     物品信息字典     |
+----------+--------+--------------------+
|    bp    |  str   |    选中方格的路径     |
+----------+--------+--------------------+

-----

【使用方法】

| 1、将您的服务端继承 ``NuoyanServerSystem`` ，此后无需再继承 ``ServerSystem`` 。
| 2、将您的UI类继承 ``ItemGridManager`` ，此后无需再继承 ``ScreenNode`` ，例如： ``class MyUi(ItemGridManager)`` ，然后正常注册与创建您的UI。
| 3、在UI类的 ``__init__`` 或 ``Create`` 方法里使用接口 ``self.RegisterItemGrid`` 注册一个物品网格。
| 4、网格第一次显示时，调用 ``self.InitItemGrids`` 对网格进行初始化，第二次显示时无需再次调用该接口。网格何时第一次显示取决于您的设定，如果您没有在UI编辑器中把网格设置为隐藏，则在 ``Create`` 方法内执行上述初始化操作即可。
| 5、完成上述步骤后您就可以调用其他接口对网格进行操作，如设置网格所有物品、设置指定位置物品的数量等。

-----

【注意事项】

| 1、如果您的UI类重写了 ``Update`` 方法，请在该方法内调用一次父类同名方法，例如： ``super(你的UI类, self).Update()`` 或 ``ItemGridManager.Update()`` 。

"""


from functools import wraps as _wraps
from ...utils.item import (
    is_same_item as _is_same_item,
    is_empty_item as _is_empty_item,
    get_max_stack as _get_max_stack
)
from item_fly_anim import ItemFlyAnim as _ItemFlyAnim
from item_tips_box import ItemTipsBox as _ItemTipsBox
from screen_node import (
    NuoyanScreenNode as _NuoyanScreenNode,
    ui_listener as _ui_listener,
)
from ui_utils import get_direct_children_path as _get_direct_children_path
from ..comp import (
    LvComp as _LvComp,
    CLIENT_ENGINE_NAMESPACE as _CLIENT_ENGINE_NAMESPACE,
    CLIENT_ENGINE_SYSTEM_NAME as _CLIENT_ENGINE_SYSTEM_NAME,
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


_SHORTCUT = "shortcut"
_INV27 = "inv27"
_INV36 = "inv36"
_RESERVED_KEYS = (_SHORTCUT, _INV27, _INV36)


class _Inv36ItemList(list):
    def __init__(self, shortcut, inv27):
        list.__init__(self, shortcut + inv27)
        self.shortcut = shortcut
        self.inv27 = inv27

    def __setitem__(self, index, val):
        len1 = len(self.shortcut)
        len2 = len(self.inv27)
        if index >= 0:
            if index <= len1 - 1:
                self.shortcut[index] = val
            else:
                self.inv27[index - len1] = val
        else:
            if -len2 <= index <= -1:
                self.inv27[index] = val
            else:
                self.shortcut[index + len2] = val
        list.__init__(self, self.shortcut + self.inv27)

    def append(self, obj):
        if len(self.shortcut) < 9:
            self.shortcut.append(obj)
        elif len(self.inv27) < 27:
            self.inv27.append(obj)
        list.__init__(self, self.shortcut + self.inv27)


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
        old = _deepcopy(self._gridItemsData)
        res = func(self, *args, **kwargs)
        new = _deepcopy(self._gridItemsData)
        changes = _analyze_changes(old, new)
        if changes:
            _update_changes(self._changes, changes)
            self.OnItemGridChanged({'changes': self._changes})
            self._changes = {}
        return res
    return wrapper


def _analyze_changes(old, new):
    changes = {}
    if old == new:
        return {}
    for key, itemList in old.items():
        for i, oldItem in enumerate(itemList):
            newItem = new[key][i]
            if oldItem != newItem:
                changes[(key, i)] = {'old': oldItem, 'new': newItem}
    return changes


def _update_changes(oldChanges, newChanges):
    for k, d in newChanges.items():
        if k not in oldChanges:
            oldChanges[k] = d
        else:
            oldChanges[k]['new'] = d['new']
    for k, d in oldChanges.items():
        if d['new'] == d['old']:
            del oldChanges[k]


class ItemGridManager(_ItemFlyAnim, _ItemTipsBox, _NuoyanScreenNode):
    """
    物品网格管理器，实现了类似于原版背包的诸多物品功能。
    """

    def __init__(self, namespace, name, param):
        # noinspection PySuperArguments
        super(ItemGridManager, self).__init__(namespace, name, param)
        self._gridItemsData = {}
        self._itemHeapData = {}
        self._selectedItem = {}
        self._gridPaths = {}
        self._gridKeys = []
        self._cellPaths = {}
        self._cellPoses = {}
        self._cellUiCtrls = {}
        self._changes = {}
        self._lockedCells = set()
        self._lockedGrids = set()
        self._moveInGridList = []
        self._orgItem = {}
        self._initedKeys = []
        self.__tick = 0
        self.__namespace = self.__class__.__name__

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
        # noinspection PySuperArguments
        super(ItemGridManager, self).Destroy()
        self.cs.UnListenForEvent(
            _CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, "GetEntityByCoordReleaseClientEvent",
            self, self._GetEntityByCoordReleaseClientEvent1
        )
        self.cs.UnListenForEvent(
            "NuoyanLib", "_TransitServerSystem", "_SyncItems", self, self._SyncItems
        )

    def OnTick(self):
        """
        *[tick]* *[event]*

        | 客户端每帧调用，1秒有30帧。
        | 若重写了该方法，请调用一次父类的同名方法。如：
        ::

            class MyUI(ItemGridManager):
                def OnTick(self):
                    super(MyUI, self).OnTick()

        -----

        :return: 无
        :rtype: None
        """
        # 物品分堆
        self.__tick += 1
        if self._itemHeapData and self._itemHeapData['animating']:
            count = self._itemHeapData['itemDict']['count']
            if count > 1:
                tick = round(45.0 / (count - 1))
                if tick < 1:
                    tick = 1
                if not self.__tick % tick and self._itemHeapData['selectedCount'] < count:
                    self._itemHeapData['selectedCount'] += 1
                    barCtrl = self._itemHeapData['barCtrl']
                    barCtrl.SetValue(float(self._itemHeapData['selectedCount']) / count)

    @_ui_listener("GetEntityByCoordReleaseClientEvent")
    def _GetEntityByCoordReleaseClientEvent1(self, args):
        if len(self._moveInGridList) >= 2:
            self.SetSelectedItem(self._selectedItem['bp'], False)
        self._moveInGridList = []
        self._orgItem = {}

    # ========================================== New Event Callback ====================================================

    def OnMoveItemsBefore(self, args):
        """
        物品发生移动前触发。

        -----

        | 【fromPath: str】 起始位置的方格路径
        | 【toPath: str】 终点位置的方格路径
        | 【fromPos: Tuple[str, int]】 起始位置的方格位置元组
        | 【toPos: Tuple[str, int]】 终点位置的方格位置元组
        | 【$moveCount: int】 移动数量，可修改
        | 【$sync: bool】 是否将物品数据同步到服务端，设置为False则不会同步
        | 【$flyAnim: bool】 是否播放物品飞行动画，设置为False则不会显示物品飞行动画
        | 【$force: bool】 是否强制移动，若设置为True，则本次移动会用起始位置的物品覆盖终点位置的物品，否则交换两个位置的物品
        | 【$cancel: bool】 是否取消本次移动，设置为True即可取消

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnMoveItemsAfter(self, args):
        """
        物品发生移动后触发。

        -----

        | 【fromPath: str】 起始位置的方格路径
        | 【toPath: str】 终点位置的方格路径
        | 【fromPos: Tuple[str, int]】 起始位置的方格位置元组
        | 【toPos: Tuple[str, int]】 终点位置的方格位置元组
        | 【moveCount: int】 移动数量
        | 【sync: bool】 本次移动的物品数据是否同步到服务端
        | 【flyAnim: bool】 是否播放物品飞行动画
        | 【force: bool】 是否强制移动

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnReceiveItemsDataFromServerBefore(self, args):
        """
        从服务端接收到物品数据，网格刷新物品数据前触发。

        -----

        | 【data: Dict[str, List[dict]]】 物品数据字典，字典键为网格的key，值为该网格所有物品的物品信息字典列表

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    def OnItemGridChanged(self, args):
        """
        网格内的物品发生改变时触发。

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
        网格内的物品被选中时触发。

        -----

        | 【itemDict: dict】 物品信息字典
        | 【cellPath: str】 方格路径
        | 【cellPos: Tuple[str, int]】 方格位置元组
        | 【$cancel: bool】 是否取消选中

        -----

        :param dict args: 参数字典，参数解释见上方

        :return: 无
        :rtype: None
        """

    # ============================================ UI Callback =========================================================

    def OnItemCellTouchUp(self, args):
        """
        方格抬起时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _onItemCellTouchUp(self, args):
        self.OnItemCellTouchUp(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        itemDict = self.GetItemCellItem(bp)
        if self._selectedItem:
            fromPath = self._selectedItem['bp']
            count = self._itemHeapData['selectedCount'] if self._itemHeapData else -1
            self.MoveItems(fromPath, bp, count)
            self.SetSelectedItem(fromPath, False)
        elif not _is_empty_item(itemDict):
            self.SetSelectedItem(bp, True)
        self.PauseItemHeapProgressBar()

    def OnItemCellTouchMoveIn(self, args):
        """
        手指移动到方格内时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _onItemCellTouchMoveIn(self, args):
        self.OnItemCellTouchMoveIn(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        if self._itemHeapData or not self._selectedItem:
            return
        fromPath = self._selectedItem['bp']
        itemDict = self.GetItemCellItem(bp)
        if bp == fromPath or not _is_empty_item(itemDict):
            return
        if not self._moveInGridList:
            self._orgItem = self._selectedItem['itemDict']
        if bp not in self._moveInGridList:
            self._moveInGridList.append(bp)
        if len(self._moveInGridList) >= 2:
            self.SeparateItemsEvenly(fromPath, self._orgItem, self._moveInGridList)

    def OnItemCellDoubleClick(self, args):
        """
        双击方格触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _onItemCellDoubleClick(self, args):
        self.OnItemCellDoubleClick(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        if self._itemHeapData:
            return
        itemDict = self.GetItemCellItem(bp)
        if _is_empty_item(itemDict):
            return
        name = itemDict['newItemName']
        aux = itemDict.get('newAuxValue', 0)
        maxStack = _LvComp.Item.GetItemBasicInfo(name, aux)['maxStackSize']
        if itemDict['count'] < maxStack:
            self.MergeItems(bp)
        self.SetSelectedItem(bp, False)

    def OnItemCellLongClick(self, args):
        """
        长按方格触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _onItemCellLongClick(self, args):
        self.OnItemCellLongClick(args)
        bp = args['ButtonPath']
        if self.IsItemCellLocked(bp):
            return
        itemDict = self.GetItemCellItem(bp)
        if self._selectedItem:
            self.SetSelectedItem(self._selectedItem['bp'], False)
        if not _is_empty_item(itemDict) and itemDict['count'] >= 2:
            self.SetItemHeapData(bp, 1)
            self.StartItemHeapProgressBar()

    def OnItemCellTouchDown(self, args):
        """
        方格按下时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def _onItemCellTouchDown(self, args):
        self.OnItemCellTouchDown(args)
        bp = args['ButtonPath']
        itemDict = self.GetItemCellItem(bp)
        self.ShowItemHoverTipsBox(itemDict)

    def OnItemCellTouchMove(self, args):
        """
        手指在方格上移动时每帧触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def OnItemCellTouchMoveOut(self, args):
        """
        手指移出方格时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    def OnItemCellTouchCancel(self, args):
        """
        方格取消按下时触发的回调函数。

        -----

        :param dict args: 参数字典，参数与通过官方接口设置的按钮回调函数相同

        :return: 无
        :rtype: None
        """

    # ============================================== UI操作 =============================================================

    def GetAllItemCellUIControls(self, key):
        """
        获取指定网格中所有方格的ButtonUIControl实例。

        -----

        :param str key: 网格的key

        :return: 网格中所有方格的ButtonUIControl实例的列表，获取不到时返回空列表
        :rtype: list[ButtonUIControl]
        """
        return self._cellUiCtrls.get(key, [])

    def GetItemCellUIControl(self, cell):
        """
        获取指定方格的ButtonUIControl。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 指定方格的ButtonUIControl实例，获取不到时返回None
        :rtype: ButtonUIControl|None
        """
        pos = self.GetItemCellPos(cell)
        return self._cellUiCtrls[pos[0]][pos[1]] if pos else None

    def SetItemCellDurabilityBar(self, cell, itemDict=None, auto=False):
        """
        设置指定方格的物品耐久显示。该接口仅改变UI显示，并不实际改变该方格内物品的耐久。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict itemDict: 物品信息字典，默认为None
        :param bool auto: 是否自动设置，默认为False，设置为True时将忽略itemDict参数，根据方格的物品数据进行设置

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        durCtrl = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_DURABILITY).asProgressBar()
        if auto:
            itemDict = self.GetItemCellItem(cell)
        if _is_empty_item(itemDict):
            durCtrl.SetVisible(False)
            return True
        durability = itemDict.get('durability', 0)
        itemName = itemDict['newItemName']
        aux = itemDict.get('newAuxValue', 0)
        isEnchanted = bool(itemDict.get('enchantData') or itemDict.get('modEnchantData'))
        basicInfo = _LvComp.Item.GetItemBasicInfo(itemName, aux, isEnchanted)
        maxDurability = basicInfo['maxDurability']
        if durability <= 0 or durability >= maxDurability:
            durCtrl.SetVisible(False)
        else:
            durCtrl.SetVisible(True)
            durCtrl.SetValue(float(durability) / maxDurability)
        return True

    def SetItemCellRenderer(self, cell, itemDict=None, auto=False):
        """
        设置指定方格的物品渲染器显示物品。该接口仅改变UI显示，并不实际改变该方格内物品。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict itemDict: 物品信息字典，默认为None
        :param bool auto: 是否自动设置，默认为False，设置为True时将忽略itemDict参数，根据方格的物品数据进行设置

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        itemRenderer = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_ITEM_RENDERER).asItemRenderer()
        if auto:
            itemDict = self.GetItemCellItem(cell)
        if not _is_empty_item(itemDict):
            itemRenderer.SetVisible(True)
            name = itemDict['newItemName']
            aux = itemDict.get('newAuxValue', 0)
            isEnchanted = bool(itemDict.get('enchantData') or itemDict.get('modEnchantData'))
            userData = itemDict.get('userData')
            itemRenderer.SetUiItem(name, aux, isEnchanted, userData)
        else:
            itemRenderer.SetVisible(False)
        return False

    def SetItemCellCountLabel(self, cell, itemDict=None, auto=False):
        """
        设置指定方格的物品数量文本。该接口仅改变UI显示，并不实际改变该方格内物品的数量，如需设置物品数量，请使用SetItemCellCount。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict itemDict: 物品信息字典，默认为None
        :param bool auto: 是否自动设置，默认为False，设置为True时将忽略itemDict参数，根据方格的物品数据进行设置

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        label = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_COUNT).asLabel()
        if auto:
            itemDict = self.GetItemCellItem(cell)
        count = itemDict.get('count', 1) if not _is_empty_item(itemDict) else 0
        if count >= 2:
            label.SetVisible(True)
            label.SetText(str(int(count)))
        else:
            label.SetVisible(False)
        return True

    def UpdateAndSyncItemGrids(self, keys=None):
        """
        刷新网格并向服务端同步物品数据。

        -----

        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格

        :return: 是否成功
        :rtype: bool
        """
        if not keys:
            keys = self._gridKeys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return False
        data = {}
        for k in keys:
            items = self._gridItemsData[k]
            self.SetItemGridItems(items, k, False)
            data[k] = items
        self.cs.NotifyToServer("_UpdateItemsData", {'data': data, 'namespace': self.__namespace})
        return True

    def ClearItemGridState(self):
        """
        清除网格状态（包括物品选中状态和长按分堆状态）。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if self._selectedItem:
            bp = self._selectedItem['bp']
            defaultImg = self.GetItemCellUIControl(bp).GetChildByName(_UI_NAME_DEFAULT).asImage()
            defaultImg.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
            self._selectedItem = {}
        if self._itemHeapData:
            self._itemHeapData['barCtrl'].SetVisible(False)
            self._itemHeapData = {}
        return True

    def _setItemFlyAnim(self, itemDict, fromCell, toCell):
        fromUi = self.GetItemCellUIControl(fromCell)
        fromPos = fromUi.GetGlobalPosition()
        uiSize = fromUi.GetSize()
        toPos = self.GetItemCellUIControl(toCell).GetGlobalPosition()
        self.SetOneItemFlyAnim(itemDict, fromPos, toPos, uiSize)

    def StartItemHeapProgressBar(self):
        """
        启动物品分堆进度条动画。需要先调用SetItemHeapData设置物品分堆数据后才有效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._itemHeapData:
            return False
        self._itemHeapData['barCtrl'].SetVisible(True)
        self._itemHeapData['animating'] = True
        self.__tick = 0
        return True

    def PauseItemHeapProgressBar(self):
        """
        暂停物品分堆进度条动画。需要先调用SetItemHeapData设置物品分堆数据后才有效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._itemHeapData:
            return False
        self._itemHeapData['animating'] = False
        return True

    def LockItemGrid(self, key, lock):
        """
        锁定或解锁指定网格，锁定后该网格内的所有方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。

        -----

        :param str key: 网格的key
        :param bool lock: 是否锁定

        :return: 是否成功
        :rtype: bool
        """
        if not self.AllItemGridsInited(key):
            return False
        if lock:
            self._lockedGrids.add(key)
        else:
            self._lockedGrids.discard(key)
        return True

    def IsItemGridLocked(self, key):
        """
        获取指定网格是否被锁定。

        -----

        :param str key: 网格的key

        :return: 是否被锁定，是则返回True，否则返回False
        :rtype: bool
        """
        return key in self._lockedGrids

    def LockItemCell(self, cell, lock):
        """
        锁定或解锁指定方格，锁定后该方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。

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
            self._lockedCells.add(pos)
        else:
            self._lockedCells.discard(pos)
        return True

    def IsItemCellLocked(self, cell):
        """
        获取指定方格是否被锁定。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 是否被锁定，是则返回True，否则返回False
        :rtype: bool
        """
        pos = self.GetItemCellPos(cell)
        return pos and (pos in self._lockedCells or pos[0] in self._lockedGrids)

    # ============================================== 物品操作 ============================================================

    def _is_cell_exist(self, *cell):
        return all(self.GetItemCellPos(c) in self._cellPaths for c in cell)

    @_listen_item_changes
    def _setCellItem(self, cell, itemDict):
        key, index = self.GetItemCellPos(cell)
        self._gridItemsData[key][index] = _deepcopy(itemDict)
        self.SetItemCellRenderer(cell, itemDict)
        self.SetItemCellCountLabel(cell, itemDict)
        self.SetItemCellDurabilityBar(cell, itemDict)

    def SetItemGridItems(self, itemDictList, key, sync=True):
        """
        将物品一键设置到网格的每个方格上。

        -----

        :param list[dict] itemDictList: 物品信息字典列表
        :param str key: 网格的key
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self.AllItemGridsInited(key):
            return False
        for i, itemDict in enumerate(itemDictList):
            self._setCellItem((key, i), itemDict)
        if sync:
            self.UpdateAndSyncItemGrids(key)
        return True

    def GetItemGridItems(self, key):
        """
        获取网格内的所有物品。

        -----

        :param str key: 网格的key

        :return: 物品信息字典列表，获取不到时返回空列表
        :rtype: list[dict|None]
        """
        return _deepcopy(self._gridItemsData[key]) if key in self._gridItemsData else []

    def SetItemCellItem(self, cell, itemDict, sync=True):
        """
        将物品设置到指定方格上。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param dict itemDict: 物品信息字典
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        self._setCellItem(cell, itemDict)
        if sync:
            self.UpdateAndSyncItemGrids(self.GetItemGridKey(cell))
        return True

    def GetItemCellItem(self, cell):
        """
        获取方格的物品信息字典。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 物品信息字典，获取不到返回None
        :rtype: dict|None
        """
        pos = self.GetItemCellPos(cell)
        return _deepcopy(self._gridItemsData[pos[0]][pos[1]]) if pos else None

    def MoveItems(self, fromCell, toCell, moveCount=-1, sync=True, flyAnim=True, force=False):
        """
        移动物品。

        -----

        :param str|tuple[str,int] fromCell: 起始位置的方格路径或方格位置元组
        :param str|tuple[str,int] toCell: 终点位置的方格路径或方格位置元组
        :param int moveCount: 移动数量，默认为-1，表示移动全部数量
        :param bool sync: 是否将物品数据同步到服务端，默认为True
        :param bool flyAnim: 是否播放物品飞行动画，默认为True
        :param bool force: 是否强制移动，默认为False；若强制移动，该接口会用起始位置的物品覆盖终点位置的物品，否则交换两个位置的物品

        :return: 是否成功
        :rtype: bool
        """
        args = {
            'fromPath': self.GetItemCellPath(fromCell),
            'toPath': self.GetItemCellPath(toCell),
            'fromPos': self.GetItemCellPos(fromCell),
            'toPos': self.GetItemCellPos(toCell),
            'moveCount': moveCount,
            'sync': sync,
            'flyAnim': flyAnim,
            'force': force,
            'cancel': False,
        }
        self.OnMoveItemsBefore(args)
        if args['cancel']:
            return False
        moveCount = args['moveCount']
        sync = args['sync']
        flyAnim = args['flyAnim']
        force = args['force']
        if not self._is_cell_exist(fromCell, toCell):
            return False
        fromItem = self.GetItemCellItem(fromCell)
        if _is_empty_item(fromItem):
            return False
        toItem = self.GetItemCellItem(toCell)
        if moveCount <= -1:
            moveCount = fromItem['count']
        if force or _is_empty_item(toItem):
            self._moveItemsToEmpty(fromCell, toCell, moveCount)
        elif _is_same_item(fromItem, toItem):
            if fromCell != toCell:
                self._moveItemsToSame(fromCell, toCell, moveCount)
        else:
            self._exchangeItems(fromCell, toCell)
            if flyAnim:
                self._setItemFlyAnim(toItem, toCell, fromCell)
        if sync:
            self.UpdateAndSyncItemGrids()
        if flyAnim:
            self._setItemFlyAnim(fromItem, fromCell, toCell)
        del args['cancel']
        self.OnMoveItemsAfter(args)
        return True

    def _exchangeItems(self, fromCell, toCell):
        fromItem = self.GetItemCellItem(fromCell)
        toItem = self.GetItemCellItem(toCell)
        self._setCellItem(fromCell, toItem)
        self._setCellItem(toCell, fromItem)

    def _moveItemsToEmpty(self, fromCell, toCell, count):
        fromItem = self.GetItemCellItem(fromCell)
        fromNewCount = fromItem['count'] - count
        fromItem['count'] = count
        self._setCellItem(toCell, fromItem)
        fromItem['count'] = fromNewCount
        if fromItem['count'] <= 0:
            fromItem = None
        self._setCellItem(fromCell, fromItem)

    def _moveItemsToSame(self, fromCell, toCell, count):
        overflowCount = self.SetItemCellCount(toCell, +count, sync=False)
        self.SetItemCellCount(fromCell, -count + overflowCount, sync=False)

    def MergeItems(self, toCell, sync=True, flyAnim=True):
        """
        将所有其他同类物品与指定物品进行合堆。

        -----

        :param str|tuple[str,int] toCell: 要合堆的方格路径或方格位置元组
        :param bool sync: 是否将物品数据同步到服务端，默认为True
        :param bool flyAnim: 是否播放物品飞行动画，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(toCell):
            return False
        toCell = self.GetItemCellPos(toCell)
        toItem = self.GetItemCellItem(toCell)
        if _is_empty_item(toItem):
            return False
        maxStack = _get_max_stack(toItem)
        for fromKey, fromAllItems in self._gridItemsData.items():
            if toItem['count'] == maxStack:
                break
            for fromIndex, fromItem in enumerate(fromAllItems):
                if toItem['count'] == maxStack:
                    break
                fromCell = (fromKey, fromIndex)
                if self.IsItemCellLocked(fromCell):
                    continue
                if fromCell == toCell:
                    continue
                if _is_empty_item(fromItem) or not _is_same_item(fromItem, toItem):
                    continue
                fromCount = fromItem['count']
                if fromCount == maxStack:
                    continue
                self._moveItemsToSame(fromCell, toCell, fromCount)
                if flyAnim:
                    self._setItemFlyAnim(fromItem, fromCell, toCell)
        if sync:
            self.UpdateAndSyncItemGrids()
        return True

    @_listen_item_changes
    def SeparateItemsEvenly(self, fromCell, fromOrgItem, toCellList, sync=True):
        """
        物品均分。

        -----

        :param str|tuple[str,int] fromCell: 要进行均分的方格路径或方格位置元组
        :param dict fromOrgItem: 均分前的物品信息字典
        :param list[str|tuple[str,int]] toCellList: 均分后位置的方格路径或方格位置元组的列表
        :param bool sync: 是否将物品数据同步到服务端，默认为True

        :return: 是否成功
        :rtype: bool
        """
        if not self._is_cell_exist(fromCell):
            return False
        if _is_empty_item(fromOrgItem):
            return False
        fromKey, fromIndex = self.GetItemCellPos(fromCell)
        fromAllItems = self._gridItemsData[fromKey]
        fromCount = fromOrgItem['count']
        gridCount = len(toCellList)
        toCount = fromCount / gridCount
        if toCount <= 0:
            return False
        for toCell in toCellList:
            toKey, toIndex = self.GetItemCellPos(toCell)
            toAllItems = self._gridItemsData[toKey]
            toAllItems[toIndex] = _deepcopy(fromOrgItem)
            toAllItems[toIndex]['count'] = toCount
        remainCount = fromCount % gridCount
        if remainCount >= 1:
            fromAllItems[fromIndex] = _deepcopy(fromOrgItem)
            fromAllItems[fromIndex]['count'] = remainCount
        else:
            fromAllItems[fromIndex] = None
        if sync:
            self.UpdateAndSyncItemGrids()
        return True

    @_listen_item_changes
    def SetItemCellCount(self, cell, count, absolute=0, sync=True):
        """
        设置指定方格内的物品的数量。

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
        item = self._gridItemsData[key][index]
        if _is_empty_item(item):
            return 0
        maxStack = _get_max_stack(item)
        if absolute:
            item['count'] = count
        else:
            item['count'] += count
        overflowCount = 0
        if item['count'] > maxStack:
            overflowCount = item['count'] - maxStack
            item['count'] = maxStack
        if item['count'] <= 0:
            self._gridItemsData[key][index] = None
        if sync:
            self.UpdateAndSyncItemGrids()
        return overflowCount

    def GetItemCellCount(self, cell):
        """
        获取指定方格内的物品的数量。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 物品数量，没有物品时返回0
        :rtype: int
        """
        item = self.GetItemCellItem(cell)
        return item['count'] if not _is_empty_item(item) else 0

    def ReturnItemsToInv(self, keys=None):
        """
        将所有背包外的物品返还给背包。必须注册了key为"inv36"的网格或同时注册了key为"inv27"和"shortcut"的网格才有效。

        -----

        :param str|tuple[str,...]|None keys: 指定要将哪些网格的物品返还给背包，多个网格可使用元组，也可不传该参数，表示所有已注册网格

        :return: 是否返还成功
        :rtype: bool
        """
        if not keys:
            keys = self._gridKeys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return False
        if _INV36 not in self._gridKeys and (_SHORTCUT not in self._gridKeys or _INV27 not in self._gridKeys):
            return False
        putKeys = _INV36 if _INV36 in self._gridKeys else (_SHORTCUT, _INV27)
        update = False
        for key in keys:
            if key in _RESERVED_KEYS:
                continue
            itemList = self._gridItemsData[key]
            for i, item in enumerate(itemList):
                if _is_empty_item(item):
                    continue
                if self.PutItemToGrids((key, i), putKeys, False):
                    update = True
        if update:
            self.UpdateAndSyncItemGrids()
        return True

    @_listen_item_changes
    def PutItemToGrids(self, putItem, keys=None, sync=True, flyAnim=True):
        """
        将物品放入指定网格。

        优先与未达到最大堆叠的同种物品进行合堆，若没有同种物品或合堆后仍有剩余则放入空格子，若没有空格子则丢弃到世界（或尝试放入下一个网格）。

        -----

        :param dict|str|tuple[str,int] putItem: 放入的物品，可传入物品信息字典、方格路径或方格位置元组
        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格
        :param bool sync: 是否将物品数据同步到服务端，默认为True，若同时执行多次物品操作，建议前几次设置sync为False，只在最后一次设置为True
        :param bool flyAnim: 是否播放物品飞行动画，默认为True

        :return: 物品放入后所在方格位置元组的列表，放入失败返回空列表
        :rtype: list[tuple[str,int]]
        """
        if not keys:
            keys = self._gridKeys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return []
        if isinstance(putItem, dict):
            putItemDict = _deepcopy(putItem)
        else:
            putItemDict = self.GetItemCellItem(putItem)
            self._setCellItem(putItem, None)
        putPoses = []
        for key in keys:
            poses = self._putItem(putItemDict, key)
            putPoses.extend(poses)
            if putItemDict['count'] <= 0:
                break
        else:
            self.ThrowItem(putItemDict, sync=False)
        if flyAnim and isinstance(putItem, (str, tuple)):
            for toPos in putPoses:
                self._setItemFlyAnim(putItemDict, putItem, toPos)
        if sync and putPoses:
            self.UpdateAndSyncItemGrids()
        return putPoses

    def _putItem(self, putItem, key):
        putPoses = []
        maxStack = _get_max_stack(putItem)
        emptyIndex = []
        if key not in self._gridItemsData:
            return []
        itemList = self._gridItemsData[key]
        # 寻找同种物品放入
        for index, item in enumerate(itemList):
            if _is_empty_item(item):
                emptyIndex.append((key, index))
                continue
            count = item['count']
            if not _is_same_item(item, putItem) or count == maxStack:
                continue
            canPutCount = maxStack - count
            if putItem['count'] <= canPutCount:
                item['count'] += putItem['count']
                putItem['count'] = 0
            else:
                item['count'] = maxStack
                putItem['count'] -= canPutCount
            putPoses.append((key, index))
            if putItem['count'] <= 0:
                break
        else:
            # 没有同种物品则放入空格
            for key, index in emptyIndex:
                count = maxStack if putItem['count'] > maxStack else putItem['count']
                newItem = _deepcopy(putItem)
                newItem['count'] = count
                putItem['count'] -= count
                itemList[index] = newItem
                putPoses.append((key, index))
                if putItem['count'] <= 0:
                    break
        return putPoses

    def ThrowItem(self, what, count=-1, sync=True):
        """
        将物品丢弃到世界。

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
                sync
            )
        if count >= 0:
            item['count'] = count
        self.cs.NotifyToServer("_ThrowItem", item)
        return True

    def SyncAllItemsFromServer(self, keys=None):
        """
        从服务端同步所有物品数据到客户端，并刷新网格。

        -----

        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格

        :return: 是否同步成功
        :rtype: bool
        """
        if not keys:
            keys = self._gridKeys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not self.AllItemGridsInited(keys):
                return False
        self.cs.NotifyToServer("_SyncItems", {'namespace': self.__namespace, 'keys': keys})
        return True

    @_ui_listener(namespace="NuoyanLib", system_name="_TransitServerSystem")
    def _SyncItems(self, args):
        data = args['data']
        namespace = args['namespace']
        if namespace != self.__namespace:
            return
        self.OnReceiveItemsDataFromServerBefore({'data': data})
        for key, itemList in data.items():
            self.SetItemGridItems(itemList, key, False)

    def SetSelectedItem(self, cell, selected=True):
        """
        设置指定物品的选中状态。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param bool selected: 是否选中，默认为True

        :return: 是否设置成功
        :rtype: bool
        """
        if not self._is_cell_exist(cell):
            return False
        defaultImg = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_DEFAULT).asImage()
        if selected:
            bp = self.GetItemCellPath(cell)
            pos = self.GetItemCellPos(cell)
            itemDict = self.GetItemCellItem(cell)
            args = {
                'itemDict': itemDict,
                'cellPath': bp,
                'cellPos': pos,
                'cancel': False,
            }
            self.OnItemGridSelectedItem(args)
            if not args['cancel']:
                defaultImg.SetSprite(_IMAGE_PATH_ITEM_CELL_SELECTED)
                self._selectedItem = {'itemDict': itemDict, 'bp': bp}
            else:
                return False
        else:
            defaultImg.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
            self.ClearItemGridState()
        return True

    def GetSelectedItem(self):
        """
        获取当前选中的物品的数据。

        -----

        :return: 选中物品数据字典，没有选中物品时返回空字典
        :rtype: dict[str,dict|str]
        """
        return self._selectedItem

    def SetItemHeapData(self, cell, count):
        """
        设置物品分堆数据。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组
        :param int count: 分堆数量

        :return: 设置成功时返回分堆数据字典，失败时返回None
        :rtype: dict[str,dict|int|bool|ProgressBarUIControl]|None
        """
        if not self._is_cell_exist(cell):
            return
        itemDict = self.GetItemCellItem(cell)
        heapBar = self.GetItemCellUIControl(cell).GetChildByName(_UI_NAME_HEAP).asProgressBar()
        heapBar.SetVisible(True)
        heapBar.SetValue(float(count) / itemDict['count'])
        self._itemHeapData = {
            'itemDict': itemDict,
            'selectedCount': count,
            'animating': False,
            'barCtrl': heapBar,
        }
        return self._itemHeapData

    def GetItemHeapData(self):
        """
        获取物品分堆数据。

        -----

        :return: 分堆数据字典，没有分堆数据时返回空字典
        :rtype: dict[str,dict|int|bool|ProgressBarUIControl]
        """
        return self._itemHeapData

    # ========================================== Basic Function ========================================================

    def RegisterItemGrid(self, key, path, isSingle=False):
        """
        注册网格或注册单个方格按钮。如果注册的是单个方格按钮，则该方格按钮将被视为只有一个元素的网格。

        | 当网格的key为shortcut、inv27或inv36时，将获得以下特殊功能：
        * 该网格将与本地玩家的背包进行绑定，shortcut表示快捷栏，inv27表示除快捷栏以外的物品栏，inv36表示整个物品栏。
        * 调用SyncAllItemsFromServer时将从服务端获取玩家所有背包物品，并显示到对应的网格上。
        * 对这些网格进行的任何物品操作可自动与本地玩家的背包进行同步。

        -----

        :param str key: 网格的key
        :param str path: 网格的UI路径
        :param bool isSingle: 是否是单个方格按钮，默认为False

        :return: 是否注册成功
        :rtype: bool
        """
        if key in self._gridKeys:
            return False
        self._gridPaths[key] = (path, isSingle)
        self._gridKeys.append(key)
        if key == _INV27 or key == _SHORTCUT:
            if _INV36 not in self._gridItemsData:
                self._gridItemsData[key] = []
            else:
                self._gridItemsData[key] = getattr(self._gridItemsData[_INV36], key)
        elif key == _INV36:
            shortcut = self._gridItemsData.get(_SHORTCUT, [])
            inv27 = self._gridItemsData.get(_INV27, [])
            self._gridItemsData[_INV36] = _Inv36ItemList(shortcut, inv27)
        else:
            self._gridItemsData[key] = []
        return True

    def InitItemGrids(self, keys=None, finishedFunc=None, *args, **kwargs):
        """
        初始化网格。初始化前请先使用RegisterItemGrid注册网格。仅在网格显示时调用才有效，调用该接口时无需设置延迟。

        -----

        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格
        :param function|None finishedFunc: 初始化完成后调用的函数，默认为None
        :param Any args: 变长参数，传入finishedFunc
        :param Any kwargs: 字典变长参数，传入finishedFunc

        :return: 是否初始化成功
        :rtype: bool
        """
        if not keys:
            keys = self._gridKeys
        else:
            if isinstance(keys, str):
                keys = (keys,)
            if not all(i in self._gridKeys for i in keys):
                return False
        _LvComp.Game.AddTimer(0, self._initItemGrids, keys, finishedFunc, args, kwargs)
        return True

    def _initItemGrids(self, keys, finishedFunc, args, kwargs):
        for key in keys:
            if key in self._initedKeys:
                continue
            # 获取网格所有元素的路径
            gp, isSingle = self._gridPaths[key]
            if isSingle:
                allChildren = (gp,)
            else:
                allChildren = tuple(_get_direct_children_path(gp, self))
            # 初始化操作
            self._cellUiCtrls[key] = []
            for i, path in enumerate(allChildren):
                pos = (key, i)
                self._cellPoses[path] = pos
                self._cellPaths[pos] = path
                self._gridItemsData[key].append(None)
                btn = self.GetBaseUIControl(path).asButton()
                btn.AddTouchEventParams()
                btn.SetButtonTouchMoveInCallback(self._onItemCellTouchMoveIn)
                btn.SetButtonTouchMoveCallback(self.OnItemCellTouchMove)
                btn.GetChildByName("heap").SetVisible(False)
                self.SetButtonDoubleClickCallback(
                    path,
                    self._onItemCellDoubleClick,
                    self._onItemCellTouchUp,
                )
                self.SetButtonLongClickCallback(
                    path,
                    self._onItemCellLongClick,
                    self._onItemCellTouchUp,
                    self.OnItemCellTouchMoveOut,
                    self._onItemCellTouchDown,
                    self.OnItemCellTouchCancel,
                )
                self._cellUiCtrls[key].append(btn)
                self.SetItemCellRenderer(pos, None)
                self.SetItemCellCountLabel(pos, None)
                self.SetItemCellDurabilityBar(pos, None)
            if key not in _RESERVED_KEYS:
                self.cs.NotifyToServer("_InitItemGrid", {
                    'key': key,
                    'count': len(allChildren),
                    'namespace': self.__namespace
                })
            self._initedKeys.append(key)
        if finishedFunc:
            finishedFunc(*args, **kwargs)

    def AllItemGridsInited(self, keys=None):
        """
        判断网格是否完成初始化。

        -----

        :param str|tuple[str,...]|None keys: 网格的key，多个网格可使用元组，也可不传该参数，表示所有已注册网格

        :return: 网格均已完成初始化时返回True，否则返回False
        :rtype: bool
        """
        if not keys:
            keys = self._gridKeys
        elif isinstance(keys, str):
            keys = (keys,)
        return all(key in self._initedKeys for key in keys)

    def GetItemGridKey(self, cell):
        """
        获取方格所在网格的key。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 方格所在网格的key，获取不到返回None
        :rtype: str|None
        """
        if isinstance(cell, tuple):
            return cell[0]
        for (key, _), path in self._cellPaths.items():
            if cell == path:
                return key

    def GetItemCellPath(self, cell):
        """
        根据方格位置元组获取方格路径。若传入方格路径，则返回其本身。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 方格路径，获取不到返回None
        :rtype: str|None
        """
        if isinstance(cell, str):
            return cell
        return self._cellPaths.get(cell)

    def GetItemCellPos(self, cell):
        """
        根据方格路径获取方格位置元组。若传入方格位置元组，则返回其本身。

        -----

        :param str|tuple[str,int] cell: 方格路径或方格位置元组

        :return: 方格位置元组，获取不到返回None
        :rtype: tuple[str,int]|None
        """
        if isinstance(cell, tuple):
            return cell
        return self._cellPoses.get(cell)



















