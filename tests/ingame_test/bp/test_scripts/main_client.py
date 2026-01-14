# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-14
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

    def OnKeyPressInGame(self, args):
        screenName = args['screenName']
        key = int(args['key'])
        isDown = int(args['isDown'])
        self.NotifyToServer(ClientEvent.OnKeyPressInGame, dict(args))
        if screenName != "hud_screen" or not isDown:
            return
        pos = PlrComp.Pos.GetFootPos()

        if key == KeyBoardType.KEY_K:
            n = 0
            center = (pos[0], pos[1] + 1.5, pos[2])
            pos1 = (pos[0] - 1.5, pos[1] + 1, pos[2] - 1.5)
            pos2 = (pos[0] + 1.5, pos[1] + 2, pos[2] + 1.5)
            # pos1 = (pos[0] - 1.5, pos[2] - 1.5)
            # pos2 = (pos[0] + 1.5, pos[2] + 1.5)
            # for p in nyl.gen_sphere_pos(center, 1.75, 500, fixed_x=False, fixed_y=False, fixed_z=False):
            # for p in nyl.gen_ring_pos(center, 1.75, 100, "y"):
            # for p in nyl.gen_box_pos(pos1, pos2, 200, True):
            # for p in nyl.gen_box_frame_pos((pos[0] - 1.5, pos[2] - 1.5), (pos[0] + 1.5, pos[2] - 1.5), 10, 4, 10):
            for p in nyl.gen_box_frame_pos(pos1, pos2, 8, 4, 8):
                if not p:
                    continue
                nyl.spawn_particle("minecraft:basic_flame_particle", p, rm_delay=1)
                # nyl.spawn_particle("minecraft:basic_flame_particle", (p[0], pos[1] + 1, p[1]), rm_delay=1)
                n += 1
            print(n)

        elif key == KeyBoardType.KEY_L:
            center = (pos[0], pos[1] - 1, pos[2])
            nyl.spawn_ground_shatter_effect(center, 2, 20)

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================

    def run_benchmark(self):
        return
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















