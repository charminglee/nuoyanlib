# -*- coding: utf-8 -*-
# ====================================================
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-05-30
#
# ====================================================


import mod.client.extraClientApi as clientApi
from ..modCommon.modConfig import *
# 导入客户端nuoyanlib
import itemgriddemoScripts.nuoyanlib.client as nyl
# 一些常用的工具可直接导入为模块变量
from itemgriddemoScripts.nuoyanlib.client import (
    NuoyanClientSystem,
    listen_for,
    LvComp,
    PlrComp,
    CompFactory,
    PLAYER_ID,
)


# 将客户端类继承NuoyanClientSystem，以获得由NuoyanClientSystem提供的各种接口。
class ItemGridDemoClientSystem(NuoyanClientSystem):
    def __init__(self, namespace, systemName):
        super(ItemGridDemoClientSystem, self).__init__(namespace, systemName)
        self.customItemGridScrNode = None

    # =========================================== Engine Event Callback ================================================

    # 重写一个与事件同名的方法即可完成对该事件的监听
    def UiInitFinished(self, args):
        # 注册物品网格
        self.RegisterItemGrid(
            "custom_inv_gird", UI_PATH_CUSTOM_ITEM_GRID_SCREEN, UI_PATH_CUSTOM_INV27_GRID, 27
        )
        self.RegisterItemGrid(
            "custom_shortcut_gird", UI_PATH_CUSTOM_ITEM_GRID_SCREEN, UI_PATH_CUSTOM_SHORTCUT_GRID, 9
        )
        self.RegisterItemGrid(
            "custom_extra_gird", UI_PATH_CUSTOM_ITEM_GRID_SCREEN, UI_PATH_EXTRA_GRID, 16
        )
        # 注册自定义物品网格界面
        clientApi.RegisterUI(
            MOD_NAME, UI_NAME_CUSTOM_ITEM_GRID_SCREEN, UI_PATH_CUSTOM_ITEM_GRID_SCREEN, UI_DEF_CUSTOM_ITEM_GRID_SCREEN,
        )

    def RightClickReleaseClientEvent(self, args):
        # 右键打开自定义物品网格界面，注意要将enable_item_grid设置为True才能启用物品网格相关功能
        self.customItemGridScrNode = clientApi.PushScreen(
            MOD_NAME, UI_NAME_CUSTOM_ITEM_GRID_SCREEN, {'enable_item_grid': True, '__cs__': self}
        )

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================





























