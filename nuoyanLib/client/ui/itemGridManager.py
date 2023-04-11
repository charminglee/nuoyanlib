# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-04-11
#
# ====================================================


from time import sleep as _sleep
from threading import Timer as _Timer
from random import randrange as _randrange
from copy import deepcopy as _deepcopy
import mod.client.extraClientApi as _clientApi
from ....nuoyanLib.utils.item import is_same_item as _is_same_item, is_empty_item as _is_empty_item, \
    get_max_stack as _get_max_stack
from ....nuoyanLib.client.ui.utils import get_ui_screen_pos as _get_ui_screen_pos
from itemFlyAnim import ItemFlyAnim as _ItemFlyAnim
from itemTipsBox import ItemTipsBox as _ItemTipsBox
from ..._config import MOD_NAME, SERVER_SYSTEM_NAME


_ClientSystem = _clientApi.GetClientSystemCls()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_PLAYER_ID = _clientApi.GetLocalPlayerId()
_PlayerItemComp = _ClientCompFactory.CreateItem(_PLAYER_ID)
_PlayerGameComp = _ClientCompFactory.CreateGame(_PLAYER_ID)


IMAGE_PATH_ITEM_CELL_SELECTED = "textures/ui/recipe_book_button_borderless_lightpressed"
IMAGE_PATH_ITEM_CELL_DEFAULT = "textures/ui/item_cell"


_SHORTCUT = "shortcut"
_INV27 = "inv27"
_INV36 = "inv36"
_RESERVED_KEYS = (_SHORTCUT, _INV27, _INV36)
_DELAY = 0.05


class _Inv36ItemList(list):
    def __init__(self, shortcut, inv27):
        list.__init__(self, shortcut + inv27)
        self.shortcut = shortcut
        self.inv27 = inv27

    def __getitem__(self, index):
        return self.ToList()[index]

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
        list.__init__(self, self.ToList())

    def __contains__(self, y):
        return y in self.ToList()

    def __len__(self):
        return len(self.ToList())

    def append(self, obj):
        if len(self.shortcut) < 9:
            self.shortcut.append(obj)
        elif len(self.inv27) < 27:
            self.inv27.append(obj)
        list.__init__(self, self.ToList())

    def ToList(self):
        return self.shortcut + self.inv27


def _listen_item_changes(func):
    def wrapper(self, *args, **kwargs):
        old = _deepcopy(self.gridItemsData)
        res = func(self, *args, **kwargs)
        new = _deepcopy(self.gridItemsData)
        changes = _analyze_changes(old, new)
        if changes:
            if self._lsnTimer:
                _PlayerGameComp.CancelTimer(self._lsnTimer)
            _update_changes(self._changes, changes)
            def delayFunc(self_):
                if self_._changes:
                    self_.OnGridItemChanged(self_._changes)
                    self_._changes = {}
                self_._lsnTimer = None
            self._lsnTimer = _PlayerGameComp.AddTimer(_DELAY, delayFunc, self)
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


