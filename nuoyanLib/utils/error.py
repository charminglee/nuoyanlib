# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-06-02
#
# ====================================================


from traceback import format_exc as _format_exc
# import mod.client.extraClientApi as _clientApi
# import mod.server.extraServerApi as _serverApi


__all__ = [
    "print_error",
    "TimerDestroyedError",
    "ConfigError",
]


def _notify_message(m):
    if _clientApi.GetLocalPlayerId() == "-1":
        _serverApi.GetEngineCompFactory().CreateGame(_serverApi.GetLevelId()).SetNotifyMsg(m)
    else:
        _clientApi.GetEngineCompFactory().CreateTextNotifyClient(_clientApi.GetLevelId()).SetLeftCornerNotify(m)


def print_error(modName=""):
    # type: (str) -> None
    """
    打印错误信息。
    -----------------------------------------------------------
    【modName: str = ""】 模组名称
    -----------------------------------------------------------
    NoReturn
    -----------------------------------------------------------
    【示例】
    try:
        a = {}
        c = a['b']
    except KeyError:
        print_error()
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


class TimerDestroyedError(Exception):
    """
    McTimer销毁后调用pause、run等方法时抛出的异常。
    """

    def __init__(self, m):
        super(TimerDestroyedError, self).__init__()
        self.m = m

    def __str__(self):
        return "This timer has been destroyed, you can no longer call '%s' method" % self.m


class ConfigError(Exception):
    """
    未修改_config.py配置文件而抛出的异常。
    """

    def __str__(self):
        return "You haven't modified \"_config.py\"."



















