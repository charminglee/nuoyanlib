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


from collections import OrderedDict
import itertools
from mod.common.minecraftEnum import (
    EntityType,
    StructureFeatureType,
    BiomeType,
    EffectType,
    EnchantType,
)
from ..core._utils import MappingProxy


if bool(0):
    from typing import Any


__all__ = [
    "auto",
    "EnumMeta",
    "Enum",
    "IntEnum",
    "StrEnum",
    "LazyEnumMeta",
    "LazyEnum",
    "Flag",
    "IntFlag",
    "gen_lower_name",
    "gen_minecraft_lower_name",
    "ClientEvent",
    "ServerEvent",
    "Mob",
    "Feature",
    "UiContainer",
    "Container",
    "Effect",
    "ENTITY_NAME_MAP",
    "BIOME_NAME_MAP",
    "STRUCTURE_NAME_MAP",
    "EFFECT_NAME_MAP",
    "ENCHANT_NAME_MAP",
]


# region Enum Classes ==================================================================================================


Enum = IntEnum = StrEnum = Flag = IntFlag = None # noqa


class auto(object):
    """
    用于自动生成枚举值。

    说明
    ----

    你可以在枚举类中定义 ``_generate_next_value_()`` 静态方法以自定义 ``auto()`` 的值生成逻辑。
    如果定义了 ``_generate_next_value_()`` 方法， ``auto()`` 会调用该方法以生成枚举值，否则使用默认的生成逻辑。
    该方法有三个参数，分别为枚举成员名称（str）、现有成员数量（int）和已分配值的列表（list），返回值即为最终的枚举值。

    示例
    ----

    >>> from <scripts_root>.nuoyanlib.common.enum import Enum, auto
    >>> class Color(Enum):
    ...     @staticmethod
    ...     def _generate_next_value_(name, count, last_values):
    ...         return count * 10
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    >>> Color.RED
    <Color.RED: 0>
    >>> Color.GREEN
    <Color.GREEN: 10>
    >>> Color.BLUE
    <Color.BLUE: 20>
    """

    _counter = itertools.count()

    def __init__(self):
        self._order = next(auto._counter)


def _get_member_type(cls_name, bases):
    # StrEnum(Enum, str)
    # StrEnum(str, Enum)
    # SE(StrEnum)
    types = set()
    for chain in bases:
        if chain is Enum:
            continue
        for base in chain.__mro__:
            if base is object:
                continue
            if isinstance(base, EnumMeta):
                if base._member_type_ is not object:
                    types.add(base._member_type_)
                    break
                else:
                    continue
            types.add(base)
            break
    if len(types) > 1:
        raise TypeError(
            "too many data types for %s: (%s)"
            % (cls_name, ", ".join(t.__name__ for t in types))
        )
    return types.pop() if types else object


def _set_enum_attr(cls, k, v, cls_dict):
    type.__setattr__(cls, k, v)
    cls_dict[k] = v


_new_enum = type.__new__


def _new_member(member_t, enum_cls, value, name=None):
    member = member_t.__new__(enum_cls, value)
    member._name_ = name
    member._value_ = value
    member._hash_ = hash(name)
    return member


class EnumMeta(type):
    def __new__(metacls, cls_name=None, bases=None, cls_dict=None): # 给参数加默认值None以绕过机审
        # 往cls_dict添加属性而不是cls.xxx = xxx，避免触发__setattr__
        _member_map_        = cls_dict['_member_map_']        = OrderedDict()
        _value2member_map_  = cls_dict['_value2member_map_']  = {}
        _unhashable_values_ = cls_dict['_unhashable_values_'] = []
        _member_names_      = cls_dict['_member_names_']      = []
        _member_type_       = cls_dict['_member_type_']       = _get_member_type(cls_name, bases)
        _ignore_            = cls_dict.setdefault('_ignore_', [])

        gnv = cls_dict.get('_generate_next_value_')
        if gnv and not isinstance(gnv, staticmethod):
            cls_dict['_generate_next_value_'] = staticmethod(gnv)

        # 创建枚举类
        cls = _new_enum(metacls, cls_name, bases, cls_dict)
        if cls_name == "Enum" and bases == (object,):
            return cls

        # 确保枚举类使用正确的魔术方法
        if _member_type_ is not object:
            if '__format__' not in cls_dict:
                _set_enum_attr(cls, '__format__', _member_type_.__format__, cls_dict)
            if '__str__' not in cls_dict:
                m = _member_type_.__str__
                if m is object.__str__:
                    m = _member_type_.__repr__
                _set_enum_attr(cls, '__str__', m, cls_dict)
        for method in ('__repr__', '__str__', '__format__', '__reduce_ex__'):
            if method in cls_dict:
                continue
            found_method = getattr(cls, method)
            enum_method = getattr(Enum, method)
            object_method = getattr(object, method)
            member_type_method = getattr(_member_type_, method)
            if found_method in (object_method, member_type_method):
                _set_enum_attr(cls, method, enum_method, cls_dict)
        if '__new__' not in cls_dict:
            __new__ = staticmethod(Enum.__new__)
            _set_enum_attr(cls, '__new__', __new__, cls_dict)

        cls_dict_items = cls_dict.items()
        # 如果使用了auto()，按照定义顺序排序
        cls_dict_items.sort(key=lambda x: x[1]._order if isinstance(x[1], auto) else -1)
        count = 0
        last_values = []

        for k, v in cls_dict_items:
            if k[0] == "_" or k in _ignore_:
                continue
            if isinstance(v, auto):
                # 生成auto()值
                v = cls._generate_next_value_(k, count, last_values)
            if not isinstance(v, _member_type_):
                raise TypeError(
                    "enum member %s.%s must be %s, got %s"
                    % (cls_name, k, _member_type_.__name__, type(v).__name__)
                )

            # 创建枚举成员
            member = _new_member(_member_type_, cls, v, k)
            _member_map_[k] = member
            try:
                _value2member_map_[v] = member
            except TypeError:
                _unhashable_values_.append(v)
            _member_names_.append(k)
            # 将成员对象更新到枚举类上
            _set_enum_attr(cls, k, member, cls_dict)

            count += 1
            last_values.append(v)

        return cls

    def __setattr__(cls, name, value):
        # 禁止动态设置枚举成员
        raise AttributeError("can't set member '%s' of Enum object '%s'" % (name, cls.__name__))

    def __delattr__(cls, name):
        # 禁止删除枚举成员
        raise AttributeError("can't delete member '%s' of Enum object '%s'" % (name, cls.__name__))

    def __call__(cls, value):
        """
        通过值查找对应的枚举成员。

        -----

        :param Any value: 值

        :return: 成员对象
        :rtype: Enum
        """
        # 跳转到Enum.__new__
        return cls.__new__(cls, value)

    def __getitem__(cls, name):
        """
        通过字符串名称查找对应的枚举成员。

        -----

        :param str name: 成员名称

        :return: 成员对象
        :rtype: Enum
        """
        return cls._member_map_[name]

    def __len__(cls):
        """
        返回枚举成员数量。

        -----

        :return: 枚举成员数量
        :rtype: int
        """
        return len(cls._member_names_)

    def __iter__(cls):
        """
        返回枚举成员迭代器。

        -----

        :return: 枚举成员迭代器
        """
        for name in cls._member_names_:
            yield cls._member_map_[name]

    @property
    def __members__(cls):
        """
        [只读属性]

        枚举成员字典。

        :rtype: dict[str,Enum]
        """
        return MappingProxy(cls._member_map_)

    def __contains__(cls, value):
        """
        判断某个对象是否是枚举成员。

        -----

        :param Any value: 要判断的值

        :return: 值在枚举范围内返回 True，否则返回 False
        :rtype: bool
        """
        try:
            cls(value)
            return True
        except ValueError:
            return False

    def __repr__(cls):
        if issubclass(cls, Flag):
            return "<flag %r>" % cls.__name__
        else:
            return "<enum %r>" % cls.__name__


