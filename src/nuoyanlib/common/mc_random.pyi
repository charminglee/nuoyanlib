# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-10
#  ⠀
# =================================================


from random import Random
from typing import Optional, Callable, Dict, Any, Union, List
from ..core._types._typing import FTuple3


def chance(p: float) -> bool: ...
def random_pos(
    center: FTuple3,
    r: float,
    dim: Optional[int] = None,
    use_top_height: bool = False,
) -> Optional[FTuple3]: ...
def _gen_str(choice: Callable[[Any], Any], s: str, l: int) -> str: ...
_random_ins: Dict[Union[Any, None], Random]
def random_string(
    length: int,
    lower: bool = True,
    upper: bool =True,
    num: bool =True,
    seed: Any = None,
    generate_num: int = 1,
) -> Union[str, List[str]]: ...
