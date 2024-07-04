# -*- coding: utf-8 -*-
# ====================================================
#
#   Copyright (c) 2023 Nuoyan
#   nuoyanlib is licensed under Mulan PSL v2.
#   You can use this software according to the terms and conditions of the Mulan PSL v2.
#   You may obtain a copy of Mulan PSL v2 at:
#            http://license.coscl.org.cn/MulanPSL2
#   THIS SOFTWARE IS PROVIDED ON AN AS IS BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#   See the Mulan PSL v2 for more details.
#
#   Author        : 诺言Nuoyan
#   Email         : 1279735247@qq.com
#   Gitee         : https://gitee.com/charming-lee
#   Last Modified : 2024-07-05
#
# ====================================================


import json
import io
import re


is_beta = True


ver = raw_input("version: ")
version_lst = map(int, ver.split("."))
if is_beta:
    version_str = "v%s-beta" % ver
else:
    version_str = "v%s" % ver


def set_manifest(path):
    with open(path, "r") as f:
        data = json.load(f)
    data['header']['version'] = version_lst
    data['modules'][0]['version'] = version_lst
    with open(path, "w") as f:
        json.dump(data, f, indent=4, separators=(", ", ": "), sort_keys=True)


set_manifest(r"..\nuoyanlib\resource_packs\nuoyanlibRes\manifest.json")
set_manifest(r"..\nuoyanlib\behavior_packs\nuoyanlibBeh\manifest.json")


def set_mod_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    data['netgame_mod_version'] = version_str
    with open(path, "w") as f:
        json.dump(data, f, indent=4, separators=(", ", ": "), sort_keys=True)


set_mod_json(r"..\nuoyanlib\developer_mods\nuoyanlibDev\mod.json")
set_mod_json(r"..\nuoyanlib\behavior_packs\nuoyanlibBeh\mod.json")


def set_const(path):
    with io.open(path, "r", encoding="utf-8") as f:
        data = f.read()
    data = re.sub('__version__ = ".+"', '__version__ = "%s"' % version_str, data)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(data)


set_const(r"..\nuoyanlib\developer_mods\nuoyanlibDev\nuoyanlib\_core\_const.py")
set_const(r"..\nuoyanlib\behavior_packs\nuoyanlibBeh\nuoyanlib\_core\_const.py")

