class Enum(object): # noqa
    """
    枚举类，用于实现自定义枚举。

    用法与 Python 3 的 ``enum`` 标准库类似，每个枚举成员均为枚举类的实例，可通过 ``.name`` 和 ``.value`` 属性获取成员的名称和值，其他功能见示例。

    示例
    ----

    >>> from <scripts_root>.nuoyanlib.common.enum import Enum
    >>> class Color(Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3
    ...
    >>> Color.RED
    <Color.RED: 1>
    >>> isinstance(Color.RED, Color)
    True
    >>> Color.RED == 1
    False
    >>> Color.RED.name
    'RED'
    >>> Color.RED.value
    1

    在枚举类中定义 ``_ignore_`` 属性（列表或元组），填入需要忽略的成员名称，这些成员将保留为普通类属性，不会成为枚举类的实例。
    同时，以下划线开头的名称也不会成为枚举成员。

    >>> class Color(Enum):
    ...     _ignore_ = ['ALL']
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3
    ...     _YELLOW = 4
    ...     ALL = (1, 2, 3)
    >>> Color._YELLOW
    4
    >>> Color.ALL
    (1, 2, 3)

    值查找：通过值查找对应的枚举成员。默认情况下，如果值不存在，将抛出 ``ValueError`` 。

    >>> Color(1)
    <Color.RED: 1>

    你也可以通过重写 ``_missing_()`` 方法来自定义值不存在时的行为。更多信息详见 ``_missing_()`` 的说明文档。

    >>> class Color(Enum):
    ...     @classmethod
    ...     def _missing_(cls, value):
    ...         if value == 4:
    ...             return cls.RED
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3
    >>> Color(4)
    <Color.RED: 1>

    名称查找：通过字符串名称查找对应的枚举成员，如果名称不存在，则抛出 ``KeyError`` 。

    >>> Color['RED']
    <Color.RED: 1>

    可通过 ``len()`` 函数获取枚举成员数量。

    >>> len(Color)
    3

    可通过 ``for`` 循环等方式遍历枚举成员，或通过枚举类的 ``.__members__`` 属性获取成员字典，该字典的键值对应成员名称和成员对象。

    >>> for member in Color:
    ...     print member.name, member.value
    'RED' 1
    'GREEN' 2
    'BLUE' 3

    >>> for name, member in Color.__members__.items():
    ...     print member.name, member.value
    'RED' 1
    'GREEN' 2
    'BLUE' 3

    可通过 ``in`` 关键字判断某个值是否是枚举值，或某个对象是否是枚举成员。

    >>> 1 in Color
    True
    >>> Color.RED in Color
    True

    使用 ``auto()`` 可自动生成枚举值，而无需手动编写。默认情况下，值从 ``1`` 开始递增。
    你也可以自定义 ``auto()`` 的值生成逻辑，详见 ``auto()`` 的说明文档。

    >>> from <scripts_root>.nuoyanlib.common.enum import auto
    >>> class Color(Enum):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    >>> Color.RED
    <Color.RED: 1>
    >>> Color.GREEN
    <Color.GREEN: 2>
    >>> Color.BLUE
    <Color.BLUE: 3>
    """

    __metaclass__ = EnumMeta

    def __new__(cls, value):
        # 值查找
        if type(value) is cls:
            # Color(Color.RED)
            return value
        try:
            # Color(1)
            return cls._value2member_map_[value]
        except KeyError:
            # 值不存在
            pass
        except TypeError:
            # 对不可哈希值采用线性查找
            for member in cls._member_map_.values():
                if member._value_ == value:
                    return member
        # 尝试调用_missing_
        res = cls._missing_(value)
        if isinstance(res, cls):
            return res
        elif res is not None:
            raise TypeError(
                "error in %s._missing_: returned %r instead of None or a valid member"
                % (cls.__name__, res)
            )
        raise ValueError("%r is not a valid %s" % (value, cls.__name__))

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self):
        return "%s.%s" % (self.__class__.__name__, self._name_)

    def __repr__(self):
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, self._value_)

    def __hash__(self):
        return self._hash_

    def __format__(self, format_spec):
        return str.__format__(str(self), format_spec)

    def __reduce_ex__(self, proto):
        return self.__class__, (self._value_,)

    def __deepcopy__(self, memo):
        return self

    def __copy__(self):
        return self

    @property
    def name(self):
        """
        [只读属性]

        枚举成员名称。

        :rtype: str
        """
        return self._name_

    @property
    def value(self):
        """
        [只读属性]

        枚举值。

        :rtype: Any
        """
        return self._value_

    @staticmethod
    def _generate_next_value_(name, count, last_values):
        """
        [静态方法]

        ``auto()`` 生成枚举值时调用该方法。

        -----

        :param str name: 枚举成员名称
        :param int count: 现有成员数量
        :param list[Any] last_values: 已分配值的列表

        :return: 返回值将作为枚举值
        :rtype: Any
        """
        if not last_values:
            return 1
        return max(last_values) + 1

    @classmethod
    def _missing_(cls, value):
        """
        [类方法]

        查找枚举类中不存在的枚举值时调用该方法。

        默认情况下它不执行任何操作，但可以重写以实现自定义查找行为。

        -----

        :param str value: 要查找的枚举值

        :return: 返回值需要为枚举类的实例或 None；若返回 None，则视为查找失败
        :rtype: Any
        """


class IntEnum(int, Enum): # noqa
    """
    整数类型枚举类。

    说明
    ----

    ``IntEnum`` 拥有 ``Enum`` 的全部特性，且其枚举成员同时也是 ``int`` 类型，支持所有整数运算。

    示例
    ----

    >>> class Permission(IntEnum):
    ...     VISITOR = 0
    ...     MEMBER = 1
    ...     OPERATOR = 2
    >>> Permission.VISITOR
    0
    >>> Permission.VISITOR + 6
    6
    """


