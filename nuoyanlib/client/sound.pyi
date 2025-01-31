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
#   Last Modified : 2023-11-26
#
# ====================================================


from typing import Optional
from .._core._typing import FTuple3


def play_custom_sound(
    sound_name: str,
    pos: FTuple3 = (0, 0, 0),
    volume: float = 1.0,
    speed: float = 1.0,
    is_loop: bool = False,
    entity_id: Optional[str] = None,
) -> str: ...
def stop_custom_sound(sound_id: str, fade_out_time: float = 0.0) -> bool: ...

















