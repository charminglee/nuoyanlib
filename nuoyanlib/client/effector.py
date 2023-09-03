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
#   Last Modified : 2023-09-03
#
# ====================================================


"""

effector
========

该模块提供了管理网易版粒子特效和序列帧特效的工具。

-----

【示例】

创建一个网易版粒子特效对象（序列帧特效类似）：

>>> from nuoyanlib import NeteaseParticle, PLAYER_ID
>>> particle = NeteaseParticle("effects/my_effect.json", bindEntityId=PLAYER_ID)

播放粒子特效：

>>> particle.Play()
True

设置粒子位置：

>>> particle.pos = (100, 100, 100)

修改粒子绑定的实体：

>>> particle.bindEntityId = entityId

"""


import mod.client.extraClientApi as _clientApi
from ..config import MOD_NAME as _MOD_NAME, CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME
from ..utils._error import ClientNotFoundError as _ClientNotFoundError
from clientComps import CompFactory as _CompFactory


__all__ = [
    "NeteaseParticle",
    "NeteaseFrameAnim",
]


class NeteaseParticle(object):
    """
    网易粒子特效管理器。

    切换维度后会自动隐藏非本维度创建的而且没有绑定实体的粒子，回到该维度后会自动重新显示。

    粒子创建之后需要调用Play方法才会播放，如果播放非本维度创建的粒子，会同时修改该粒子的创建维度为当前维度。

    -----

    【接口一览】

    1、BindEntity：绑定粒子到实体上。

    2、BindSkeleton：绑定粒子到骨骼模型上。

    3、Play：播放粒子特效。

    4、Pause：暂停粒子特效。

    5、Destroy：销毁粒子。

    6、SetFadeDistance：设置粒子开始自动调整透明度的距离。

    7、SetLayer：设置粒子渲染层级。

    8、SetRelative：设置当粒子绑定了实体或骨骼模型时，发射出的粒子使用相对坐标系还是世界坐标系。

    9、SetUsePointFiltering：设置粒子材质的纹理滤波是否使用点滤波方法。

    -----

    【属性一览】

    1、id：粒子特效ID（只读属性，不可修改）。

    2、bindEntId：粒子绑定的实体ID。

    3、bindEntOffset：粒子绑定的偏移量。

    4、bindEntRot：粒子绑定的旋转角度。

    5、bindEntCorrection：是否开启特效旋转角度修正。

    6、bindSkelModelId：粒子绑定的骨骼模型的ID。

    7、bindSkelBoneName：粒子绑定的具体骨骼的名称。

    8、bindSkelOffset：粒子绑定骨骼时的偏移量。

    9、bindSkelRot：粒子绑定骨骼时的旋转角度。

    10、emissionRate：粒子发射器每帧发射粒子的频率。

    11、maxNum：粒子发射器包含的最大粒子数量。

    12、size：粒子大小的最小值和最大值。

    13、volumeSize：粒子发射器的体积大小缩放值。

    14、pos：粒子发射器的世界坐标位置。

    15、rot：粒子发射器的旋转角度。

    16、playing：粒子是否正在播放（只读属性，不可修改）。

    17、destroyed：粒子是否已销毁（只读属性，不可修改）。

    -----

    :param str jsonPath: 粒子特效json文件路径，包含后缀名.json，如"effects/my_effect.json"
    :param tuple[float,float,float]|None pos: 粒子的世界坐标位置，默认为None，绑定实体或骨骼时可忽略该参数
    :param dict[str,str|tuple[float,float,float]|bool]|None bindEntity: 实体绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindEntity方法
    :param dict[str,int|str|tuple[float,float,float]]|None bindSkeleton: 骨骼模型绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindSkeleton方法
    """

    def __init__(self, jsonPath, pos=None, bindEntity=None, bindSkeleton=None):
        self.__cs = _clientApi.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        if not self.__cs:
            raise _ClientNotFoundError
        self._id = self.__cs.CreateEngineParticle(jsonPath, pos)
        if not self._id:
            raise RuntimeError("Create particle failed. jsonPath='%s'." % jsonPath)
        self._ctrl = _CompFactory.CreateParticleControl(self._id)
        self._trans = _CompFactory.CreateParticleTrans(self._id)
        self._bindEntComp = _CompFactory.CreateParticleEntityBind(self._id)
        self._bindSkelComp = _CompFactory.CreateParticleSkeletonBind(self._id)
        self._bindEntId = ""
        self._bindEntOffset = (0.0, 0.0, 0.0)
        self._bindEntRot = (0.0, 0.0, 0.0)
        self._bindEntCorrection = False
        self._bindSkelModelId = -1
        self._bindSkelBoneName = ""
        self._bindSkelOffset = (0.0, 0.0, 0.0)
        self._bindSkelRot = (0.0, 0.0, 0.0)
        if bindEntity and bindSkeleton:
            raise AssertionError("Parameters 'bindEntity' and 'bindSkeleton' cannot be given at the same time.")
        if bindEntity and not self.BindEntity(**bindEntity):
            raise RuntimeError("Bind particle to entity failed. bindEntity=%s." % bindEntity)
        if bindSkeleton and not self.BindSkeleton(**bindSkeleton):
            raise RuntimeError("Bind particle to skeleton failed. bindSkeleton=%s." % bindSkeleton)
        self._playing = False
        self._destroyed = False

    @property
    def id(self):
        """
        粒子特效ID。
        """
        return self._id

    @property
    def bindEntId(self):
        """
        粒子绑定的实体ID。
        """
        return self._bindEntId

    @bindEntId.setter
    def bindEntId(self, value):
        """
        设置粒子绑定的实体ID。
        """
        self.BindEntity(value, self._bindEntOffset, self._bindEntRot, self._bindEntCorrection)

    @property
    def bindEntOffset(self):
        """
        粒子绑定实体时的偏移量。
        """
        return self._bindEntOffset

    @bindEntOffset.setter
    def bindEntOffset(self, value):
        """
        设置粒子绑定实体时的偏移量。
        """
        self.BindEntity(self._bindEntId, value, self._bindEntRot, self._bindEntCorrection)

    @property
    def bindEntRot(self):
        """
        粒子绑定实体时的旋转角度。
        """
        return self._bindEntRot

    @bindEntRot.setter
    def bindEntRot(self, value):
        """
        设置粒子绑定实体时的旋转角度。
        """
        self.BindEntity(self._bindEntId, self._bindEntOffset, value, self._bindEntCorrection)

    @property
    def bindEntCorrection(self):
        """
        粒子绑定实体时是否开启特效旋转角度修正。
        """
        return self._bindEntCorrection

    @bindEntCorrection.setter
    def bindEntCorrection(self, value):
        """
        设置粒子绑定实体时是否开启特效旋转角度修正。
        """
        self.BindEntity(self._bindEntId, self._bindEntOffset, self._bindEntRot, value)

    @property
    def bindSkelModelId(self):
        """
        粒子绑定的骨骼模型的ID。
        """
        return self._bindSkelModelId

    @bindSkelModelId.setter
    def bindSkelModelId(self, value):
        """
        设置粒子绑定的骨骼模型的ID。
        """
        self.BindSkeleton(value, self._bindSkelBoneName, self._bindSkelOffset, self._bindSkelRot)

    @property
    def bindSkelBoneName(self):
        """
        粒子绑定的具体骨骼的名称。
        """
        return self._bindSkelBoneName

    @bindSkelBoneName.setter
    def bindSkelBoneName(self, value):
        """
        设置粒子绑定的具体骨骼的名称。
        """
        self.BindSkeleton(self._bindSkelModelId, value, self._bindSkelOffset, self._bindSkelRot)

    @property
    def bindSkelOffset(self):
        """
        粒子绑定骨骼时的偏移量。
        """
        return self._bindSkelOffset

    @bindSkelOffset.setter
    def bindSkelOffset(self, value):
        """
        设置粒子绑定骨骼时的偏移量。
        """
        self.BindSkeleton(self._bindSkelModelId, self._bindSkelBoneName, value, self._bindSkelRot)

    @property
    def bindSkelRot(self):
        """
        粒子绑定骨骼时的旋转角度。
        """
        return self._bindSkelRot

    @bindSkelRot.setter
    def bindSkelRot(self, value):
        """
        设置粒子绑定骨骼时的旋转角度。
        """
        self.BindSkeleton(self._bindSkelModelId, self._bindSkelBoneName, self._bindSkelOffset, value)

    @property
    def emissionRate(self):
        """
        粒子发射器每帧发射粒子的频率，数据类型为元组：(min, max)，其中min表示每帧发射粒子频率的最小值，max表示每帧发射粒子频率的最大值。

        对应粒子特效json文件中"emissionrate"的值。
        """
        return self._ctrl.GetParticleEmissionRate()

    @emissionRate.setter
    def emissionRate(self, value):
        """
        设置粒子发射器每帧发射粒子的频率，数据类型为元组：(min, max)，其中min表示每帧发射粒子频率的最小值，max表示每帧发射粒子频率的最大值。

        频率越大则每帧发射的粒子数量越多，但粒子数量不会超过粒子发射器的粒子容量，同时由于性能考虑，每帧发射的粒子数量也不会超过100个。

        每帧发射粒子的频率将在频率最小值和频率最大值之间取随机数进行插值。当值设置为负值时设置将会失败。

        对应粒子特效json文件中"emissionrate"的值。
        """
        self._ctrl.SetParticleEmissionRate(*value)

    @property
    def maxNum(self):
        """
        粒子发射器包含的最大粒子数量，数据类型为整数。

        对应粒子特效json文件中"numparticles"的值。
        """
        return self._ctrl.GetParticleMaxNum()

    @maxNum.setter
    def maxNum(self, value):
        """
        设置粒子发射器的粒子容量，即粒子发射器所包含的最大粒子数量，数据类型为整数，不能为负值，粒子的数量最大值不超过100000。

        该数量并不代表目前粒子发射器所发射的粒子数量，如需要增加发射的粒子数量，需同时改变粒子的发射频率。

        对应粒子特效json文件中"numparticles"的值。
        """
        self._ctrl.SetParticleMaxNum(value)

    @property
    def size(self):
        """
        粒子大小的最小值和最大值，数据类型为元组：((minx,miny), (maxx,maxy))，其中minx为粒子x轴大小的最小值，miny为粒子y轴大小的最小值，maxx为粒子x轴大小的最大值，maxy为粒子y轴大小的最大值。

        对应粒子特效json文件中"particlesize"的"min"和"max"值。
        """
        return self._ctrl.GetParticleMinSize(), self._ctrl.GetParticleMaxSize()

    @size.setter
    def size(self, value):
        """
        设置粒子大小的最小值及最大值，数据类型为元组：((minx,miny), (maxx,maxy))，其中minx为粒子x轴大小的最小值，miny为粒子y轴大小的最小值，maxx为粒子x轴大小的最大值，maxy为粒子y轴大小的最大值。

        粒子大小会在最小值和最大值当中取随机值进行决定，当该值设置为负值时设置将会失败。

        对应粒子特效json文件中"particlesize"的"min"和"max"值。
        """
        self._ctrl.SetParticleSize(*value)

    @property
    def volumeSize(self):
        """
        粒子发射器的体积大小缩放值，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴方向的缩放值。
        """
        return self._ctrl.GetParticleVolumeSize()

    @volumeSize.setter
    def volumeSize(self, value):
        """
        设置粒子发射器的体积大小缩放，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴方向的缩放值。

        不影响单个粒子的尺寸，粒子发射器的体积越大，则粒子的发射范围越大。

        当粒子绑定实体时该设置无效。
        """
        self._ctrl.SetParticleVolumeSize(value)

    @property
    def pos(self):
        """
        粒子发射器的世界坐标位置，数据类型为元组：(x, y, z)。
        """
        return self._trans.GetPos()

    @pos.setter
    def pos(self, value):
        """
        设置粒子发射器的世界坐标位置，数据类型为元组：(x, y, z)。
        """
        self._trans.SetPos(value)

    @property
    def rot(self):
        """
        粒子发射器的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。
        """
        return self._trans.GetRot()

    @rot.setter
    def rot(self, value):
        """
        粒子发射器的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。

        旋转顺序按照绕z、x、y轴旋转。
        """
        self._trans.SetRotUseZXY(value)

    @property
    def playing(self):
        """
        粒子是否正在播放。
        """
        return self._playing

    @property
    def destroyed(self):
        """
        粒子是否已销毁。
        """
        return self._destroyed

    def BindEntity(self, bindEntityId, offset=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0), correction=False):
        """
        绑定粒子到实体上。

        -----

        :param str bindEntityId: 特效绑定的实体ID
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0.0, 0.0, 0.0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0.0, 0.0, 0.0)
        :param bool correction: 是否开启特效旋转角度修正，开启后可以使特效的旋转角度准确设置为参照玩家的相对角度，默认为False

        :return: 是否成功
        :rtype: bool
        """
        res = self._bindEntComp.Bind(bindEntityId, offset, rot, correction)
        if res:
            self._bindEntId = bindEntityId
            self._bindEntOffset = offset
            self._bindEntRot = rot
            self._bindEntCorrection = correction
            self._bindSkelModelId = -1
            self._bindSkelBoneName = ""
            self._bindSkelOffset = (0.0, 0.0, 0.0)
            self._bindSkelRot = (0.0, 0.0, 0.0)
        return res

    def BindSkeleton(self, modelId, boneName, offset=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0)):
        """
        绑定粒子到骨骼模型上。

        -----

        :param int modelId: 绑定的骨骼模型的ID（使用Model组件的GetModelId获取）
        :param str boneName: 绑定具体骨骼的名称
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0.0, 0.0, 0.0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0.0, 0.0, 0.0)

        :return: 是否成功
        :rtype: bool
        """
        res = self._bindSkelComp.Bind(modelId, boneName, offset, rot)
        if res:
            self._bindSkelModelId = modelId
            self._bindSkelBoneName = boneName
            self._bindSkelOffset = offset
            self._bindSkelRot = rot
            self._bindEntId = ""
            self._bindEntOffset = (0.0, 0.0, 0.0)
            self._bindEntRot = (0.0, 0.0, 0.0)
            self._bindEntCorrection = False
        return res

    def Play(self):
        """
        播放粒子特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        res = self._ctrl.Play()
        if res:
            self._playing = True
        return res

    def Pause(self):
        """
        暂停粒子特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        res = self._ctrl.Pause()
        if res:
            self._playing = False
        return res

    def Destroy(self):
        """
        销毁粒子。

        -----

        :return: 是否成功
        :rtype: bool
        """
        res = self.__cs.DestroyEntity(self._id)
        if res:
            self._destroyed = True
            self._bindEntId = ""
            self._bindEntOffset = (0.0, 0.0, 0.0)
            self._bindEntRot = (0.0, 0.0, 0.0)
            self._bindEntCorrection = False
            self._bindSkelModelId = -1
            self._bindSkelBoneName = ""
            self._bindSkelOffset = (0.0, 0.0, 0.0)
            self._bindSkelRot = (0.0, 0.0, 0.0)
            self._playing = False
            self._ctrl = None
            self._trans = None
            self._bindEntComp = None
            self._bindSkelComp = None
            self._id = None
        return res

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

        :param int layer: 粒子渲染层级，总共包含0-15的层级

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetLayer(layer)

    def SetRelative(self, relative):
        """
        设置当粒子绑定了实体或骨骼模型时，发射出的粒子使用相对坐标系还是世界坐标系。

        与mcstudio特效编辑器中粒子的“相对挂点运动”选项功能相同。

        -----

        :param bool relative: True表示相对坐标系，False表示世界坐标系

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetRelative(relative)

    def SetUsePointFiltering(self, use):
        """
        设置粒子材质的纹理滤波是否使用点滤波方法。

        -----

        :param bool use: True为使用点滤波方法，False为使用默认的双线性滤波

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetUsePointFiltering(use)


