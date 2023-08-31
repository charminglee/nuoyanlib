# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-08-31
#
# ====================================================


"""

effector
========

该模块提供了管理网易版粒子特效和序列帧特效的工具。

-----

示例：

创建一个网易版粒子特效（序列帧特效类似）：

>>> from nuoyanlib import NeteaseParticleMgr, PLAYER_ID
>>> particle = NeteaseParticleMgr("effects/my_effect.json", bindEntityId=PLAYER_ID)

播放粒子特效：

>>> particle.Play()

设置粒子位置：

>>>

修改粒子绑定的实体：

>>>

"""


import mod.client.extraClientApi as _clientApi
from ..config import MOD_NAME as _MOD_NAME, CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME


__all__ = [
    "NeteaseParticleMgr",
    "NeteaseFrameMgr",
]


_ClientCompFactory = _clientApi.GetEngineCompFactory()


class NeteaseParticleMgr(object):
    """
    网易粒子特效管理器。

    -----

    接口一览：

    1、Destroy：销毁粒子。

    2、BindEntity：绑定粒子到实体上。

    3、Play：播放粒子特效。

    4、Pause：暂停粒子特效。

    5、SetFadeDistance：设置粒子开始自动调整透明度的距离。

    6、SetLayer：设置粒子渲染层级。

    7、SetRelative：设置当粒子绑定了实体或骨骼模型时，发射出的粒子使用相对坐标系还是世界坐标系。

    8、SetUsePointFiltering：设置粒子材质的纹理滤波是否使用点滤波方法。

    -----

    属性一览：

    1、id：粒子特效ID（只读属性，不可修改）。

    2、bindEntityId：粒子绑定的实体ID。

    3、bindOffset：粒子绑定的偏移量。

    4、bindRot：粒子绑定的旋转角度。

    5、bindCorrection：是否开启特效旋转角度修正。

    6、emissionRate：粒子发射器每帧发射粒子的频率，对应粒子特效json文件中"emissionrate"的值。

    7、maxNum：粒子特效ID。

    8、size：粒子特效ID。

    9、volumeSize：粒子特效ID。

    10、pos：粒子特效ID。

    11、rot：粒子特效ID。

    -----

    :param str jsonPath: 粒子特效json文件路径，包含后缀名.json
    :param tuple[float,float,float] pos: 创建位置坐标，默认为(0.0, 0.0, 0.0)
    :param str bindEntityId: 特效绑定的实体ID，默认为空字符串，设置bindEntityId后可不设置pos参数
    :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0.0, 0.0, 0.0)
    :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0.0, 0.0, 0.0)
    :param bool correction: 是否开启特效旋转角度修正，开启后可以使特效的旋转角度准确设置为参照绑定实体的相对角度，默认为False
    """

    def __init__(
            self,
            jsonPath,
            pos=(0.0, 0.0, 0.0),
            bindEntityId="",
            offset=(0.0, 0.0, 0.0),
            rot=(0, 0, 0),
            correction=False,
    ):
        self.__cs = _clientApi.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        self._id = self.__cs.CreateEngineParticle(jsonPath, pos)
        if not self._id:
            raise RuntimeError("Create particle failed. jsonPath='%s'." % jsonPath)
        self._ctrl = _ClientCompFactory.CreateParticleControl(self._id)
        self._trans = _ClientCompFactory.CreateParticleTrans(self._id)
        self._bindEntComp = _ClientCompFactory.CreateParticleEntityBind(self._id)
        self._bindEntComp = _ClientCompFactory.CreateParticleSkeletonBind(self._id)
        self._bindEntityId = ""
        self._bindOffset = (0.0, 0.0, 0.0)
        self._bindRot = (0.0, 0.0, 0.0)
        self._bindCorrection = False
        if bindEntityId and not self.BindEntity(bindEntityId, offset, rot, correction):
            raise RuntimeError("Bind particle to entity failed. bindEntityId='%s'." % bindEntityId)

    @property
    def id(self):
        """
        粒子特效ID。
        """
        return self._id

    @property
    def bindEntityId(self):
        """
        粒子绑定的实体ID。
        """
        return self._bindEntityId

    @property
    def bindOffset(self):
        """
        粒子绑定的偏移量。
        """
        return self._bindOffset

    @property
    def bindRot(self):
        """
        粒子绑定的旋转角度。
        """
        return self._bindRot

    @property
    def bindCorrection(self):
        """
        是否开启特效旋转角度修正。
        """
        return self._bindCorrection

    @property
    def emissionRate(self):
        """
        粒子发射器每帧发射粒子的频率，对应粒子特效json文件中"emissionrate"的值。
        """
        return self._ctrl.GetParticleEmissionRate()

    @emissionRate.setter
    def emissionRate(self, value):
        """
        设置粒子发射器每帧发射粒子的频率，数据类型为元组：(每帧发射粒子频率的最小值, 每帧发射粒子频率的最大值)。

        频率越大则每帧发射的粒子数量越多，但粒子数量不会超过粒子发射器的粒子容量，同时由于性能考虑，每帧发射的粒子数量也不会超过100个。

        每帧发射粒子的频率将在频率最小值和频率最大值之间取随机数进行插值。

        当值设置为负值时设置将会失败。
        """
        self._ctrl.SetParticleEmissionRate(*value)

    @property
    def maxNum(self):
        """

        """
        return self._ctrl.GetParticleMaxNum()

    @maxNum.setter
    def maxNum(self, value):
        """

        """
        self._ctrl.SetParticleMaxNum(value)

    @property
    def size(self):
        """

        """
        return self._ctrl.GetParticleMinSize(), self._ctrl.GetParticleMaxSize()

    @size.setter
    def size(self, value):
        """

        """
        self._ctrl.SetParticleSize(*value)

    @property
    def volumeSize(self):
        """

        """
        return self._ctrl.GetParticleVolumeSize()

    @volumeSize.setter
    def volumeSize(self, value):
        """

        """
        self._ctrl.SetParticleVolumeSize(value)

    @property
    def pos(self):
        """

        """
        return self._trans.GetPos()

    @pos.setter
    def pos(self, value):
        """

        """
        self._trans.SetPos(value)

    @property
    def rot(self):
        """

        """
        return self._trans.GetRot()

    @rot.setter
    def rot(self, value):
        """

        """
        self._trans.SetRotUseZXY(value)

    def Destroy(self):
        """
        销毁粒子。

        -----

        :return: 是否成功
        :rtype: bool
        """
        return self.__cs.DestroyEntity(self._id)

    def BindEntity(self, bindEntityId, offset=(0, 0, 0), rot=(0, 0, 0), correction=False):
        """
        绑定粒子到实体上。

        -----

        :param str bindEntityId: 特效绑定的实体ID，默认为空字符串，设置bindEntityId后可不设置pos参数
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0.0, 0.0, 0.0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0.0, 0.0, 0.0)
        :param bool correction: 是否开启特效旋转角度修正，开启后可以使特效的旋转角度准确设置为参照玩家的相对角度，默认为False

        :return: 是否成功
        :rtype: bool
        """
        res = self._bindEntComp.Bind(bindEntityId, offset, rot, correction)
        if res:
            self._bindEntityId = bindEntityId
            self._bindOffset = offset
            self._bindRot = rot
            self._bindCorrection = correction
        return res

    def Play(self):
        """
        播放粒子特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.Play()

    def Pause(self):
        """
        暂停粒子特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.Pause()

    def SetFadeDistance(self, dist):
        """
        设置粒子开始自动调整透明度的距离。

        粒子与摄像机之间的距离小于该值时会自动调整粒子的透明度，距离摄像机越近，粒子越透明。

        -----

        :param float dist: 自动调整透明度的距离，应为正数，负数将视作零来处理

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetFadeDistance(dist)

    def SetLayer(self, layer):
        """
        设置粒子渲染层级。粒子默认层级为1，当层级不为1时表示该特效开启特效分层渲染功能。

        分层渲染时，层级越高渲染越靠后，层级大的会遮挡层级低的，且同一层级的特效会根据特效的相对位置产生正确的相互遮挡关系。

        -----

        :param layer: 粒子渲染层级，总共包含0-15的层级

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetLayer(layer)

    def SetRelative(self, relative):
        """
        设置当粒子绑定了实体或骨骼模型时，发射出的粒子使用相对坐标系还是世界坐标系。

        与mcstudio特效编辑器中粒子的“相对挂点运动”选项功能相同。

        -----

        :param relative: True表示相对坐标系，False表示世界坐标系

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetRelative(relative)

    def SetUsePointFiltering(self, use):
        """
        设置粒子材质的纹理滤波是否使用点滤波方法。默认为使用双线性滤波。

        -----

        :param use: True为使用点滤波方法，False为使用默认的双线性滤波

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetUsePointFiltering(use)


