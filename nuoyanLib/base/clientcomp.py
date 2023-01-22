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
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-15
#
# ====================================================


import mod.client.extraClientApi as _clientApi
from nuoyanClientSystem import NuoyanClientSystem
from nuoyanScreenNode import NuoyanScreenNode


ENGINE_NAMESPACE = _clientApi.GetEngineNamespace()
ENGINE_SYSTEM_NAME = _clientApi.GetEngineSystemName()


ClientSystem = _clientApi.GetClientSystemCls()
ClientCompFactory = _clientApi.GetEngineCompFactory()


ScreenNode = _clientApi.GetScreenNodeCls()
ViewBinder = _clientApi.GetViewBinderCls()
ViewRequest = _clientApi.GetViewViewRequestCls()


PLAYER_ID = _clientApi.GetLocalPlayerId()
LEVEL_ID = _clientApi.GetLevelId()


PlayerActorRenderComp = ClientCompFactory.CreateActorRender(PLAYER_ID)
PlayerQueryVariableComp = ClientCompFactory.CreateQueryVariable(PLAYER_ID)
PlayerItemComp = ClientCompFactory.CreateItem(PLAYER_ID)
PlayerGameComp = ClientCompFactory.CreateGame(PLAYER_ID)
PlayerCameraComp = ClientCompFactory.CreateCamera(PLAYER_ID)
PlayerViewComp = ClientCompFactory.CreatePlayerView(PLAYER_ID)
PlayerPosComp = ClientCompFactory.CreatePos(PLAYER_ID)
PlayerActorMotionComp = ClientCompFactory.CreateActorMotion(PLAYER_ID)
PlayerComp = ClientCompFactory.CreatePlayer(PLAYER_ID)
PlayerRotComp = ClientCompFactory.CreateRot(PLAYER_ID)
PlayerActorCollidableComp = ClientCompFactory.CreateActorCollidable(PLAYER_ID)
PlayerAttrComp = ClientCompFactory.CreateAttr(PLAYER_ID)
PlayerBrightnessComp = ClientCompFactory.CreateBrightness(PLAYER_ID)
PlayerEngineEffectBindControlComp = ClientCompFactory.CreateEngineEffectBindControl(PLAYER_ID)
PlayerEngineTypeComp = ClientCompFactory.CreateEngineType(PLAYER_ID)
PlayerHealthComp = ClientCompFactory.CreateHealth(PLAYER_ID)
PlayerModAttrComp = ClientCompFactory.CreateModAttr(PLAYER_ID)
PlayerModelComp = ClientCompFactory.CreateModel(PLAYER_ID)
PlayerNameComp = ClientCompFactory.CreateName(PLAYER_ID)
PlayerOperationComp = ClientCompFactory.CreateOperation(PLAYER_ID)
PlayerPlayerAnimComp = ClientCompFactory.CreatePlayerAnim(PLAYER_ID)


LevelGameComp = ClientCompFactory.CreateGame(LEVEL_ID)
LevelActorRenderComp = ClientCompFactory.CreateActorRender(LEVEL_ID)
LevelItemComp = ClientCompFactory.CreateItem(LEVEL_ID)
LevelTextNotifyClientComp = ClientCompFactory.CreateTextNotifyClient(LEVEL_ID)
LevelSkyRenderComp = ClientCompFactory.CreateSkyRender(LEVEL_ID)
LevelFogComp = ClientCompFactory.CreateFog(LEVEL_ID)
LevelBlockInfoComp = ClientCompFactory.CreateBlockInfo(LEVEL_ID)
LevelBlockComp = ClientCompFactory.CreateBlock(LEVEL_ID)
LevelBlockGeometryComp = ClientCompFactory.CreateBlockGeometry(LEVEL_ID)
LevelBlockUseEventWhiteListComp = ClientCompFactory.CreateBlockUseEventWhiteList(LEVEL_ID)
LevelChunkSourceComp = ClientCompFactory.CreateChunkSource(LEVEL_ID)
LevelConfigClientComp = ClientCompFactory.CreateConfigClient(LEVEL_ID)
LevelCustomAudioComp = ClientCompFactory.CreateCustomAudio(LEVEL_ID)
LevelDeviceComp = ClientCompFactory.CreateDevice(LEVEL_ID)
LevelNeteaseShopComp = ClientCompFactory.CreateNeteaseShop(LEVEL_ID)
LevelPostProcessComp = ClientCompFactory.CreatePostProcess(LEVEL_ID)
LevelRecipeComp = ClientCompFactory.CreateRecipe(LEVEL_ID)
LevelTextBoardComp = ClientCompFactory.CreateTextBoard(LEVEL_ID)
LevelVirtualWorldComp = ClientCompFactory.CreateVirtualWorld(LEVEL_ID)


ParticleSystemComp = ClientCompFactory.CreateParticleSystem(None)