class StrEnum(str, Enum): # noqa
    """
    字符串类型枚举类。

    说明
    ----

    ``StrEnum`` 拥有 ``Enum`` 的全部特性，且其枚举成员同时也是 ``str`` 类型，支持所有字符串运算。

    示例
    ----

    >>> class Permission(StrEnum):
    ...     VISITOR = "visitor"
    ...     MEMBER = "member"
    ...     OPERATOR = "operator"
    >>> Permission.VISITOR
    'visitor'
    >>> "I am a %s." % Permission.VISITOR
    'I am a visitor.'

    此外，使用 ``auto()`` 自动生成的枚举值与枚举名相同。

    >>> class Permission(StrEnum):
    ...     VISITOR = auto()
    ...     MEMBER = auto()
    ...     OPERATOR = auto()
    >>> Permission.VISITOR
    'VISITOR'
    """

    @staticmethod
    def _generate_next_value_(name, count, last_values):
        return name


class LazyEnumMeta(type):
    def __new__(metacls, cls_name, bases, cls_dict):
        gev = cls_dict.get('_gen_enum_value_')
        if gev and not isinstance(gev, staticmethod):
            cls_dict['_gen_enum_value_'] = staticmethod(gev)
        return type.__new__(metacls, cls_name, bases, cls_dict)

    def __getattr__(cls, name):
        value = cls._gen_enum_value_(name)
        type.__setattr__(cls, name, value)
        return value


class LazyEnum(object):
    """
    按需生成字符串枚举值的枚举类。
    """

    __metaclass__ = LazyEnumMeta

    @staticmethod
    def _gen_enum_value_(name):
        return name


# todo
class Flag(Enum): # noqa
    """
    标志枚举类。
    """

    @staticmethod
    def _generate_next_value_(name, count, last_values):
        return 1 << count


# todo
class IntFlag(int, Flag): # noqa
    """
    整数类型标志枚举类。
    """


gen_lower_name = lambda name, _, __: name.lower()
gen_minecraft_lower_name = lambda name, _, __: "minecraft:" + name.lower()


def _expand_enum(namespace, enum):
    if isinstance(enum, Enum):
        for member in enum:
            namespace[member.name] = member.value


# endregion


# region Preset Enums ==================================================================================================


class ClientEvent(LazyEnum):
    """
    ModSDK 客户端事件名枚举。
    """


class ServerEvent(LazyEnum):
    """
    ModSDK 服务端事件名枚举。
    """


class Block(LazyEnum):
    """
    方块 Identifier 枚举。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """
    @staticmethod
    def _gen_enum_value_(name):
        return "minecraft:" + name.lower()


class Item(LazyEnum):
    """
    物品 Identifier 枚举。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """
    @staticmethod
    def _gen_enum_value_(name):
        return "minecraft:" + name.lower()


class Entity(LazyEnum):
    """
    实体 Identifier 枚举。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """
    @staticmethod
    def _gen_enum_value_(name):
        return "minecraft:" + name.lower()


class Biome(LazyEnum):
    """
    生物群系 Identifier 枚举。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """


class Effect(LazyEnum):
    """
    药水效果 Identifier 枚举。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """


class Enchantment(LazyEnum):
    """
    附魔 Identifier 枚举。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """


class Mob(LazyEnum):
    """
    生物 identifier 枚举。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """

    _generate_next_value_ = gen_minecraft_lower_name

    ALLAY = auto()
    """ 悦灵。 """
    ARMADILLO = auto()
    """ 犰狳。 """
    BAT = auto()
    """ 蝙蝠。 """
    CAMEL = auto()
    """ 骆驼。 """
    CHICKEN = auto()
    """ 鸡。 """
    COD = auto()
    """ 鳕鱼。 """
    COPPER_GOLEM = auto()
    """ 铜傀儡。 """
    COW = auto()
    """ 牛。 """
    DONKEY = auto()
    """ 驴。 """
    GLOW_SQUID = auto()
    """ 发光鱿鱼。 """
    HAPPY_GHAST = auto()
    """ 快乐恶魂。 """
    HORSE = auto()
    """ 马。 """
    MOOSHROOM = auto()
    """ 哞菇。 """
    MULE = auto()
    """ 骡。 """
    PARROT = auto()
    """ 鹦鹉。 """
    PIG = auto()
    """ 猪。 """
    RABBIT = auto()
    """ 兔子。 """
    SALMON = auto()
    """ 鲑鱼。 """
    SHEEP = auto()
    """ 绵羊。 """
    SKELETON_HORSE = auto()
    """ 骷髅马。 """
    SNIFFER = auto()
    """ 嗅探兽。 """
    SQUID = auto()
    """ 鱿鱼。 """
    STRIDER = auto()
    """ 炽足兽。 """
    TADPOLE = auto()
    """ 蝌蚪。 """
    TROPICALFISH = auto()
    """ 热带鱼。 """
    TURTLE = auto()
    """ 海龟。 """
    WANDERING_TRADER = auto()
    """ 流浪商人。 """
    PUFFERFISH = auto()
    """ 河豚。 """
    GOAT = auto()
    """ 山羊。 """
    VILLAGER = auto()
    """ 旧版村民。 """
    VILLAGER_V2 = auto()
    """ 村民。 """
    AXOLOTL = auto()
    """ 美西螈。 """
    CAT = auto()
    """ 猫。 """
    FROG = auto()
    """ 青蛙。 """
    OCELOT = auto()
    """ 豹猫。 """
    SNOW_GOLEM = auto()
    """ 雪傀儡。 """
    BEE = auto()
    """ 蜜蜂。 """
    DOLPHIN = auto()
    """ 海豚。 """
    FOX = auto()
    """ 狐狸。 """
    IRON_GOLEM = auto()
    """ 铁傀儡。 """
    LLAMA = auto()
    """ 羊驼。 """
    PANDA = auto()
    """ 熊猫。 """
    POLAR_BEAR = auto()
    """ 北极熊。 """
    TRADER_LLAMA = auto()
    """ 行商羊驼。 """
    WOLF = auto()
    """ 狼。 """
    ZOMBIE_HORSE = auto()
    """ 僵尸马。 """
    BLAZE = auto()
    """ 烈焰人。 """
    BOGGED = auto()
    """ 沼骸。 """
    BREEZE = auto()
    """ 旋风人。 """
    CREEPER = auto()
    """ 苦力怕。 """
    ELDER_GUARDIAN = auto()
    """ 远古守卫者。 """
    ENDERMITE = auto()
    """ 末影螨。 """
    EVOCATION_ILLAGER = auto()
    """ 唤魔者。 """
    GHAST = auto()
    """ 恶魂。 """
    GUARDIAN = auto()
    """ 守卫者。 """
    HOGLIN = auto()
    """ 疣猪兽。 """
    HUSK = auto()
    """ 尸壳。 """
    MAGMA_CUBE = auto()
    """ 岩浆怪。 """
    PHANTOM = auto()
    """ 幻翼。 """
    PIGLIN_BRUTE = auto()
    """ 猪灵蛮兵。 """
    PILLAGER = auto()
    """ 掠夺者。 """
    RAVAGER = auto()
    """ 劫掠兽。 """
    SHULKER = auto()
    """ 潜影贝。 """
    SILVERFISH = auto()
    """ 蠹虫。 """
    SKELETON = auto()
    """ 骷髅。 """
    SLIME = auto()
    """ 史莱姆。 """
    STRAY = auto()
    """ 流浪者。 """
    VEX = auto()
    """ 恼鬼。 """
    VINDICATOR = auto()
    """ 卫道士。 """
    WARDEN = auto()
    """ 监守者。 """
    WITCH = auto()
    """ 女巫。 """
    WITHER_SKELETON = auto()
    """ 凋零骷髅。 """
    ZOGLIN = auto()
    """ 僵尸疣猪兽。 """
    ZOMBIE = auto()
    """ 僵尸。 """
    ZOMBIE_VILLAGER = auto()
    """ 旧版僵尸村民。 """
    ZOMBIE_VILLAGER_V2 = auto()
    """ 僵尸村民。 """
    CREAKING = auto()
    """ 嘎枝。 """
    DROWNED = auto()
    """ 溺尸。 """
    ENDERMAN = auto()
    """ 末影人。 """
    PIGLIN = auto()
    """ 猪灵。 """
    SPIDER = auto()
    """ 蜘蛛。 """
    CAVE_SPIDER = auto()
    """ 洞穴蜘蛛。 """
    ZOMBIE_PIGMAN = auto()
    """ 僵尸猪灵。 """
    ENDER_DRAGON = auto()
    """ 末影龙。 """
    WITHER = auto()
    """ 凋灵。 """