class NeteaseFrameAnim(object):
    """
    网易序列帧特效管理器。

    切换维度后会自动隐藏非本维度创建的而且没有绑定实体的序列帧，回到该维度后会自动重新显示。

    需要注意，序列帧创建之后需要调用Play方法才会播放，如果播放非本维度创建的序列帧，会同时修改该序列帧的创建维度为当前维度。

    -----

    【接口一览】

    1、BindEntity：绑定序列帧到实体上。

    2、BindSkeleton：绑定序列帧到骨骼模型上。

    3、Play：播放序列帧特效。

    4、Pause：暂停播放序列帧特效。

    5、SetDeepTest：设置序列帧是否开启深度测试。

    6、SetFaceCamera：设置序列帧是否始终朝向摄像机。

    7、SetFadeDistance：设置序列帧开始自动调整透明度的距离。

    8、SetLayer：设置序列帧渲染层级。

    9、SetLoop：设置序列帧是否循环播放。

    10、SetUsePointFiltering：设置序列帧材质的纹理滤波是否使用点滤波方法。

    -----

    【属性一览】

    1、id：序列帧特效ID（只读属性，不可修改）。

    2、bindEntId：序列帧绑定的实体ID。

    3、bindEntOffset：设置序列帧绑定实体时的偏移量。

    4、bindEntRot：序列帧绑定实体时的旋转角度。

    5、bindSkelModelId：序列帧绑定的骨骼模型的ID。

    6、bindSkelBoneName：序列帧绑定的具体骨骼的名称。

    7、bindSkelOffset：序列帧绑定骨骼时的偏移量。

    8、bindSkelRot：序列帧绑定骨骼时的旋转角度。

    9、pos：序列帧的世界坐标位置。

    10、rot：序列帧的旋转角度。

    11、scale：序列帧的缩放值。

    12、playing：序列帧是否正在播放。

    13、destroyed：序列帧是否已销毁。

    -----

    :param str jsonPath: 特效json配置路径，如"effects/xxx.json"，jsonPath与texPath选择其中一个参数传入即可，两个参数都传入时以jsonPath为准，默认为空字符串
    :param str texPath: 特效贴图路径，如"textures/xxx"，不用后缀名，jsonPath与texPath选择其中一个参数传入即可，两个参数都传入时以jsonPath为准，默认为空字符串
    :param tuple[float,float,float] pos: 创建位置，默认为None，绑定实体或骨骼时可忽略该参数
    :param tuple[float,float,float] rot: 角度，默认为None，绑定实体或骨骼时可忽略该参数
    :param tuple[float,float,float] scale: 缩放系数，默认为None
    :param dict[str,str|tuple[float,float,float]]|None bindEntity: 实体绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindEntity方法
    :param dict[str,int|str|tuple[float,float,float]]|None bindSkeleton: 骨骼模型绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindSkeleton方法
    """

    def __init__(self, jsonPath="", texPath="", pos=None, rot=None, scale=None, bindEntity=None, bindSkeleton=None):
        self.__cs = _clientApi.GetSystem(_MOD_NAME, _CLIENT_SYSTEM_NAME)
        if not self.__cs:
            raise _ClientNotFoundError
        if jsonPath:
            self._id = self.__cs.CreateEngineSfxFromEditor(jsonPath, pos, rot, scale)
        elif texPath:
            self._id = self.__cs.CreateEngineSfx(texPath, pos, rot, scale)
        else:
            raise AssertionError("Parameters 'jsonPath' or 'texPath' must be given.")
        if not self._id:
            raise RuntimeError("Create frame animation failed. path='%s'." % (jsonPath or texPath))
        self._ctrl = _CompFactory.CreateFrameAniControl(self._id)
        self._trans = _CompFactory.CreateFrameAniTrans(self._id)
        self._bindEntComp = _CompFactory.CreateFrameAniEntityBind(self._id)
        self._bindSkelComp = _CompFactory.CreateFrameAniSkeletonBind(self._id)
        self._bindEntId = ""
        self._bindEntOffset = (0.0, 0.0, 0.0)
        self._bindEntRot = (0.0, 0.0, 0.0)
        self._bindSkelModelId = -1
        self._bindSkelBoneName = ""
        self._bindSkelOffset = (0.0, 0.0, 0.0)
        self._bindSkelRot = (0.0, 0.0, 0.0)
        if bindEntity and bindSkeleton:
            raise AssertionError("Parameters 'bindEntity' and 'bindSkeleton' cannot be given at the same time.")
        if bindEntity and not self.BindEntity(**bindEntity):
            raise RuntimeError("Bind frame animation to entity failed. bindEntity=%s." % bindEntity)
        if bindSkeleton and not self.BindSkeleton(**bindSkeleton):
            raise RuntimeError("Bind frame animation to skeleton failed. bindSkeleton=%s." % bindSkeleton)
        self._playing = False
        self._destroyed = False

    @property
    def id(self):
        """
        序列帧特效ID。
        """
        return self._id

    @property
    def bindEntId(self):
        """
        序列帧绑定的实体ID。
        """
        return self._bindEntId

    @bindEntId.setter
    def bindEntId(self, value):
        """
        设置序列帧绑定的实体ID。
        """
        self.BindEntity(value, self._bindEntOffset, self._bindEntRot)

    @property
    def bindEntOffset(self):
        """
        序列帧绑定实体时的偏移量。
        """
        return self._bindEntOffset

    @bindEntOffset.setter
    def bindEntOffset(self, value):
        """
        设置序列帧绑定实体时的偏移量。
        """
        self.BindEntity(self._bindEntId, value, self._bindEntRot)

    @property
    def bindEntRot(self):
        """
        序列帧绑定实体时的旋转角度。
        """
        return self._bindEntRot

    @bindEntRot.setter
    def bindEntRot(self, value):
        """
        设置序列帧绑定实体时的旋转角度。
        """
        self.BindEntity(self._bindEntId, self._bindEntOffset, value)

    @property
    def bindSkelModelId(self):
        """
        序列帧绑定的骨骼模型的ID。
        """
        return self._bindSkelModelId

    @bindSkelModelId.setter
    def bindSkelModelId(self, value):
        """
        设置序列帧绑定的骨骼模型的ID。
        """
        self.BindSkeleton(value, self._bindSkelBoneName, self._bindSkelOffset, self._bindSkelRot)

    @property
    def bindSkelBoneName(self):
        """
        序列帧绑定的具体骨骼的名称。
        """
        return self._bindSkelBoneName

    @bindSkelBoneName.setter
    def bindSkelBoneName(self, value):
        """
        设置序列帧绑定的具体骨骼的名称。
        """
        self.BindSkeleton(self._bindSkelModelId, value, self._bindSkelOffset, self._bindSkelRot)

    @property
    def bindSkelOffset(self):
        """
        序列帧绑定骨骼时的偏移量。
        """
        return self._bindSkelOffset

    @bindSkelOffset.setter
    def bindSkelOffset(self, value):
        """
        设置序列帧绑定骨骼时的偏移量。
        """
        self.BindSkeleton(self._bindSkelModelId, self._bindSkelBoneName, value, self._bindSkelRot)

    @property
    def bindSkelRot(self):
        """
        序列帧绑定骨骼时的旋转角度。
        """
        return self._bindSkelRot

    @bindSkelRot.setter
    def bindSkelRot(self, value):
        """
        设置序列帧绑定骨骼时的旋转角度。
        """
        self.BindSkeleton(self._bindSkelModelId, self._bindSkelBoneName, self._bindSkelOffset, value)

    @property
    def pos(self):
        """
        序列帧的世界坐标位置，数据类型为元组：(x, y, z)。
        """
        return self._trans.GetPos()

    @pos.setter
    def pos(self, value):
        """
        设置序列帧的世界坐标位置，数据类型为元组：(x, y, z)。
        """
        self._trans.SetPos(value)

    @property
    def rot(self):
        """
        序列帧的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。
        """
        return self._trans.GetRot()

    @rot.setter
    def rot(self, value):
        """
        序列帧的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。

        旋转顺序按照绕z、x、y轴旋转。
        """
        self._trans.SetRotUseZXY(value)

    @property
    def scale(self):
        """
        序列帧的缩放值，数据类型为元组：(x, y, z)。

        对于平面序列帧，第一个参数为贴图横向上的缩放，第二个参数为纵向上的缩放，第三个参数无用。

        对于环状序列帧，三个参数分别为三个坐标轴上的缩放。
        """
        return self._trans.GetScale()

    @scale.setter
    def scale(self, value):
        """
        设置序列帧的缩放值，数据类型为元组：(x, y, z)。

        对于平面序列帧，第一个参数为贴图横向上的缩放，第二个参数为纵向上的缩放，第三个参数无用。

        对于环状序列帧，三个参数分别为三个坐标轴上的缩放。
        """
        self._trans.SetScale(value)

    @property
    def playing(self):
        """
        序列帧是否正在播放。
        """
        return self._playing

    @property
    def destroyed(self):
        """
        序列帧是否已销毁。
        """
        return self._destroyed

    def BindEntity(self, bindEntityId, offset=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0)):
        """
        绑定序列帧到实体上。

        -----

        :param str bindEntityId: 特效绑定的实体ID
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0.0, 0.0, 0.0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0.0, 0.0, 0.0)

        :return: 是否成功
        :rtype: bool
        """
        res = self._bindEntComp.Bind(bindEntityId, offset, rot)
        if res:
            self._bindEntId = bindEntityId
            self._bindEntOffset = offset
            self._bindEntRot = rot
            self._bindSkelModelId = -1
            self._bindSkelBoneName = ""
            self._bindSkelOffset = (0.0, 0.0, 0.0)
            self._bindSkelRot = (0.0, 0.0, 0.0)
        return res

    def BindSkeleton(self, modelId, boneName, offset=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0)):
        """
        绑定序列帧到骨骼模型上。

        -----

        :param int modelId: 绑定的骨骼模型的ID（使用Model组件的GetModelId获取）
        :param str boneName: 绑定具体骨骼的名称
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0.0, 0.0, 0.0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0.0, 0.0, 0.0)

        :return: 是否成功
        :rtype: bool
        """
        res = self._bindSkelComp.Bind(modelId, boneName, offset, rot)
        if res:
            self._bindSkelModelId = modelId
            self._bindSkelBoneName = boneName
            self._bindSkelOffset = offset
            self._bindSkelRot = rot
            self._bindEntId = ""
            self._bindEntOffset = (0.0, 0.0, 0.0)
            self._bindEntRot = (0.0, 0.0, 0.0)
        return res

    def Play(self):
        """
        播放序列帧特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        res = self._ctrl.Play()
        if res:
            self._playing = True
        return res

    def Pause(self):
        """
        暂停序列帧特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        res = self._ctrl.Pause()
        if res:
            self._playing = False
        return res

    def SetDeepTest(self, enabled):
        """
        设置序列帧是否开启深度测试。

        -----

        :param bool enabled: 是否开启深度测试，关闭时序列帧被物体/方块阻挡时仍然能看到

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetDeepTest(enabled)

    def SetFaceCamera(self, face):
        """
        设置序列帧是否始终朝向摄像机。

        -----

        :param bool face: 是否始终朝向摄像机

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetFaceCamera(face)

    def SetFadeDistance(self, dist):
        """
        设置序列帧开始自动调整透明度的距离。

        序列帧与摄像机之间的距离小于该值时会自动调整序列帧的透明度，距离摄像机越近，序列帧越透明。

        -----

        :param float dist: 自动调整透明度的距离，应为正数，负数将视作零来处理

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetFadeDistance(dist)

    def SetLayer(self, layer):
        """
        设置序列帧渲染层级。序列帧默认层级为1，当层级不为1时表示该特效开启特效分层渲染功能。

        分层渲染时，层级越高渲染越靠后，层级大的会遮挡层级低的，且同一层级的特效会根据特效的相对位置产生正确的相互遮挡关系。

        -----

        :param int layer: 序列帧渲染层级，总共包含0-15的层级

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetLayer(layer)

    def SetLoop(self, loop):
        """
        设置序列帧是否循环播放。

        -----

        :param bool loop: 是否循环播放

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetLoop(loop)

    def SetUsePointFiltering(self, use):
        """
        设置序列帧材质的纹理滤波是否使用点滤波方法。

        -----

        :param bool use: True为使用点滤波方法，False为使用默认的双线性滤波

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetUsePointFiltering(use)

















