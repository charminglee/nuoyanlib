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
#   Last Modified : 2025-05-16
#
# ====================================================


from ..client import (
    ClientSystem as _ClientSystem,
)
from .._core._utils import (
    is_not_inv_key as _is_not_inv_key,
    singleton as _singleton,
)
from .._core._listener import (
    lib_sys_event as _lib_sys_event,
    ClientEventProxy as _ClientEventProxy,
)
from .._core._logging import log as _log


@_singleton
class ItemGridClient(_ClientEventProxy, _ClientSystem):
    def __init__(self, namespace, system_name):
        super(ItemGridClient, self).__init__(namespace, system_name)
        self.item_grid_path = {}
        self.item_grid_size = {}
        self.item_grid_items = {}
        self.registered_keys = {}

    @_lib_sys_event
    def _UpdateItemGrids(self, args):
        data = args['data']
        self.item_grid_items.update(data)

    def register_item_grid(self, key, cls_path, path, size, is_single):
        if key in self.item_grid_path:
            _log("Register item grid failed: key '%s' already exists" % key, level="ERROR")
            return False
        self.registered_keys.setdefault(cls_path, []).append(key)
        self.item_grid_path[key] = (path, is_single)
        self.item_grid_size[key] = size
        if _is_not_inv_key(key):
            self.item_grid_items[key] = [None] * size
            self.NotifyToServer("_RegisterItemGrid", {'key': key, 'size': size})
        return True













