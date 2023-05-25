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
#   Last Modified : 2023-05-20
#
# ====================================================


import mod.client.extraClientApi as _clientApi


__all__ = [
    "EffectController",
]


_ClientCompFactory = _clientApi.GetEngineCompFactory()


class EffectController(object):
    def __init__(self, clientCls):
        self._mClientCls = clientCls
        self._particleEntityId = None
        self._particleCtrl = None
        self._particleTrans = None
        self._particleBindComp = None
        self._isParticlePlaying = False
        self._sfxEntityId = None
        self._sfxCtrl = None
        self._sfxTrans = None
        self._sfxBindComp = None
        self._isSfxPlaying = False

    def createParticle(self, particleJsonPath, particlePos=(0, 0, 0)):
        self._particleEntityId = self._mClientCls.CreateEngineParticle(particleJsonPath, particlePos)
        self._particleCtrl = _ClientCompFactory.CreateParticleControl(self._particleEntityId)
        self._particleTrans = _ClientCompFactory.CreateParticleTrans(self._particleEntityId)
        self._particleBindComp = _ClientCompFactory.CreateParticleEntityBind(self._particleEntityId)

    def removeParticle(self):
        if not self._particleEntityId:
            return
        self._mClientCls.DestroyEntity(self._particleEntityId)
        self._particleEntityId = None
        self._particleCtrl = None
        self._particleBindComp = None

    def bindParticle(self, bindEntityId, offset=(0, 0, 0), rot=(0, 0, 0), correction=False):
        if not self._particleBindComp:
            return
        self._particleBindComp.Bind(bindEntityId, offset, rot, correction)

    def playParticle(self):
        if self._particleCtrl:
            self._particleCtrl.Play()
            self._isParticlePlaying = True

    def stopParticle(self):
        if self._particleCtrl:
            self._particleCtrl.Stop()
            self._isParticlePlaying = False

    def pauseParticle(self):
        if self._particleCtrl:
            self._particleCtrl.Pause()
            self._isParticlePlaying = False

    def getParticleTrans(self):
        return self._particleTrans

    def getParticleCtrl(self):
        return self._particleCtrl

    def createSfx(self, sfxJsonPath, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self._sfxEntityId = self._mClientCls.CreateEngineSfxFromEditor(sfxJsonPath, pos, rot, scale)
        self._sfxCtrl = _ClientCompFactory.CreateFrameAniControl(self._sfxEntityId)
        self._sfxTrans = _ClientCompFactory.CreateFrameAniTrans(self._sfxEntityId)
        self._sfxBindComp = _ClientCompFactory.CreateFrameAniEntityBind(self._sfxEntityId)

    def removeSfx(self):
        if not self._sfxEntityId:
            return
        self._mClientCls.DestroyEntity(self._sfxEntityId)
        self._sfxEntityId = None
        self._sfxCtrl = None
        self._sfxTrans = None
        self._sfxBindComp = None

    def bindSfx(self, bindEntityId, offset=(0, 0, 0), rot=(0, 0, 0)):
        if not self._sfxBindComp:
            return
        self._sfxBindComp.Bind(bindEntityId, offset, rot)

    def bindSfxToSkeleton(self, path, entityId, anim):
        self._sfxEntityId = self._mClientCls.CreateEngineEffectBind(path, entityId, anim)
        self._sfxCtrl = _ClientCompFactory.CreateFrameAniControl(self._sfxEntityId)
        self._sfxTrans = _ClientCompFactory.CreateFrameAniTrans(self._sfxEntityId)
        self._sfxBindComp = _ClientCompFactory.CreateFrameAniEntityBind(self._sfxEntityId)

    def playSfx(self):
        if self._sfxCtrl:
            self._sfxCtrl.Play()
            self._isSfxPlaying = True

    def stopSfx(self):
        if self._sfxCtrl:
            self._sfxCtrl.Stop()
            self._isSfxPlaying = False

    def pauseSfx(self):
        if self._sfxCtrl:
            self._sfxCtrl.Pause()
            self._isSfxPlaying = False

    def getSfxTrans(self):
        return self._sfxTrans

    def getSfxCtrl(self):
        return self._sfxCtrl















