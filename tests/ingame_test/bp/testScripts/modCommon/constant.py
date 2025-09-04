# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-09
|
| ==============================================
"""


MOD_NAME = "Template"
MOD_NAME_S = MOD_NAME.lower()
MOD_VERSION = "0.0.1"
CLIENT_SYSTEM_NAME = "%sClientSystem" % MOD_NAME
CLIENT_SYSTEM_CLASS_PATH = "{0}Scripts.{0}ClientSystem.{1}".format(MOD_NAME_S, CLIENT_SYSTEM_NAME)
SERVER_SYSTEM_NAME = "%sServerSystem" % MOD_NAME
SERVER_SYSTEM_CLASS_PATH = "{0}Scripts.{0}ServerSystem.{1}".format(MOD_NAME_S, SERVER_SYSTEM_NAME)


# 注册管理器
CLIENT_MGRS = {
    # 'template': MOD_NAME_S + "Scripts.mgr.templateMgr.templateClientMgr.TemplateClientMgr",
}
SERVER_MGRS = {
    # 'template': MOD_NAME_S + "Scripts.mgr.templateMgr.templateServerMgr.TemplateServerMgr",
}












