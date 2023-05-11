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
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-05-11
#
# ====================================================


from copy import deepcopy as _deepcopy
import mod.client.extraClientApi as _clientApi
from ...utils.item import is_same_item as _is_same_item, is_empty_item as _is_empty_item, \
    get_max_stack as _get_max_stack
from .utils import get_ui_screen_pos as _get_ui_screen_pos
from itemFlyAnim import ItemFlyAnim as _ItemFlyAnim
from itemTipsBox import ItemTipsBox as _ItemTipsBox
from ..._config import MOD_NAME as _MOD_NAME, SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME
from ...mctypes.client.ui.controls.buttonUIControl import ButtonUIControl as _ButtonUIControl
from collections import Callable as _Callable


_ClientSystem = _clientApi.GetClientSystemCls()
_ClientCompFactory = _clientApi.GetEngineCompFactory()
_PLAYER_ID = _clientApi.GetLocalPlayerId()
_PlayerItemComp = _ClientCompFactory.CreateItem(_PLAYER_ID)
_PlayerGameComp = _ClientCompFactory.CreateGame(_PLAYER_ID)


_IMAGE_PATH_ITEM_CELL_SELECTED = "textures/ui/recipe_book_button_borderless_lightpressed"
_IMAGE_PATH_ITEM_CELL_DEFAULT = "textures/ui/item_cell"


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
        return self.toList()[index]

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
        list.__init__(self, self.toList())

    def __contains__(self, y):
        return y in self.toList()

    def __len__(self):
        return len(self.toList())

    def append(self, obj):
        if len(self.shortcut) < 9:
            self.shortcut.append(obj)
        elif len(self.inv27) < 27:
            self.inv27.append(obj)
        list.__init__(self, self.toList())

    def toList(self):
        return self.shortcut + self.inv27


