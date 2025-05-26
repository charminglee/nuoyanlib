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
#   Last Modified : 2025-05-20
#
# ====================================================


"""
nuoyanlib UI库。
"""


from ..._core._sys import is_client
if not is_client():
    raise ImportError("Cannot import nuoyanlib.client.ui in server environment.")
del is_client


from ..._core._client._comp import (
    ScreenNode,
    ViewBinder,
    ViewRequest,
    CustomUIControlProxy,
)


from .screen_node import (
    ScreenNodeExtension,
)
from .ui_utils import (
    to_button,
    to_path,
    to_control,
    ButtonCallback,
    get_parent_path,
    get_all_children_path_by_level,
    get_parent_control,
    notify_server,
)
