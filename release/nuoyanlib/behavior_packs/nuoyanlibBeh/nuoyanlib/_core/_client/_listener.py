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
#   Last Modified : 2024-07-02
#
# ====================================================


import mod.client.extraClientApi as _api
from .._const import (
    LIB_NAME as _LIB_NAME,
    LIB_SERVER_NAME as _LIB_SERVER_NAME,
)
from .._utils import (
    get_opposite_system as _get_opposite_system,
)
from ...utils.utils import (
    is_method_overridden as _is_method_overridden,
)


__all__ = [
    "event",
    "listen_custom",
    "listen_engine_and_lib",
    "listen_for_lib_sys",
]


_ALL_CLIENT_ENGINE_EVENTS = (
    "GyroSensorChangedClientEvent",
    "ModBlockEntityTickClientEvent",
    "ModBlockEntityRemoveClientEvent",
    "AchievementButtonMovedClientEvent",
    "OnKeyboardControllerLayoutChangeClientEvent",
    "OnGamepadControllerLayoutChangeClientEvent",
    "OnGamepadTriggerClientEvent",
    "OnGamepadStickClientEvent",
    "OnGamepadKeyPressClientEvent",
    "ModBlockEntityLoadedClientEvent",
    "CloseNeteaseShopEvent",
    "PopScreenAfterClientEvent",
    "OnScriptTickClient",
    "UiInitFinished",
    "AddEntityClientEvent",
    "AddPlayerAOIClientEvent",
    "AddPlayerCreatedClientEvent",
    "ChunkAcquireDiscardedClientEvent",
    "ChunkLoadedClientEvent",
    "LoadClientAddonScriptsAfter",
    "OnCommandOutputClientEvent",
    "OnLocalPlayerStopLoading",
    "RemoveEntityClientEvent",
    "RemovePlayerAOIClientEvent",
    "UnLoadClientAddonScriptsBefore",
    "ApproachEntityClientEvent",
    "EntityModelChangedClientEvent",
    "EntityStopRidingEvent",
    "HealthChangeClientEvent",
    "OnGroundClientEvent",
    "OnMobHitMobClientEvent",
    "StartRidingClientEvent",
    "LeaveEntityClientEvent",
    "CameraMotionStartClientEvent",
    "CameraMotionStopClientEvent",
    "DimensionChangeClientEvent",
    "DimensionChangeFinishClientEvent",
    "ExtinguishFireClientEvent",
    "GameTypeChangedClientEvent",
    "OnPlayerHitBlockClientEvent",
    "PerspChangeClientEvent",
    "ClientBlockUseEvent",
    "FallingBlockCauseDamageBeforeClientEvent",
    "OnAfterFallOnBlockClientEvent",
    "OnEntityInsideBlockClientEvent",
    "OnModBlockNeteaseEffectCreatedClientEvent",
    "OnStandOnBlockClientEvent",
    "PlayerTryDestroyBlockClientEvent",
    "ShearsDestoryBlockBeforeClientEvent",
    "StepOffBlockClientEvent",
    "StartDestroyBlockClientEvent",
    "StepOnBlockClientEvent",
    "ActorAcquiredItemClientEvent",
    "ActorUseItemClientEvent",
    "AnvilCreateResultItemAfterClientEvent",
    "ClientItemTryUseEvent",
    "ClientItemUseOnEvent",
    "ClientShapedRecipeTriggeredEvent",
    "GrindStoneRemovedEnchantClientEvent",
    "InventoryItemChangedClientEvent",
    "ItemReleaseUsingClientEvent",
    "OnCarriedNewItemChangedClientEvent",
    "PlayerTryDropItemClientEvent",
    "StartUsingItemClientEvent",
    "StopUsingItemClientEvent",
    "AttackAnimBeginClientEvent",
    "AttackAnimEndClientEvent",
    "WalkAnimBeginClientEvent",
    "WalkAnimEndClientEvent",
    "ClientChestCloseEvent",
    "ClientChestOpenEvent",
    "ClientPlayerInventoryCloseEvent",
    "ClientPlayerInventoryOpenEvent",
    "GridComponentSizeChangedClientEvent",
    "OnItemSlotButtonClickedEvent",
    "PlayerChatButtonClickClientEvent",
    "PopScreenEvent",
    "PushScreenEvent",
    "ScreenSizeChangedClientEvent",
    "OnMusicStopClientEvent",
    "PlayMusicClientEvent",
    "PlaySoundClientEvent",
    "ClientJumpButtonPressDownEvent",
    "ClientJumpButtonReleaseEvent",
    "GetEntityByCoordEvent",
    "GetEntityByCoordReleaseClientEvent",
    "HoldBeforeClientEvent",
    "LeftClickBeforeClientEvent",
    "LeftClickReleaseClientEvent",
    "MouseWheelClientEvent",
    "OnBackButtonReleaseClientEvent",
    "OnClientPlayerStartMove",
    "OnClientPlayerStopMove",
    "OnKeyPressInGame",
    "OnMouseMiddleDownClientEvent",
    "RightClickBeforeClientEvent",
    "RightClickReleaseClientEvent",
    "TapBeforeClientEvent",
    "TapOrHoldReleaseClientEvent",
)
_ALL_CLIENT_LIB_EVENTS = {

}


