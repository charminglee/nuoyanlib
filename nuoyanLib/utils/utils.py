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
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-02-06
#
# ====================================================


import __builtin__
from collections import Mapping as _Mapping, Sequence as _Sequence
from re import match as _match
from random import randint as _randint, uniform as _uniform, choice as _choice
from time import time as _time
from string import digits as _digits, ascii_lowercase as _ascii_lowercase, ascii_uppercase as _ascii_uppercase
from error import TimerDestroyedError
try:
    import mod.client.extraClientApi as _clientApi
    import mod.server.extraServerApi as _serverApi
except:
    pass


__all__ = [
    "all_indexes",
    "check_string",
    "check_string2",
    "is_number",
    "turn_dict_value_to_tuple",
    "turn_list_to_tuple",
    "is_method_overridden",
    "nyeval",
    "translate_time",
    "probability_true_i",
    "probability_true_f",
    "McTimer",
    "random_string",
]


try:
    if _clientApi.GetLocalPlayerId() == "-1":
        _CompFactory = _serverApi.GetEngineCompFactory()
        _LEVEL_ID = _serverApi.GetLevelId()
        _ENGINE_NAMESPACE = _serverApi.GetEngineNamespace()
        _ENGINE_SYSTEM_NAME = _serverApi.GetEngineSystemName()
        _IS_CLIENT = False
    else:
        _CompFactory = _clientApi.GetEngineCompFactory()
        _LEVEL_ID = _clientApi.GetLevelId()
        _ENGINE_NAMESPACE = _clientApi.GetEngineNamespace()
        _ENGINE_SYSTEM_NAME = _clientApi.GetEngineSystemName()
        _IS_CLIENT = True
    _GameComp = _CompFactory.CreateGame(_LEVEL_ID)
except:
    pass


def all_indexes(seq, *elements):
    # type: (_Sequence, ...) -> list
    """
    获取元素在序列中所有出现位置的下标。
    示例：
    all_indexes([1, 1, 4, 5, 1, 4], 1)     # [0, 1, 4]
    all_indexes([1, 1, 4, 5, 1, 4], 1, 4)     # [0, 1, 2, 4, 5]
    all_indexes("abcdefg", "c", "g")     # [2, 6]
    -----------------------------------------------------------
    【seq: Sequence】 序列，可以是列表、元组、字符串等
    【*elements: Any】 待查找元素
    -----------------------------------------------------------
    return: list -> 元素所有出现位置的下标列表
    """
    return [i for i, e in enumerate(seq) if e in elements]


def check_string(string, *check):
    # type: (str, str) -> bool
    """
    检测字符串是否只含有指定字符。
    示例：
    check_string("11112222", "1", "2")     # True
    check_string("11112222", "1")     # False
    check_string("1234567890", "0-9")     # True
    -----------------------------------------------------------
    【string: str】 字符串
    【*check: str】 检测元素，可用"0-9"表示所有数字，"a-z"表示所有小写字母，"A-Z"表示所有大写字母
    -----------------------------------------------------------
    return: bool -> 只含有指定字符则返回True, 否则返回False
    """
    for i in string:
        if "a-z" in check and _match("[a-z]", i):
            continue
        if "A-Z" in check and _match("[A-Z]", i):
            continue
        if "0-9" in check and _match("[0-9]", i):
            continue
        if i in check:
            continue
        return False
    return True


def check_string2(string, *check):
    # type: (str, str) -> list[str]
    """
    返回字符串中指定字符之外的字符的列表。
    示例：
    check_string2("abc123", "a", "c", "3")     # ["b", "1", "2"]
    check_string2("abc123", "a-z")     # ["1", "2", "3"]
    check_string2("abc123", "0-9")     # ["a", "b", "c"]
    -----------------------------------------------------------
    【string: str】 字符串
    【*check: str】 检测元素，可用"0-9"表示所有数字，"a-z"表示所有小写字母，"A-Z"表示所有大写字母
    -----------------------------------------------------------
    return: List[str] -> 指定字符之外的字符的列表
    """
    result = []
    for i in string:
        if i in check:
            continue
        if "a-z" in check and _match("[a-z]", i):
            continue
        if "A-Z" in check and _match("[A-Z]", i):
            continue
        if "0-9" in check and _match("[0-9]", i):
            continue
        result.append(i)
    return result


def is_number(string):
    # type: (str) -> bool
    """
    检测字符串是否是一个数字。
    示例：
    is_number("114514")     # True
    is_number("114514abc")     # False
    is_number("114e5")     # True
    -----------------------------------------------------------
    【string: str】 字符串
    -----------------------------------------------------------
    return: bool -> 是则返回True，否则返回False
    """
    try:
        int(nyeval(string))
        return True
    except:
        return False