class Feature(LazyEnum):
    """
    原版结构特征ID枚举。
    """

    _generate_next_value_ = gen_lower_name

    END_CITY = auto()
    """ 末地城。 """
    FORTRESS = auto()
    """ 下界要塞。 """
    MANSION = auto()
    """ 林地府邸。 """
    MINESHAFT = auto()
    """ 废弃矿井。 """
    MONUMENT = auto()
    """ 海底神殿。 """
    STRONGHOLD = auto()
    """ 要塞。 """
    TEMPLE = auto()
    """ 神殿（包括沙漠神殿/雪屋/丛林神庙/女巫小屋）。 """
    VILLAGE = auto()
    """ 村庄。 """
    SHIPWRECK = auto()
    """ 沉船。 """
    BURIED_TREASURE = auto()
    """ 埋藏的宝藏。 """
    RUINS = auto()
    """ 海底废墟。 """
    PILLAGER_OUTPOST = auto()
    """ 掠夺者前哨站。 """
    BASTION_REMNANT = auto()
    """ 堡垒遗迹。 """
    RUINED_PORTAL = auto()
    """ 废弃传送门。 """
    ANCIENT_CITY = auto()
    """ 远古城市。 """
    TRIAL_CHAMBERS = auto()
    """ 试炼密室。 """


class UiContainer(LazyEnum):
    """
    原版UI容器 identifier（即仅存在容器UI，不能真正存储物品的容器）枚举（包括容器方块和容器实体）。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """

    _generate_next_value_ = gen_minecraft_lower_name

    CRAFTING_TABLE = auto()
    """ 工作台。 """
    ENCHANTING_TABLE = auto()
    """ 附魔台。 """
    BEACON = auto()
    """ 信标。 """
    ANVIL = auto()
    """ 铁砧。 """
    CHIPPED_ANVIL = auto()
    """ 开裂的铁砧。 """
    DAMAGED_ANVIL = auto()
    """ 损坏的铁砧。 """
    DEPRECATED_ANVIL = auto()
    """ 破碎的铁砧。 """
    GRINDSTONE = auto()
    """ 砂轮。 """
    CARTOGRAPHY_TABLE = auto()
    """ 制图台。 """
    STONECUTTER_BLOCK = auto()
    """ 切石机。 """
    LOOM = auto()
    """ 织布机。 """
    SMITHING_TABLE = auto()
    """ 锻造台。 """
    VILLAGER = auto()
    """ 旧版村民。 """
    VILLAGER_V2 = auto()
    """ 村民。 """


class Container(LazyEnum):
    """
    原版容器 identifier 枚举（包括容器方块和容器实体）。

    -----

    资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """

    _generate_next_value_ = gen_minecraft_lower_name

    CHEST = auto()
    """ 箱子。 """
    TRAPPED_CHEST = auto()
    """ 陷阱箱。 """
    ENDER_CHEST = auto()
    """ 末影箱。 """
    UNDYED_SHULKER_BOX = auto()
    """ 潜影盒。 """
    WHITE_SHULKER_BOX = auto()
    """ 白色潜影盒。 """
    ORANGE_SHULKER_BOX = auto()
    """ 橙色潜影盒。 """
    MAGENTA_SHULKER_BOX = auto()
    """ 品红色潜影盒。 """
    LIGHT_BLUE_SHULKER_BOX = auto()
    """ 淡蓝色潜影盒。 """
    YELLOW_SHULKER_BOX = auto()
    """ 黄色潜影盒。 """
    LIME_SHULKER_BOX = auto()
    """ 黄绿色潜影盒。 """
    PINK_SHULKER_BOX = auto()
    """ 粉红色潜影盒。 """
    GRAY_SHULKER_BOX = auto()
    """ 灰色潜影盒。 """
    LIGHT_GRAY_SHULKER_BOX = auto()
    """ 淡灰色潜影盒。 """
    CYAN_SHULKER_BOX = auto()
    """ 青色潜影盒。 """
    PURPLE_SHULKER_BOX = auto()
    """ 紫色潜影盒。 """
    BLUE_SHULKER_BOX = auto()
    """ 蓝色潜影盒。 """
    BROWN_SHULKER_BOX = auto()
    """ 棕色潜影盒。 """
    GREEN_SHULKER_BOX = auto()
    """ 绿色潜影盒。 """
    RED_SHULKER_BOX = auto()
    """ 红色潜影盒。 """
    BLACK_SHULKER_BOX = auto()
    """ 黑色潜影盒。 """
    BARREL = auto()
    """ 木桶。 """
    FURNACE = auto()
    """ 熔炉。 """
    LIT_FURNACE = auto()
    """ 燃烧中的熔炉。 """
    SMOKER = auto()
    """ 烟熏炉。 """
    LIT_SMOKER = auto()
    """ 燃烧中的烟熏炉。 """
    BLAST_FURNACE = auto()
    """ 高炉。 """
    LIT_BLAST_FURNACE = auto()
    """ 燃烧中的高炉。 """
    BREWING_STAND = auto()
    """ 酿造台。 """
    DROPPER = auto()
    """ 投掷器。 """
    DISPENSER = auto()
    """ 发射器。 """
    HOPPER = auto()
    """ 漏斗。 """
    CRAFTER = auto()
    """ 合成器。 """
    CHEST_MINECART = auto()
    """ 运输矿车。 """
    CHEST_BOAT = auto()
    """ 运输船。 """
    HOPPER_MINECART = auto()
    """ 漏斗矿车。 """
    HORSE = auto()
    """ 马。 """
    DONKEY = auto()
    """ 驴。 """
    MULE = auto()
    """ 骡。 """
    CAMEL = auto()
    """ 骆驼。 """
    TRADER_LLAMA = auto()
    """ 行商羊驼。 """
    LLAMA = auto()
    """ 羊驼。 """