_lsn_func_args = []


_CLIENT_ENGINE_NAMESPACE = _api.GetEngineNamespace()
_CLIENT_ENGINE_SYSTEM_NAME = _api.GetEngineSystemName()


def event(event_name="", namespace="", system_name="", priority=0):
    """
    | 函数装饰器，通过对函数进行装饰即可实现事件监听。用于客户端。
    | 监听引擎事件（ ``event_name`` 为引擎事件名）时，可省略 ``namespace`` 和 ``system_name`` 参数。

    -----

    :param str event_name: 事件名称，默认为被装饰函数名
    :param str namespace: 指定命名空间，默认为当前客户端对应的服务端的命名空间
    :param str system_name: 指定系统名称，默认为当前客户端对应的服务端的名称
    :param int priority: 优先级，默认为0
    """
    def add_listener(func):
        if event_name and isinstance(event_name, str):
            _event_name = event_name
        else:
            _event_name = func.__name__
        _namespace, _system_name = namespace, system_name
        if not _namespace and not _system_name:
            if _event_name in _ALL_CLIENT_ENGINE_EVENTS:
                _namespace = _CLIENT_ENGINE_NAMESPACE
                _system_name = _CLIENT_ENGINE_SYSTEM_NAME
        elif not _namespace:
            raise ValueError("Missing parameter 'namespace'.")
        elif not _system_name:
            raise ValueError("Missing parameter 'system_name'.")
        _lsn_func_args.append((_namespace, _system_name, _event_name, func, priority))
        return func
    if isinstance(event_name, str):
        return add_listener
    else:
        return add_listener(event_name)


def listen_custom(self):
    from ._lib_client import get_lib_system
    lib_sys = get_lib_system()
    for args in _lsn_func_args:
        # noinspection PyUnresolvedReferences
        namespace = args[0] or (self.cs.namespace if hasattr(self, 'cs') else self.namespace)
        # noinspection PyUnresolvedReferences
        system_name = args[1] or _get_opposite_system(self.cs.systemName if hasattr(self, 'cs') else self.systemName)
        func = args[3]
        method = getattr(self, func.__name__, None)
        if method and method.__func__ is func:
            lib_sys.ListenForEvent(namespace, system_name, args[2], self, method, args[4])


def listen_engine_and_lib(self):
    from ...client.client_system import NuoyanClientSystem
    for name in _ALL_CLIENT_ENGINE_EVENTS:
        if _is_method_overridden(self.__class__, NuoyanClientSystem, name):
            method = getattr(self, name)
            self.ListenForEvent(_CLIENT_ENGINE_NAMESPACE, _CLIENT_ENGINE_SYSTEM_NAME, name, self, method)
    for name, sys_name in _ALL_CLIENT_LIB_EVENTS.items():
        if _is_method_overridden(self.__class__, NuoyanClientSystem, name):
            method = getattr(self, name)
            self.ListenForEvent(_LIB_NAME, sys_name, name, self, method)


def listen_for_lib_sys(name):
    return event(name, _LIB_NAME, _LIB_SERVER_NAME)