def _listen_item_changes(func):
    def wrapper(self, *args, **kwargs):
        old = _deepcopy(self.gridItemsData)
        res = func(self, *args, **kwargs)
        new = _deepcopy(self.gridItemsData)
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
        self.gridKeys = []
        self.blockPaths = {}
        self.blockPoses = {}
        self.blockUiCtrls = {}
        self._moveInGridList = []
        self._inited = []
        self.__tick = 0
        self._orgItem = {}
        self.__namespace = self.__class__.__name__
        self._changes = {}
        self._lockedBlocks = set()
        self._lockedGrids = set()
        self.__listen()

    def __listen(self):
        clientNamespace = _clientApi.GetEngineNamespace()
        clientSystemName = _clientApi.GetEngineSystemName()
        self.cs.ListenForEvent(clientNamespace, clientSystemName, "GetEntityByCoordReleaseClientEvent", self, self._OnCoordRelease)
        self.cs.ListenForEvent(_MOD_NAME, _SERVER_SYSTEM_NAME, "_SyncItems", self, self._receiveItemsData)

    def Update(self):
        super(ItemGridManager, self).Update()
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

    # todo:==================================== System Event Callback ==================================================

    def _OnCoordRelease(self, args):
        if len(self._moveInGridList) >= 2:
            self.SetSelectedItem(self.selectedItem['bp'], False)
        self._moveInGridList = []
        self._orgItem = {}

    # todo:==================================== Custom Event Callback ==================================================

    def OnItemGridChanged(self, args):
        """
        网格内的物品发生改变时触发。
        -----------------------------------------------------------
        【changes: Dict[Tuple[str, int], Dict[str, dict]]】 字典，key为发生改变的方格的位置元组，value为另一个字典，结构为：{'old': 改变前的物品信息字典, 'new': 改变后的物品信息字典}
        """

    def OnItemGridSelectedItem(self, args):
        """
        网格内的物品被选中时触发。
        -----------------------------------------------------------
        【itemDict: dict】 物品信息字典
        【blockPath: str】 方格路径
        【blockPos: Tuple[str, int]】 方格位置元组
        【$cancel: bool】 是否取消选中
        """

    # todo:========================================= UI Callback =======================================================

    def OnItemBlockTouchUp(self, args):
        """
        方格抬起时触发的回调函数。
        """

    def _onItemBlockTouchUp(self, args):
        self.OnItemBlockTouchUp(args)
        bp = args['ButtonPath']
        if self.IsItemBlockLocked(bp):
            return
        itemDict = self.GetBlockItem(bp)
        if self.selectedItem:
            fromPath = self.selectedItem['bp']
            count = self.itemHeapData['selectedCount'] if self.itemHeapData else -1
            self.MoveItems(fromPath, bp, count)
            self.SetSelectedItem(fromPath, False)
        elif not _is_empty_item(itemDict):
            self.SetSelectedItem(bp, True)
        self.StopItemHeapProgressBar()

    def OnItemBlockTouchMoveIn(self, args):
        """
        手指移动到方格内时触发的回调函数
        """

    def _onItemBlockTouchMoveIn(self, args):
        self.OnItemBlockTouchMoveIn(args)
        bp = args['ButtonPath']
        if self.IsItemBlockLocked(bp):
            return
        if self.itemHeapData or not self.selectedItem:
            return
        fromPath = self.selectedItem['bp']
        itemDict = self.GetBlockItem(bp)
        if bp == fromPath or not _is_empty_item(itemDict):
            return
        if not self._moveInGridList:
            self._orgItem = self.selectedItem['itemDict']
        if bp not in self._moveInGridList:
            self._moveInGridList.append(bp)
        if len(self._moveInGridList) >= 2:
            self.SeparateItemsEvenly(fromPath, self._orgItem, self._moveInGridList)

    def OnItemBlockDoubleClick(self, args):
        """
        双击方格触发的回调函数。
        """

    def _onItemBlockDoubleClick(self, args):
        self.OnItemBlockDoubleClick(args)
        bp = args['ButtonPath']
        if self.IsItemBlockLocked(bp):
            return
        if self.itemHeapData:
            return
        itemDict = self.GetBlockItem(bp)
        if _is_empty_item(itemDict):
            return
        name = itemDict['newItemName']
        aux = itemDict.get('newAuxValue', 0)
        maxStack = _PlayerItemComp.GetItemBasicInfo(name, aux)['maxStackSize']
        if itemDict['count'] < maxStack:
            self.MergeItems(bp)
        self.SetSelectedItem(bp, False)

    def OnItemBlockLongClick(self, args):
        """
        长按方格触发的回调函数。
        """

    def _onItemBlockLongClick(self, args):
        self.OnItemBlockLongClick(args)
        bp = args['ButtonPath']
        if self.IsItemBlockLocked(bp):
            return
        itemDict = self.GetBlockItem(bp)
        if self.selectedItem:
            self.SetSelectedItem(self.selectedItem['bp'], False)
        if not _is_empty_item(itemDict) and itemDict['count'] >= 2:
            self.SetItemHeapData(bp, 1)
            self.StartItemHeapProgressBar()

    def OnItemBlockTouchDown(self, args):
        """
        方格按下时触发的回调函数。
        """

    def _onItemBlockTouchDown(self, args):
        self.OnItemBlockTouchDown(args)
        bp = args['ButtonPath']
        itemDict = self.GetBlockItem(bp)
        self.ShowItemTipsBox(itemDict)

    def OnItemBlockTouchMove(self, args):
        """
        手指在方格上移动时每帧触发的回调函数。
        """

    def OnItemBlockTouchMoveOut(self, args):
        """
        手指移出方格时触发的回调函数。
        """

    def OnItemBlockTouchCancel(self, args):
        """
        方格取消按下时触发的回调函数。
        """

    # todo:=========================================== UI操作 ===========================================================

    def GetAllItemBlockUIControls(self, key):
        # type: (str) -> list[_ButtonUIControl]
        """
        获取指定网格中所有方格的ButtonUIControl实例。
        """
        if not self.AllItemGridsInited(key):
            return
        return self.blockUiCtrls[key]

    def InitItemGrids(self, keys=None, finishedFunc=None, *args, **kwargs):
        # type: (str | tuple[str, ...] | None, _Callable | None, ..., ...) -> None
        """
        初始化网格。
        """
        if not keys:
            keys = self.gridKeys
        elif isinstance(keys, str):
            keys = (keys,)
        _PlayerGameComp.AddTimer(0, self._initItemGrids, keys, finishedFunc, args, kwargs)

    def _initItemGrids(self, keys, finishedFunc, args, kwargs):
        for key, (gp, single) in self.gridPaths.items():
            if key not in keys or key in self._inited:
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
            self.blockPaths[key] = tuple(allChildren)
            self.blockUiCtrls[key] = []
            for i, path in enumerate(allChildren):
                self.SetButtonDoubleClickCallback(
                    path, self._onItemBlockDoubleClick, self._onItemBlockTouchUp
                )
                self.SetButtonLongClickCallback(
                    path, self._onItemBlockLongClick, self._onItemBlockTouchUp, self.OnItemBlockTouchMoveOut,
                    self._onItemBlockTouchDown, self.OnItemBlockTouchCancel
                )
                btn = self.GetBaseUIControl(path).asButton()
                btn.SetButtonTouchMoveInCallback(self._onItemBlockTouchMoveIn)
                btn.SetButtonTouchMoveCallback(self.OnItemBlockTouchMove)
                btn.GetChildByName("heap").SetVisible(False)
                pos = (key, i)
                self.SetItemBlockRenderer(pos, None)
                self.SetItemBlockCountLabel(pos, None)
                self.SetItemBlockDurationBar(pos, None)
                self.blockPoses[path] = pos
                self.gridItemsData[key].append(None)
                self.blockUiCtrls[key].append(btn)
            self.blockUiCtrls[key] = tuple(self.blockUiCtrls[key])
            if key not in _RESERVED_KEYS:
                self.cs.NotifyToServer("_InitItemGrid", {
                    'key': key,
                    'count': len(allChildren),
                    'namespace': self.__namespace
                })
            self._inited.append(key)
        if finishedFunc:
            finishedFunc(*args, **kwargs)

    def SetItemBlockDurationBar(self, block, itemDict):
        # type: (str | tuple[str, int], dict) -> None
        """
        设置物品耐久显示。
        """
        bp = self.GetItemBlockPath(block)
        durCtrl = self.GetBaseUIControl(bp).GetChildByName("durability").asProgressBar()
        if not _is_empty_item(itemDict):
            dur = float(itemDict.get('durability', 0))
            itemName = itemDict['newItemName']
            aux = itemDict.get('newAuxValue', 0)
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

    def SetItemBlockRenderer(self, block, itemDict):
        # type: (str | tuple[str, int], dict) -> None
        """
        设置物品渲染器显示物品。
        """
        bp = self.GetItemBlockPath(block)
        itemRenderer = self.GetBaseUIControl(bp).GetChildByName("item_renderer").asItemRenderer()
        if not _is_empty_item(itemDict):
            itemRenderer.SetVisible(True)
            name = itemDict['newItemName']
            aux = itemDict.get('newAuxValue', 0)
            isEnchanted = bool(itemDict.get('enchantData') or itemDict.get('modEnchantData'))
            userData = itemDict.get('userData')
            itemRenderer.SetUiItem(name, aux, isEnchanted, userData)
        else:
            itemRenderer.SetVisible(False)

    def SetItemBlockCountLabel(self, block, itemDict):
        # type: (str | tuple[str, int], dict) -> None
        """
        物品数量文本显示。
        """
        bp = self.GetItemBlockPath(block)
        label = self.GetBaseUIControl(bp).GetChildByName("count").asLabel()
        count = itemDict.get('count', 1) if not _is_empty_item(itemDict) else 0
        if count > 1:
            label.SetVisible(True)
            label.SetText(str(int(count)))
        else:
            label.SetVisible(False)

    def UpdateAndSyncItemGrids(self, *keys):
        # type: (str) -> None
        """
        刷新网格并向服务端同步数据。
        """
        if not self.AllItemGridsInited():
            return
        keys = set(keys if keys else self.gridKeys)
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
                data[k] = items.toList()
        self.cs.NotifyToServer("_UpdateItemsData", {
            'data': data,
            'namespace': self.__namespace,
        })

    def ClearItemGridState(self):
        # type: () -> None
        """
        清除网格状态（如物品选中状态等）。
        """
        if self.selectedItem:
            bp = self.selectedItem['bp']
            defaultImg = self.GetBaseUIControl(bp).GetChildByName("default").asImage()
            defaultImg.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
            self.selectedItem = {}
        if self.itemHeapData:
            self.itemHeapData['barCtrl'].SetVisible(False)
            self.itemHeapData = {}

    def _setItemFlyAnim(self, itemDict, fromBlock, toBlock):
        fromPath = self.GetItemBlockPath(fromBlock)
        fromPos = _get_ui_screen_pos(self, fromPath)
        uiSize = self.GetBaseUIControl(fromPath).GetSize()
        toPath = self.GetItemBlockPath(toBlock)
        toPos = _get_ui_screen_pos(self, toPath)
        self.SetOneItemFlyAnim(itemDict, fromPos, toPos, uiSize)

    def StartItemHeapProgressBar(self):
        # type: () -> None
        """
        开始物品分堆进度条动画。
        """
        if self.itemHeapData:
            self.itemHeapData['barCtrl'].SetVisible(True)
            self.itemHeapData['animating'] = True
            self.__tick = 0

    def StopItemHeapProgressBar(self):
        # type: () -> None
        """
        停止物品分堆进度条动画。
        """
        if self.itemHeapData:
            self.itemHeapData['animating'] = False

    # todo:=========================================== 物品操作 ==========================================================

    def LockItemGrid(self, key, lock):
        # type: (str, bool) -> None
        """
        锁定或解锁指定网格，锁定后该网格内的所有方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。
        """
        if lock:
            self._lockedGrids.add(key)
        else:
            self._lockedGrids.discard(key)

    def IsItemGridLocked(self, key):
        # type: (str) -> bool
        """
        获取指定网格是否被锁定。
        """
        return key in self._lockedGrids

    def LockItemBlock(self, block, lock):
        # type: (str | tuple[str, int], bool) -> None
        """
        锁定或解锁指定方格，锁定后该方格将屏蔽物品点击选中、移动、长按分堆、滑动分堆、双击合堆操作。
        """
        blockPos = self.GetItemBlockPos(block)
        if lock:
            self._lockedBlocks.add(blockPos)
        else:
            self._lockedBlocks.discard(blockPos)

    def IsItemBlockLocked(self, block):
        # type: (str | tuple[str, int]) -> bool
        """
        获取指定方格是否被锁定。
        """
        blockPos = self.GetItemBlockPos(block)
        return blockPos in self._lockedBlocks or blockPos[0] in self._lockedGrids

    def SetGridItems(self, itemDictList, key, sync=True):
        # type: (list[dict], str, bool) -> None
        """
        将物品一键设置到网格的每个方格上。
        """
        if not self.AllItemGridsInited(key):
            return
        for i, itemDict in enumerate(itemDictList):
            self._setBlockItem((key, i), itemDict)
        if sync:
            self.UpdateAndSyncItemGrids(key)

    def GetGridItems(self, key):
        # type: (str) -> list[dict]
        """
        获取网格内的所有物品。
        """
        return _deepcopy(self.gridItemsData[key]) if key in self.gridItemsData else []

    def SetBlockItem(self, block, itemDict, sync=True):
        # type: (str | tuple[str, int], dict, bool) -> None
        """
        将物品显示在指定方格上。
        """
        if not self.AllItemGridsInited():
            return
        self._setBlockItem(block, itemDict)
        if sync:
            self.UpdateAndSyncItemGrids(self.GetItemGridKey(block))

    @_listen_item_changes
    def _setBlockItem(self, block, itemDict):
        key, index = self.GetItemBlockPos(block)
        self.gridItemsData[key][index] = _deepcopy(itemDict)
        self.SetItemBlockRenderer(block, itemDict)
        self.SetItemBlockCountLabel(block, itemDict)
        self.SetItemBlockDurationBar(block, itemDict)

    def GetBlockItem(self, block):
        # type: (str | tuple[str, int]) -> dict | None
        """
        获取方格的物品信息字典。
        """
        try:
            key, index = self.GetItemBlockPos(block)
            return _deepcopy(self.gridItemsData[key][index])
        except:
            return None

    def MoveItems(self, fromBlock, toBlock, moveCount, sync=True, flyAnim=True, force=False):
        # type: (str | tuple[str, int], str | tuple[str, int], int, bool, bool, bool) -> None
        """
        移动物品。
        """
        if not self.AllItemGridsInited():
            return
        fromItem = self.GetBlockItem(fromBlock)
        if _is_empty_item(fromItem):
            return
        toItem = self.GetBlockItem(toBlock)
        if moveCount == -1:
            moveCount = fromItem['count']
        if force or _is_empty_item(toItem):
            self._moveItemsToEmpty(fromBlock, toBlock, moveCount)
        elif _is_same_item(fromItem, toItem):
            if fromBlock != toBlock:
                self._moveItemsToSame(fromBlock, toBlock, moveCount)
        else:
            self._exchangeItems(fromBlock, toBlock)
            if flyAnim:
                self._setItemFlyAnim(toItem, toBlock, fromBlock)
        if sync:
            self.UpdateAndSyncItemGrids()
        if flyAnim:
            self._setItemFlyAnim(fromItem, fromBlock, toBlock)

    def _exchangeItems(self, fromBlock, toBlock):
        fromItem = self.GetBlockItem(fromBlock)
        toItem = self.GetBlockItem(toBlock)
        self._setBlockItem(fromBlock, toItem)
        self._setBlockItem(toBlock, fromItem)

    def _moveItemsToEmpty(self, fromBlock, toBlock, count):
        fromItem = self.GetBlockItem(fromBlock)
        fromNewCount = fromItem['count'] - count
        fromItem['count'] = count
        self._setBlockItem(toBlock, fromItem)
        fromItem['count'] = fromNewCount
        if fromItem['count'] <= 0:
            fromItem = None
        self._setBlockItem(fromBlock, fromItem)

    def _moveItemsToSame(self, fromBlock, toBlock, count):
        overflowCount = self.SetItemBlockCount(toBlock, +count, sync=False)
        self.SetItemBlockCount(fromBlock, -count + overflowCount, sync=False)

    def MergeItems(self, toBlock, sync=True, flyAnim=True):
        # type: (str | tuple[str, int], bool, bool) -> None
        """
        物品合堆。
        """
        if not self.AllItemGridsInited():
            return
        toBlock = self.GetItemBlockPos(toBlock)
        fromKeys = []
        toItem = self.GetBlockItem(toBlock)
        if _is_empty_item(toItem):
            return
        maxStack = _get_max_stack(toItem)
        for fromKey, fromAllItems in self.gridItemsData.items():
            if toItem['count'] == maxStack:
                break
            for fromIndex, fromItem in enumerate(fromAllItems):
                if toItem['count'] == maxStack:
                    break
                fromBlock = (fromKey, fromIndex)
                if self.IsItemBlockLocked(fromBlock):
                    continue
                if fromBlock == toBlock:
                    continue
                if _is_empty_item(fromItem) or not _is_same_item(fromItem, toItem):
                    continue
                fromCount = fromItem['count']
                if fromCount == maxStack:
                    continue
                self._moveItemsToSame(fromBlock, toBlock, fromCount)
                if flyAnim:
                    self._setItemFlyAnim(fromItem, fromBlock, toBlock)
                fromKeys.append(fromKey)
        if sync:
            self.UpdateAndSyncItemGrids()

    @_listen_item_changes
    def SeparateItemsEvenly(self, fromBlock, fromOrgItem, toBlockList, sync=True):
        # type: (str | tuple[str, int], dict, list[str | tuple[str, int]], bool) -> None
        """
        物品均分。
        """
        if not self.AllItemGridsInited():
            return
        if _is_empty_item(fromOrgItem):
            return
        fromKey, fromIndex = self.GetItemBlockPos(fromBlock)
        fromAllItems = self.gridItemsData[fromKey]
        fromCount = fromOrgItem['count']
        gridCount = len(toBlockList)
        toCount = fromCount / gridCount
        if toCount <= 0:
            return
        for toBlock in toBlockList:
            toKey, toIndex = self.GetItemBlockPos(toBlock)
            toAllItems = self.gridItemsData[toKey]
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

    @_listen_item_changes
    def SetItemBlockCount(self, block, count, absolute=0, sync=True):
        # type: (str | tuple[str, int], int, int, bool) -> int
        """
        设置指定方格内的物品的数量。
        """
        if not self.AllItemGridsInited():
            return 0
        key, index = self.GetItemBlockPos(block)
        item = self.gridItemsData[key][index]
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
            self.gridItemsData[key][index] = None
        if sync:
            self.UpdateAndSyncItemGrids()
        return overflowCount

    def GetItemBlockCount(self, block):
        # type: (str | tuple[str, int]) -> int
        """
        获取指定方格内的物品的数量。
        """
        item = self.GetBlockItem(block)
        return item['count'] if item else -1

    def ReturnItemsToInv(self, items=None, *keys):
        # type: (list[dict] | None, str) -> None
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
            self.UpdateAndSyncItemGrids()

    @_listen_item_changes
    def PutItemToGrids(self, putItem, keys, sync=True, flyAnim=True):
        # type: (dict | str | tuple[str, int], str | tuple[str, ...], bool, bool) -> list[tuple[str, int]]
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
        putPoses = []
        if isinstance(putItem, dict):
            putItemDict = _deepcopy(putItem)
        else:
            putItemDict = self.GetBlockItem(putItem)
            self._setBlockItem(putItem, None)
        if isinstance(keys, str):
            keys = [keys]
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
        if key not in self.gridItemsData:
            return []
        itemList = self.gridItemsData[key]
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
        # type: (dict | str | tuple[str, int], int, bool) -> None
        """
        将物品丢弃到世界。
        """
        if isinstance(what, dict):
            item = _deepcopy(what)
        else:
            item = self.GetBlockItem(what)
            self.SetItemBlockCount(
                what,
                -count if count != -1 else 0,
                0 if count != -1 else 1,
                sync
            )
        if _is_empty_item(item):
            return
        if count != -1:
            item['count'] = count
        self.cs.NotifyToServer("_ThrowItem", item)

    def SyncAllItemsFromServer(self, *keys):
        # type: (str) -> None
        """
        从服务端同步所有物品数据到客户端。
        """
        if not self.AllItemGridsInited():
            return
        self.cs.NotifyToServer("_SyncItems", {
            'namespace': self.__namespace,
            'keys': keys if keys else self.gridKeys
        })

    def _receiveItemsData(self, args):
        data = args['data']
        namespace = args['namespace']
        if namespace != self.__namespace:
            return
        for key, itemList in data.items():
            self.SetGridItems(itemList, key, False)

    def SetSelectedItem(self, block, value):
        # type: (str | tuple[str, int], bool) -> None
        """
        设置指定物品的选中状态。
        """
        if not self.AllItemGridsInited():
            return
        bp = self.GetItemBlockPath(block)
        pos = self.GetItemBlockPos(block)
        itemDict = self.GetBlockItem(block)
        defaultImg = self.GetBaseUIControl(bp).GetChildByName("default").asImage()
        if value:
            args = {
                'itemDict': itemDict,
                'blockPath': bp,
                'blockPos': pos,
                'cancel': False,
            }
            self.OnItemGridSelectedItem(args)
            if not args['cancel']:
                defaultImg.SetSprite(_IMAGE_PATH_ITEM_CELL_SELECTED)
                self.selectedItem = {
                    'itemDict': itemDict,
                    'bp': bp,
                }
        else:
            defaultImg.SetSprite(_IMAGE_PATH_ITEM_CELL_DEFAULT)
            self.ClearItemGridState()

    def GetSelectedItem(self):
        # type: () -> dict
        """
        获取当前选中的物品的数据。
        """
        return self.selectedItem

    def SetItemHeapData(self, block, count):
        # type: (str | tuple[str, int], int) -> None
        """
        设置物品分堆。
        """
        if not self.AllItemGridsInited():
            return
        itemDict = self.GetBlockItem(block)
        bp = self.GetItemBlockPath(block)
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
        # type: () -> dict
        """
        获取当前选中物品的分堆数据。
        """
        return self.itemHeapData

    # todo:======================================= Basic Function ======================================================

    def RegisterItemGrid(self, key, path, single=0):
        # type: (str, str, int) -> None
        """
        注册网格。
        """
        self.gridPaths[key] = (path, single)
        self.gridKeys.append(key)
        if key == _INV27 or key == _SHORTCUT:
            if _INV36 not in self.gridItemsData:
                self.gridItemsData[key] = []
            else:
                self.gridItemsData[key] = getattr(self.gridItemsData[_INV36], key)
        elif key == _INV36:
            shortcut = self.gridItemsData.get(_SHORTCUT, [])
            inv27 = self.gridItemsData.get(_INV27, [])
            self.gridItemsData[_INV36] = _Inv36ItemList(shortcut, inv27)
        else:
            self.gridItemsData[key] = []

    def AllItemGridsInited(self, *keys):
        # type: (str) -> bool
        """
        判断所有已注册的网格是否全部完成初始化。
        """
        if not keys:
            keys = self.gridKeys
        return all((key in self._inited) for key in keys)

    def GetItemGridKey(self, block):
        # type: (str | tuple[str, int]) -> str | None
        """
        获取方格所在网格的key。
        """
        if isinstance(block, tuple):
            return block[0]
        for k, (path, _) in self.gridPaths.items():
            if path in block:
                return k

    def GetItemBlockPath(self, block):
        # type: (str | tuple[str, int]) -> str | None
        """
        获取方格路径。
        """
        if isinstance(block, str):
            return block
        try:
            return self.blockPaths[block[0]][block[1]]
        except (KeyError, IndexError):
            return None

    def GetItemBlockPos(self, block):
        # type: (str | tuple[str, int]) -> tuple[str, int] | None
        """
        获取方格位置。
        """
        if isinstance(block, tuple):
            return block
        try:
            return self.blockPoses[block]
        except KeyError:
            return None





