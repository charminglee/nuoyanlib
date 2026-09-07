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


from typing import List, Tuple, Optional


__version__: str
__author__: str
__author_qq__: str
__author_email__: str


def run(
    mod_name: str,
    *,
    clients: Optional[List[Tuple[str, str]]] = None,
    servers: Optional[List[Tuple[str, str]]] = None,
    globals: Optional[dict] = None,
) -> None: ...
