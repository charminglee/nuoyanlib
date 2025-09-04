# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-04
|
| ==============================================
"""


from mod.common.minecraftEnum import (
    EntityType,
    StructureFeatureType,
    BiomeType,
    EffectType,
    EnchantType,
)


__all__ = [
    "Enum",
    "GridCallbackType",
    "ComboBoxCallbackType",
    "ButtonCallbackType",
    "ControlType",
    "FriendlyMob",
    "HostileMob",
    "Mob",
    "Feature",
    "UiContainer",
    "Container",
    "PositiveEffect",
    "NegativeEffect",
    "NeutralEffect",
    "ENTITY_NAME_MAP",
    "BIOME_NAME_MAP",
    "STRUCTURE_NAME_MAP",
    "EFFECT_NAME_MAP",
    "ENCHANT_NAME_MAP",
]


class _EnumMeta(type):
    def __new__(metacls, name, bases, dct, restrict_type=None):
        dct['_enum_flag'] = 0
        cls = type.__new__(metacls, name, bases, dct) # type: type[Enum]
        members = {}
        if name != "Enum":
            # 遍历当前Enum成员
            for k, v in dct.items():
                if k.startswith("_"):
                    continue
                if isinstance(v, Enum.auto):
                    member = cls._gen_auto_value(k) # NOQA
                elif cls._restrict_type:
                    if type(v) is not cls._restrict_type:
                        raise TypeError(
                            "member of '%s' must be '%s', not '%s'"
                            % (name, cls._restrict_type.__name__, type(v).__name__)
                        )
                    member = v
                else:
                    member = cls(k, v) # type: Enum
                members[k] = member
                setattr(cls, k, member)
            # 继承父Enum成员
            for base in bases:
                if isinstance(base, _EnumMeta):
                    members.update(base.__members__)
        else:
            cls._restrict_type = restrict_type
        cls.__members__ = members
        cls._enum_flag = 1
        return cls

    def __setattr__(cls, name, value):
        # 禁止动态设置枚举值
        if getattr(cls, '_enum_flag', 0) == 1:
            raise AttributeError("can't set member '%s' in '%s'" % (name, cls.__name__))
        type.__setattr__(cls, name, value)

    def __delattr__(cls, name):
        # 禁止删除枚举值
        raise AttributeError("can't delete member '%s' in '%s'" % (name, cls.__name__))

    def __contains__(cls, member):
        # 支持in
        for v in cls.__members__.values():
            if cls._restrict_type:
                if v == member:
                    return True
            elif v.value == member:
                return True
        return False

    def __len__(cls):
        # 支持len()
        return len(cls.__members__)

    def __iter__(cls):
        # 支持遍历
        return iter(cls.__members__.items())

    def __getitem__(cls, item):
        # 支持Enum[type]/Enum['xxx']
        if cls is Enum:
            dct = dict(Enum.__dict__)
            del dct['__dict__']
            del dct['__weakref__']
            del dct['__members__']
            del dct['_enum_flag']
            new_cls = _EnumMeta.__new__(_EnumMeta, "Enum", (object,), dct, item)
            return new_cls
        else:
            return cls.__members__[item]

    def _gen_auto_value(cls, name=None):
        t = getattr(cls, '_restrict_type', None)
        if t is str:
            val = name
        elif t is int:
            val = getattr(cls, '_last_auto_value', -1) + 1
            cls._last_auto_value = val
        else:
            raise TypeError("unsupported type '%s'" % t.__name__)
        return val


class Enum(object):
    """
    | 枚举类型，用于实现自定义枚举值。
    | 支持以下功能：
    - ``len()``: 获取枚举值数量
    - 通过for循环等方式进行遍历
    - 通过 ``in`` 关键字判断某个值是否在枚举范围内
    - 可通过 ``Enum[type]`` 的方式定义特定类型的枚举值，如 ``Enum[int]`` 定义int类型枚举值
    - 可通过 ``MyEnum.xxx`` 或 ``MyEnum['xxx']`` 的方式获取指定枚举值
    | 注意事项：
    - 枚举值是无序的（类似于字典），因此遍历顺序与编写顺序无关
    - 不支持动态插入或删除枚举值
    - 枚举名不能以下划线开头
    """

    __metaclass__ = _EnumMeta

    class auto(object):
        pass

    def __init__(self, name, value):
        self.__name = name
        self.__value = value
        self.__hash = hash(name)

    def __repr__(self):
        return "<%s.%s: %s>" % (self.__class__.__name__, self.__name, repr(self.__value))

    def __hash__(self):
        return self.__hash

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value


def __test__():
    class E(Enum[str]):
        a = Enum.auto()
        b = Enum.auto()
        c = Enum.auto()
    class EE(Enum[str]):
        aa = Enum.auto()
        bb = Enum.auto()
        cc = Enum.auto()
    class T(E, EE):
        d = Enum.auto()
        e = Enum.auto()
    assert E.a == "a"
    assert T.a == "a"
    assert T.aa == "aa"
    assert T.d == "d"

    class E1(Enum):
        A = 1
        B = 2
        C = 3
    class E2(E1):
        X = 7
        Y = 8
        Z = 9
    assert sorted(E2.__members__.keys()) == ["A", "B", "C", "X", "Y", "Z"]
    assert 7 in E2
    assert 0 not in E2
    assert len(E2) == 6
    assert isinstance(E2.X, E2)
    assert E2.A.name == "A"
    assert E2.A.value == 1
    a = {E2.A, E2.X}
    assert E2.A in a
    assert E2.X in a

    class E3(Enum[str]):
        Q = "114514"
    assert E3.Q == "114514"
    from .._core._utils import assert_error
    def f():
        E3.Q = 123
    assert_error(f, (), AttributeError)
    def f():
        del E3.Q
    assert_error(f, (), AttributeError)

    class E4(Enum[int]):
        a = Enum.auto()
        b = Enum.auto()
        c = Enum.auto()
    assert sorted(E4.__members__.values()) == [0, 1, 2]


class GridCallbackType(Enum[str]):
    """
    网格回调函数类型枚举。
    """

    UPDATE = Enum.auto()
    """
    网格元素刷新时触发。
    """

    LOADED = Enum.auto()
    """
    网格初次加载完成时触发。
    """


class ComboBoxCallbackType(Enum[str]):
    """
    下拉框回调函数类型枚举。
    """

    OPEN = Enum.auto()
    """
    展开下拉框。
    """

    CLOSE = Enum.auto()
    """
    关闭下拉框。
    """

    SELECT = Enum.auto()
    """
    选中下拉框内容。
    """


class ButtonCallbackType(Enum[str]):
    """
    按钮回调函数类型枚举。
    """

    UP = Enum.auto()
    """
    触控在按钮范围内抬起。
    """

    DOWN = Enum.auto()
    """
    按钮按下。
    """

    CANCEL = Enum.auto()
    """
    触控在按钮范围外抬起。
    """

    MOVE = Enum.auto()
    """
    按下后触控移动。
    """

    MOVE_IN = Enum.auto()
    """
    按下按钮后触控进入按钮。
    """

    MOVE_OUT = Enum.auto()
    """
    按下按钮后触控退出按钮。
    """

    DOUBLE_CLICK = Enum.auto()
    """
    双击按钮。
    """

    LONG_CLICK = Enum.auto()
    """
    长按按钮。
    """

    HOVER_IN = Enum.auto()
    """
    鼠标进入按钮。
    """

    HOVER_OUT = Enum.auto()
    """
    鼠标退出按钮。
    """

    SCREEN_EXIT = Enum.auto()
    """
    按钮所在画布退出，且鼠标仍未抬起时触发。
    """


class ControlType(Enum[str]):
    """
    | UI控件类型枚举。
    """

    BASE_CONTROL = "BaseControl"
    """
    | 通用控件。
    """

    BUTTON = "Button"
    """
    | 按钮。
    """

    IMAGE = "Image"
    """
    | 图片。
    """

    LABEL = "Label"
    """
    | 文本。
    """

    PANEL = "Panel"
    """
    | 面板。
    """

    INPUT_PANEL = "InputPanel"
    """
    | 输入面板。
    """

    STACK_PANEL = "StackPanel"
    """
    | 栈面板。
    """

    EDIT_BOX = "TextEditBox"
    """
    | 文本编辑框。
    """

    PAPER_DOLL = "PaperDoll"
    """
    | 纸娃娃。
    """

    NETEASE_PAPER_DOLL = "NeteasePaperDoll"
    """
    | 网易纸娃娃。
    """

    ITEM_RENDERER = "ItemRenderer"
    """
    | 物品渲染器。
    """

    GRADIENT_RENDERER = "GradientRenderer"
    """
    | 渐变渲染器。
    """

    SCROLL_VIEW = "ScrollView"
    """
    | 滚动视图。
    """

    GRID = "Grid"
    """
    | 网格。
    """

    PROGRESS_BAR = "ProgressBar"
    """
    | 进度条。
    """

    TOGGLE = "SwitchToggle"
    """
    | 开关。
    """

    SLIDER = "Slider"
    """
    | 滑动条。
    """

    SELECTION_WHEEL = "SelectionWheel"
    """
    | 轮盘。
    """

    COMBO_BOX = "NeteaseComboBox"
    """
    | 下拉框。
    """

    MINI_MAP = "MiniMap"
    """
    | 小地图。
    """

    _NOT_SPECIAL = (BASE_CONTROL, PANEL, PAPER_DOLL, GRADIENT_RENDERER)


class FriendlyMob(Enum[str]):
    """
    | 友好生物identifier枚举。

    -----

    | 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """

    ALLAY = "minecraft:allay"
    """
    | 悦灵。
    """

    ARMADILLO = "minecraft:armadillo"
    """
    | 犰狳。
    """

    BAT = "minecraft:bat"
    """
    | 蝙蝠。
    """

    CAMEL = "minecraft:camel"
    """
    | 骆驼。
    """

    CHICKEN = "minecraft:chicken"
    """
    | 鸡。
    """

    COD = "minecraft:cod"
    """
    | 鳕鱼。
    """

    COPPER_GOLEM = "minecraft:copper_golem"
    """
    | 铜傀儡。
    """

    COW = "minecraft:cow"
    """
    | 牛。
    """

    DONKEY = "minecraft:donkey"
    """
    | 驴。
    """

    GLOW_SQUID = "minecraft:glow_squid"
    """
    | 发光鱿鱼。
    """

    HAPPY_GHAST = "minecraft:happy_ghast"
    """
    | 快乐恶魂。
    """

    HORSE = "minecraft:horse"
    """
    | 马。
    """

    MOOSHROOM = "minecraft:mooshroom"
    """
    | 哞菇。
    """

    MULE = "minecraft:mule"
    """
    | 骡。
    """

    PARROT = "minecraft:parrot"
    """
    | 鹦鹉。
    """

    PIG = "minecraft:pig"
    """
    | 猪。
    """

    RABBIT = "minecraft:rabbit"
    """
    | 兔子。
    """

    SALMON = "minecraft:salmon"
    """
    | 鲑鱼。
    """

    SHEEP = "minecraft:sheep"
    """
    | 绵羊。
    """

    SKELETON_HORSE = "minecraft:skeleton_horse"
    """
    | 骷髅马。
    """

    SNIFFER = "minecraft:sniffer"
    """
    | 嗅探兽。
    """

    SQUID = "minecraft:squid"
    """
    | 鱿鱼。
    """

    STRIDER = "minecraft:strider"
    """
    | 炽足兽。
    """

    TADPOLE = "minecraft:tadpole"
    """
    | 蝌蚪。
    """

    TROPICAL_FISH = "minecraft:tropicalfish"
    """
    | 热带鱼。
    """

    TURTLE = "minecraft:turtle"
    """
    | 海龟。
    """

    WANDERING_TRADER = "minecraft:wandering_trader"
    """
    | 流浪商人。
    """

    PUFFERFISH = "minecraft:pufferfish"
    """
    | 河豚。
    """

    GOAT = "minecraft:goat"
    """
    | 山羊。
    """

    VILLAGER = "minecraft:villager"
    """
    | 旧版村民。
    """

    VILLAGER_V2 = "minecraft:villager_v2"
    """
    | 村民。
    """

    AXOLOTL = "minecraft:axolotl"
    """
    | 美西螈。
    """

    CAT = "minecraft:cat"
    """
    | 猫。
    """

    FROG = "minecraft:frog"
    """
    | 青蛙。
    """

    OCELOT = "minecraft:ocelot"
    """
    | 豹猫。
    """

    SNOW_GOLEM = "minecraft:snow_golem"
    """
    | 雪傀儡。
    """

    BEE = "minecraft:bee"
    """
    | 蜜蜂。
    """

    DOLPHIN = "minecraft:dolphin"
    """
    | 海豚。
    """

    FOX = "minecraft:fox"
    """
    | 狐狸。
    """

    IRON_GOLEM = "minecraft:iron_golem"
    """
    | 铁傀儡。
    """

    LLAMA = "minecraft:llama"
    """
    | 羊驼。
    """

    PANDA = "minecraft:panda"
    """
    | 熊猫。
    """

    POLAR_BEAR = "minecraft:polar_bear"
    """
    | 北极熊。
    """

    TRADER_LLAMA = "minecraft:trader_llama"
    """
    | 行商羊驼。
    """

    WOLF = "minecraft:wolf"
    """
    | 狼。
    """

    ZOMBIE_HORSE = "minecraft:zombie_horse"
    """
    | 僵尸马。
    """


class HostileMob(Enum[str]):
    """
    | 敌对生物identifier枚举。

    -----

    | 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """

    BLAZE = "minecraft:blaze"
    """
    | 烈焰人。
    """

    BOGGED = "minecraft:bogged"
    """
    | 沼骸。
    """

    BREEZE = "minecraft:breeze"
    """
    | 旋风人。
    """

    CREEPER = "minecraft:creeper"
    """
    | 苦力怕。
    """

    ELDER_GUARDIAN = "minecraft:elder_guardian"
    """
    | 远古守卫者。
    """

    ENDERMITE = "minecraft:endermite"
    """
    | 末影螨。
    """

    EVOCATION_ILLAGER = "minecraft:evocation_illager"
    """
    | 唤魔者。
    """

    GHAST = "minecraft:ghast"
    """
    | 恶魂。
    """

    GUARDIAN = "minecraft:guardian"
    """
    | 守卫者。
    """

    HOGLIN = "minecraft:hoglin"
    """
    | 疣猪兽。
    """

    HUSK = "minecraft:husk"
    """
    | 尸壳。
    """

    MAGMA_CUBE = "minecraft:magma_cube"
    """
    | 岩浆怪。
    """

    PHANTOM = "minecraft:phantom"
    """
    | 幻翼。
    """

    PIGLIN_BRUTE = "minecraft:piglin_brute"
    """
    | 猪灵蛮兵。
    """

    PILLAGER = "minecraft:pillager"
    """
    | 掠夺者。
    """

    RAVAGER = "minecraft:ravager"
    """
    | 劫掠兽。
    """

    SHULKER = "minecraft:shulker"
    """
    | 潜影贝。
    """

    SILVERFISH = "minecraft:silverfish"
    """
    | 蠹虫。
    """

    SKELETON = "minecraft:skeleton"
    """
    | 骷髅。
    """

    SLIME = "minecraft:slime"
    """
    | 史莱姆。
    """

    STRAY = "minecraft:stray"
    """
    | 流浪者。
    """

    VEX = "minecraft:vex"
    """
    | 恼鬼。
    """

    VINDICATOR = "minecraft:vindicator"
    """
    | 卫道士。
    """

    WARDEN = "minecraft:warden"
    """
    | 监守者。
    """

    WITCH = "minecraft:witch"
    """
    | 女巫。
    """

    WITHER_SKELETON = "minecraft:wither_skeleton"
    """
    | 凋零骷髅。
    """

    ZOGLIN = "minecraft:zoglin"
    """
    | 僵尸疣猪兽。
    """

    ZOMBIE = "minecraft:zombie"
    """
    | 僵尸。
    """

    ZOMBIE_VILLAGER = "minecraft:zombie_villager"
    """
    | 旧版僵尸村民。
    """

    ZOMBIE_VILLAGER_V2 = "minecraft:zombie_villager_v2"
    """
    | 僵尸村民。
    """

    CREAKING = "minecraft:creaking"
    """
    | 嘎枝。
    """

    DROWNED = "minecraft:drowned"
    """
    | 溺尸。
    """

    ENDERMAN = "minecraft:enderman"
    """
    | 末影人。
    """

    PIGLIN = "minecraft:piglin"
    """
    | 猪灵。
    """

    SPIDER = "minecraft:spider"
    """
    | 蜘蛛。
    """

    CAVE_SPIDER = "minecraft:cave_spider"
    """
    | 洞穴蜘蛛。
    """

    ZOMBIE_PIGMAN = "minecraft:zombie_pigman"
    """
    | 僵尸猪灵。
    """

    ENDER_DRAGON = "minecraft:ender_dragon"
    """
    | 末影龙。
    """

    WITHER = "minecraft:wither"
    """
    | 凋灵。
    """


class Mob(FriendlyMob, HostileMob):
    """
    | 生物identifier枚举。
    """


class Feature(Enum[str]):
    """
    | 原版结构特征枚举，值为结构特征ID（字符串）。
    """

    END_CITY = "end_city"
    """
    | 末地城。
    """

    FORTRESS = "fortress"
    """
    | 下界要塞。
    """

    MANSION = "mansion"
    """
    | 林地府邸。
    """

    MINESHAFT = "mineshaft"
    """
    | 废弃矿井。
    """

    MONUMENT = "monument"
    """
    | 海底神殿。
    """

    STRONGHOLD = "stronghold"
    """
    | 要塞。
    """

    TEMPLE = "temple"
    """
    | 神殿（包括沙漠神殿/雪屋/丛林神庙/女巫小屋）。
    """

    VILLAGE = "village"
    """
    | 村庄。
    """

    SHIPWRECK = "shipwreck"
    """
    | 沉船。
    """

    BURIED_TREASURE = "buried_treasure"
    """
    | 埋藏的宝藏。
    """

    RUINS = "ruins"
    """
    | 海底废墟。
    """

    PILLAGER_OUTPOST = "pillager_outpost"
    """
    | 掠夺者前哨站。
    """

    BASTION_REMNANT = "bastion_remnant"
    """
    | 堡垒遗迹。
    """

    RUINED_PORTAL = "ruined_portal"
    """
    | 废弃传送门。
    """

    ANCIENT_CITY = "ancient_city"
    """
    | 远古城市。
    """

    TRIAL_CHAMBERS = "trial_chambers"
    """
    | 试炼密室。
    """


class UiContainer(Enum[str]):
    """
    | 原版UI容器identifier（即仅存在容器UI，不能真正存储物品的容器）枚举（包括容器方块和容器实体）。

    -----

    | 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """

    CRAFTING_TABLE = "minecraft:crafting_table"
    """
    | 工作台。
    """

    ENCHANTING_TABLE = "minecraft:enchanting_table"
    """
    | 附魔台。
    """

    BEACON = "minecraft:beacon"
    """
    | 信标。
    """

    ANVIL = "minecraft:anvil"
    """
    | 铁砧。
    """

    CHIPPED_ANVIL = "minecraft:chipped_anvil"
    """
    | 开裂的铁砧。
    """

    DAMAGED_ANVIL = "minecraft:damaged_anvil"
    """
    | 损坏的铁砧。
    """

    DEPRECATED_ANVIL = "minecraft:deprecated_anvil"
    """
    | 破碎的铁砧。
    """

    GRINDSTONE = "minecraft:grindstone"
    """
    | 砂轮。
    """

    CARTOGRAPHY_TABLE = "minecraft:cartography_table"
    """
    | 制图台。
    """

    STONECUTTER_BLOCK = "minecraft:stonecutter_block"
    """
    | 切石机。
    """

    LOOM = "minecraft:loom"
    """
    | 织布机。
    """

    SMITHING_TABLE = "minecraft:smithing_table"
    """
    | 锻造台。
    """

    VILLAGER = "minecraft:villager"
    """
    | 旧版村民。
    """

    VILLAGER_V2 = "minecraft:villager_v2"
    """
    | 村民。
    """


class Container(Enum[str]):
    """
    | 原版容器identifier枚举（包括容器方块和容器实体）。

    -----

    | 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
    """

    CHEST = "minecraft:chest"
    """
    | 箱子。
    """

    TRAPPED_CHEST = "minecraft:trapped_chest"
    """
    | 陷阱箱。
    """

    CHEST = "minecraft:"
    """
    | 箱子。
    """

    ENDER_CHEST = "minecraft:ender_chest"
    """
    | 末影箱。
    """

    UNDYED_SHULKER_BOX = "minecraft:undyed_shulker_box"
    """
    | 潜影盒。
    """

    WHITE_SHULKER_BOX = "minecraft:white_shulker_box"
    """
    | 白色潜影盒。
    """

    ORANGE_SHULKER_BOX = "minecraft:orange_shulker_box"
    """
    | 橙色潜影盒。
    """

    MAGENTA_SHULKER_BOX = "minecraft:magenta_shulker_box"
    """
    | 品红色潜影盒。
    """

    LIGHT_BLUE_SHULKER_BOX = "minecraft:light_blue_shulker_box"
    """
    | 淡蓝色潜影盒。
    """

    YELLOW_SHULKER_BOX = "minecraft:yellow_shulker_box"
    """
    | 黄色潜影盒。
    """

    LIME_SHULKER_BOX = "minecraft:lime_shulker_box"
    """
    | 黄绿色潜影盒。
    """

    PINK_SHULKER_BOX = "minecraft:pink_shulker_box"
    """
    | 粉红色潜影盒。
    """

    GRAY_SHULKER_BOX = "minecraft:gray_shulker_box"
    """
    | 灰色潜影盒。
    """

    LIGHT_GRAY_SHULKER_BOX = "minecraft:light_gray_shulker_box"
    """
    | 淡灰色潜影盒。
    """

    CYAN_SHULKER_BOX = "minecraft:cyan_shulker_box"
    """
    | 青色潜影盒。
    """

    PURPLE_SHULKER_BOX = "minecraft:purple_shulker_box"
    """
    | 紫色潜影盒。
    """

    BLUE_SHULKER_BOX = "minecraft:blue_shulker_box"
    """
    | 蓝色潜影盒。
    """

    BROWN_SHULKER_BOX = "minecraft:brown_shulker_box"
    """
    | 棕色潜影盒。
    """

    GREEN_SHULKER_BOX = "minecraft:green_shulker_box"
    """
    | 绿色潜影盒。
    """

    RED_SHULKER_BOX = "minecraft:red_shulker_box"
    """
    | 红色潜影盒。
    """

    BLACK_SHULKER_BOX = "minecraft:black_shulker_box"
    """
    | 黑色潜影盒。
    """

    BARREL = "minecraft:barrel"
    """
    | 木桶。
    """

    FURNACE = "minecraft:furnace"
    """
    | 熔炉。
    """

    LIT_FURNACE = "minecraft:lit_furnace"
    """
    | 燃烧中的熔炉。
    """

    SMOKER = "minecraft:smoker"
    """
    | 烟熏炉。
    """

    LIT_SMOKER = "minecraft:lit_smoker"
    """
    | 燃烧中的烟熏炉。
    """

    BLAST_FURNACE = "minecraft:blast_furnace"
    """
    | 高炉。
    """

    LIT_BLAST_FURNACE = "minecraft:lit_blast_furnace"
    """
    | 燃烧中的高炉。
    """

    BREWING_STAND = "minecraft:brewing_stand"
    """
    | 酿造台。
    """

    DROPPER = "minecraft:dropper"
    """
    | 投掷器。
    """

    DISPENSER = "minecraft:dispenser"
    """
    | 发射器。
    """

    HOPPER = "minecraft:hopper"
    """
    | 漏斗。
    """

    CRAFTER = "minecraft:crafter"
    """
    | 合成器。
    """

    CHEST_MINECART = "minecraft:chest_minecart"
    """
    | 运输矿车。
    """

    CHEST_BOAT = "minecraft:chest_boat"
    """
    | 运输船。
    """

    HOPPER_MINECART = "minecraft:hopper_minecart"
    """
    | 漏斗矿车。
    """

    HORSE = "minecraft:horse"
    """
    | 马。
    """

    DONKEY = "minecraft:donkey"
    """
    | 驴。
    """

    MULE = "minecraft:mule"
    """
    | 骡。
    """

    CAMEL = "minecraft:camel"
    """
    | 骆驼。
    """

    TRADER_LLAMA = "minecraft:trader_llama"
    """
    | 行商羊驼。
    """

    LLAMA = "minecraft:llama"
    """
    | 羊驼。
    """


class PositiveEffect(Enum[str]):
    """
    | 正面状态效果枚举。
    """

    SPEED = EffectType.MOVEMENT_SPEED
    """
    | 迅捷。
    """

    HASTE = EffectType.DIG_SPEED
    """
    | 急迫。
    """

    STRENGTH = EffectType.DAMAGE_BOOST
    """
    | 力量。
    """

    INSTANT_HEALTH = EffectType.HEAL
    """
    | 瞬间治疗。
    """

    JUMP_BOOST = EffectType.JUMP
    """
    | 跳跃提升。
    """

    REGENERATION = EffectType.REGENERATION
    """
    | 生命恢复。
    """

    RESISTANCE = EffectType.DAMAGE_RESISTANCE
    """
    | 抗性提升。
    """

    FIRE_RESISTANCE = EffectType.FIRE_RESISTANCE
    """
    | 抗火。
    """

    WATER_BREATHING = EffectType.WATER_BREATHING
    """
    | 水下呼吸。
    """

    INVISIBILITY = EffectType.INVISIBILITY
    """
    | 隐身。
    """

    NIGHT_VISION = EffectType.NIGHT_VISION
    """
    | 夜视。
    """

    HEALTH_BOOST = EffectType.HEALTH_BOOST
    """
    | 生命提升。
    """

    ABSORPTION = EffectType.ABSORPTION
    """
    | 伤害吸收。
    """

    SATURATION = EffectType.SATURATION
    """
    | 饱和。
    """

    SLOW_FALLING = EffectType.SLOW_FALLING
    """
    | 缓降。
    """

    VILLAGE_HERO = EffectType.HERO_OF_THE_VILLAGE
    """
    | 村庄英雄。
    """


class NegativeEffect(Enum[str]):
    """
    | 负面状态效果枚举。
    """

    SLOWDOWN = EffectType.MOVEMENT_SLOWDOWN
    """
    | 缓慢。
    """

    MINING_FATIGUE = EffectType.DIG_SLOWDOWN
    """
    | 挖掘疲劳。
    """

    INSTANT_DAMAGE = EffectType.HARM
    """
    | 瞬间伤害。
    """

    NAUSEA = EffectType.CONFUSION
    """
    | 反胃。
    """

    BLINDNESS = EffectType.BLINDNESS
    """
    | 失明。
    """

    HUNGER = EffectType.HUNGER
    """
    | 饥饿。
    """

    WEAKNESS = EffectType.WEAKNESS
    """
    | 虚弱。
    """

    POISON = EffectType.POISON
    """
    | 中毒。
    """

    WITHER = EffectType.WITHER
    """
    | 凋零。
    """

    LEVITATION = EffectType.LEVITATION
    """
    | 飘浮。
    """

    FATAL_POISON = EffectType.FATAL_POISON
    """
    | 中毒（致命）。
    """

    DARKNESS = EffectType.DARKNESS
    """
    | 黑暗。
    """

    WIND_CHARGED = EffectType.WIND_CHARGED
    """
    | 蓄风。
    """

    WEAVING = EffectType.WEAVING
    """
    | 盘丝。
    """

    OOZING = EffectType.OOZING
    """
    | 渗浆。
    """

    INFESTED = EffectType.INFESTED
    """
    | 寄生。
    """


class NeutralEffect(Enum[str]):
    """
    | 中性状态效果枚举。
    """

    BAD_OMEN = EffectType.BAD_OMEN
    """
    | 不祥之兆。
    """

    TRIAL_OMEN = EffectType.TRIAL_OMEN
    """
    | 试炼之兆。
    """

    RAID_OMEN = EffectType.RAID_OMEN
    """
    | 袭击之兆。
    """


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
| 用于将网易实体类型ID（详见 `EntityType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EntityType.html?catalog=1>`_ ）转换为原版数字ID、identifier或中文名称的字典，结构如下：
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
| 用于将网易生物群系ID（详见 `BiomeType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/BiomeType.html?catalog=1>`_ ）转换为原版ID或中文名称的字典，结构如下：
::

    {
        <biome_type: int>: (<orig_id: str>, <biome_name: str>)
    }
    
-----

| 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
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
| 用于将网易结构特征ID（详见 `StructureFeatureType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/StructureFeatureType.html?catalog=1>`_ ）转换为原版ID或中文名称的字典，结构如下：
::

    {
        <structure_type: int>: (<orig_id: str>, <structure_name: str>)
    }

-----

| 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
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
| 用于将状态效果ID（详见 `EffectType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EffectType.html?catalog=1>`_ ）转换为中文名称的字典，结构如下：
::

    {
        <effect_id: str>: <effect_name: str>
    }

-----

| 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
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
| 用于将网易附魔ID（详见 `EnchantType <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%9E%9A%E4%B8%BE%E5%80%BC/EnchantType.html?catalog=1>`_ ）转换为原版ID或中文名称的字典，结构如下：
::

    {
        <enchant_type: int>: (<orig_id: str>, <enchant_name: str>)
    }

-----

| 资料来源： `中文Minecraft Wiki <https://zh.minecraft.wiki/>`_
"""













