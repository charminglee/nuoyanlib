# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-8
#  ⠀
#  ================================================


from nuoyanlib.common.enum import Enum, IntEnum, StrEnum, Mob, auto
from nuoyanlib.core._utils import assert_error


assert Enum._member_type_ is object
assert IntEnum._member_type_ is int
assert StrEnum._member_type_ is str


def test_enum(_IntEnum=IntEnum, _StrEnum=StrEnum):
    class E(Enum):
        @classmethod
        def _missing_(cls, value):
            if value == 33:
                return cls.A
            if value == 44:
                return 44

        A = 0
        B = "1"
        C = [2]

    assert isinstance(E.A, E)
    assert E.A.name == "A"
    assert E.A.value == 0

    def f():
        E.A = 1
    assert_error(f, exc=AttributeError)
    def f():
        del E.A
    assert_error(f, exc=AttributeError)

    assert E(0) is E.A
    assert E("1") is E.B
    assert E([2]) is E.C
    assert E['A'] is E.A
    assert len(E) == 3
    assert E(33) is E.A
    assert_error(E, (44,), exc=TypeError)

    for member in E:
        assert isinstance(member, E)
        assert E(member.value) is E[member.name]
    for name, member in E.__members__.items():
        assert isinstance(member, E)
        assert E(member) is E[name]

    assert repr(E) == "<enum 'E'>"
    assert repr(E.A) == "<E.A: 0>"
    assert repr(E.B) == "<E.B: '1'>"
    assert repr(E.C) == "<E.C: [2]>"
    assert str(E.A) == "E.A"
    assert str(E.B) == "E.B"
    assert str(E.C) == "E.C"

    assert 0 in E
    assert "1" in E
    assert [2] in E
    assert E.A in E
    assert 4 not in E

    class SE(_StrEnum):
        A = "a"
        B = "b"
        C = "c"

    assert isinstance(SE.A, SE)
    assert SE.A.name == "A"
    assert SE.A.value == "a"
    assert SE.A == "a"
    assert SE.B == "b"
    assert SE.C == "c"
    assert SE("a") is SE.A
    assert SE['A'] is SE.A # noqa
    assert repr(SE) == "<enum 'SE'>"
    assert repr(SE.A) == "<SE.A: 'a'>"
    assert str(SE.A) == "a"
    assert "a" in SE
    assert "d" not in SE
    assert SE.A in SE
    assert "a" + SE.A == "aa"
    assert "a%s" % SE.A == "aa"

    class IE(_IntEnum):
        A = 0
        B = 1
        C = 2

    assert isinstance(IE.A, IE)
    assert IE.A.name == "A"
    assert IE.A.value == 0
    assert IE.A == 0
    assert IE.B == 1
    assert IE.C == 2
    assert IE(0) is IE.A
    assert IE['A'] is IE.A
    assert repr(IE) == "<enum 'IE'>"
    assert repr(IE.A) == "<IE.A: 0>"
    assert str(IE.A) == "0"
    assert 0 in IE
    assert 4 not in IE
    assert IE.A in IE
    assert 1 + IE.C == 3
    assert "%d" % IE.A == "0"

    def f():
        class SE(_StrEnum):
            A = 0
    assert_error(f, exc=TypeError)
    def f():
        class IE(_IntEnum):
            A = "0"
    assert_error(f, exc=TypeError)

    class ASE(_StrEnum):
        C = auto()
        B = auto()
        A = auto()
    assert ASE._member_names_ == ["C", "B", "A"]
    assert ASE.C == "C"
    assert ASE.B == "B"

    class AIE(_IntEnum):
        C = auto()
        A = auto()
        B = auto()
    assert AIE._member_names_ == ["C", "A", "B"]
    assert AIE.C == 1
    assert AIE.B == 3


test_enum()


class IntEnum2(Enum, int):
    pass
class StrEnum2(Enum, str):
    @staticmethod
    def _generate_next_value_(name, count, last_values): # noqa
        return name


test_enum(IntEnum2, StrEnum2) # noqa


def f():
    class IntEnum2(Enum, int, str):
        pass
assert_error(f, exc=TypeError)


assert Mob.WITHER == "minecraft:wither"
