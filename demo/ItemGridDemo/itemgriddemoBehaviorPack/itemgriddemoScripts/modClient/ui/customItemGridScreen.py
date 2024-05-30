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
from ...modCommon.modConfig import *
import itemgriddemoScripts.nuoyanlib.client as nyl
from itemgriddemoScripts.nuoyanlib.client import (
    listen_for,
    LvComp,
    PlrComp,
    CompFactory,
    PLAYER_ID,
)
# 导入UI端nuoyanlib
from itemgriddemoScripts.nuoyanlib.client.ui import (
    NuoyanScreenNode,
)


# 将UI类继承NuoyanScreenNode，以获得由NuoyanScreenNode提供的接口。
class CustomItemGridScreen(NuoyanScreenNode):
    def __init__(self, namespace, name, param):
        super(CustomItemGridScreen, self).__init__(namespace, name, param)
        self.cs = param['__cs__']
        self.closeBtn = None

    # =========================================== Engine Event Callback ================================================

    def Create(self):
        super(CustomItemGridScreen, self).Create()
        self.closeBtn = self.GetBaseUIControl(UI_PATH_CLOSE_BTN).asButton()
        self.closeBtn.AddTouchEventParams()
        self.closeBtn.SetButtonTouchUpCallback(self.OnCloseBtnTouchUp)
        # 界面显示时若物品网格还未进行初始化，则调用初始化函数
        if not self.AllItemGridsInited():
            self.InitItemGrids()

    # =========================================== Custom Event Callback ================================================

    # ================================================ UI Callback =====================================================

    def OnCloseBtnTouchUp(self, args):
        """
        关闭按钮。
        """
        clientApi.PopScreen()

    # ============================================== Basic Function ====================================================





















