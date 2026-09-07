# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-7
#  ⠀
#  ================================================


from .common.constant import (
    MOD_NAME,
    SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLASS_PATH,
    CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLASS_PATH,
    UI_NUOYANLIB_TEST, UI_PATH_NUOYANLIB_TEST,
)


import nuoyanlib
nuoyanlib.run(
    MOD_NAME,
    clients=[
        (CLIENT_SYSTEM_NAME, CLIENT_SYSTEM_CLASS_PATH),
        (UI_NUOYANLIB_TEST, UI_PATH_NUOYANLIB_TEST),
        # (xxx, MODULES_PATH + ".xxx.client"),
    ],
    servers=[
        (SERVER_SYSTEM_NAME, SERVER_SYSTEM_CLASS_PATH),
        # (xxx, MODULES_PATH + ".xxx.server"),
    ]
)
