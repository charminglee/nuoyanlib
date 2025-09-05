# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-05
|
| ==============================================
"""


from typing import Dict, Tuple, Any, Optional, Iterator, Union, overload, Type
from _typeshed import Self
from .._core._types._typing import STuple


class _EnumMeta(type):
    __enum_flag__: int
    __members__: Dict[str, Any]
    _restrict_type: Optional[type]
    def __new__(
        metacls: Type[Self],
        name: str,
        bases: Tuple[type, ...],
        dct: Dict[str, Any],
        restrict_type: Optional[type] = None,
    ) -> Self: ...
    def __setattr__(cls, name: str, value: Any) -> None: ...
    def __delattr__(cls, name: str) -> None: ...
    def __contains__(cls, member: Any) -> bool: ...
    def __len__(cls) -> int: ...
    def __iter__(cls: Type[Self]) -> Iterator[Self]: ...
    @overload
    def __getitem__(cls, item: type) -> Type[Enum]: ...
    @overload
    def __getitem__(cls, item: str) -> Any: ...
    @staticmethod
    def _gen_cls(restrict_type: type) -> Type[Enum]: ...
    def _gen_auto_value(cls, name: Optional[str] = None) -> Union[str, int]: ...


class Enum(metaclass=_EnumMeta):
    __name: str
    __value: Any
    __hash: int
    class auto(object):
        pass
    def __init__(self: ..., name: str, value: Any) -> None: ...
    def __repr__(self) -> str: ...
    def __hash__(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> Any: ...
    @classmethod
    def __class_getitem__(cls, item: type) -> Type[Enum]: ...


class GridCallbackType(Enum[str]):
    UPDATE: str
    LOADED: str


class ComboBoxCallbackType(Enum[str]):
    OPEN: str
    CLOSE: str
    SELECT: str


class ButtonCallbackType(Enum[str]):
    UP: str
    DOWN: str
    CANCEL: str
    MOVE: str
    MOVE_IN: str
    MOVE_OUT: str
    DOUBLE_CLICK: str
    LONG_CLICK: str
    HOVER_IN: str
    HOVER_OUT: str
    SCREEN_EXIT: str


class ControlType(Enum[str]):
    BASE_CONTROL: str
    BUTTON: str
    IMAGE: str
    LABEL: str
    PANEL: str
    INPUT_PANEL: str
    STACK_PANEL: str
    EDIT_BOX: str
    PAPER_DOLL: str
    NETEASE_PAPER_DOLL: str
    ITEM_RENDERER: str
    GRADIENT_RENDERER: str
    SCROLL_VIEW: str
    GRID: str
    PROGRESS_BAR: str
    TOGGLE: str
    SLIDER: str
    SELECTION_WHEEL: str
    COMBO_BOX: str
    MINI_MAP: str
    _NOT_SPECIAL: STuple


class FriendlyMob(Enum[str]):
    ALLAY: str
    ARMADILLO: str
    BAT: str
    CAMEL: str
    CHICKEN: str
    COD: str
    COPPER_GOLEM: str
    COW: str
    DONKEY: str
    GLOW_SQUID: str
    HAPPY_GHAST: str
    HORSE: str
    MOOSHROOM: str
    MULE: str
    PARROT: str
    PIG: str
    RABBIT: str
    SALMON: str
    SHEEP: str
    SKELETON_HORSE: str
    SNIFFER: str
    SQUID: str
    STRIDER: str
    TADPOLE: str
    TROPICAL_FISH: str
    TURTLE: str
    WANDERING_TRADER: str
    PUFFERFISH: str
    GOAT: str
    VILLAGER: str
    VILLAGER_V2: str
    AXOLOTL: str
    CAT: str
    FROG: str
    OCELOT: str
    SNOW_GOLEM: str
    BEE: str
    DOLPHIN: str
    FOX: str
    IRON_GOLEM: str
    LLAMA: str
    PANDA: str
    POLAR_BEAR: str
    TRADER_LLAMA: str
    WOLF: str
    ZOMBIE_HORSE: str


class HostileMob(Enum[str]):
    BLAZE: str
    BOGGED: str
    BREEZE: str
    CREEPER: str
    ELDER_GUARDIAN: str
    ENDERMITE: str
    EVOCATION_ILLAGER: str
    GHAST: str
    GUARDIAN: str
    HOGLIN: str
    HUSK: str
    MAGMA_CUBE: str
    PHANTOM: str
    PIGLIN_BRUTE: str
    PILLAGER: str
    RAVAGER: str
    SHULKER: str
    SILVERFISH: str
    SKELETON: str
    SLIME: str
    STRAY: str
    VEX: str
    VINDICATOR: str
    WARDEN: str
    WITCH: str
    WITHER_SKELETON: str
    ZOGLIN: str
    ZOMBIE: str
    ZOMBIE_VILLAGER: str
    ZOMBIE_VILLAGER_V2: str
    CREAKING: str
    DROWNED: str
    ENDERMAN: str
    PIGLIN: str
    SPIDER: str
    CAVE_SPIDER: str
    ZOMBIE_PIGMAN: str
    ENDER_DRAGON: str
    WITHER: str


class Mob(FriendlyMob, HostileMob):
    pass


class Feature(Enum[str]):
    END_CITY: str
    FORTRESS: str
    MANSION: str
    MINESHAFT: str
    MISSINGNO: str
    MONUMENT: str
    STRONGHOLD: str
    TEMPLE: str
    VILLAGE: str
    SHIPWRECK: str
    BURIED_TREASURE: str
    RUINS: str
    PILLAGER_OUTPOST: str
    BASTION_REMNANT: str
    RUINED_PORTAL: str
    TRIAL_CHAMBERS: str


class UiContainer(Enum[str]):
    CRAFTING_TABLE: str
    ENCHANTING_TABLE: str
    BEACON: str
    ANVIL: str
    CHIPPED_ANVIL: str
    DAMAGED_ANVIL: str
    DEPRECATED_ANVIL: str
    GRINDSTONE: str
    CARTOGRAPHY_TABLE: str
    STONECUTTER_BLOCK: str
    LOOM: str
    SMITHING_TABLE: str
    VILLAGER: str
    VILLAGER_V2: str


class Container(Enum[str]):
    CHEST: str
    TRAPPED_CHEST: str
    CHEST: str
    ENDER_CHEST: str
    UNDYED_SHULKER_BOX: str
    WHITE_SHULKER_BOX: str
    ORANGE_SHULKER_BOX: str
    MAGENTA_SHULKER_BOX: str
    LIGHT_BLUE_SHULKER_BOX: str
    YELLOW_SHULKER_BOX: str
    LIME_SHULKER_BOX: str
    PINK_SHULKER_BOX: str
    GRAY_SHULKER_BOX: str
    LIGHT_GRAY_SHULKER_BOX: str
    CYAN_SHULKER_BOX: str
    PURPLE_SHULKER_BOX: str
    BLUE_SHULKER_BOX: str
    BROWN_SHULKER_BOX: str
    GREEN_SHULKER_BOX: str
    RED_SHULKER_BOX: str
    BLACK_SHULKER_BOX: str
    BARREL: str
    FURNACE: str
    LIT_FURNACE: str
    SMOKER: str
    LIT_SMOKER: str
    BLAST_FURNACE: str
    LIT_BLAST_FURNACE: str
    BREWING_STAND: str
    DROPPER: str
    DISPENSER: str
    HOPPER: str
    CRAFTER: str
    CHEST_MINECART: str
    CHEST_BOAT: str
    HOPPER_MINECART: str
    HORSE: str
    DONKEY: str
    MULE: str
    CAMEL: str
    TRADER_LLAMA: str
    LLAMA: str


class PositiveEffect(Enum[str]):
    SPEED: str
    HASTE: str
    STRENGTH: str
    INSTANT_HEALTH: str
    JUMP_BOOST: str
    REGENERATION: str
    RESISTANCE: str
    FIRE_RESISTANCE: str
    WATER_BREATHING: str
    INVISIBILITY: str
    NIGHT_VISION: str
    HEALTH_BOOST: str
    ABSORPTION: str
    SATURATION: str
    SLOW_FALLING: str
    VILLAGE_HERO: str


class NegativeEffect(Enum[str]):
    SLOWDOWN: str
    MINING_FATIGUE: str
    INSTANT_DAMAGE: str
    NAUSEA: str
    BLINDNESS: str
    HUNGER: str
    WEAKNESS: str
    POISON: str
    WITHER: str
    LEVITATION: str
    FATAL_POISON: str
    DARKNESS: str
    WIND_CHARGED: str
    WEAVING: str
    OOZING: str
    INFESTED: str


class NeutralEffect(Enum[str]):
    BAD_OMEN: str
    TRIAL_OMEN: str
    RAID_OMEN: str


ENTITY_NAME_MAP: Dict[int, Tuple[int, str, str]]
BIOME_NAME_MAP: Dict[int, Tuple[str, str]]
STRUCTURE_NAME_MAP: Dict[int, Tuple[str, str]]
EFFECT_NAME_MAP: Dict[str, str]
ENCHANT_NAME_MAP: Dict[int, Tuple[str, str]]