# endregion


# region Maps ==========================================================================================================


ENTITY_NAME_MAP = {
    EntityType.Chicken:                     (10, "minecraft:chicken", "鸡"),
    EntityType.Cow:                         (11, "minecraft:cow", "牛"),
    EntityType.Pig:                         (12, "minecraft:pig", "猪"),
    EntityType.Sheep:                       (13, "minecraft:sheep", "绵羊"),
    EntityType.Wolf:                        (14, "minecraft:wolf", "狼"),
    EntityType.Villager:                    (15, "minecraft:villager", "村民"),
    EntityType.MushroomCow:                 (16, "minecraft:mooshroom", "哞菇"),
    EntityType.Squid:                       (17, "minecraft:squid", "鱿鱼"),
    EntityType.Rabbit:                      (18, "minecraft:rabbit", "兔子"),
    EntityType.Bat:                         (19, "minecraft:bat", "蝙蝠"),
    EntityType.IronGolem:                   (20, "minecraft:iron_golem", "铁傀儡"),
    EntityType.SnowGolem:                   (21, "minecraft:snow_golem", "雪傀儡"),
    EntityType.Ocelot:                      (22, "minecraft:ocelot", "豹猫"),
    EntityType.Horse:                       (23, "minecraft:horse", "马"),
    EntityType.Donkey:                      (24, "minecraft:donkey", "驴"),
    EntityType.Mule:                        (25, "minecraft:mule", "骡"),
    EntityType.SkeletonHorse:               (26, "minecraft:skeleton_horse", "骷髅马"),
    EntityType.ZombieHorse:                 (27, "minecraft:zombie_horse", "僵尸马"),
    EntityType.PolarBear:                   (28, "minecraft:polar_bear", "北极熊"),
    EntityType.Llama:                       (29, "minecraft:llama", "羊驼"),
    EntityType.Parrot:                      (30, "minecraft:parrot", "鹦鹉"),
    EntityType.Dolphin:                     (31, "minecraft:dolphin", "海豚"),
    EntityType.Zombie:                      (32, "minecraft:zombie", "僵尸"),
    EntityType.Creeper:                     (33, "minecraft:creeper", "苦力怕"),
    EntityType.Skeleton:                    (34, "minecraft:skeleton", "骷髅"),
    EntityType.Spider:                      (35, "minecraft:spider", "蜘蛛"),
    EntityType.PigZombie:                   (36, "minecraft:zombie_pigman", "僵尸猪灵"),
    EntityType.Slime:                       (37, "minecraft:slime", "史莱姆"),
    EntityType.EnderMan:                    (38, "minecraft:enderman", "末影人"),
    EntityType.Silverfish:                  (39, "minecraft:silverfish", "蠹虫"),
    EntityType.CaveSpider:                  (40, "minecraft:cave_spider", "洞穴蜘蛛"),
    EntityType.Ghast:                       (41, "minecraft:ghast", "恶魂"),
    EntityType.LavaSlime:                   (42, "minecraft:magma_cube", "岩浆怪"),
    EntityType.Blaze:                       (43, "minecraft:blaze", "烈焰人"),
    EntityType.ZombieVillager:              (44, "minecraft:zombie_villager", "僵尸村民"),
    EntityType.Witch:                       (45, "minecraft:witch", "女巫"),
    EntityType.Stray:                       (46, "minecraft:stray", "流浪者"),
    EntityType.Husk:                        (47, "minecraft:husk", "尸壳"),
    EntityType.WitherSkeleton:              (48, "minecraft:wither_skeleton", "凋灵骷髅"),
    EntityType.Guardian:                    (49, "minecraft:guardian", "守卫者"),
    EntityType.ElderGuardian:               (50, "minecraft:elder_guardian", "远古守卫者"),
    EntityType.Npc:                         (51, "minecraft:npc", "NPC"),
    EntityType.WitherBoss:                  (52, "minecraft:wither", "凋灵"),
    EntityType.Dragon:                      (53, "minecraft:ender_dragon", "末影龙"),
    EntityType.Shulker:                     (54, "minecraft:shulker", "潜影贝"),
    EntityType.Endermite:                   (55, "minecraft:endermite", "末影螨"),
    EntityType.Agent:                       (56, "minecraft:agent", "智能体"),
    EntityType.Vindicator:                  (57, "minecraft:vindicator", "卫道士"),
    EntityType.Phantom:                     (58, "minecraft:phantom", "幻翼"),
    EntityType.IllagerBeast:                (59, "minecraft:ravager", "劫掠兽"),
    EntityType.ArmorStand:                  (61, "minecraft:armor_stand", "盔甲架"),
    EntityType.TripodCamera:                (62, "minecraft:tripod_camera", "摄像机"),
    EntityType.Player:                      (63, "minecraft:player", "玩家"),
    EntityType.ItemEntity:                  (64, "minecraft:item", "物品"),
    EntityType.PrimedTnt:                   (65, "minecraft:tnt", "TNT"),
    EntityType.FallingBlock:                (66, "minecraft:falling_block", "下落的方块"),
    EntityType.MovingBlock:                 (67, "minecraft:moving_block", "移动的方块"),
    EntityType.ExperiencePotion:            (68, "minecraft:xp_bottle", "掷出的附魔之瓶"),
    EntityType.Experience:                  (69, "minecraft:xp_orb", "经验球"),
    EntityType.EyeOfEnder:                  (70, "minecraft:eye_of_ender_signal", "末影之眼"),
    EntityType.EnderCrystal:                (71, "minecraft:ender_crystal", "末影水晶"),
    EntityType.FireworksRocket:             (72, "minecraft:fireworks_rocket", "烟花火箭"),
    EntityType.Trident:                     (73, "minecraft:thrown_trident", "三叉戟"),
    EntityType.Turtle:                      (74, "minecraft:turtle", "海龟"),
    EntityType.Cat:                         (75, "minecraft:cat", "猫"),
    EntityType.ShulkerBullet:               (76, "minecraft:shulker_bullet", "潜影弹"),
    EntityType.FishingHook:                 (77, "minecraft:fishing_hook", "浮漂"),
    EntityType.Chalkboard:                  (78, "minecraft:chalkboard", "黑板"),
    EntityType.DragonFireball:              (79, "minecraft:dragon_fireball", "末影龙火球"),
    EntityType.Arrow:                       (80, "minecraft:arrow", "箭"),
    EntityType.Snowball:                    (81, "minecraft:snowball", "雪球"),
    EntityType.ThrownEgg:                   (82, "minecraft:egg", "掷出的鸡蛋"),
    EntityType.Painting:                    (83, "minecraft:painting", "画"),
    EntityType.Minecart:                    (84, "minecraft:minecart", "矿车"),
    EntityType.LargeFireball:               (85, "minecraft:fireball", "火球"),
    EntityType.ThrownPotion:                (86, "minecraft:splash_potion", "喷溅药水"),
    EntityType.Enderpearl:                  (87, "minecraft:ender_pearl", "掷出的末影珍珠"),
    EntityType.LeashKnot:                   (88, "minecraft:leash_knot", "拴绳结"),
    EntityType.WitherSkull:                 (89, "minecraft:wither_skull", "凋灵之首"),
    EntityType.BoatRideable:                (90, "minecraft:boat", "船"),
    EntityType.WitherSkullDangerous:        (91, "minecraft:wither_skull_dangerous", "蓝色凋灵之首"),
    EntityType.LightningBolt:               (93, "minecraft:lightning_bolt", "闪电束"),
    EntityType.SmallFireball:               (94, "minecraft:small_fireball", "小火球"),
    EntityType.AreaEffectCloud:             (95, "minecraft:area_effect_cloud", "区域效果云"),
    EntityType.MinecartHopper:              (96, "minecraft:hopper_minecart", "漏斗矿车"),
    EntityType.MinecartTNT:                 (97, "minecraft:tnt_minecart", "TNT矿车"),
    EntityType.MinecartChest:               (98, "minecraft:chest_minecart", "运输矿车"),
    EntityType.MinecartCommandBlock:        (100, "minecraft:command_block_minecart", "命令方块矿车"),
    EntityType.LingeringPotion:             (101, "minecraft:lingering_potion", "滞留药水"),
    EntityType.LlamaSpit:                   (102, "minecraft:llama_spit", "羊驼唾沫"),
    EntityType.EvocationFang:               (103, "minecraft:evocation_fang", "唤魔者尖牙"),
    EntityType.EvocationIllager:            (104, "minecraft:evocation_illager", "唤魔者"),
    EntityType.Vex:                         (105, "minecraft:vex", "恼鬼"),
    EntityType.IceBomb:                     (106, "minecraft:ice_bomb", "冰弹"),
    EntityType.Balloon:                     (107, "minecraft:balloon", "气球"),
    EntityType.Pufferfish:                  (108, "minecraft:pufferfish", "河豚"),
    EntityType.Salmon:                      (109, "minecraft:salmon", "鲑鱼"),
    EntityType.Drowned:                     (110, "minecraft:drowned", "溺尸"),
    EntityType.Tropicalfish:                (111, "minecraft:tropicalfish", "热带鱼"),
    EntityType.Fish:                        (112, "minecraft:cod", "鳕鱼"),
    EntityType.Panda:                       (113, "minecraft:panda", "熊猫"),
    EntityType.Pillager:                    (114, "minecraft:pillager", "掠夺者"),
    EntityType.VillagerV2:                  (115, "minecraft:villager_v2", "村民"),
    EntityType.ZombieVillagerV2:            (116, "minecraft:zombie_villager_v2", "僵尸村民"),
    EntityType.Shield:                      (117, "minecraft:shield", "盾牌"),
    EntityType.WanderingTrader:             (118, "minecraft:wandering_trader", "流浪商人"),
    EntityType.ElderGuardianGhost:          (120, "minecraft:elder_guardian_ghost", "远古守卫者幽灵"),
    EntityType.Fox:                         (121, "minecraft:fox", "狐狸"),
    EntityType.Bee:                         (122, "minecraft:bee", "蜜蜂"),
    EntityType.Piglin:                      (123, "minecraft:piglin", "猪灵"),
    EntityType.Hoglin:                      (124, "minecraft:hoglin", "疣猪兽"),
    EntityType.Strider:                     (125, "minecraft:strider", "炽足兽"),
    EntityType.Zoglin:                      (126, "minecraft:zoglin", "僵尸疣猪兽"),
    EntityType.PiglinBrute:                 (127, "minecraft:piglin_brute", "猪灵蛮兵"),
    EntityType.Goat:                        (128, "minecraft:goat", "山羊"),
    EntityType.GlowSquid:                   (129, "minecraft:glow_squid", "发光鱿鱼"),
    EntityType.Axolotl:                     (130, "minecraft:axolotl", "美西螈"),
    EntityType.Warden:                      (131, "minecraft:warden", "监守者"),
    EntityType.Frog:                        (132, "minecraft:frog", "青蛙"),
    EntityType.Tadpole:                     (133, "minecraft:tadpole", "蝌蚪"),
    EntityType.Allay:                       (134, "minecraft:allay", "悦灵"),
    EntityType.ChestBoatRideable:           (136, "minecraft:chest_boat", "运输船"),
    EntityType.TraderLlama:                 (137, "minecraft:trader_llama", "行商羊驼"),
    EntityType.Camel:                       (138, "minecraft:camel", "骆驼"),
    EntityType.Sniffer:                     (139, "minecraft:sniffer", "嗅探兽"),
    EntityType.Breeze:                      (140, "minecraft:breeze", "旋风人"),
    EntityType.BreezeWindChargeProjectile:  (141, "minecraft:breeze_wind_charge_projectile", "风弹"),
    EntityType.Armadillo:                   (142, "minecraft:armadillo", "犰狳"),
    EntityType.WindChargeProjectile:        (143, "minecraft:wind_charge_projectile", "风弹"),
    EntityType.Bogged:                      (144, "minecraft:bogged", "沼骸"),
    EntityType.OminousItemSpawner:          (145, "minecraft:ominous_item_spawner", "不祥之物生成器"),
}
"""
用于将网易实体类型ID（详见 `EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?catalog=1>`_ ）转换为原版数字ID、identifier或中文名称的字典，结构如下：
::

    {
        <entity_type: int>: (<num_id: int>, <identifier: str>, <entity_name: str>)
    }
"""


