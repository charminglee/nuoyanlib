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


from mod.client.ui.controls.sliderUIControl import SliderUIControl
from .control import NyControl
from ..screen_node import NyScreenBase
from ....core._types._checker import args_type_check


class NySlider(NyControl):
    _base_control: SliderUIControl
    def __init__(
        self,
        ny_screen_node: NyScreenBase,
        path: str,
    ) -> None: ...
    @args_type_check(str)
    def __truediv__(self, other: str) -> NyControl: ...
    __div__ = __truediv__
    @property
    def value(self) -> float: ...
    @value.setter
    def value(self, val: float) -> None: ...
    get_slider_value = GetSliderValue = SliderUIControl.GetSliderValue
    set_slider_value = SetSliderValue = SliderUIControl.SetSliderValue