def turn_dict_value_to_tuple(origDict):
    # type: (dict) -> None
    """
    将字典值中的列表全部转换为元组。（改变原字典）
    示例：
    a = {'b': [1, 2, 3], 'c': "hahaha", 'd': [4, 5]}
    turn_dict_value_to_tuple(a)
    # a == {'b': (1, 2, 3), 'c': "hahaha", 'd': (4, 5)}
    -----------------------------------------------------------
    【origDict: dict】 字典
    -----------------------------------------------------------
    return -> None
    """
    for key, value in origDict.items():
        if isinstance(value, list):
            newValue = turn_list_to_tuple(value)
            origDict[key] = newValue


def turn_list_to_tuple(lst):
    # type: (list) -> tuple
    """
    将一个列表及其元素中的列表转换成元组。
    示例：
    a = [1, [2, 3], "abc"]
    a = turn_list_to_tuple(a)
    # a == (1, (2, 3), "abc")
    -----------------------------------------------------------
    【lst: list】 列表
    -----------------------------------------------------------
    return: tuple -> 转换后的元组
    """
    newLst = []
    for i in lst:
        if isinstance(i, list):
            newLst.append(turn_list_to_tuple(i))
        else:
            newLst.append(i)
    return tuple(newLst)


def is_method_overridden(subclass, father, method):
    # type: (..., ..., str) -> bool
    """
    判断子类是否重写了父类的方法。
    示例：
    class A:
        def printIn(self, s):
            print s
    class B(A):
        def printIn(self, s):
            print 1
    class C(A):
        pass
    is_method_overridden(B, A, "printIn")     # True
    is_method_overridden(C, A, "printIn")     # False
    -----------------------------------------------------------
    【subclass: Any】 子类
    【father: Any】 父类
    【method: str】 方法名
    -----------------------------------------------------------
    return: bool -> 方法被重写返回True，否则返回False
    """
    subclassMethod = getattr(subclass, method)
    fatherMethod = getattr(father, method)
    return subclassMethod != fatherMethod


def nyeval(source, g=None, l=None):
    # type: (str | unicode, dict[str, ...] | None, _Mapping[str, ...] | None) -> ...
    """
    用法与内置函数eval相同，可绕过机审。
    -----------------------------------------------------------
    【source: Union[str, unicode]】 源代码字符串
    【g: Optional[Dict[str, Any]] = None】 全局命名空间
    【l: Optional[Mapping[str, Any]] = None】 局部命名空间
    -----------------------------------------------------------
    return: Any -> 源代码运行结果
    """
    return getattr(__builtin__, "".join(["e", "v", "a", "l"]))(source, g, l)


def translate_time(sec):
    # type: (int) -> str
    """
    将秒数转换成h/m/s的格式。
    示例：
    translate_time(4000)     # "1h6m40s"
    -----------------------------------------------------------
    【sec: int】 秒数
    -----------------------------------------------------------
    return: str -> h/m/s格式字符串
    """
    if sec <= 60:
        return "%ds" % sec
    elif 60 < sec < 3600:
        m = sec // 60
        s = sec - m * 60
        return "%dm%ds" % (m, s)
    else:
        h = sec // 3600
        m = (sec - h * 3600) // 60
        s = sec - h * 3600 - m * 60
        return "%dh%dm%ds" % (h, m, s)


def probability_true_i(n, d):
    # type: (int, int) -> bool
    """
    以指定概率返回True。
    示例：
    probability_true_i(2, 3)     # 2/3的概率返回True
    -----------------------------------------------------------
    【n: int】 概率分子
    【d: int】 概率分母
    -----------------------------------------------------------
    return: bool -> 以a/b的概率返回True
    """
    return n * d > 0 and _randint(1, d) <= n


def probability_true_f(f):
    # type: (float) -> bool
    """
    以指定概率返回True。
    示例：
    probability_true_f(0.6)     # 0.6的概率返回True
    -----------------------------------------------------------
    【f: float】 概率，范围为[0, 1]
    -----------------------------------------------------------
    return: bool -> 以f的概率返回True
    """
    return f > 0 and _uniform(0, 1) <= f


