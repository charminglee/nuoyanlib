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


from nuoyanlib.common.enum import (
    Entity,
    Enum,
    IntEnum,
    StrEnum,
    Flag,
    IntFlag,
    ClientEvent,
    ServerEvent,
    auto,
)
from nuoyanlib.core._utils import assert_error


assert Enum._member_type_ is object
assert IntEnum._member_type_ is int
assert StrEnum._member_type_ is str
assert Flag._member_type_ is object
assert IntFlag._member_type_ is int


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


def test_flag(_Flag=Flag, _IntFlag=IntFlag):
    class P(_Flag):
        READ = auto()
        WRITE = auto()
        EXECUTE = auto()

    assert P._member_names_ == ["READ", "WRITE", "EXECUTE"]
    assert P.READ.value == 1
    assert P.WRITE.value == 2
    assert P.EXECUTE.value == 4

    rw = P.READ | P.WRITE
    assert isinstance(rw, P)
    assert rw.name == "READ|WRITE"
    assert rw.value == 3
    assert (P.WRITE | P.READ) is rw
    assert (P.READ | P.READ) is P.READ
    assert P(3) is rw
    assert P(1) is P.READ
    assert P(1L) is P.READ # noqa
    assert P(P.READ) is P.READ
    assert len(P) == 3
    assert list(P) == [P.READ, P.WRITE, P.EXECUTE]

    assert repr(P) == "<flag 'P'>"
    assert repr(P.READ) == "<P.READ: 1>"
    assert repr(rw) == "<P.READ|WRITE: 3>"
    assert str(P.READ) == "P.READ"
    assert str(rw) == "P.READ|WRITE"
    assert format(rw) == "P.READ|WRITE"

    empty = P.READ & P.WRITE
    assert empty.value == 0
    assert empty.name is None
    assert repr(empty) == "<P: 0>"
    assert str(empty) == "P(0)"
    assert not empty
    assert bool(P.READ)
    assert len(empty) == 0
    assert P(0) is empty
    assert (P.READ ^ P.READ) is empty

    assert list(rw) == [P.READ, P.WRITE]
    assert len(rw) == 2
    assert P.READ in rw
    assert P.WRITE in rw
    assert P.EXECUTE not in rw
    assert 3 in rw
    assert 4 not in rw
    assert (rw & P.WRITE) is P.WRITE
    assert (rw ^ P.WRITE) is P.READ
    assert (rw & P.EXECUTE) is empty
    assert (~P.READ) is (P.WRITE | P.EXECUTE)
    assert ~(~P.READ) is P.READ
    assert (~rw) is P.EXECUTE

    def f():
        P(8)
    assert_error(f, exc=ValueError)
    def f():
        P(-1)
    assert_error(f, exc=ValueError)
    def f():
        P.READ | 1
    assert_error(f, exc=TypeError)
    def f():
        1 | P.READ
    assert_error(f, exc=TypeError)

    class IP(_IntFlag):
        READ = auto()
        WRITE = auto()
        EXECUTE = auto()

    assert isinstance(IP.READ, int)
    assert IP.READ == 1
    assert IP.WRITE == 2
    assert IP.EXECUTE == 4
    assert 1 == IP.READ
    assert "%d" % IP.READ == "1"

    irw = IP.READ | IP.WRITE
    assert isinstance(irw, IP)
    assert irw == 3
    assert irw.name == "READ|WRITE"
    assert repr(irw) == "<IP.READ|WRITE: 3>"
    assert str(irw) == "3"
    assert format(IP.READ) == "1"
    assert IP(3) is irw
    assert (IP.WRITE | IP.READ) is irw
    assert (irw & 1) is IP.READ
    assert (irw | 4) is (IP.READ | IP.WRITE | IP.EXECUTE)
    assert 2 | IP.READ is IP.WRITE | IP.READ
    assert irw + 1 == 4
    assert not IP(0)
    assert bool(IP.READ)
    assert list(irw) == [IP.READ, IP.WRITE]
    assert IP.READ in irw
    assert 2 in irw
    assert 4 not in irw
    assert (irw & IP.EXECUTE) == 0
    assert ~(~IP.READ) is IP.READ

    def f():
        IP(8)
    assert_error(f, exc=ValueError)
    def f():
        IP(-1)
    assert_error(f, exc=ValueError)

    # auto() 取比现有最大值更高一位的 2 的幂，避免与显式定义的值冲突
    class Mix(_Flag):
        A = 1
        B = 4
        C = auto()
    assert Mix.C.value == 8
    assert repr(Mix.A | Mix.B) == "<Mix.A|B: 5>"

    # 类体中定义的组合值成为该值的正式成员
    class Alias(_Flag):
        R = 1
        W = 2
        X = 4
        RW = R | W
    assert Alias(3) is Alias.RW
    assert (Alias.R | Alias.W) is Alias.RW
    assert list(Alias.RW) == [Alias.R, Alias.W]
    assert Alias.RW in (Alias.R | Alias.W | Alias.X)
    assert 3 in Alias
    assert 8 not in Alias


test_flag()


class Flag2(Flag):
    pass
class IntFlag2(Flag2, int):
    pass


test_flag(Flag2, IntFlag2) # noqa


assert Entity.AGENT == "minecraft:agent"
assert ClientEvent.OnKeyPressInGame == "OnKeyPressInGame"
assert ServerEvent.ServerItemUseOnEvent == "ServerItemUseOnEvent"
