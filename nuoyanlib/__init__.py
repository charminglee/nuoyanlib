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
#   Last Modified : 2025-02-21
#
# ====================================================


from ._core._logging import log as _log


__version__ = "v0.8.0-beta"
__authorname__ = "诺言Nuoyan"
__authorqq__ = "1279735247"
__authoremail__ = "1279735247@qq.com"


_log("Start loading, version: %s" % __version__)


# todo：为函数添加调用失败时输出异常信息的功能，新增_error模块用于管理可能出现的异常
# todo：Entity类、Player类
