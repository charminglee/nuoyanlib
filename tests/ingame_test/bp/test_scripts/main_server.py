# -*- coding: utf-8 -*-
"""
| ====================================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: `Nuoyan <https://github.com/charminglee>`_
|   Email : 1279735247@qq.com
|   Date  : 2025-12-04
|
| ====================================================
"""


import mod.server.extraServerApi as s_api
from mod.common.minecraftEnum import *
from .common.mod_config import *
from .nuoyanlib import server as nyl
from .nuoyanlib.server import (
    LvComp,
    CF,
    event,
)
from .benchmark import print_msg, run_benchmark, print_res


class MainServerSystem(nyl.ServerEventProxy, nyl.ServerSystem):
    def __init__(self, namespace, systemName):
        super(MainServerSystem, self).__init__(namespace, systemName)
        LvComp.Game.AddTimer(8, self.run_benchmark)
        self.c = 0
        self.comm_time = 0
        self.comm_cost = 0
        self.player_id = None

    # =========================================== Engine Event Callback ================================================

    def BlockRemoveServerEvent(self, args):
        print_msg(args)

    @event
    @event
    def PlayerAttackEntityEvent(self, args):
        print_msg(1)

    # =========================================== Custom Event Callback ================================================

    # ============================================== Basic Function ====================================================

    def run_benchmark(self):
        self.player_id = s_api.GetPlayerList()[0]
        run_benchmark("nuoyanlib.core.listener", 10000)
        run_benchmark("nuoyanlib.core.server.comp")
        self.communicate_benchmark()

    def communicate_benchmark(self):
        def callback(success, ret, player_id):
            print_msg("return from client: %s, %s, %s" % (success, ret, player_id))
            assert success and ret == "abc" and player_id == self.player_id
        nyl.call(
            MOD_NAME, CLIENT_SYSTEM_NAME,
            "test_c", (1, 2), {'p3': 3},
            self.player_id,
            callback,
        )

        n = 1000
        print_msg("=" * 45)
        print_msg("[{}]".format("nuoyanlib.utils.communicate"))
        print_msg("n={}".format(n))

        t = nyl.get_time()
        for _ in xrange(n):
            nyl.call(MOD_NAME, CLIENT_SYSTEM_NAME, "test1", player_id=self.player_id)
        cost = nyl.get_time() - t
        print_res(cost, n, "call no return")

        def callback1(success, ret, player_id):
            t = nyl.get_time()
            self.comm_cost += t - self.comm_time
            self.c += 1
            if self.c >= n:
                print_res(self.comm_cost, n, "call with return")
                return
            self.comm_time = nyl.get_time()
            nyl.call(
                MOD_NAME, CLIENT_SYSTEM_NAME,
                "test1",
                player_id=self.player_id,
                callback=callback1,
            )
        self.comm_time = nyl.get_time()
        nyl.call(
            MOD_NAME, CLIENT_SYSTEM_NAME,
            "test1",
            player_id=self.player_id,
            callback=callback1,
        )

    def test_s(self, p1, p2, p3):
        print_msg("server called from client: %s, %s, %s" % (p1, p2, p3))
        return "abc"

    def test1(self):
        pass























