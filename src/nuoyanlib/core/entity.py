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


from ._utils import cached_property, client_api, server_api
from ._sys import is_client, get_cf


__all__ = [
    "Entity",
]


class Entity(object):
    def __init__(self, entity_id, _is_client=None):
        if not entity_id:
            return
        if _is_client is None:
            _is_client = is_client()
        self._is_client = _is_client
        self._cf = get_cf(entity_id)
        self.entity_id = entity_id

    # region Properties ================================================================================================

    @cached_property
    def type(self):
        """
        [只读属性]

        实体类型（网易 `EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html>`_ 枚举值）。

        :rtype: str
        """
        return self._cf.EngineType.GetEngineType()

    @cached_property
    def identifier(self):
        """
        [只读属性]

        实体 identifier（TypeStr）。

        :rtype: str
        """
        return self._cf.EngineType.GetEngineTypeStr()

    # @property
    # def definitions(self):
    #     """
    #     [只读属性] [服务端]
    #
    #     实体的命名空间ID及其当前和之前的定义组件群。
    #
    #     :rtype: list[str]
    #     """
    #     return self._cf.EntityDefinitions.GetEntityDefinitions()

    @cached_property
    def aux_value(self):
        """
        [只读属性]

        射出的弓箭或投掷出的药水的附加值。

        :rtype: int
        """
        return self._cf.AuxValue.GetAuxValue()

    @property
    @server_api
    def nbt(self):
        """
        [只读属性] [服务端]

        实体 NBT 数据。

        :rtype: dict[str,Any]|None
        """
        return self._cf.EntityDefinitions.GetEntityNBTTags()

    @property
    @client_api
    def body_rot(self):
        """
        [只读属性] [客户端]

        实体身体y轴旋转角度，如果没有身体，返回 0。

        :rtype: float
        """
        return self._cf.Rot.GetBodyRot()

    # endregion














