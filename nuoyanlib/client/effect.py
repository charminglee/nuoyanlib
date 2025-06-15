# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-09
|
| ==============================================
"""


from .._core._client.comp import CF
from .._core._client import _lib_client


__all__ = [
    "NeteaseParticle",
    "NeteaseFrameAnim",
]


class NeteaseParticle(object):
    """
    | 网易粒子特效管理器。
    | 切换维度后会自动隐藏非本维度创建的而且没有绑定实体的粒子，回到该维度后会自动重新显示。
    | 粒子创建之后需要调用 ``.Play()`` 方法才会播放，如果播放非本维度创建的粒子，会同时修改该粒子的创建维度为当前维度。

    -----

    :param str json_path: 粒子特效json文件路径，包含后缀名.json，如"effects/my_effect.json"
    :param tuple[float,float,float]|None pos: 粒子的世界坐标位置，默认为(0, 0, 0)，绑定实体或骨骼时可忽略该参数
    :param dict[str,str|tuple[float,float,float]|bool]|None bind_entity: 实体绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindEntity方法
    :param dict[str,int|str|tuple[float,float,float]]|None bind_skeleton: 骨骼模型绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindSkeleton方法
    """

    def __init__(self, json_path, pos=(0, 0, 0), bind_entity=None, bind_skeleton=None):
        self.__lib_sys = _lib_client.instance()
        self._id = self.__lib_sys.CreateEngineParticle(json_path, pos)
        if not self._id:
            raise RuntimeError("create particle failed, json_path='%s'" % json_path)
        cf = CF(self._id)
        self._ctrl = cf.ParticleControl
        self._trans = cf.ParticleTrans
        self._bind_ent_comp = cf.ParticleEntityBind
        self._bind_skel_comp = cf.ParticleSkeletonBind
        self._bind_ent_id = ""
        self._bind_ent_offset = (0, 0, 0)
        self._bind_ent_rot = (0, 0, 0)
        self._bind_ent_corr = False
        self._bind_skel_model_id = -1
        self._bind_skel_bone_name = ""
        self._bind_skel_offset = (0, 0, 0)
        self._bind_skel_rot = (0, 0, 0)
        if bind_entity and bind_skeleton:
            raise ValueError(
                "parameters 'bind_entity' and 'bind_skeleton' cannot be given at the same time"
            )
        if bind_entity and not self.BindEntity(**bind_entity):
            raise RuntimeError("bind particle to entity failed, bind_entity=%s" % bind_entity)
        if bind_skeleton and not self.BindSkeleton(**bind_skeleton):
            raise RuntimeError("bind particle to skeleton failed, bind_skeleton=%s" % bind_skeleton)
        self._playing = False
        self._destroyed = False

    @property
    def id(self):
        """
        [只读属性]

        | 粒子特效ID。

        :rtype: int
        """
        return self._id

    @property
    def ent_id(self):
        """
        [可读写属性]

        | 粒子绑定的实体ID。

        :rtype: str
        """
        return self._bind_ent_id

    @ent_id.setter
    def ent_id(self, value):
        """
        [可读写属性]

        | 粒子绑定的实体ID。

        :type value: str
        """
        self.BindEntity(value, self._bind_ent_offset, self._bind_ent_rot, self._bind_ent_corr)

    @property
    def ent_offset(self):
        """
        [可读写属性]

        | 粒子绑定实体时的偏移量。

        :rtype: tuple[float,float,float]
        """
        return self._bind_ent_offset

    @ent_offset.setter
    def ent_offset(self, value):
        """
        [可读写属性]

        | 粒子绑定实体时的偏移量。

        :type value: tuple[float,float,float]
        """
        self.BindEntity(self._bind_ent_id, value, self._bind_ent_rot, self._bind_ent_corr)

    @property
    def ent_rot(self):
        """
        [可读写属性]

        | 粒子绑定实体时的旋转角度。

        :rtype: tuple[float,float,float]
        """
        return self._bind_ent_rot

    @ent_rot.setter
    def ent_rot(self, value):
        """
        [可读写属性]

        | 粒子绑定实体时的旋转角度。

        :type value: tuple[float,float,float]
        """
        self.BindEntity(self._bind_ent_id, self._bind_ent_offset, value, self._bind_ent_corr)

    @property
    def correction(self):
        """
        [可读写属性]

        | 粒子绑定实体时是否开启特效旋转角度修正。

        :rtype: bool
        """
        return self._bind_ent_corr

    @correction.setter
    def correction(self, value):
        """
        [可读写属性]

        | 粒子绑定实体时是否开启特效旋转角度修正。

        :type value: bool
        """
        self.BindEntity(self._bind_ent_id, self._bind_ent_offset, self._bind_ent_rot, value)

    @property
    def model_id(self):
        """
        [可读写属性]

        | 粒子绑定的骨骼模型的ID。

        :rtype: int
        """
        return self._bind_skel_model_id

    @model_id.setter
    def model_id(self, value):
        """
        [可读写属性]

        | 粒子绑定的骨骼模型的ID。

        :type value: int
        """
        self.BindSkeleton(value, self._bind_skel_bone_name, self._bind_skel_offset, self._bind_skel_rot)

    @property
    def bone_name(self):
        """
        [可读写属性]

        | 粒子绑定的具体骨骼的名称。

        :rtype: str
        """
        return self._bind_skel_bone_name

    @bone_name.setter
    def bone_name(self, value):
        """
        [可读写属性]

        | 粒子绑定的具体骨骼的名称。

        :type value: str
        """
        self.BindSkeleton(self._bind_skel_model_id, value, self._bind_skel_offset, self._bind_skel_rot)

    @property
    def skel_offset(self):
        """
        [可读写属性]

        | 粒子绑定骨骼时的偏移量。

        :rtype: tuple[float,float,float]
        """
        return self._bind_skel_offset

    @skel_offset.setter
    def skel_offset(self, value):
        """
        [可读写属性]

        | 粒子绑定骨骼时的偏移量。

        :type value: tuple[float,float,float]
        """
        self.BindSkeleton(self._bind_skel_model_id, self._bind_skel_bone_name, value, self._bind_skel_rot)

    @property
    def skel_rot(self):
        """
        [可读写属性]

        | 粒子绑定骨骼时的旋转角度。

        :rtype: tuple[float,float,float]
        """
        return self._bind_skel_rot

    @skel_rot.setter
    def skel_rot(self, value):
        """
        [可读写属性]

        | 粒子绑定骨骼时的旋转角度。

        :type value: tuple[float,float,float]
        """
        self.BindSkeleton(self._bind_skel_model_id, self._bind_skel_bone_name, self._bind_skel_offset, value)

    @property
    def emission_rate(self):
        """
        [可读写属性]

        | 粒子发射器每帧发射粒子的频率，数据类型为元组：(min, max)，其中min表示每帧发射粒子频率的最小值，max表示每帧发射粒子频率的最大值。
        | 对应粒子特效json文件中 ``"emissionrate"`` 的值。

        :rtype: tuple[float,float]
        """
        return self._ctrl.GetParticleEmissionRate()

    @emission_rate.setter
    def emission_rate(self, value):
        """
        [可读写属性]

        | 设置粒子发射器每帧发射粒子的频率，数据类型为元组：(min, max)，其中min表示每帧发射粒子频率的最小值，max表示每帧发射粒子频率的最大值。
        | 频率越大则每帧发射的粒子数量越多，但粒子数量不会超过粒子发射器的粒子容量，同时由于性能考虑，每帧发射的粒子数量也不会超过100个。
        | 每帧发射粒子的频率将在频率最小值和频率最大值之间取随机数进行插值。当值设置为负值时设置将会失败。
        | 对应粒子特效json文件中 ``"emissionrate"`` 的值。

        :type value: tuple[float,float]
        """
        self._ctrl.SetParticleEmissionRate(*value)

    @property
    def max_num(self):
        """
        [可读写属性]

        | 粒子发射器包含的最大粒子数量，数据类型为整数。
        | 对应粒子特效json文件中 ``"numparticles"`` 的值。

        :rtype: int
        """
        return self._ctrl.GetParticleMaxNum()

    @max_num.setter
    def max_num(self, value):
        """
        [可读写属性]

        | 设置粒子发射器的粒子容量，即粒子发射器所包含的最大粒子数量，数据类型为整数，不能为负值，粒子的数量最大值不超过100000。
        | 该数量并不代表目前粒子发射器所发射的粒子数量，如需要增加发射的粒子数量，需同时改变粒子的发射频率。
        | 对应粒子特效json文件中 ``"numparticles"`` 的值。

        :type value: int
        """
        self._ctrl.SetParticleMaxNum(value)

    @property
    def size(self):
        """
        [可读写属性]

        | 粒子大小的最小值和最大值，数据类型为元组：((minx, miny), (maxx, maxy))，其中minx为粒子x轴大小的最小值，miny为粒子y轴大小的最小值，maxx为粒子x轴大小的最大值，maxy为粒子y轴大小的最大值。
        | 对应粒子特效json文件中 ``"particlesize"`` 的 ``"min"`` 和 ``"max"`` 值。

        :rtype: tuple[tuple[float,float],tuple[float,float]]
        """
        return self._ctrl.GetParticleMinSize(), self._ctrl.GetParticleMaxSize()

    @size.setter
    def size(self, value):
        """
        [可读写属性]

        | 设置粒子大小的最小值及最大值，数据类型为元组：((minx, miny), (maxx, maxy))，其中minx为粒子x轴大小的最小值，miny为粒子y轴大小的最小值，maxx为粒子x轴大小的最大值，maxy为粒子y轴大小的最大值。
        | 粒子大小会在最小值和最大值当中取随机值进行决定，当该值设置为负值时设置将会失败。
        | 对应粒子特效json文件中 ``"particlesize"`` 的 ``"min"`` 和 ``"max"`` 值。

        :type value: tuple[tuple[float,float],tuple[float,float]]
        """
        self._ctrl.SetParticleSize(*value)

    @property
    def volume_size(self):
        """
        [可读写属性]

        | 粒子发射器的体积大小缩放值，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴方向的缩放值。

        :rtype: tuple[float,float,float]
        """
        return self._ctrl.GetParticleVolumeSize()

    @volume_size.setter
    def volume_size(self, value):
        """
        [可读写属性]

        | 设置粒子发射器的体积大小缩放，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴方向的缩放值。
        | 不影响单个粒子的尺寸，粒子发射器的体积越大，则粒子的发射范围越大。
        | 当粒子绑定实体时该设置无效。

        :type value: tuple[float,float,float]
        """
        self._ctrl.SetParticleVolumeSize(value)

    @property
    def pos(self):
        """
        [可读写属性]

        | 粒子发射器的世界坐标位置，数据类型为元组：(x, y, z)。

        :rtype: tuple[float,float,float]
        """
        return self._trans.GetPos()

    @pos.setter
    def pos(self, value):
        """
        [可读写属性]

        | 粒子发射器的世界坐标位置，数据类型为元组：(x, y, z)。

        :type value: tuple[float,float,float]
        """
        self._trans.SetPos(value)

    @property
    def rot(self):
        """
        [可读写属性]

        | 粒子发射器的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。

        :rtype: tuple[float,float,float]
        """
        return self._trans.GetRot()

    @rot.setter
    def rot(self, value):
        """
        [可读写属性]

        | 粒子发射器的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。
        | 旋转顺序按照绕z、x、y轴旋转。

        :type value: tuple[float,float,float]
        """
        self._trans.SetRotUseZXY(value)

    @property
    def playing(self):
        """
        [只读属性]

        | 粒子是否正在播放。

        :rtype: bool
        """
        return self._playing

    @property
    def destroyed(self):
        """
        [只读属性]

        | 粒子是否已销毁。

        :rtype: bool
        """
        return self._destroyed

    def BindEntity(self, ent_id, offset=(0, 0, 0), rot=(0, 0, 0), correction=False):
        """
        | 绑定粒子到实体上。

        -----

        :param str ent_id: 特效绑定的实体ID
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0, 0, 0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0, 0, 0)
        :param bool correction: 是否开启特效旋转角度修正，开启后可以使特效的旋转角度准确设置为参照玩家的相对角度，默认为False

        :return: 是否成功
        :rtype: bool
        """
        res = self._bind_ent_comp.Bind(ent_id, offset, rot, correction)
        if res:
            self._bind_ent_id = ent_id
            self._bind_ent_offset = offset
            self._bind_ent_rot = rot
            self._bind_ent_corr = correction
            self._bind_skel_model_id = -1
            self._bind_skel_bone_name = ""
            self._bind_skel_offset = (0, 0, 0)
            self._bind_skel_rot = (0, 0, 0)
        return res

    def BindSkeleton(self, model_id, bone_name, offset=(0, 0, 0), rot=(0, 0, 0)):
        """
        | 绑定粒子到骨骼模型上。

        -----

        :param int model_id: 绑定的骨骼模型的ID（使用Model组件的GetModelId获取）
        :param str bone_name: 绑定具体骨骼的名称
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0, 0, 0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0, 0, 0)

        :return: 是否成功
        :rtype: bool
        """
        res = self._bind_skel_comp.Bind(model_id, bone_name, offset, rot)
        if res:
            self._bind_skel_model_id = model_id
            self._bind_skel_bone_name = bone_name
            self._bind_skel_offset = offset
            self._bind_skel_rot = rot
            self._bind_ent_id = ""
            self._bind_ent_offset = (0, 0, 0)
            self._bind_ent_rot = (0, 0, 0)
            self._bind_ent_corr = False
        return res

    def Play(self):
        """
        | 播放粒子特效。

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
        | 暂停粒子特效。

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
        | 销毁粒子特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        res = self.__lib_sys.DestroyEntity(self._id)
        if res:
            self._destroyed = True
            self._bind_ent_id = ""
            self._bind_ent_offset = (0, 0, 0)
            self._bind_ent_rot = (0, 0, 0)
            self._bind_ent_corr = False
            self._bind_skel_model_id = -1
            self._bind_skel_bone_name = ""
            self._bind_skel_offset = (0, 0, 0)
            self._bind_skel_rot = (0, 0, 0)
            self._playing = False
            self._ctrl = None
            self._trans = None
            self._bind_ent_comp = None
            self._bind_skel_comp = None
            self._id = None
        return res

    def SetFadeDistance(self, dist):
        """
        | 设置粒子开始自动调整透明度的距离。
        | 粒子与摄像机之间的距离小于该值时会自动调整粒子的透明度，距离摄像机越近，粒子越透明。

        -----

        :param float dist: 自动调整透明度的距离，应为正数，负数将视作零来处理

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetFadeDistance(dist)

    def SetLayer(self, layer):
        """
        | 设置粒子渲染层级。粒子默认层级为1，当层级不为1时表示该特效开启特效分层渲染功能。
        | 分层渲染时，层级越高渲染越靠后，层级大的会遮挡层级低的，且同一层级的特效会根据特效的相对位置产生正确的相互遮挡关系。

        -----

        :param int layer: 粒子渲染层级，总共包含0-15的层级

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetLayer(layer)

    def SetRelative(self, relative):
        """
        | 设置当粒子绑定了实体或骨骼模型时，发射出的粒子使用相对坐标系还是世界坐标系。
        | 与mcstudio特效编辑器中粒子的“相对挂点运动”选项功能相同。

        -----

        :param bool relative: True表示相对坐标系，False表示世界坐标系

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetRelative(relative)

    def SetUsePointFiltering(self, use):
        """
        | 设置粒子材质的纹理滤波是否使用点滤波方法。

        -----

        :param bool use: True为使用点滤波方法，False为使用默认的双线性滤波

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetUsePointFiltering(use)


