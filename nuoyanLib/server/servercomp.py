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
#   Last Modified : 2023-01-15
#
# ====================================================


import mod.server.extraServerApi as _serverApi


ENGINE_NAMESPACE = _serverApi.GetEngineNamespace()
ENGINE_SYSTEM_NAME = _serverApi.GetEngineSystemName()


ServerSystem = _serverApi.GetServerSystemCls()
ServerCompFactory = _serverApi.GetEngineCompFactory()


LEVEL_ID = _serverApi.GetLevelId()


LevelExplosionComp = ServerCompFactory.CreateExplosion(LEVEL_ID)
LevelCommandComp = ServerCompFactory.CreateCommand(LEVEL_ID)
LevelGameComp = ServerCompFactory.CreateGame(LEVEL_ID)
LevelBlockInfoComp = ServerCompFactory.CreateBlockInfo(LEVEL_ID)
LevelWeatherComp = ServerCompFactory.CreateWeather(LEVEL_ID)
LevelTimeComp = ServerCompFactory.CreateTime(LEVEL_ID)
LevelProjectileComp = ServerCompFactory.CreateProjectile(LEVEL_ID)
LevelBlockStateComp = ServerCompFactory.CreateBlockState(LEVEL_ID)
LevelMsgComp = ServerCompFactory.CreateMsg(LEVEL_ID)
LevelItemComp = ServerCompFactory.CreateItem(LEVEL_ID)
LevelAchievementComp = ServerCompFactory.CreateAchievement(LEVEL_ID)
LevelActorLootComp = ServerCompFactory.CreateActorLoot(LEVEL_ID)
LevelBiomeComp = ServerCompFactory.CreateBiome(LEVEL_ID)
LevelBlockComp = ServerCompFactory.CreateBlock(LEVEL_ID)
LevelBlockEntityDataComp = ServerCompFactory.CreateBlockEntityData(LEVEL_ID)
LevelBlockUseEventWhiteListComp = ServerCompFactory.CreateBlockUseEventWhiteList(LEVEL_ID)
LevelChatExtensionComp = ServerCompFactory.CreateChatExtension(LEVEL_ID)
LevelChestBlockComp = ServerCompFactory.CreateChestBlock(LEVEL_ID)
LevelChunkSourceComp = ServerCompFactory.CreateChunkSource(LEVEL_ID)
LevelDimensionComp = ServerCompFactory.CreateDimension(LEVEL_ID)
LevelExpComp = ServerCompFactory.CreateExp(LEVEL_ID)
LevelExtraDataComp = ServerCompFactory.CreateExtraData(LEVEL_ID)
LevelFeatureComp = ServerCompFactory.CreateFeature(LEVEL_ID)
LevelHttpComp = ServerCompFactory.CreateHttp(LEVEL_ID)
LevelItemBannedComp = ServerCompFactory.CreateItemBanned(LEVEL_ID)
LevelMobSpawnComp = ServerCompFactory.CreateMobSpawn(LEVEL_ID)
LevelPetComp = ServerCompFactory.CreatePet(LEVEL_ID)
LevelPortalComp = ServerCompFactory.CreatePortal(LEVEL_ID)
LevelRecipeComp = ServerCompFactory.CreateRecipe(LEVEL_ID)
LevelRedStoneComp = ServerCompFactory.CreateRedStone(LEVEL_ID)
LevelRideComp = ServerCompFactory.CreateRide(LEVEL_ID)
LevelTameComp = ServerCompFactory.CreateTame(LEVEL_ID)



















