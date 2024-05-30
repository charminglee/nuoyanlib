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
#   Last Modified : 2024-05-30
#
# ====================================================


from .._core._client._listener import (
    listen_for,
)
from client_system import (
    NuoyanClientSystem,
)
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
from effect import (
    NeteaseParticle,
    NeteaseFrameAnim,
)
from player import (
    player_plunge,
)
from setting import (
    save_setting,
    read_setting,
    check_setting,
)
from sound import (
    play_custom_sound,
    stop_custom_sound,
)