class NeteaseFrameAnim(object):
    """
    | 网易序列帧特效管理器。
    | 切换维度后会自动隐藏非本维度创建的而且没有绑定实体的序列帧，回到该维度后会自动重新显示。
    | 需要注意，序列帧创建之后需要调用 ``.Play()`` 方法才会播放，如果播放非本维度创建的序列帧，会同时修改该序列帧的创建维度为当前维度。

    -----

    :param str json_path: 特效json配置路径，如"effects/xxx.json"；json_path与tex_path选择其中一个参数传入即可，两个参数都传入时以json_path为准，默认为空字符串
    :param str tex_path: 特效贴图路径，如"textures/xxx"，不用后缀名；json_path与tex_path选择其中一个参数传入即可，两个参数都传入时以json_path为准，默认为空字符串
    :param tuple[float,float,float] pos: 创建位置，默认为None，绑定实体或骨骼时可忽略该参数
    :param tuple[float,float,float] rot: 角度，默认为None，绑定实体或骨骼时可忽略该参数
    :param tuple[float,float,float] scale: 缩放系数，默认为None
    :param dict[str,str|tuple[float,float,float]]|None bind_entity: 实体绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindEntity方法
    :param dict[str,int|str|tuple[float,float,float]]|None bind_skeleton: 骨骼模型绑定参数字典，默认为None，不能同时绑定实体和骨骼模型，具体参数详见BindSkeleton方法
    """

    def __init__(
            self,
            json_path="",
            tex_path="",
            pos=None,
            rot=None,
            scale=None,
            bind_entity=None,
            bind_skeleton=None,
    ):
        self.__lib_sys = _lib_client.instance()
        if json_path:
            self._id = self.__lib_sys.CreateEngineSfxFromEditor(json_path, pos, rot, scale)
        elif tex_path:
            self._id = self.__lib_sys.CreateEngineSfx(tex_path, pos, rot, scale)
        else:
            raise ValueError("parameter 'json_path' or 'tex_path' must be given")
        if not self._id:
            raise RuntimeError("create frame animation failed, path='%s'" % (json_path or tex_path))
        cf = CF(self._id)
        self._ctrl = cf.FrameAniControl
        self._trans = cf.FrameAniTrans
        self._bind_ent_comp = cf.FrameAniEntityBind
        self._bind_skel_comp = cf.FrameAniSkeletonBind
        self._bind_ent_id = ""
        self._bind_ent_offset = (0, 0, 0)
        self._bind_ent_rot = (0, 0, 0)
        self._bind_skel_model_id = -1
        self._bind_skel_bone_name = ""
        self._bind_skel_offset = (0, 0, 0)
        self._bind_skel_rot = (0, 0, 0)
        if bind_entity and bind_skeleton:
            raise ValueError(
                "parameters 'bind_entity' and 'bind_skeleton' cannot be given at the same time"
            )
        if bind_entity and not self.BindEntity(**bind_entity):
            raise RuntimeError("bind frame animation to entity failed, bind_entity=%s" % bind_entity)
        if bind_skeleton and not self.BindSkeleton(**bind_skeleton):
            raise RuntimeError("bind frame animation to skeleton failed, bind_skeleton=%s" % bind_skeleton)
        self._playing = False
        self._destroyed = False

    @property
    def id(self):
        """
        [只读属性]

        | 序列帧特效ID。

        :rtype: int
        """
        return self._id

    @property
    def ent_id(self):
        """
        [可读写属性]

        | 序列帧绑定的实体ID。

        :rtype: str
        """
        return self._bind_ent_id

    @ent_id.setter
    def ent_id(self, value):
        """
        [可读写属性]

        | 序列帧绑定的实体ID。

        :type value: str
        """
        self.BindEntity(value, self._bind_ent_offset, self._bind_ent_rot)

    @property
    def ent_offset(self):
        """
        [可读写属性]

        | 序列帧绑定实体时的偏移量。

        :rtype: tuple[float,float,float]
        """
        return self._bind_ent_offset

    @ent_offset.setter
    def ent_offset(self, value):
        """
        [可读写属性]

        | 序列帧绑定实体时的偏移量。

        :type value: tuple[float,float,float]
        """
        self.BindEntity(self._bind_ent_id, value, self._bind_ent_rot)

    @property
    def ent_rot(self):
        """
        [可读写属性]

        | 序列帧绑定实体时的旋转角度。

        :rtype: tuple[float,float,float]
        """
        return self._bind_ent_rot

    @ent_rot.setter
    def ent_rot(self, value):
        """
        [可读写属性]

        | 序列帧绑定实体时的旋转角度。

        :type value: tuple[float,float,float]
        """
        self.BindEntity(self._bind_ent_id, self._bind_ent_offset, value)

    @property
    def model_id(self):
        """
        [可读写属性]

        | 序列帧绑定的骨骼模型的ID。

        :rtype: int
        """
        return self._bind_skel_model_id

    @model_id.setter
    def model_id(self, value):
        """
        [可读写属性]

        | 序列帧绑定的骨骼模型的ID。

        :type value: int
        """
        self.BindSkeleton(value, self._bind_skel_bone_name, self._bind_skel_offset, self._bind_skel_rot)

    @property
    def bone_name(self):
        """
        [可读写属性]

        | 序列帧绑定的具体骨骼的名称。

        :rtype: str
        """
        return self._bind_skel_bone_name

    @bone_name.setter
    def bone_name(self, value):
        """
        [可读写属性]

        | 序列帧绑定的具体骨骼的名称。

        :type value: str
        """
        self.BindSkeleton(self._bind_skel_model_id, value, self._bind_skel_offset, self._bind_skel_rot)

    @property
    def skel_offset(self):
        """
        [可读写属性]

        | 序列帧绑定骨骼时的偏移量。

        :rtype: tuple[float,float,float]
        """
        return self._bind_skel_offset

    @skel_offset.setter
    def skel_offset(self, value):
        """
        [可读写属性]

        | 序列帧绑定骨骼时的偏移量。

        :type value: tuple[float,float,float]
        """
        self.BindSkeleton(self._bind_skel_model_id, self._bind_skel_bone_name, value, self._bind_skel_rot)

    @property
    def skel_rot(self):
        """
        [可读写属性]

        | 序列帧绑定骨骼时的旋转角度。

        :rtype: tuple[float,float,float]
        """
        return self._bind_skel_rot

    @skel_rot.setter
    def skel_rot(self, value):
        """
        [可读写属性]

        | 序列帧绑定骨骼时的旋转角度。

        :type value: tuple[float,float,float]
        """
        self.BindSkeleton(self._bind_skel_model_id, self._bind_skel_bone_name, self._bind_skel_offset, value)

    @property
    def pos(self):
        """
        [可读写属性]

        | 序列帧的世界坐标位置，数据类型为元组：(x, y, z)。

        :rtype: tuple[float,float,float]
        """
        return self._trans.GetPos()

    @pos.setter
    def pos(self, value):
        """
        [可读写属性]

        | 序列帧的世界坐标位置，数据类型为元组：(x, y, z)。

        :type value: tuple[float,float,float]
        """
        self._trans.SetPos(value)

    @property
    def rot(self):
        """
        [可读写属性]

        | 序列帧的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。

        :rtype: tuple[float,float,float]
        """
        return self._trans.GetRot()

    @rot.setter
    def rot(self, value):
        """
        [可读写属性]

        | 序列帧的旋转角度，数据类型为元组：(x, y, z)，其中x、y、z分别为各个坐标轴的旋转角度。
        | 旋转顺序按照绕z、x、y轴旋转。

        :type value: tuple[float,float,float]
        """
        self._trans.SetRotUseZXY(value)

    @property
    def scale(self):
        """
        [可读写属性]

        | 序列帧的缩放值，数据类型为元组：(x, y, z)。
        | 对于平面序列帧，第一个参数为贴图横向上的缩放，第二个参数为纵向上的缩放，第三个参数无用。
        | 对于环状序列帧，三个参数分别为三个坐标轴上的缩放。

        :rtype: tuple[float,float,float]
        """
        return self._trans.GetScale()

    @scale.setter
    def scale(self, value):
        """
        [可读写属性]

        | 序列帧的缩放值，数据类型为元组：(x, y, z)。
        | 对于平面序列帧，第一个参数为贴图横向上的缩放，第二个参数为纵向上的缩放，第三个参数无用。
        | 对于环状序列帧，三个参数分别为三个坐标轴上的缩放。

        :type value: tuple[float,float,float]
        """
        self._trans.SetScale(value)

    @property
    def playing(self):
        """
        [只读属性]

        | 序列帧是否正在播放。

        :rtype: bool
        """
        return self._playing

    @property
    def destroyed(self):
        """
        [只读属性]

        | 序列帧是否已销毁。

        :rtype: bool
        """
        return self._destroyed

    def BindEntity(self, bind_entity_id, offset=(0, 0, 0), rot=(0, 0, 0)):
        """
        | 绑定序列帧到实体上。

        -----

        :param str bind_entity_id: 特效绑定的实体ID
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0, 0, 0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0, 0, 0)

        :return: 是否成功
        :rtype: bool
        """
        res = self._bind_ent_comp.Bind(bind_entity_id, offset, rot)
        if res:
            self._bind_ent_id = bind_entity_id
            self._bind_ent_offset = offset
            self._bind_ent_rot = rot
            self._bind_skel_model_id = -1
            self._bind_skel_bone_name = ""
            self._bind_skel_offset = (0, 0, 0)
            self._bind_skel_rot = (0, 0, 0)
        return res

    def BindSkeleton(self, model_id, bone_name, offset=(0, 0, 0), rot=(0, 0, 0)):
        """
        | 绑定序列帧到骨骼模型上。

        -----

        :param int model_id: 绑定的骨骼模型的ID（使用Model组件的GetModelId获取）
        :param str bone_name: 绑定具体骨骼的名称
        :param tuple[float,float,float] offset: 绑定的偏移量，默认为(0, 0, 0)
        :param tuple[float,float,float] rot: 绑定的旋转角度，默认为(0, 0, 0)

        :return: 是否成功
        :rtype: bool
        """
        res = self._bind_skel_comp.Bind(model_id, bone_name, offset, rot)
        if res:
            self._bind_skel_model_id = model_id
            self._bind_skel_bone_name = bone_name
            self._bind_skel_offset = offset
            self._bind_skel_rot = rot
            self._bind_ent_id = ""
            self._bind_ent_offset = (0, 0, 0)
            self._bind_ent_rot = (0, 0, 0)
        return res

    def Play(self):
        """
        | 播放序列帧特效。

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
        | 暂停序列帧特效。

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
        | 销毁序列帧特效。

        -----

        :return: 是否成功
        :rtype: bool
        """
        res = self.__lib_sys.DestroyEntity(self._id)
        if res:
            self._destroyed = True
            self._bind_ent_id = ""
            self._bind_ent_offset = (0, 0, 0)
            self._bind_ent_rot = (0, 0, 0)
            self._bind_skel_model_id = -1
            self._bind_skel_bone_name = ""
            self._bind_skel_offset = (0, 0, 0)
            self._bind_skel_rot = (0, 0, 0)
            self._playing = False
            self._ctrl = None
            self._trans = None
            self._bind_ent_comp = None
            self._bind_skel_comp = None
            self._id = None
        return res

    def SetDeepTest(self, enabled):
        """
        | 设置序列帧是否开启深度测试。

        -----

        :param bool enabled: 是否开启深度测试，关闭时序列帧被物体/方块阻挡时仍然能看到

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetDeepTest(enabled)

    def SetFaceCamera(self, face):
        """
        | 设置序列帧是否始终朝向摄像机。

        -----

        :param bool face: 是否始终朝向摄像机

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetFaceCamera(face)

    def SetFadeDistance(self, dist):
        """
        | 设置序列帧开始自动调整透明度的距离。
        | 序列帧与摄像机之间的距离小于该值时会自动调整序列帧的透明度，距离摄像机越近，序列帧越透明。

        -----

        :param float dist: 自动调整透明度的距离，应为正数，负数将视作零来处理

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetFadeDistance(dist)

    def SetLayer(self, layer):
        """
        | 设置序列帧渲染层级。序列帧默认层级为1，当层级不为1时表示该特效开启特效分层渲染功能。
        | 分层渲染时，层级越高渲染越靠后，层级大的会遮挡层级低的，且同一层级的特效会根据特效的相对位置产生正确的相互遮挡关系。

        -----

        :param int layer: 序列帧渲染层级，总共包含0-15的层级

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetLayer(layer)

    def SetLoop(self, loop):
        """
        | 设置序列帧是否循环播放。

        -----

        :param bool loop: 是否循环播放

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetLoop(loop)

    def SetUsePointFiltering(self, use):
        """
        | 设置序列帧材质的纹理滤波是否使用点滤波方法。

        -----

        :param bool use: True为使用点滤波方法，False为使用默认的双线性滤波

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetUsePointFiltering(use)

    def SetGlobal(self, isGlobal):
        """
        | 设置序列帧是否是全局的。
        | 全局时，不会因摄像机的视野范围而被裁剪。

        -----

        :param bool isGlobal: True为全局，False为非全局，默认为False

        :return: 是否成功
        :rtype: bool
        """
        return self._ctrl.SetGlobal(isGlobal)

















