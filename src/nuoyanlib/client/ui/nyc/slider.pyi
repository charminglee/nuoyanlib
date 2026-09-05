# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-6
#  ⠀
#  ================================================


from typing import Union
from mod.client.ui.controls.sliderUIControl import SliderUIControl
from .control import NyControl
from ..screen_node import NyScreenNode, NyScreenProxy
from ....core._types._checker import args_type_check


class NySlider(NyControl):
    _base_control: SliderUIControl
    def __new__(
        cls,
        ny_screen_node: Union[NyScreenNode, NyScreenProxy],
        path: str,
    ) -> NySlider: ...
    def __init__(
        self,
        ny_screen_node: Union[NyScreenNode, NyScreenProxy],
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, val: float) -> None: ...
    GetSliderValue = SliderUIControl.GetSliderValue
    SetSliderValue = SliderUIControl.SetSliderValue
