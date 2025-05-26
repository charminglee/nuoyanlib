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
#   Last Modified : 2024-04-20
#
# ====================================================


from typing import Callable, Any, Optional
from threading import Timer


class McTimer(object):
    type: str
    sec: float
    func: Optional[Callable]
    args: Any
    kwargs: Any
    _pause: bool
    _cancel: bool
    __timer: Optional[Timer]
    def __init__(self: ..., ttype: str, sec: float, func: Callable, *args: Any, **kwargs: Any): ...
    def _execute(self) -> Any: ...
    def __func(self) -> None: ...
    def Start(self) -> McTimer: ...
    def Cancel(self) -> None: ...
    def _release(self) -> None: ...
    def Pause(self, sec: Optional[float] = None) -> McTimer: ...
    def Continue(self) -> McTimer: ...
    def Execute(self) -> Any: ...
    def IsCanceled(self) -> bool: ...
    def IsPaused(self) -> bool: ...