class ItemGridManager(_ItemFlyAnim, _ItemTipsBox):
    """
    物品网格管理器。
    """

    def __init__(self, namespace, name, param):
        super(ItemGridManager, self).__init__(namespace, name, param)
        self.gridItemsData = {}
        self.itemHeapData = {}
        self.selectedItem = {}
        self.gridPaths = {}
        self.gridKeys = set()
        self.blockPaths = {}
        self.blockPoses = {}
        self._moveInGridList = []
        self._inited = set()
        self.__tick = 0
        self._orgItem = {}
        self.__namespace = self.__class__.__name__
        self._changes = {}
        self._lsnTimer = None
        self.__listen()

    def __listen(self):
        clientNamespace = _clientApi.GetEngineNamespace()
        clientSystemName = _clientApi.GetEngineSystemName()
        self.cs.ListenForEvent(clientNamespace, clientSystemName, "GetEntityByCoordReleaseClientEvent", self, self._OnCoordRelease)
        self.cs.ListenForEvent(clientNamespace, clientSystemName, "OnScriptTickClient", self, self._OnTick)
        self.cs.ListenForEvent(MOD_NAME, SERVER_SYSTEM_NAME, "_SyncItems", self, self._receiveItemsData)

    # todo:==================================== System Event Callback ==================================================

    def _OnTick(self):
        # 物品分堆
        self.__tick += 1
        if self.itemHeapData and self.itemHeapData['animating']:
            count = self.itemHeapData['itemDict']['count']
            if count > 1:
                tick = round(45.0 / (count - 1))
                if tick < 1:
                    tick = 1
                if not self.__tick % tick and self.itemHeapData['selectedCount'] < count:
                    self.itemHeapData['selectedCount'] += 1
                    barCtrl = self.itemHeapData['barCtrl']
                    barCtrl.SetValue(float(self.itemHeapData['selectedCount']) / count)

    def _OnCoordRelease(self, args):
        if len(self._moveInGridList) >= 2:
            self.SetSelectedItem(self.selectedItem['bp'], False)
        self._moveInGridList = []
        self._orgItem = {}

    # todo:==================================== Custom Event Callback ==================================================

    def OnGridItemChanged(self, args):
        """
        网格内的物品改变时触发。
        -----------------------------------------------------------
        【changes: Dict[Tuple[str, int], Dict[str, dict]]】 字典，key为发生改变的方格的位置元组，value为另一个字典，结构为：{'old': 改变前的物品信息字典, 'new': 改变后的物品信息字典}
        """

    def OnSelectedItem(self, args):
        """
        选中物品时触发。
        -----------------------------------------------------------
        【itemDict: dict】 物品信息字典
        【blockPath: str】 所选方格的路径
        【blockPos: Tuple[str, int]】 方格位置元组
        【$cancel: bool】 是否取消选中
        """

    # todo:========================================= UI Callback =======================================================

    def OnBlockButtonTouchUp(self, args):
        """
        方格按下后抬起触发的回调函数。
        """
        bp = args['ButtonPath']
        itemDict = self.GetBlockItem(bp)
        if self.selectedItem:
            fromPath = self.selectedItem['bp']
            count = self.itemHeapData['selectedCount'] if self.itemHeapData else -1
            self.MoveItems(fromPath, bp, count)
            self.SetSelectedItem(fromPath, False)
        elif not _is_empty_item(itemDict):
            self.SetSelectedItem(bp, True)
        self.StopItemHeapProgressBar()

    def OnBlockButtonTouchMoveIn(self, args):
        """
        手指移动到方格内时触发的回调函数
        """
        if self.itemHeapData or not self.selectedItem:
            return
        bp = args['ButtonPath']
        fromPath = self.selectedItem['bp']
        itemDict = self.GetBlockItem(bp)
        if bp == fromPath:
            return
        if not _is_empty_item(itemDict):
            return
        if not self._moveInGridList:
            self._orgItem = self.selectedItem['itemDict']
        if bp not in self._moveInGridList:
            self._moveInGridList.append(bp)
        if len(self._moveInGridList) >= 2:
            self.SeparateItemsEvenly(fromPath, self._orgItem, self._moveInGridList)

    def OnBlockButtonDoubleClick(self, args):
        """
        双击方格触发的回调函数。
        """
        if self.itemHeapData:
            return
        bp = args['ButtonPath']
        itemDict = self.GetBlockItem(bp)
        if _is_empty_item(itemDict):
            return
        name = itemDict['newItemName']
        aux = itemDict['newAuxValue']
        maxStack = _PlayerItemComp.GetItemBasicInfo(name, aux)['maxStackSize']
        if itemDict['count'] < maxStack:
            self.MergeItems(bp)
        self.SetSelectedItem(bp, False)

    def OnBlockButtonLongClick(self, args):
        """
        长按方格触发的回调函数。
        """
        bp = args['ButtonPath']
        itemDict = self.GetBlockItem(bp)
        if self.selectedItem:
            self.SetSelectedItem(self.selectedItem['bp'], False)
        if not _is_empty_item(itemDict) and itemDict['count'] >= 2:
            self.SetItemHeapData(bp, 1)
            self.StartItemHeapProgressBar()

    def OnBlockButtonTouchDown(self, args):
        """
        方格按下时触发的回调函数。
        """
        bp = args['ButtonPath']
        itemDict = self.GetBlockItem(bp)
        self.ShowItemTipsBox(itemDict)

    def OnBlockButtonTouchMove(self, args):
        """
        手指在方格上移动时每帧触发的回调函数。
        """

    def OnBlockButtonTouchMoveOut(self, args):
        """
        手指移出方格时触发的回调函数。
        """

    def OnBlockButtonTouchCancel(self, args):
        """
        方格取消按下时触发的回调函数。
        """

    # todo:=========================================== UI操作 ===========================================================

    def InitItemGrids(self, keys=(), finishedFunc=None, *args, **kwargs):
        """
        初始化网格。
        """
        if not keys:
            keys = self.gridKeys
        _PlayerGameComp.AddTimer(0, self._initItemGrids, keys, finishedFunc, args, kwargs)

    def _initItemGrids(self, keys, finishedFunc, args, kwargs):
        for key, (gp, single) in self.gridPaths.items():
            if key not in keys:
                continue
            if single:
                allChildren = [gp]
            else:
                gpLen = len(gp.split("/"))
                allChildren = []
                for p in self.GetAllChildrenPath(gp):
                    if p.startswith("/safezone_screen_matrix"):
                        p = "/variables_button_mappings_and_controls" + p
                    if len(p.split("/")) == gpLen + 1:
                        allChildren.append(p)
            self.blockPaths[key] = allChildren
            for i, path in enumerate(allChildren):
                self.SetButtonDoubleClickCallback(
                    path, self.OnBlockButtonDoubleClick, self.OnBlockButtonTouchUp
                )
                self.SetButtonLongClickCallback(
                    path, self.OnBlockButtonLongClick, self.OnBlockButtonTouchUp, self.OnBlockButtonTouchMoveOut,
                    self.OnBlockButtonTouchDown, self.OnBlockButtonTouchCancel
                )
                btn = self.GetBaseUIControl(path).asButton()
                btn.SetButtonTouchMoveInCallback(self.OnBlockButtonTouchMoveIn)
                btn.SetButtonTouchMoveCallback(self.OnBlockButtonTouchMove)
                btn.GetChildByName("heap").SetVisible(False)
                self.blockPoses[path] = key, i
                self.gridItemsData[key].append(None)
                self.SetItemRenderer((key, i), None)
                self.SetItemCountLabel((key, i), None)
                self.SetItemDurationBar((key, i), None)
            if key not in _RESERVED_KEYS:
                self.cs.NotifyToServer("_InitItemGrid", {
                    'key': key,
                    'count': len(allChildren),
                    'namespace': self.__namespace
                })
            self._inited.add(key)
        if finishedFunc:
            finishedFunc(*args, **kwargs)

    def SetItemDurationBar(self, block, itemDict):
        """
        设置物品耐久显示。
        """
        bp = self.GetBlockPath(block)
        durCtrl = self.GetBaseUIControl(bp).GetChildByName("durability").asProgressBar()
        if not _is_empty_item(itemDict):
            dur = float(itemDict.get('durability', 0))
            itemName = itemDict['newItemName']
            aux = itemDict['newAuxValue']
            isEnchanted = bool(itemDict.get('enchantData') or itemDict.get('modEnchantData'))
            basicInfo = _PlayerItemComp.GetItemBasicInfo(itemName, aux, isEnchanted)
            maxDur = float(basicInfo['maxDurability'])
            if not dur or dur == maxDur:
                durCtrl.SetVisible(False)
            else:
                durCtrl.SetVisible(True)
                durCtrl.SetValue(dur / maxDur)
        else:
            durCtrl.SetVisible(False)

    def SetItemRenderer(self, block, itemDict):
        """
        设置物品渲染器显示物品。
        """
        bp = self.GetBlockPath(block)
        itemRenderer = self.GetBaseUIControl(bp).GetChildByName("item_renderer").asItemRenderer()
        if not _is_empty_item(itemDict):
            itemRenderer.SetVisible(True)
            name = itemDict['newItemName']
            aux = itemDict['newAuxValue']
            isEnchanted = bool(itemDict.get('enchantData') or itemDict.get('modEnchantData'))
            userData = itemDict.get('userData')
            itemRenderer.SetUiItem(name, aux, isEnchanted, userData)
        else:
            itemRenderer.SetVisible(False)

    def SetItemCountLabel(self, block, itemDict):
        """
        物品数量文本显示。
        """
        bp = self.GetBlockPath(block)
        label = self.GetBaseUIControl(bp).GetChildByName("count").asLabel()
        if not _is_empty_item(itemDict) and itemDict['count'] > 1:
            label.SetVisible(True)
            label.SetText(str(int(itemDict['count'])))
        else:
            label.SetVisible(False)

    def UpdateAndSyncGrid(self, *keys):
        """
        刷新网格并向服务端同步数据。
        """
        if not self.AllItemGridsInited():
            return
        keys = set(keys) if keys else _deepcopy(self.gridKeys)
        if _INV27 in keys or _SHORTCUT in keys:
            keys.add(_INV36)
        keys = {k for k in keys if k in self.gridItemsData}
        data = {}
        for k in keys:
            items = self.gridItemsData[k]
            self.SetGridItems(items, k, False)
            if k != _INV36:
                data[k] = items
            else:
                data[k] = items.ToList()
        self.cs.NotifyToServer("_UpdateItemsData", {
            'data': data,
            'namespace': self.__namespace,
        })

    def ClearGridsState(self):
        """
        清除网格状态（如物品选中状态等）。
        """
        if self.selectedItem:
            bp = self.selectedItem['bp']
            defaultImg = self.GetBaseUIControl(bp).GetChildByName("default").asImage()
            defaultImg.SetSprite(IMAGE_PATH_ITEM_CELL_DEFAULT)
            self.selectedItem = {}
        if self.itemHeapData:
            self.itemHeapData['barCtrl'].SetVisible(False)
            self.itemHeapData = {}

    def _setItemFlyAnim(self, itemDict, fromBlock, toBlock):
        fromPath = self.GetBlockPath(fromBlock)
        fromPos = _get_ui_screen_pos(self, fromPath)
        uiSize = self.GetBaseUIControl(fromPath).GetSize()
        toPath = self.GetBlockPath(toBlock)
        toPos = _get_ui_screen_pos(self, toPath)
        self.SetOneItemFlyAnim(itemDict, fromPos, toPos, uiSize)

    def StartItemHeapProgressBar(self):
        """
        开始物品分堆进度条。
        """
        if self.itemHeapData:
            self.itemHeapData['barCtrl'].SetVisible(True)
            self.itemHeapData['animating'] = True
            self.__tick = 0

    def StopItemHeapProgressBar(self):
        """
        停止物品分堆进度条。
        """
        if self.itemHeapData:
            self.itemHeapData['animating'] = False

    # todo:=========================================== 物品操作 ==========================================================

    def SetGridItems(self, itemDictList, key, sync=True):
        """
        将物品一键设置到网格的每个方格上。
        """
        if not self.AllItemGridsInited(key):
            return
        for i, itemDict in enumerate(itemDictList):
            self.SetBlockItem((key, i), itemDict, False)
        if sync:
            self.UpdateAndSyncGrid(key)

    def GetGridItems(self, key):
        """
        获取网格内的所有物品。
        """
        return self.gridItemsData[key] if key in self.gridItemsData else []

    @_listen_item_changes
    def SetBlockItem(self, block, itemDict, sync=True):
        """
        将物品显示在指定方格上。
        """
        if not self.AllItemGridsInited():
            return
        key, index = self.GetBlockPos(block)
        itemList = self.gridItemsData[key]
        itemList[index] = itemDict
        self.SetItemRenderer(block, itemDict)
        self.SetItemCountLabel(block, itemDict)
        self.SetItemDurationBar(block, itemDict)
        if sync:
            self.UpdateAndSyncGrid(key)

    def GetBlockItem(self, block):
        """
        获取方格的物品信息字典。
        """
        if isinstance(block, str):
            key, index = self.GetBlockPos(block)
        else:
            key, index = block
        try:
            return self.gridItemsData[key][index]
        except:
            return None

    def MoveItems(self, fromBlock, toBlock, moveCount, sync=True, flyAnim=True, force=False):
        """
        移动物品。
        """
        if not self.AllItemGridsInited():
            return
        fromItem = self.GetBlockItem(fromBlock)
        if _is_empty_item(fromItem):
            return
        toItem = self.GetBlockItem(toBlock)
        fromPath = self.GetBlockPath(fromBlock)
        toPath = self.GetBlockPath(toBlock)
        fromUiPos = _get_ui_screen_pos(self, fromPath)
        toUiPos = _get_ui_screen_pos(self, toPath)
        fromUiSize = self.GetBaseUIControl(fromPath).GetSize()
        toUiSize = self.GetBaseUIControl(toPath).GetSize()
        if moveCount == -1:
            moveCount = fromItem['count']
        if force or _is_empty_item(toItem):
            self._moveItemsToEmpty(fromBlock, toBlock, moveCount)
        elif _is_same_item(fromItem, toItem):
            if fromBlock != toBlock:
                self._moveItemsToSame(fromBlock, toBlock, fromItem['count'])
        else:
            self._exchangeItems(fromBlock, toBlock)
            if flyAnim:
                self.SetOneItemFlyAnim(toItem, toUiPos, fromUiPos, toUiSize)
        if sync:
            self.UpdateAndSyncGrid(self.GetGridKey(fromBlock), self.GetGridKey(toBlock))
        if flyAnim:
            self.SetOneItemFlyAnim(fromItem, fromUiPos, toUiPos, fromUiSize)

    def _exchangeItems(self, fromBlock, toBlock):
        fromItem = self.GetBlockItem(fromBlock)
        toItem = self.GetBlockItem(toBlock)
        self.SetBlockItem(fromBlock, toItem, False)
        self.SetBlockItem(toBlock, fromItem, False)

    def _moveItemsToEmpty(self, fromBlock, toBlock, count):
        fromItem = self.GetBlockItem(fromBlock)
        self.SetBlockItem(toBlock, _deepcopy(fromItem), False)
        self.SetBlockItemCount(toBlock, count, 1, False)
        self.SetBlockItemCount(fromBlock, -count, 0, False)

    def _moveItemsToSame(self, fromBlock, toBlock, count):
        overflowCount = self.SetBlockItemCount(toBlock, count, 0, False)
        self.SetBlockItemCount(fromBlock, -count + overflowCount, 0, False)

    def MergeItems(self, toBlock, sync=True, flyAnim=True):
        """
        物品合堆。
        """
        if not self.AllItemGridsInited():
            return
        toBlock = self.GetBlockPos(toBlock)
        fromTypes = []
        toItem = self.GetBlockItem(toBlock)
        if _is_empty_item(toItem):
            return
        maxStack = _get_max_stack(toItem)
        for fromType, fromAllItems in self.gridItemsData.items():
            if toItem['count'] == maxStack:
                break
            for fromIndex, fromItem in enumerate(fromAllItems):
                fromBlock = (fromType, fromIndex)
                if fromBlock == toBlock:
                    continue
                if toItem['count'] == maxStack:
                    break
                if _is_empty_item(fromItem) or not _is_same_item(fromItem, toItem):
                    continue
                if fromItem['count'] == maxStack:
                    continue
                overflow = self.SetBlockItemCount(toBlock, fromItem['count'], 0, False)
                self.SetBlockItemCount(fromBlock, overflow, 1, False)
                if flyAnim:
                    self._setItemFlyAnim(fromItem, fromBlock, toBlock)
                fromTypes.append(fromType)
        if sync:
            self.UpdateAndSyncGrid(self.GetGridKey(toBlock), *fromTypes)

    @_listen_item_changes
    def SeparateItemsEvenly(self, fromBlock, fromOrgItem, toBlockList, sync=True):
        """
        物品均分。
        """
        if not self.AllItemGridsInited():
            return
        if _is_empty_item(fromOrgItem):
            return
        fromType, fromIndex = self.GetBlockPos(fromBlock)
        fromAllItems = self.gridItemsData[fromType]
        fromCount = fromOrgItem['count']
        gridCount = len(toBlockList)
        toCount = fromCount / gridCount
        if toCount <= 0:
            return
        for toPath in toBlockList:
            toType, toIndex = self.GetBlockPos(toPath)
            toAllItems = self.gridItemsData[toType]
            toAllItems[toIndex] = _deepcopy(fromOrgItem)
            toAllItems[toIndex]['count'] = toCount
        remainCount = fromCount % gridCount
        if remainCount >= 1:
            fromAllItems[fromIndex] = _deepcopy(fromOrgItem)
            fromAllItems[fromIndex]['count'] = remainCount
        else:
            fromAllItems[fromIndex] = None
        toTypes = [self.GetGridKey(i) for i in toBlockList]
        if sync:
            self.UpdateAndSyncGrid(fromType, *toTypes)

    @_listen_item_changes
    def SetBlockItemCount(self, block, count, absolute=0, sync=True):
        """
        设置指定方格内的物品的数量。
        """
        if not self.AllItemGridsInited():
            return 0
        item = self.GetBlockItem(block)
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
            key, index = self.GetBlockPos(block)
            self.gridItemsData[key][index] = None
        if sync:
            self.UpdateAndSyncGrid(self.GetGridKey(block))
        return overflowCount

    def GetBlockItemCount(self, block):
        """
        获取指定方格内的物品的数量。
        """
        item = self.GetBlockItem(block)
        return item['count'] if item else 0

    def ReturnItemsToInv(self, items=None, *keys):
        """
        将所有背包外的物品返还给背包。
        """
        if not self.AllItemGridsInited():
            return
        if _INV36 not in self.gridKeys and (_SHORTCUT not in self.gridKeys or _INV27 not in self.gridKeys):
            return
        update = False
        if items:
            for i in items:
                if self.PutItemToGrids(i, _RESERVED_KEYS, False):
                    update = True
        else:
            if not keys:
                keys = self.gridKeys
            for key, itemList in self.gridItemsData.items():
                if key in _RESERVED_KEYS or key not in keys:
                    continue
                for i, item in enumerate(itemList):
                    if _is_empty_item(item):
                        continue
                    if self.PutItemToGrids((key, i), _RESERVED_KEYS, False):
                        update = True
        if update:
            self.UpdateAndSyncGrid()

    @_listen_item_changes
    def PutItemToGrids(self, putItem, keys, sync=True):
        # type: (dict | str | tuple[str, int], str | tuple[str, ...], bool) -> list[tuple[str, int]]
        """
        将物品放入指定网格。
        优先与未达到最大堆叠的同种物品进行合堆，若没有同种物品或合堆后仍有剩余则放入空格子，若没有空格子则丢弃到世界（或尝试放入下一个网格）。
        -----------------------------------------------------------
        【putItem: Union[dict, str, Tuple[str, int]]】 放入的物品，可传入物品信息字典、方格路径或方格位置元组
        【keys: Union[str, Tuple[str, ...]]】 放入的网格的key，多个网格请用元组，当某个网格无法完全放入物品时，剩余物品会尝试放入下一个网格
        【sync: bool = True】 是否刷新数据，若同时执行多次物品操作，建议前几次设置sync为False，只在最后一次设置为True
        -----------------------------------------------------------
        return: List[Tuple[str, int]] -> 物品放入后所在方格的位置元组的列表
        """
        if not self.AllItemGridsInited():
            return []
        putIndex = []
        if isinstance(putItem, dict):
            fromBlock = None
            putItem = _deepcopy(putItem)
        else:
            fromBlock = putItem
            putItem = _deepcopy(self.GetBlockItem(putItem))
        if isinstance(keys, str):
            keys = [keys]
        for key in keys:
            index = self._putItem(putItem, key)
            putIndex.extend(index)
            if putItem['count'] <= 0:
                break
        else:
            self.ThrowItem(putItem, sync=False)
        if fromBlock:
            self.SetBlockItem(fromBlock, None, False)
        if putIndex and sync:
            self.UpdateAndSyncGrid(fromBlock, *_RESERVED_KEYS)
        return putIndex

    def _putItem(self, putItem, key):
        putIndex = []
        maxStack = _get_max_stack(putItem)
        emptyIndex = []
        if key not in self.gridItemsData:
            return []
        itemList = self.gridItemsData[key]
        # 寻找背包同种物品放入
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
            putIndex.append((key, index))
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
                putIndex.append((key, index))
                if putItem['count'] <= 0:
                    break
        return putIndex

    def ThrowItem(self, what, count=-1, sync=True):
        """
        将物品丢弃到世界。
        """
        if isinstance(what, dict):
            item = what
        else:
            item = self.GetBlockItem(what)
        if _is_empty_item(item):
            return
        throwItem = _deepcopy(item)
        if count != -1:
            throwItem['count'] = count
        self.cs.NotifyToServer("_ThrowItem", throwItem)
        if isinstance(what, (str, tuple)):
            self.SetBlockItemCount(
                what,
                -count if count != -1 else 0,
                0 if count != -1 else 1,
                sync
            )

    def SyncAllItemsFromServer(self, *keys):
        """
        从服务端同步所有物品数据到客户端。
        """
        if not self.AllItemGridsInited():
            return
        self.cs.NotifyToServer("_SyncItems", {
            'namespace': self.__namespace,
            'keys': keys if keys else tuple(self.gridKeys)
        })

    def _receiveItemsData(self, args):
        data = args['data']
        namespace = args['namespace']
        if namespace != self.__namespace:
            return
        for key, itemList in data.items():
            self.SetGridItems(itemList, key, False)

    def SetSelectedItem(self, block, value):
        """
        设置指定物品的选中状态。
        """
        if not self.AllItemGridsInited():
            return
        bp = self.GetBlockPath(block)
        pos = self.GetBlockPos(block)
        itemDict = self.GetBlockItem(block)
        defaultImg = self.GetBaseUIControl(bp).GetChildByName("default").asImage()
        if value:
            args = {
                'itemDict': itemDict,
                'blockPath': bp,
                'blockPos': pos,
                'cancel': False,
            }
            self.OnSelectedItem(args)
            if not args['cancel']:
                defaultImg.SetSprite(IMAGE_PATH_ITEM_CELL_SELECTED)
                self.selectedItem = {
                    'itemDict': itemDict,
                    'bp': bp,
                    'gridType': pos[0],
                    'index': pos[1],
                }
        else:
            defaultImg.SetSprite(IMAGE_PATH_ITEM_CELL_DEFAULT)
            self.ClearGridsState()

    def GetSelectedItem(self):
        """
        获取当前选中的物品的数据。
        """
        return self.selectedItem

    def SetItemHeapData(self, block, count):
        """
        设置物品分堆。
        """
        if not self.AllItemGridsInited():
            return
        itemDict = self.GetBlockItem(block)
        bp = self.GetBlockPath(block)
        heapBar = self.GetBaseUIControl(bp).GetChildByName("heap").asProgressBar()
        heapBar.SetVisible(True)
        heapBar.SetValue(float(count) / itemDict['count'])
        self.itemHeapData = {
            'itemDict': itemDict,
            'selectedCount': count,
            'animating': False,
            'barCtrl': heapBar,
        }

    def GetItemHeapData(self):
        """
        获取当前选中物品的分堆数据。
        """
        return self.itemHeapData

    # todo:======================================= Basic Function ======================================================

    def RegisterItemGrid(self, key, path, single=0):
        """
        注册网格。
        """
        self.gridPaths[key] = path, single
        self.blockPaths[key] = []
        self.gridKeys.add(key)
        if key == _INV27 or key == _SHORTCUT:
            if _INV36 not in self.gridItemsData:
                self.gridItemsData[key] = []
            else:
                self.gridItemsData[key] = getattr(self.gridItemsData[_INV36], key)
        elif key == _INV36:
            shortcut = self.gridItemsData.get(_SHORTCUT, [])
            inv27 = self.gridItemsData.get(_INV27, [])
            self.gridItemsData[key] = _Inv36ItemList(shortcut, inv27)
        else:
            self.gridItemsData[key] = []

    def AllItemGridsInited(self, *keys):
        """
        判断所有注册的网格是否均已完成初始化。
        """
        if not keys:
            keys = self.gridKeys
        return all((key in self._inited) for key in keys)

    def GetGridKey(self, block):
        """
        获取方格所在网格的key。
        """
        if isinstance(block, tuple):
            return block[0]
        for k, (gp, _) in self.gridPaths.items():
            if gp in block:
                return k

    def GetBlockPath(self, block):
        """
        获取方格路径。
        """
        if isinstance(block, str):
            return block
        try:
            return self.blockPaths[block[0]][block[1]]
        except (KeyError, IndexError):
            return None

    def GetBlockPos(self, path):
        """
        获取方格位置。
        """
        if isinstance(path, tuple):
            return path
        try:
            return self.blockPoses[path]
        except KeyError:
            return None


