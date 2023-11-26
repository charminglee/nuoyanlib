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


from traceback import format_exc as _format_exc
import mod.client.extraClientApi as _clientApi
import mod.server.extraServerApi as _serverApi
from ..config import (
    MOD_NAME as _MOD_NAME,
    CLIENT_SYSTEM_NAME as _CLIENT_SYSTEM_NAME,
    SERVER_SYSTEM_NAME as _SERVER_SYSTEM_NAME,
)


__all__ = [
    "print_error",
    "ConfigError",
    "ClientNotFoundError",
    "ServerNotFoundError",
]


def _notify_message(m):
    if _clientApi.GetLocalPlayerId() == "-1":
        _serverApi.GetEngineCompFactory().CreateGame(_serverApi.GetLevelId()).SetNotifyMsg(m)
    else:
        _clientApi.GetEngineCompFactory().CreateTextNotifyClient(_clientApi.GetLevelId()).SetLeftCornerNotify(m)


def print_error(modName=""):
    """
    打印错误信息。
    
    -----

    :param str modName: 模组名称，默认为空字符串

    :return: 无
    :rtype: None
    """
    if modName:
        modName = "[%s] " % modName
    errorInfo = _format_exc()
    errorLine = errorInfo.split("\n")
    for i in range(len(errorLine)):
        error = errorLine[i]
        if not i:
            text = ("§4§l%s运行出错！请将以下错误代码截图并向作者反馈：\n§r" % modName) + error
        else:
            text = error
        _notify_message(text)


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


















