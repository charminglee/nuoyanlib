# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-17
#  ⠀
# =================================================


from typing import Tuple, overload


@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    res_tuple3: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    res_tuple3: Tuple[str, str],
    res_tuple4: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool, bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    res_tuple3: Tuple[str, str],
    res_tuple4: Tuple[str, str],
    res_tuple5: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool, bool, bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    res_tuple3: Tuple[str, str],
    res_tuple4: Tuple[str, str],
    res_tuple5: Tuple[str, str],
    res_tuple6: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool, bool, bool, bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    res_tuple3: Tuple[str, str],
    res_tuple4: Tuple[str, str],
    res_tuple5: Tuple[str, str],
    res_tuple6: Tuple[str, str],
    res_tuple7: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool, bool, bool, bool, bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    res_tuple3: Tuple[str, str],
    res_tuple4: Tuple[str, str],
    res_tuple5: Tuple[str, str],
    res_tuple6: Tuple[str, str],
    res_tuple7: Tuple[str, str],
    res_tuple8: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool, bool, bool, bool, bool, bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    res_tuple: Tuple[str, str],
    res_tuple2: Tuple[str, str],
    res_tuple3: Tuple[str, str],
    res_tuple4: Tuple[str, str],
    res_tuple5: Tuple[str, str],
    res_tuple6: Tuple[str, str],
    res_tuple7: Tuple[str, str],
    res_tuple8: Tuple[str, str],
    res_tuple9: Tuple[str, str],
    /,
    *,
    rebuild: bool = False,
) -> Tuple[bool, bool, bool, bool, bool, bool, bool, bool, bool]: ...
@overload
def add_entity_render_resources(
    entity_id: str,
    *res_tuple: Tuple[str, str],
    rebuild: bool = False,
) -> Tuple[bool, ...]: ...