class NeteaseFrameMgr(object):
    def __init__(self, clientCls):
        self.__cs = clientCls
        self._sfxEntityId = None
        self._sfxCtrl = None
        self._sfxTrans = None
        self._sfxBindComp = None
        self._isSfxPlaying = False

    def createSfx(self, sfxJsonPath, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self._sfxEntityId = self.__cs.CreateEngineSfxFromEditor(sfxJsonPath, pos, rot, scale)
        self._sfxCtrl = _ClientCompFactory.CreateFrameAniControl(self._sfxEntityId)
        self._sfxTrans = _ClientCompFactory.CreateFrameAniTrans(self._sfxEntityId)
        self._sfxBindComp = _ClientCompFactory.CreateFrameAniEntityBind(self._sfxEntityId)

    def removeSfx(self):
        if not self._sfxEntityId:
            return
        self.__cs.DestroyEntity(self._sfxEntityId)
        self._sfxEntityId = None
        self._sfxCtrl = None
        self._sfxTrans = None
        self._sfxBindComp = None

    def bindSfx(self, bindEntityId, offset=(0, 0, 0), rot=(0, 0, 0)):
        if not self._sfxBindComp:
            return
        self._sfxBindComp.Bind(bindEntityId, offset, rot)

    def bindSfxToSkeleton(self, path, entityId, anim):
        self._sfxEntityId = self.__cs.CreateEngineEffectBind(path, entityId, anim)
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