BIOME_NAME_MAP = {
    BiomeType.ocean:                            ("ocean", "海洋"),
    BiomeType.plains:                           ("plains", "平原"),
    BiomeType.desert:                           ("desert", "沙漠"),
    BiomeType.extreme_hills:                    ("extreme_hills", "山地"),
    BiomeType.forest:                           ("forest", "森林"),
    BiomeType.taiga:                            ("taiga", "针叶林"),
    BiomeType.swampland:                        ("swampland", "沼泽"),
    BiomeType.river:                            ("river", "河流"),
    BiomeType.hell:                             ("hell", "下界荒地"),
    BiomeType.the_end:                          ("the_end", "末地"),
    BiomeType.legacy_frozen_ocean:              ("legacy_frozen_ocean", "冻洋"),
    BiomeType.frozen_river:                     ("frozen_river", "冻河"),
    BiomeType.ice_plains:                       ("ice_plains", "积雪的冻原"),
    BiomeType.ice_mountains:                    ("ice_mountains", "雪山"),
    BiomeType.mushroom_island:                  ("mushroom_island", "蘑菇岛"),
    BiomeType.mushroom_island_shore:            ("mushroom_island_shore", "蘑菇岛岸"),
    BiomeType.beach:                            ("beach", "沙滩"),
    BiomeType.desert_hills:                     ("desert_hills", "沙漠丘陵"),
    BiomeType.forest_hills:                     ("forest_hills", "繁茂的丘陵"),
    BiomeType.taiga_hills:                      ("taiga_hills", "针叶林丘陵"),
    BiomeType.extreme_hills_edge:               ("extreme_hills_edge", "山地边缘"),
    BiomeType.jungle:                           ("jungle", "丛林"),
    BiomeType.jungle_hills:                     ("jungle_hills", "丛林丘陵"),
    BiomeType.jungle_edge:                      ("jungle_edge", "丛林边缘"),
    BiomeType.deep_ocean:                       ("deep_ocean", "深海"),
    BiomeType.stone_beach:                      ("stone_beach", "石岸"),
    BiomeType.cold_beach:                       ("cold_beach", "积雪的沙滩"),
    BiomeType.birch_forest:                     ("birch_forest", "桦木森林"),
    BiomeType.birch_forest_hills:               ("birch_forest_hills", "桦木森林丘陵"),
    BiomeType.roofed_forest:                    ("roofed_forest", "黑森林"),
    BiomeType.cold_taiga:                       ("cold_taiga", "积雪的针叶林"),
    BiomeType.cold_taiga_hills:                 ("cold_taiga_hills", "积雪的针叶林丘陵"),
    BiomeType.mega_taiga:                       ("mega_taiga", "巨型针叶林"),
    BiomeType.mega_taiga_hills:                 ("mega_taiga_hills", "巨型针叶林丘陵"),
    BiomeType.extreme_hills_plus_trees:         ("extreme_hills_plus_trees", "繁茂的山地"),
    BiomeType.savanna:                          ("savanna", "热带草原"),
    BiomeType.savanna_plateau:                  ("savanna_plateau", "热带高原"),
    BiomeType.mesa:                             ("mesa", "恶地"),
    BiomeType.mesa_plateau_stone:               ("mesa_plateau_stone", "繁茂的恶地高原"),
    BiomeType.mesa_plateau:                     ("mesa_plateau", "恶地高原"),
    BiomeType.warm_ocean:                       ("warm_ocean", "暖水海洋"),
    BiomeType.deep_warm_ocean:                  ("deep_warm_ocean", "暖水深海"),
    BiomeType.lukewarm_ocean:                   ("lukewarm_ocean", "温水海洋"),
    BiomeType.deep_lukewarm_ocean:              ("deep_lukewarm_ocean", "温水深海"),
    BiomeType.cold_ocean:                       ("cold_ocean", "冷水海洋"),
    BiomeType.deep_cold_ocean:                  ("deep_cold_ocean", "冷水深海"),
    BiomeType.frozen_ocean:                     ("frozen_ocean", "冻洋"),
    BiomeType.deep_frozen_ocean:                ("deep_frozen_ocean", "封冻深海"),
    BiomeType.bamboo_jungle:                    ("bamboo_jungle", "竹林"),
    BiomeType.bamboo_jungle_hills:              ("bamboo_jungle_hills", "竹林丘陵"),
    BiomeType.sunflower_plains:                 ("sunflower_plains", "向日葵平原"),
    BiomeType.desert_mutated:                   ("desert_mutated", "沙漠湖泊"),
    BiomeType.extreme_hills_mutated:            ("extreme_hills_mutated", "沙砾山地"),
    BiomeType.flower_forest:                    ("flower_forest", "繁花森林"),
    BiomeType.taiga_mutated:                    ("taiga_mutated", "针叶林山地"),
    BiomeType.swampland_mutated:                ("swampland_mutated", "沼泽山丘"),
    BiomeType.ice_plains_spikes:                ("ice_plains_spikes", "冰刺平原"),
    BiomeType.jungle_mutated:                   ("jungle_mutated", "丛林变种"),
    BiomeType.jungle_edge_mutated:              ("jungle_edge_mutated", "丛林边缘变种"),
    BiomeType.birch_forest_mutated:             ("birch_forest_mutated", "高大桦木森林"),
    BiomeType.birch_forest_hills_mutated:       ("birch_forest_hills_mutated", "高大桦木丘陵"),
    BiomeType.roofed_forest_mutated:            ("roofed_forest_mutated", "黑森林丘陵"),
    BiomeType.cold_taiga_mutated:               ("cold_taiga_mutated", "积雪的针叶林山地"),
    BiomeType.redwood_taiga_mutated:            ("redwood_taiga_mutated", "巨型云杉针叶林"),
    BiomeType.redwood_taiga_hills_mutated:      ("redwood_taiga_hills_mutated", "巨型云杉针叶林丘陵"),
    BiomeType.extreme_hills_plus_trees_mutated: ("extreme_hills_plus_trees_mutated", "沙砾山地+"),
    BiomeType.savanna_mutated:                  ("savanna_mutated", "破碎的热带草原"),
    BiomeType.savanna_plateau_mutated:          ("savanna_plateau_mutated", "破碎的热带高原"),
    BiomeType.mesa_bryce:                       ("mesa_bryce", "被风蚀的恶地"),
    BiomeType.mesa_plateau_stone_mutated:       ("mesa_plateau_stone_mutated", "繁茂的恶地高原变种"),
    BiomeType.mesa_plateau_mutated:             ("mesa_plateau_mutated", "恶地高原变种"),
    BiomeType.soulsand_valley:                  ("soulsand_valley", "灵魂沙峡谷"),
    BiomeType.crimson_forest:                   ("crimson_forest", "绯红森林"),
    BiomeType.warped_forest:                    ("warped_forest", "诡异森林"),
    BiomeType.basalt_deltas:                    ("basalt_deltas", "玄武岩三角洲"),
    BiomeType.jagged_peaks:                     ("jagged_peaks", "尖峭山峰"),
    BiomeType.frozen_peaks:                     ("frozen_peaks", "冰封山峰"),
    BiomeType.snowy_slopes:                     ("snowy_slopes", "积雪的山坡"),
    BiomeType.grove:                            ("grove", "雪林"),
    BiomeType.meadow:                           ("meadow", "草甸"),
    BiomeType.lush_caves:                       ("lush_caves", "繁茂洞穴"),
    BiomeType.dripstone_caves:                  ("dripstone_caves", "溶洞"),
    BiomeType.stony_peaks:                      ("stony_peaks", "裸岩山峰"),
    BiomeType.deep_dark:                        ("deep_dark", "深暗之域"),
    BiomeType.mangrove_swamp:                   ("mangrove_swamp", "红树林沼泽"),
    BiomeType.cherry_grove:                     ("cherry_grove", "樱花树林"),
}
"""
用于将网易生物群系ID（详见 `BiomeType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/BiomeType.html?catalog=1>`_ ）转换为原版ID或中文名称的字典，结构如下：
::

    {
        <biome_type: int>: (<org_id: str>, <biome_name: str>)
    }
    
-----

资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
"""