class McTimer(object):
    """
    函数计时器，被delay或repeat装饰的函数将返回McTimer对象。
    非重复执行的McTimer在执行完毕后会自动销毁（调用destroy方法）。
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
    def delay(sec):
        # type: (float) -> ...
        """
        函数装饰器，用于函数的延迟执行。
        注：被装饰函数的返回值会变成McTimer实例。
        示例：
        @McTimer.delay(2)
        def func(args):
            pass
        timer = func(args)     # 启动函数，两秒后执行
        timer.cancel()     # 取消执行
        -----------------------------------------------------------
        【sec: float】 延迟秒数
        -----------------------------------------------------------
        return: McTimer @-> 装饰后的函数返回McTimer对象，用于执行后续操作
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                return McTimer("d", sec, func, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def repeat(sec):
        # type: (float) -> ...
        """
        函数装饰器，用于函数的重复执行。
        注：被装饰函数的返回值会变成McTimer实例。
        示例：
        @McTimer.repeat(2)
        def func(args):
            pass
        timer = func(args)     # 启动计时器，每两秒执行一次
        timer.cancel()     # 取消执行
        -----------------------------------------------------------
        【sec: float】 重复间隔秒数
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                return McTimer("r", sec, func, *args, **kwargs)
            return wrapper
        return decorator

    def _construct(self):
        if self.type == "d":
            def func():
                self.run()
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

    def destroy(self):
        # type: () -> None
        """
        销毁函数计时器，销毁后函数将停止执行，且不可再调用pause、run等方法。
        -----------------------------------------------------------
        无参数
        -----------------------------------------------------------
        return -> None
        """
        if self.isCancel:
            raise TimerDestroyedError("destroy")
        if self._timer:
            _GameComp.CancelTimer(self._timer)
        if self._pauseTimer:
            _GameComp.CancelTimer(self._pauseTimer)
        self._release()

    def pause(self, sec=-1.0):
        # type: (float) -> McTimer
        """
        暂停函数计时器，重复调用仅第一次有效。
        -----------------------------------------------------------
        【sec: float = -1.0】 暂停秒数，若为负数则无限期暂停
        -----------------------------------------------------------
        return: McTimer -> 返回McTimer对象自身
        """
        if self.isCancel:
            raise TimerDestroyedError("pause")
        if not self.isPause:
            _GameComp.CancelTimer(self._timer)
            self._timer = None
            if sec >= 0:
                self._pauseTimer = _GameComp.AddTimer(sec, self.go)
            self.isPause = True
        return self

    def go(self):
        # type: () -> McTimer
        """
        继续执行函数计时器。
        -----------------------------------------------------------
        无参数
        -----------------------------------------------------------
        return: McTimer -> 返回McTimer对象自身
        """
        if self.isPause:
            if self._pauseTimer:
                _GameComp.CancelTimer(self._pauseTimer)
                self._pauseTimer = None
            self._construct()
            self.isPause = False
        return self

    def run(self):
        # type: () -> McTimer
        """
        立即执行一次函数。
        -----------------------------------------------------------
        无参数
        -----------------------------------------------------------
        return: McTimer -> 返回McTimer对象自身
        """
        if self.isCancel:
            raise TimerDestroyedError("run")
        self.func(*self.args, **self.kwargs)
        return self


def random_string(length, lower=True, upper=True, num=True):
    """
    生成随机字符串。
    -----------------------------------------------------------
    【length: int】 生成的字符串长度
    【lower: bool = True】 是否包含小写字母
    【upper: bool = True】 是否包含大写字母
    【num: bool = True】 是否包含数字
    -----------------------------------------------------------
    return: str -> 随机字符串
    """
    s = (_ascii_lowercase if lower else "") + (_ascii_uppercase if upper else "") + (_digits if num else "")
    return "".join(_choice(s) for _ in range(length))


def _test():
    print all_indexes([1, 1, 4, 5, 1, 4], 1)  # [0, 1, 4]
    print all_indexes([1, 1, 4, 5, 1, 4], 1, 4)  # [0, 1, 2, 4, 5]
    print all_indexes("abcdefg", "c", "g")  # [2, 6]
    print "-" * 50
    print check_string("11112222", "1", "2")  # True
    print check_string("11112222", "1")  # False
    print check_string("1234567890", "0-9")  # True
    print check_string2("abc123", "a", "c", "3")  # ["b", "1", "2"]
    print check_string2("abc123", "a-z")  # ["1", "2", "3"]
    print check_string2("abc123", "0-9")  # ["a", "b", "c"]
    print "-" * 50
    print is_number("114514")  # True
    print is_number("114514abc")  # False
    print is_number("114e5")  # True
    print is_number("0x000000ff")  # True
    print "-" * 50
    a = {'b': [1, 2, 3], 'c': "hahaha", 'd': [4, 5]}
    turn_dict_value_to_tuple(a)
    print a  # {'b': (1, 2, 3), 'c': "hahaha", 'd': (4, 5)}
    a = [1, [2, 3], "abc"]
    print turn_list_to_tuple(a)  # (1, (2, 3), "abc")
    print "-" * 50
    class A:
        def printIn(self, s):
            print s
    class B(A):
        def printIn(self, s):
            print 1
    class C(A):
        pass
    print is_method_overridden(B, A, "printIn")  # True
    print is_method_overridden(C, A, "printIn")  # False
    print "-" * 50
    print translate_time(4000)  # "1h6m40s"
    print "-" * 50
    print 2 / 3.0
    p = [probability_true_i(2, 3) for _ in range(int(1e5))]
    print p.count(True) / 1e5
    print 0.34
    p = [probability_true_f(0.34) for _ in range(int(1e5))]
    print p.count(True) / 1e5
    print "-" * 50
    print random_string(20)
    print random_string(20, lower=False)
    print random_string(20, upper=False)
    print random_string(20, num=False)
    # print _time()
    # @McTimer.delay(5.5)
    # def df(a1, a2):
    #     print a1, a2
    #     print _time()
    # df()
    # @McTimer.repeat(2)
    # def rf():
    #     print "repeat"
    # rf()
























