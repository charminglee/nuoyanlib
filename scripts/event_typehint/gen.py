# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-21
|
| ==============================================
"""


import os
import shutil
import re
from _all_events import ClientEvent, ServerEvent


root = os.getcwd()
event_dir = f"{root}\\nuoyanlib\\_core\\event"
script_dir = f"{root}\\scripts\\event_typehint"


for cls in ClientEvent, ServerEvent:
    cls._data = {}
    for event_name, func in cls.__dict__.items():
        if event_name.startswith("_"):
            continue
        doc = func.__doc__
        args = []
        for line in doc[doc.index("【事件参数】"):].splitlines():
            line = line.strip()
            if line.startswith("-"):
                try:
                    # 提取参数名
                    param_name = line[line.index("``") + 2: line.rindex("``")]
                    # 提取类型
                    typ = line[line.index("--") + 3: line.index("，")]
                    # 提取说明
                    param_doc = line[line.index("，") + 1:]
                except ValueError:
                    continue
                param_name = param_name.replace("$", "")
                typ = (
                    typ.replace("dict[", "Dict[")
                    .replace("list[", "List[")
                    .replace("tuple[", "Tuple[")
                )
                args.append((param_name, typ, param_doc))
        cls._data[event_name] = (args, doc)
print("events:", len(ClientEvent._data) + len(ServerEvent._data))


shutil.copyfile(f"{event_dir}\\_events.py", f"{script_dir}\\_events.py")
shutil.copyfile(f"{event_dir}\\_events.pyi", f"{script_dir}\\_events.pyi")
shutil.copyfile(f"{event_dir}\\_event_typing.pyi", f"{script_dir}\\_event_typing.pyi")


_events_py = open(f"{script_dir}\\_events.py", "r", encoding="utf-8").read()
all_client_events = "ALL_CLIENT_ENGINE_EVENTS = {\n"
for k in ClientEvent._data.keys():
    all_client_events += f'    "{k}",\n'
all_client_events += "}\nALL_SERVER_ENGINE_EVENTS"
_events_py = re.sub(
    r"ALL_CLIENT_ENGINE_EVENTS = \{.*}\nALL_SERVER_ENGINE_EVENTS",
    all_client_events, _events_py, 1, re.S
)
all_server_events = "ALL_SERVER_ENGINE_EVENTS = {\n"
for k in ServerEvent._data.keys():
    all_server_events += f'    "{k}",\n'
all_server_events += "}\nALL_CLIENT_LIB_EVENTS"
_events_py = re.sub(
    r"ALL_SERVER_ENGINE_EVENTS = \{.*}\nALL_CLIENT_LIB_EVENTS",
    all_server_events, _events_py, 1, re.S
)
open(f"{script_dir}\\_events.py", "w", encoding="utf-8").write(_events_py)


# 生成事件枚举
_events_pyi = open(f"{script_dir}\\_events.pyi", "r", encoding="utf-8").read()
_events_pyi = re.sub(r"# clear.*", "# clear\n\n\n", _events_pyi, 1, re.S)
_events_pyi += "class ClientEventEnum:\n"
for data in ClientEvent._data, ServerEvent._data:
    for event_name, (args, doc) in data.items():
        _events_pyi += f"    {event_name}: str\n"
        doc = doc.replace("\n        ", "\n    ")
        _events_pyi += f'    """{doc}"""\n'
    if "ServerEventEnum" not in _events_pyi:
        _events_pyi += "\n\nclass ServerEventEnum:\n"
open(f"{script_dir}\\_events.pyi", "w", encoding="utf-8").write(_events_pyi)


_event_typing = open(f"{script_dir}\\_event_typing.pyi", "r", encoding="utf-8").read()
_event_typing = re.sub(r"# clear.*", "# clear\n\n\n", _event_typing, 1, re.S)
_event_typing += "class ClientEvent:\n"


# 生成ClientEvent、ServerEvent类
n = 0
for data in ClientEvent._data, ServerEvent._data:
    for event_name, (args, doc) in data.items():
        _event_typing += f"    def {event_name}(self, args: EventArgs{n}):\n"
        _event_typing += f'        """{doc}"""\n'
        n += 1
    if "class ServerEvent" not in _event_typing:
        _event_typing += "\n\nclass ServerEvent:\n"
_event_typing += "\n"


# 生成EventArgs类
n = 0
for data in ClientEvent._data, ServerEvent._data:
    for event_name, (args, doc) in data.items():
        _event_typing += f"\n# {event_name}\nclass EventArgs{n}(EventArgsProxy):\n"
        if args:
            for param_name, typ, param_doc in args:
                if param_name == "from":
                    param_name += "_"
                _event_typing += f"    {param_name}: {typ}\n"
                _event_typing += f'    """\n    {param_doc}\n    """\n'
        else:
            _event_typing += "    pass\n"
        n += 1
open(f"{script_dir}\\_event_typing.pyi", "w", encoding="utf-8").write(_event_typing)