def _test_listen_item_changes(func):
    def wrapper(self, *args, **kwargs):
        old = _deepcopy(self.gridItemsData)
        res = func(self, *args, **kwargs)
        new = _deepcopy(self.gridItemsData)
        changes = _analyze_changes(old, new)
        if changes:
            if self._lsnTimer and self._lsnTimer.isAlive():
                self._lsnTimer.cancel()
            else:
                self._changes = {}
            _update_changes(self._changes, changes)
            self._lsnTimer = _Timer(_DELAY, self.OnGridItemChanged, (self._changes,))
            self._lsnTimer.start()
        return res
    return wrapper


def _test():
    lst1 = [1, 2]
    lst2 = [1, 2, 3]
    inv36 = _Inv36ItemList(lst1, lst2)
    print inv36[0], inv36[3], inv36[-1]  # 1, 2, 3
    print "=" * 50

    lst1.append("a")
    lst2.append("b")
    print inv36.ToList()  # [1, 2, "a", 1, 2, 3, "b"]
    print "=" * 50

    inv36[0] = 11
    inv36[3] = 11
    inv36[-3] = 22
    inv36[-6] = 22
    print lst1, lst2  # [11, 22, "a"], [11, 22, 3, "b"]
    print "=" * 50

    for i in inv36:
        print i  # 11, 22, "a", 11, 22, 3, "b"
    print "=" * 50

    inv36.append("test")
    print lst1, lst2  # [11, 22, "a", "test"], [11, 22, 3, "b"]
    print "test" in inv36, "a" in inv36  # True, True
    print "=" * 50

    class Test(object):
        def __init__(self):
            self._changes = {}
            self._lsnTimer = None
            self.gridItemsData = {
                'k1': [None] * 9,
                'k2': [None] * 27,
            }

        def OnGridItemChanged(self, args):
            print args

        @_test_listen_item_changes
        def change(self):
            r1, r2, r3, r4 = _randrange(9), _randrange(27), _randrange(100), _randrange(100)
            self.gridItemsData['k1'][r1] = r3
            self.gridItemsData['k2'][r2] = r4
            return "k1:%d -> %d; k2:%d -> %d" % (r1, r3, r2, r4)

    t = Test()
    for i in range(3):
        # noinspection PyArgumentList
        print t.change()
        if i == 2:
            _sleep(1)
            # noinspection PyArgumentList
            print t.change()



