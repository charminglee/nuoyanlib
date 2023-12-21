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
#   Last Modified : 2023-11-30
#
# ====================================================


from ..config import (
    MOD_NAME as _MOD_NAME,
    CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME,
    SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME,
)


__all__ = [
    "ConfigError",
    "ClientNotFoundError",
    "ServerNotFoundError",
]


class ConfigError(Exception):
    """
    未修改config.py配置文件而抛出的异常。
    """

    def __str__(self):
        return "You haven't modified \"config.py\"."


class ClientNotFoundError(Exception):
    """
    没有找到config.py中配置的客户端系统而抛出的异常。
    """

    def __str__(self):
        return "MOD_NAME='%s', CLIENT_SYSTEM_NAME='%s'." % (_MOD_NAME, _CLIENT_SYSTEM_NAME)


class ServerNotFoundError(Exception):
    """
    没有找到config.py中配置的服务端系统而抛出的异常。
    """

    def __str__(self):
        return "MOD_NAME='%s', SERVER_SYSTEM_NAME='%s'." % (_MOD_NAME, _SERVER_SYSTEM_NAME)


















