# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-06-20
#
# ====================================================


from typing import Union
import mod.client.extraClientApi as client_api
import mod.server.extraServerApi as server_api
from mod.client.component.engineCompFactoryClient import EngineCompFactoryClient
from mod.server.component.engineCompFactoryServer import EngineCompFactoryServer


def is_client() -> bool: ...
def get_api() -> Union[client_api, server_api]: ...
def get_comp_factory() -> Union[EngineCompFactoryClient, EngineCompFactoryServer]: ...


LEVEL_ID: str