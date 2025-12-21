# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-21
#  ⠀
# =================================================


import mod.client.extraClientApi as c_api
from mod.common.minecraftEnum import *
from .common.mod_config import *
from .nuoyanlib import client as nyl
from .nuoyanlib.client import (
    LvComp,
    PlrComp,
    CF,
    PLAYER_ID,
    event,
)
from .benchmark import run_benchmark, print_res, print_msg


clientEvent = event(ns=MOD_NAME, sys_name=CLIENT_SYSTEM_NAME)
serverEvent = event(ns=MOD_NAME, sys_name=SERVER_SYSTEM_NAME)


class MainClientSystem(nyl.ClientEventProxy, nyl.ClientSystem):
    def __init__(self, namespace, systemName):
        super(MainClientSystem, self).__init__(namespace, systemName)
        LvComp.Game.AddTimer(6, self.run_benchmark)

    # =========================================== Engine Event Callback ================================================

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================

    def run_benchmark(self):
        self.communicate_benchmark()
        nyl.create_ui(
            MOD_NAME, UI_NAME_NUOYANLIB_TEST, UI_PATH_NUOYANLIB_TEST, UI_DEF_NUOYANLIB_TEST,
            push=True,
            client_system=self,
        )

    def communicate_benchmark(self):
        def callback(success, ret):
            print_msg("return from server: %s, %s" % (success, ret))
            assert success and ret == "abc"
        nyl.call(
            MOD_NAME, SERVER_SYSTEM_NAME,
            "test_s", (1, 2), {'p3': 3},
            callback=callback,
        )

    def test_c(self, p1, p2, p3):
        print_msg("client called from server: %s, %s, %s" % (p1, p2, p3))
        return "abc"

    def test1(self):
        pass















