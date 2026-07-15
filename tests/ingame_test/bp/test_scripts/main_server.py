# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-7-16
#  ⠀
# =================================================


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
        self.c = 0
        self.comm_time = 0
        self.comm_cost = 0
        self.player_id = None
        LvComp.Game.AddTimer(6, self.run_benchmark)

    def run_benchmark(self):
        # from .nuoyanlib.core._doc import get_signature
        # for attr in dir(LvComp.Physx):
        #     m = getattr(LvComp.Physx, attr)
        #     if callable(m) and not attr.startswith("__"):
        #         print(attr + "(" + get_signature(m) + ")")
        self.player_id = s_api.GetHostPlayerId()
        run_benchmark("nuoyanlib.common.mc_math.vector", self.player_id, 1000000)
        run_benchmark("nuoyanlib.common.mc_math.mc_math", self.player_id)
        run_benchmark("nuoyanlib.common.filter", self.player_id)
        run_benchmark("nuoyanlib.core.listener", self.player_id, 10000)
        run_benchmark("nuoyanlib.core.server.comp", self.player_id)
        self.communicate_benchmark()
        print("server benchmark over")

    @nyl.event(ns=MOD_NAME, sys_name=CLIENT_SYSTEM_NAME)
    def OnKeyPressInGame(self, args):
        playerId = args['__id__']
        screenName = args['screenName']
        key = int(args['key'])
        isDown = int(args['isDown'])
        if screenName != "hud_screen" or not isDown:
            return
        pos = CF(playerId).Pos.GetFootPos()

        if key == KeyBoardType.KEY_L:
            center = (pos[0], pos[1] - 1, pos[2])
            # nyl.spawn_ground_shatter_effect(center, 0, 2, 20)

        elif key == KeyBoardType.KEY_M:
            all_entities = s_api.GetEngineActor().keys() + s_api.GetPlayerList()
            ef = nyl.EntityFilter(all_entities)
            assert self.player_id in ef[ef.identifier == "minecraft:player"]
            assert self.player_id in ef[ef.health > 0]
            assert self.player_id not in ef[ef.in_water]
            assert self.player_id in ef[ef.in_lava]
            assert self.player_id in ef[ef.on_fire]
            assert self.player_id in ef[ef.family == "player"]
            print("assert passed")

    def BlockRemoveServerEvent(self, args):
        print_msg(args)

    @event
    @event
    def PlayerAttackEntityEvent(self, args):
        print_msg(1)

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
        print_msg("=" * 75)
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























