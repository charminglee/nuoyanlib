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
#   Last Modified : 2025-05-23
#
# ====================================================


"""
nuoyanlib客户端库。
"""


from .._core._sys import check_env, init_lib_sys


check_env("client")
init_lib_sys()
del check_env, init_lib_sys


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
from .._core._listener import (
    event,
    ClientEventProxy,
)


from .effect import (
    NeteaseParticle,
    NeteaseFrameAnim,
)
from .player import (
    player_plunge,
)
from .setting import (
    save_setting,
    read_setting,
    check_setting,
)
from .sound import (
    play_custom_sound,
    stop_custom_sound,
)
from .render import (
    set_query_mod_var,
    add_player_render_resources,
    add_entity_render_resources,
)
from .camera import (
    get_entities_within_view,
)


from .ui import *


from ..utils import *
