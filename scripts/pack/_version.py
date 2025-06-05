# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-05
|
| ==============================================
"""


import json
import io
import re
import os


is_beta = True


ver = raw_input("version: ")
version_lst = map(int, ver.split("."))
if is_beta:
    version_str = "v%s-beta" % ver
else:
    version_str = "v%s" % ver
cwd = os.getcwd()
root_path = "\\".join(cwd.split("\\")[:-2])


def set_manifest(path):
    with open(path, "r") as f:
        data = json.load(f)
    data['header']['version'] = version_lst
    data['modules'][0]['version'] = version_lst
    with open(path, "w") as f:
        json.dump(data, f, indent=4, separators=(", ", ": "), sort_keys=True)


set_manifest(r"%s\release\nuoyanlib\resource_packs\nuoyanlib\manifest.json" % root_path)
set_manifest(r"%s\release\nuoyanlib\behavior_packs\nuoyanlib\manifest.json" % root_path)


def set_mod_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        data = f.read()
    data = re.sub('"netgame_mod_version": ".+"', '"netgame_mod_version": "%s"' % version_str, data)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(data)


set_mod_json(r"%s\release\nuoyanlib\developer_mods\nuoyanlib\mod.json" % root_path)
# set_mod_json(r"%s\release\nuoyanlib\behavior_packs\nuoyanlib\mod.json" % root_path)


def set_const(path):
    with io.open(path, "r", encoding="utf-8") as f:
        data = f.read()
    data = re.sub('__version__ = ".+"', '__version__ = "%s"' % version_str, data)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(data)


set_const(r"%s\release\nuoyanlib\developer_mods\nuoyanlib\nuoyanlib\_core\_const.py" % root_path)
set_const(r"%s\release\nuoyanlib\behavior_packs\nuoyanlib\nuoyanlib\_core\_const.py" % root_path)


def set_world_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    data[0]['version'] = version_lst
    with open(path, "w") as f:
        json.dump(data, f, indent=4, separators=(", ", ": "), sort_keys=True)


set_world_json(r"%s\release\nuoyanlib\worlds\level\world_behavior_packs.json" % root_path)
set_world_json(r"%s\release\nuoyanlib\worlds\level\world_resource_packs.json" % root_path)

















