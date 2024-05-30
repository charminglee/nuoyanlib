# -*- coding: utf-8 -*-
# ====================================================
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-05-30
#
# ====================================================


MOD_NAME = "ItemGridDemo"
MOD_NAME_S = MOD_NAME.lower()
MOD_VERSION = "0.0.1"
CLIENT_SYSTEM_NAME = "%sClientSystem" % MOD_NAME
CLIENT_SYSTEM_CLASS_PATH = "{0}Scripts.modClient.{0}ClientSystem.{1}".format(MOD_NAME_S, CLIENT_SYSTEM_NAME)
SERVER_SYSTEM_NAME = "%sServerSystem" % MOD_NAME
SERVER_SYSTEM_CLASS_PATH = "{0}Scripts.modServer.{0}ServerSystem.{1}".format(MOD_NAME_S, SERVER_SYSTEM_NAME)


UI_NAME_CUSTOM_ITEM_GRID_SCREEN = "CustomItemGridScreen"
UI_PATH_CUSTOM_ITEM_GRID_SCREEN = MOD_NAME_S + "Scripts.modClient.ui.customItemGridScreen.CustomItemGridScreen"
UI_DEF_CUSTOM_ITEM_GRID_SCREEN = "CustomItemGridScreen.main"
UI_PATH_CLOSE_BTN = "/stack_panel/panel/close_btn"
UI_PATH_CUSTOM_INV27_GRID = "/stack_panel/inv27_grid"
UI_PATH_CUSTOM_SHORTCUT_GRID = "/stack_panel/shortcut_grid"
UI_PATH_EXTRA_GRID = "/stack_panel/panel/extra_gird"









