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


from nuoyanlib.common.utils import (
    rgb2hex,
    hex2rgb,
    check_string,
    convert_dict_value_to_tuple,
    convert_list_to_tuple,
    translate_time,
)
from nuoyanlib.core._utils import assert_error


assert rgb2hex((255, 69, 0), False) == "#FF4500"
assert rgb2hex((255, 69, 0), False, False, False) == "ff4500"
assert rgb2hex((0, 0, 0)) == "#000000"
assert_error(rgb2hex, ((255, 69), False), exc=ValueError)
assert_error(rgb2hex, ((255, 69, 300), False), exc=ValueError)


assert hex2rgb("#FF4500", False) == (255, 69, 0)
assert hex2rgb("#000000", True) == (0, 0, 0)
assert_error(hex2rgb, ("#FF45",), exc=ValueError)
assert_error(hex2rgb, ("#FF45AV",), exc=ValueError)


assert check_string("11112222", "1", "2")
assert not check_string("11112222", "1")
assert check_string("1234567890", "0-9")


a = {'b': [1, 2, 3], 'c': "hahaha", 'd': [4, 5]}
convert_dict_value_to_tuple(a)
assert a == {'b': (1, 2, 3), 'c': "hahaha", 'd': (4, 5)}


a = [1, [2, 3], "abc"]
assert convert_list_to_tuple(a) == (1, (2, 3), "abc")


assert translate_time(3660, ":", ("H", "M", "S"), True) == "1H:01M:00S"
assert translate_time(3660, unit=("H", "M", "S"), zfill=True) == "1H01M00S"
assert translate_time(3660, unit=("H", "M", "S"), zfill=False) == "1H1M"
assert translate_time(3661, ":", None, True) == "1:01:01"
assert translate_time(3660, ":", None, True) == "1:01:00"
assert translate_time(3600, ":", None, True) == "1:00:00"
assert translate_time(61, ":", None, True) == "1:01"
assert translate_time(60, ":", None, True) == "1:00"
assert translate_time(1, ":", None, True) == "0:01"
assert translate_time(0, ":", None, True) == "0:00"
assert translate_time(3700) == "1h1m40s"
assert translate_time(3660) == "1h1m"
assert translate_time(3601) == "1h1s"
assert translate_time(61) == "1m1s"
assert translate_time(3600) == "1h"
assert translate_time(60) == "1m"
assert translate_time(1) == "1s"
assert translate_time(0) == "0s"
