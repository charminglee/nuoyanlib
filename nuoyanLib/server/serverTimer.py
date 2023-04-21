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
#   Last Modified : 2023-02-08
#
# ====================================================


from ..utils.error import TimerDestroyedError
try:
    import mod.server.extraServerApi as _serverApi
except:
    pass


__all__ = [
    "ServerTimer",
]


try:
    _LEVEL_ID = _serverApi.GetLevelId()
    _CompFactory = _serverApi.GetEngineCompFactory()
    _GameComp = _CompFactory.CreateGame(_LEVEL_ID)
except:
    pass


class ServerTimer(object):
    """
    服务端函数计时器。
    非重复执行的ServerTimer在执行完毕后会自动销毁（调用Destroy方法）。
    """

    def __init__(self, t, sec, func, *args, **kwargs):
        self.type = t
        self.sec = sec
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.isCancel = False
        self.isPause = False
        self._timer = None
        self._pauseTimer = None
        self._construct()

    @staticmethod
    def Delay(sec):
        # type: (float) -> ...
        """
        函数装饰器，用于函数的延迟执行。
        注：被装饰函数的返回值会变成ServerTimer实例。
        示例：
        @ServerTimer.Delay(2)
        def func(args):
            pass
        timer = func(args)     # 启动函数，两秒后执行
        timer.Cancel()     # 取消执行
        -----------------------------------------------------------
        【sec: float】 延迟秒数
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                return ServerTimer("d", sec, func, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def Repeat(sec):
        # type: (float) -> ...
        """
        函数装饰器，用于函数的重复执行。
        注：被装饰函数的返回值会变成ServerTimer实例。
        示例：
        @ServerTimer.Repeat(2)
        def func(args):
            pass
        timer = func(args)     # 启动计时器，每两秒执行一次
        timer.Cancel()     # 取消执行
        -----------------------------------------------------------
        【sec: float】 重复间隔秒数
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                return ServerTimer("r", sec, func, *args, **kwargs)
            return wrapper
        return decorator

    def _construct(self):
        if self.type == "d":
            def func():
                self.Run()
                self._release()
            self._timer = _GameComp.AddTimer(self.sec, func)
        else:
            self._timer = _GameComp.AddRepeatedTimer(self.sec, self.func, *self.args, **self.kwargs)

    def _release(self):
        self.isCancel = True
        self.isPause = False
        self._timer = None
        self._pauseTimer = None
        self.type = None
        self.sec = None
        self.func = None
        self.args = None
        self.kwargs = None

    def Destroy(self):
        # type: () -> None
        """
        销毁函数计时器，销毁后函数将停止执行，且不可再调用Pause、Run等方法。
        -----------------------------------------------------------
        无参数
        -----------------------------------------------------------
        NoReturn
        """
        if self.isCancel:
            raise TimerDestroyedError("Destroy")
        if self._timer:
            _GameComp.CancelTimer(self._timer)
        if self._pauseTimer:
            _GameComp.CancelTimer(self._pauseTimer)
        self._release()

    def Pause(self, sec=-1.0):
        # type: (float) -> ServerTimer
        """
        暂停函数计时器，重复调用仅第一次有效。
        -----------------------------------------------------------
        【sec: float = -1.0】 暂停秒数，若为负数则无限期暂停
        -----------------------------------------------------------
        return: ServerTimer -> 返回ServerTimer对象自身
        """
        if self.isCancel:
            raise TimerDestroyedError("Pause")
        if not self.isPause:
            _GameComp.CancelTimer(self._timer)
            self._timer = None
            if sec >= 0:
                self._pauseTimer = _GameComp.AddTimer(sec, self.Go)
            self.isPause = True
        return self

    def Go(self):
        # type: () -> ServerTimer
        """
        继续执行函数计时器。
        -----------------------------------------------------------
        无参数
        -----------------------------------------------------------
        return: ServerTimer -> 返回ServerTimer对象自身
        """
        if self.isCancel:
            raise TimerDestroyedError("Go")
        if self.isPause:
            if self._pauseTimer:
                _GameComp.CancelTimer(self._pauseTimer)
                self._pauseTimer = None
            self._construct()
            self.isPause = False
        return self

    def Run(self):
        # type: () -> ServerTimer
        """
        立即执行一次函数。
        -----------------------------------------------------------
        无参数
        -----------------------------------------------------------
        return: ServerTimer -> 返回ServerTimer对象自身
        """
        if self.isCancel:
            raise TimerDestroyedError("Run")
        self.func(*self.args, **self.kwargs)
        return self