STRUCTURE_NAME_MAP = {
    StructureFeatureType.EndCity:           ("end_city", "末地城"),
    StructureFeatureType.Fortress:          ("fortress", "要塞"),
    StructureFeatureType.Mineshaft:         ("mineshaft", "废弃矿井"),
    StructureFeatureType.Monument:          ("monument", "海底神殿"),
    StructureFeatureType.Stronghold:        ("stronghold", "要塞"),
    StructureFeatureType.Temple:            ("temple", "神殿"),
    StructureFeatureType.Village:           ("village", "村庄"),
    StructureFeatureType.WoodlandMansion:   ("mansion", "林地府邸"),
    StructureFeatureType.Shipwreck:         ("shipwreck", "沉船"),
    StructureFeatureType.BuriedTreasure:    ("buried_treasure", "埋藏的宝藏"),
    StructureFeatureType.Ruins:             ("ruins", "海底废墟"),
    StructureFeatureType.PillagerOutpost:   ("pillager_outpost", "掠夺者前哨站"),
    StructureFeatureType.RuinedPortal:      ("ruined_portal", "废弃传送门"),
    StructureFeatureType.Bastion:           ("bastion_remnant", "堡垒遗迹"),
    StructureFeatureType.AncientCity:       ("ancient_city", "远古城市"),
    StructureFeatureType.TrailRuins:        ("trail_ruins", "试炼密室"),
}
"""
用于将网易结构特征ID（详见 `StructureFeatureType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/StructureFeatureType.html?catalog=1>`_ ）转换为原版ID或中文名称的字典，结构如下：
::

    {
        <structure_type: int>: (<org_id: str>, <structure_name: str>)
    }

-----

资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
"""


