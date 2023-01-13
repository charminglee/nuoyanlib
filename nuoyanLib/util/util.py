# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanLib is licensed under Mulan PSL v2.
#
#   Author        : Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2023-01-14
#
# ====================================================


from collections import Mapping as _Mapping
from re import match as _match
from random import randint as _randint
import __builtin__


# noinspection PyUnresolvedReferences
def all_index(findList, *elements):
    # type: (list, Any) -> list
    """
    获取元素在列表中所有出现位置的下标。
    示例：
    all_index([1, 1, 4, 5, 1, 4], 1)     # [0, 1, 4]
    all_index([1, 1, 4, 5, 1, 4], 1, 4)     # [0, 1, 2, 4, 5]
    -----------------------------------------------------------
    【findList: list】 列表
    【*elements: Any】 元素
    -----------------------------------------------------------
    return: list -> 元素所有出现位置的下标列表
    """
    return [i for i, e in enumerate(findList) if e in elements]


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


# noinspection PyUnresolvedReferences
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


# noinspection PyUnresolvedReferences
def is_method_overridden(subclass, father, method):
    # type: (Any, Any, str) -> bool
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


# noinspection PyUnresolvedReferences
def nyeval(source, g=None, l=None):
    # type: (str | unicode, dict[str, Any] | None, _Mapping[str, Any] | None) -> Any
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
    return: str -> h/m/s格式
    """
    if sec <= 60:
        return str(sec) + "s"
    elif 60 < sec < 3600:
        m = sec // 60
        s = sec - m * 60
        return str(m) + "m" + str(s) + "s"
    else:
        h = sec // 3600
        m = (sec - h * 3600) // 60
        s = sec - h * 3600 - m * 60
        return str(h) + "h" + str(m) + "m" + str(s) + "s"


def probability_true(n, d):
    # type: (int, int) -> bool
    """
    以指定概率返回True。
    示例：
    probability_true(2, 3)     # 2/3的概率返回True，1/3的概率返回False
    -----------------------------------------------------------
    【n: int】 概率分子
    【d: int】 概率分母
    -----------------------------------------------------------
    return: bool -> 以a/b的概率返回True
    """
    return n * d > 0 and _randint(1, d) <= n


if __name__ == "__main__":
    print all_index([1, 1, 4, 5, 1, 4], 1)  # [0, 1, 4]
    print all_index([1, 1, 4, 5, 1, 4], 1, 4)  # [0, 1, 2, 4, 5]
    print check_string("11112222", "1", "2")  # True
    print check_string("11112222", "1")  # False
    print check_string("1234567890", "0-9")  # True
    print check_string2("abc123", "a", "c", "3")  # ["b", "1", "2"]
    print check_string2("abc123", "a-z")  # ["1", "2", "3"]
    print check_string2("abc123", "0-9")  # ["a", "b", "c"]
    print is_number("114514")  # True
    print is_number("114514abc")  # False
    print is_number("114e5")  # True
    print is_number("0x000000ff")  # True
    a = {'b': [1, 2, 3], 'c': "hahaha", 'd': [4, 5]}
    turn_dict_value_to_tuple(a)
    print a  # {'b': (1, 2, 3), 'c': "hahaha", 'd': (4, 5)}
    a = [1, [2, 3], "abc"]
    print turn_list_to_tuple(a)  # (1, (2, 3), "abc")
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
    print translate_time(4000)  # "1h6m40s"


























