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
#   Last Modified : 2023-11-27
#
# ====================================================


# 在modMain注册时填写的模组名称（命名空间）
MOD_NAME = ""
# 客户端系统名称
CLIENT_SYSTEM_NAME = ""
# 服务端系统名称
SERVER_SYSTEM_NAME = ""


__version__ = "v0.2.0-beta"
__authorname__ = "诺言Nuoyan"
__authorqq__ = "1279735247"
__authoremail__ = "1279735247@qq.com"


if not MOD_NAME or not CLIENT_SYSTEM_NAME or not SERVER_SYSTEM_NAME:
    from utils._error import ConfigError
    raise ConfigError