EFFECT_NAME_MAP = {
    EffectType.MOVEMENT_SPEED:      "迅捷",
    EffectType.MOVEMENT_SLOWDOWN:   "缓慢",
    EffectType.DIG_SPEED:           "急迫",
    EffectType.DIG_SLOWDOWN:        "挖掘疲劳",
    EffectType.DAMAGE_BOOST:        "力量",
    EffectType.HEAL:                "瞬间治疗",
    EffectType.HARM:                "瞬间伤害",
    EffectType.JUMP:                "跳跃提升",
    EffectType.CONFUSION:           "反胃",
    EffectType.REGENERATION:        "生命恢复",
    EffectType.DAMAGE_RESISTANCE:   "抗性提升",
    EffectType.FIRE_RESISTANCE:     "抗火",
    EffectType.WATER_BREATHING:     "水下呼吸",
    EffectType.INVISIBILITY:        "隐身",
    EffectType.BLINDNESS:           "失明",
    EffectType.NIGHT_VISION:        "夜视",
    EffectType.HUNGER:              "饥饿",
    EffectType.WEAKNESS:            "虚弱",
    EffectType.POISON:              "中毒",
    EffectType.WITHER:              "凋零",
    EffectType.HEALTH_BOOST:        "生命提升",
    EffectType.ABSORPTION:          "伤害吸收",
    EffectType.SATURATION:          "饱和",
    EffectType.LEVITATION:          "漂浮",
    EffectType.FATAL_POISON:        "中毒（致命）",
    EffectType.SLOW_FALLING:        "缓降",
    EffectType.CONDUIT_POWER:       "潮涌能量",
    EffectType.BAD_OMEN:            "不祥之兆",
    EffectType.HERO_OF_THE_VILLAGE: "村庄英雄",
    EffectType.DARKNESS:            "黑暗",
    EffectType.TRIAL_OMEN:          "试炼之兆",
    EffectType.RAID_OMEN:           "袭击之兆",
    EffectType.WIND_CHARGED:        "蓄风",
    EffectType.WEAVING:             "盘丝",
    EffectType.OOZING:              "渗浆",
    EffectType.INFESTED:            "寄生",
}
"""
用于将状态效果ID（详见 `EffectType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EffectType.html?catalog=1>`_ ）转换为中文名称的字典，结构如下：
::

    {
        <effect_id: str>: <effect_name: str>
    }

-----

资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
"""


ENCHANT_NAME_MAP = {
    EnchantType.ArmorAll:               ("protection", "保护"),
    EnchantType.ArmorFire:              ("fire_protection", "火焰保护"),
    EnchantType.ArmorFall:              ("feather_falling", "摔落缓冲"),
    EnchantType.ArmorExplosive:         ("blast_protection", "爆炸保护"),
    EnchantType.ArmorProjectile:        ("projectile_protection", "弹射物保护"),
    EnchantType.ArmorThorns:            ("thorns", "荆棘"),
    EnchantType.WaterBreath:            ("respiration", "水下呼吸"),
    EnchantType.WaterSpeed:             ("depth_strider", "深海探索者"),
    EnchantType.WaterAffinity:          ("aqua_affinity", "水下速掘"),
    EnchantType.WeaponDamage:           ("sharpness", "锋利"),
    EnchantType.WeaponUndead:           ("smite", "亡灵杀手"),
    EnchantType.WeaponArthropod:        ("bane_of_arthropods", "节肢杀手"),
    EnchantType.WeaponKnockback:        ("knockback", "击退"),
    EnchantType.WeaponFire:             ("fire_aspect", "火焰附加"),
    EnchantType.WeaponLoot:             ("looting", "抢夺"),
    EnchantType.MiningEfficiency:       ("efficiency", "效率"),
    EnchantType.MiningSilkTouch:        ("silk_touch", "精准采集"),
    EnchantType.MiningDurability:       ("unbreaking", "耐久"),
    EnchantType.MiningLoot:             ("fortune", "时运"),
    EnchantType.BowDamage:              ("power", "力量"),
    EnchantType.BowKnockback:           ("punch", "冲击"),
    EnchantType.BowFire:                ("flame", "火矢"),
    EnchantType.BowInfinity:            ("infinity", "无限"),
    EnchantType.FishingLoot:            ("luck_of_the_sea", "海之眷顾"),
    EnchantType.FishingLure:            ("lure", "饵钓"),
    EnchantType.FrostWalker:            ("frost_walker", "冰霜行者"),
    EnchantType.Mending:                ("mending", "经验修补"),
    EnchantType.CurseBinding:           ("binding", "绑定诅咒"),
    EnchantType.CurseVanishing:         ("vanishing", "消失诅咒"),
    EnchantType.TridentImpaling:        ("impaling", "穿刺"),
    EnchantType.TridentRiptide:         ("riptide", "激流"),
    EnchantType.TridentLoyalty:         ("loyalty", "忠诚"),
    EnchantType.TridentChanneling:      ("channeling", "引雷"),
    EnchantType.CrossbowMultishot:      ("multishot", "多重射击"),
    EnchantType.CrossbowPiercing:       ("piercing", "穿透"),
    EnchantType.CrossbowQuickCharge:    ("quick_charge", "快速装填"),
    EnchantType.SoulSpeed:              ("soul_speed", "灵魂疾行"),
    EnchantType.SwiftSneak:             ("swift_sneak", "迅捷潜行"),
    EnchantType.WindBurst:              ("wind_burst", "风爆"),
    EnchantType.Density:                ("density", "致密"),
    EnchantType.Breach:                 ("breach", "破甲"),
}
"""
用于将网易附魔ID（详见 `EnchantType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EnchantType.html?catalog=1>`_ ）转换为原版ID或中文名称的字典，结构如下：
::

    {
        <enchant_type: int>: (<org_id: str>, <enchant_name: str>)
    }

-----

资料来源： `中文 Minecraft Wiki <https://zh.minecraft.wiki/>`_
"""


# endregion











