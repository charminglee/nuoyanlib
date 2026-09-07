# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-7
#  ⠀
#  ================================================


import threading
from typing import Union, Literal, Type
import mod.client.extraClientApi as c_api
import mod.server.extraServerApi as s_api
from .client._lib_client import NuoyanLibClientSystem
from .server._lib_server import NuoyanLibServerSystem
from .client.comp import CF as CCF
from .server.comp import CF as SCF


def get_cls_path(cls: type) -> str: ...
def get_env() -> Literal["client", "server"]: ...
def check_env(target: Literal["client", "server"]) -> None: ...
_THREAD_LOCAL: threading.local
def get_lib_system() -> Union[NuoyanLibClientSystem, NuoyanLibServerSystem]: ...
def is_client() -> bool: ...
def get_api() -> Union[Type[c_api], Type[s_api]]: ...
def get_lv_comp() -> Union[CCF, SCF]: ...
def get_cf(entity_id: str) -> Union[CCF, SCF]: ...
LEVEL_ID: str
