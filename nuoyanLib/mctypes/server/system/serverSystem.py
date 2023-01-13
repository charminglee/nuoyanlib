# -*- coding: utf-8 -*-


from ...common.system.baseSystem import BaseSystem


class ServerSystem(BaseSystem):
    def BroadcastToAllClient(self, eventName, eventData):
        # type: (str, dict) -> None
        """
        服务器广播事件到所有客户端
        """
        pass

    def NotifyToMultiClients(self, targetIdList, eventName, eventData):
        # type: (list[str], str, dict) -> None
        """
        2.0版本仅Apollo可用，服务器发送事件到指定一批客户端
        """
        pass

    def NotifyToClient(self, targetId, eventName, eventData):
        # type: (str, str, dict) -> None
        """
        服务器发送事件到指定客户端
        """
        pass

    def CreateEngineEntityByTypeStr(self, engineTypeStr, pos, rot, dimensionId=0, isNpc=False):
        # type: (str, tuple[float,float,float], tuple[float,float], int, bool) -> str | None
        """
        创建指定identifier的实体
        """
        pass

    def CreateEngineItemEntity(self, itemDict, dimensionId=0, pos=(0, 0, 0)):
        # type: (dict, int, tuple[float,float,float]) -> str | None
        """
        用于创建物品实体（即掉落物），返回物品实体的entityId
        """
        pass

    def DestroyEntity(self, entityId):
        # type: (str) -> bool
        """
        销毁实体
        """
        pass

