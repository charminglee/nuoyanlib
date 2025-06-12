# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-06
|
| ==============================================
"""


from threading import Timer


__all__ = [
    "McTimer",
]


class McTimer(object):
    """
    | 客户端函数定时器。非重复执行的定时器在执行完毕后会自动销毁。
    | 与官方的定时器不同的是，该定时器使用threading标准库实现，比官方的定时器计时更精准。

    -----

    :param str ttype: 定时器类型，可选值为"d"和"r"，分别表示普通定时器和重复定时器
    :param float sec: 延迟秒数
    :param function func: 延迟函数
    :param Any args: 变长参数，调用func时传入
    :param Any kwargs: 字典变长参数，调用func时传入
    """

    def __init__(self, ttype, sec, func, *args, **kwargs):
        self.type = ttype
        self.sec = sec
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._pause = False
        self._cancel = False
        self.__timer = Timer(sec, self.__func)

    def _execute(self):
        return self.func(*self.args, **self.kwargs)

    def __func(self):
        self._execute()
        if self.type == "r" and not self._cancel:
            self.__timer = Timer(self.sec, self.__func)
            self.__timer.start()
        else:
            self._release()

    def Start(self):
        """
        | 启动定时器。

        -----

        :return: 定时器自身
        :rtype: McTimer
        """
        self.__timer.start()
        return self

    def Cancel(self):
        """
        | 取消定时器。

        -----

        :return: 无
        :rtype: None
        """
        self.__timer.cancel()
        self._release()

    def _release(self):
        self.__timer = None
        self._cancel = True
        self._pause = False
        self.sec = -1
        self.func = None
        self.args = None
        self.kwargs = None

    def Pause(self, sec=None):
        # todo: Pause
        """
        | 暂停定时器，重复调用时仅第一次有效。

        -----

        :param float|None sec: 暂停秒数，默认为None，表示无限期暂停

        :return: 定时器自身
        :rtype: McTimer
        """
        if not self._pause:
            pass
        return self

    def Continue(self):
        # todo: Continue
        """
        | 继续运行被暂停的定时器。

        -----

        :return: 定时器自身
        :rtype: McTimer
        """
        if self._pause:
            pass
        return self

    def Execute(self):
        """
        | 立即执行一次函数。

        -----

        :return: 返回原函数的返回值
        :rtype: Any
        """
        return self._execute()

    def IsCanceled(self):
        """
        | 获取定时器是否已经取消。

        -----

        :return: 定时器正在运行时返回True，定时器已取消或执行完毕时返回False
        :rtype: bool
        """
        return self._cancel

    def IsPaused(self):
        """
        | 获取定时器是否暂停。

        -----

        :return: 是否暂停
        :rtype: bool
        """
        return not self._cancel and self._pause


if __name__ == "__main__":
    def func1(x, y):
        print(x + y)
    timer1 = McTimer("d", 1, func1, 1, 2)
    a = []
    def func2(x):
        a.append(x)
        print(a)
        if len(a) >= 3:
            timer2.Cancel()
    timer2 = McTimer("r", 2, func2, 1)
    timer1.Start()
    timer2.Start()
    def func3():
        print(114514)
    timer3 = McTimer("d", 2, func3).Start()
    def func4():
        timer3.Cancel()
        print("stop 114514")
    McTimer("d", 1, func4).Start()














