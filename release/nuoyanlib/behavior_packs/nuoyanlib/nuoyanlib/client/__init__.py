# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN AS IS BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-07-05
#
# ====================================================


from .._core._const import LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH
import mod.client.extraClientApi as client_api
if not client_api.GetSystem(LIB_NAME, LIB_CLIENT_NAME):
    client_api.RegisterSystem(LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH)
del client_api, LIB_NAME, LIB_CLIENT_NAME, LIB_CLIENT_PATH


from .._core._client._comp import (
    CLIENT_ENGINE_NAMESPACE,
    CLIENT_ENGINE_SYSTEM_NAME,
    ClientSystem,
    CompFactory,
    PLAYER_ID,
    LEVEL_ID,
    PlrComp,
    LvComp,
)
from .._core._client._listener import (
    event,
)
from .client_system import *
from .effect import *
from .player import *
from .setting import *
from .sound import *
from .render import *


__all__ = [
    # _comp
    "CLIENT_ENGINE_NAMESPACE",
    "CLIENT_ENGINE_SYSTEM_NAME",
    "ClientSystem",
    "CompFactory",
    "PLAYER_ID",
    "LEVEL_ID",
    "PlrComp",
    "LvComp",
    # _listener
    "event",
    # client_system
    "NuoyanClientSystem",
    # effect
    "NeteaseParticle",
    "NeteaseFrameAnim",
    # player
    "player_plunge",
    # setting
    "save_setting",
    "read_setting",
    "check_setting",
    # sound
    "play_custom_sound",
    "stop_custom_sound",
    # render
    "set_query_mod_var",
    "add_player_render_resources",
    "add_entity_render_resources",
]
