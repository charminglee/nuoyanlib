# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-12
#  ⠀
#  ================================================


import threading


from nuoyanlib.core._utils import (
    DefaultLocal,
    hook_method,
    Singleton,
    ArgsSingleton,
    cached_property,
    write_only_property,
    kwargs_defaults,
    assert_error,
    dualmethod,
)


class E(object):
    @dualmethod
    def foo(self):
        return self
e = E()
assert e.foo() is e
assert E.foo() is E


dl = DefaultLocal(list)
def f():
    dl.lst.append(1)
    assert dl.lst == [1]
f()
t = threading.Thread(target=f)
t.start()
t.join()


class A(object):
    def __init__(self):
        self.lst = []
    def test(self, a):
        return a
    def hook(self, a):
        self.lst.append(a)
ins = A()
hook_method(ins, "test", ins.hook)
assert ins.test(1) == 1
assert ins.test(2) == 2
assert ins.lst == [1, 2]
def hook(a):
    ins.lst.append(a)
hook_method(ins, "test", hook)
assert ins.test(3) == 3
assert ins.lst == [1, 2, 3, 3]


# class B(object):
#     def value(self, a):
#         return a + 1
#     def fail(self):
#         raise ValueError("expected")
# b = B()
# l = []
# hook_method(b, "fail", after_hook=lambda: l.append(1))
# b.fail()
# assert l == [1]


n = [0]
class A(Singleton):
    def __init__(self):
        n[0] += 1
assert A() is A()
assert n[0] == 1
nn = [0]
class B(A):
    def __init__(self):
        A.__init__(self)
        nn[0] += 1
assert B() is not A()
assert B() is B()
assert n[0] == 2
assert nn[0] == 1


n = [0]
class C(ArgsSingleton):
    def __init__(self, a, b=""):
        n[0] += 1
c1 = C(1, b="a")
c2 = C(1, b="a")
c3 = C(1, b="b")
c4 = C(2, b="a")
assert c1 is c2
assert c1 is not c3
assert c1 is not c4
assert C(2, b="a") is c4
assert n[0] == 3


n = [0]
class D(ArgsSingleton):
    def __init__(self, a, b=None):
        n[0] += 1
d1 = D([1, 2], b={'xxx': [0]})
d2 = D([1, 2], b={'xxx': [0]})
d3 = D([1, 3], b={'xxx': [0]})
d4 = D([1, 2], b={'xxx': [1]})
assert d1 is d2
assert d1 is not d3
assert d1 is not d4
assert D([1, 2], b={'xxx': [1]}) is d4
assert n[0] == 3


a = [0]
class T(object):
    @cached_property
    def prop1(self):
        a[0] += 1
        return "a" + "b"
    @cached_property
    def prop2(self):
        a[0] += 1
        return "c" + "d"
t = T()
assert t.prop1 == "ab"
assert t.prop1 == "ab"
assert t.prop2 == "cd"
assert t.prop2 == "cd"
assert a[0] == 2


values = []
class WriteOnlyPropertyTest(object):
    value = write_only_property()

    @value.setter
    def value(self, val):
        values.append(val)


write_only = WriteOnlyPropertyTest()
write_only.value = 1
assert values == [1]
assert_error(lambda: write_only.value, exc=AttributeError)
assert_error(lambda: delattr(write_only, "value"), exc=AttributeError)


values = []
class WriteOnlyPropertyTest2(object):
    @write_only_property
    def value(self, val):
        values.append(val)


write_only = WriteOnlyPropertyTest2()
write_only.value = 1
assert values == [1]
assert_error(lambda: write_only.value, exc=AttributeError)
assert_error(lambda: delattr(write_only, "value"), exc=AttributeError)


@kwargs_defaults(c=3, d=4)
def func(a, b=2, **kwargs):
    return a, b, kwargs['c'], kwargs['d']
assert func(1, 2) == (1, 2, 3, 4)
assert func(1, 2, c=6) == (1, 2, 6, 4)
assert func(1, b=5, c=6) == (1, 5, 6, 4)
assert func(1, c=6) == (1, 2, 6, 4)
assert func.__doc__ == "func(a, b=2, *, c=3, d=4)"
assert_error(func, (1,), {'e': 1}, TypeError)
