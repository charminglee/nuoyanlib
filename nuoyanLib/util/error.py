# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Email         : 1279735247@qq.com
#   Last Modified : 2023-01-13
#
# ====================================================


from traceback import format_exc as _format_exc
import mod.client.extraClientApi as _clientApi
import mod.server.extraServerApi as _serverApi
from .._config import MOD_NAME as _MOD_NAME


def _notify_message(message):
    if _clientApi.GetLocalPlayerId() == "-1":
        _serverApi.GetEngineCompFactory().CreateGame(_serverApi.GetLevelId()).SetNotifyMsg(message)
    else:
        _clientApi.GetEngineCompFactory().CreateTextNotifyClient(_clientApi.GetLevelId()).SetLeftCornerNotify(message)


def print_error():
    # type: () -> None
    """
    打印错误信息。
    示例：
    try:
        a = {}
        c = a['b']
    except KeyError:
        print_error()
    -----------------------------------------------------------
    无参数
    -----------------------------------------------------------
    return -> None
    """
    errorInfo = _format_exc()
    errorLine = errorInfo.split("\n")
    for i in range(len(errorLine)):
        error = errorLine[i]
        if not i:
            text = ("§4§l[%s] 运行出错！请将以下错误代码截图并向作者反馈：\n§r" % _MOD_NAME) + error
        else:
            text = error
        _notify_message(text)



















