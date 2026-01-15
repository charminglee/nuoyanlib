# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-16
#  ⠀
# =================================================


import os
import shutil
import re
from all_events import ClientEvent, ServerEvent


root = os.getcwd()
event_dir = f"{root}\\src\\nuoyanlib\\core"
script_dir = f"{root}\\scripts\\event_typehint"


def extract_events(cls):
    data = {}
    for event_name, func in cls.__dict__.items():
        if event_name.startswith("_"):
            continue
        args = []
        doc = func.__doc__
        for line in doc[doc.index("事件参数"):].splitlines():
            line = line.strip()
            if line.startswith("- "):
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
        data[event_name] = (args, doc)
    return data


c_events = extract_events(ClientEvent)
s_events = extract_events(ServerEvent)
print("events:", len(c_events) + len(s_events))


shutil.copyfile(f"{event_dir}\\_types\\_event_typing.pyi", f"{script_dir}\\_event_typing.pyi")


def read(path, mode="r"):
    with open(path, mode, encoding="utf-8") as f:
        content = f.read()
    return content


def write(path, content, mode="w"):
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)


_event_typing = read(f"{script_dir}\\_event_typing.pyi")
_event_typing = re.sub(r"# clear.*", "# clear\n\n\n", _event_typing, 1, re.S)
_event_typing += "class ClientEvent:\n"


# 生成ClientEvent、ServerEvent类
n = 0
for data in c_events, s_events:
    for event_name, (args, doc) in data.items():
        _event_typing += f"    def {event_name}(self, args: EventArgs{n}):\n"
        _event_typing += f'        """{doc}"""\n'
        n += 1
    if "class ServerEvent" not in _event_typing:
        _event_typing += "\n\nclass ServerEvent:\n"
_event_typing += "\n"


# 生成EventArgs类
n = 0
for data in c_events, s_events:
    for event_name, (args, doc) in data.items():
        _event_typing += f"\n# {event_name}\nclass EventArgs{n}(EventArgsWrap):\n"
        if args:
            for param_name, typ, param_doc in args:
                if param_name == "from":
                    param_name += "_"
                _event_typing += f"    {param_name}: {typ}\n"
                _event_typing += f'    """\n    {param_doc}\n    """\n'
        else:
            _event_typing += "    pass\n"
        n += 1
write(f"{script_dir}\\_event_typing.pyi", _event_typing)


# 生成enum.py
enum_py = "class ClientEvent(StrEnum):\n"
for data in c_events, s_events:
    for event_name in data:
        enum_py += f"    {event_name} = auto()\n"
    if "ServerEvent(StrEnum)" not in enum_py:
        enum_py += "\n\nclass ServerEvent(StrEnum):\n"
write(f"{script_dir}\\enum.py", enum_py)


# 生成enum.pyi
enum_pyi = "class ClientEvent(StrEnum):\n"
for data in c_events, s_events:
    for event_name, (args, doc) in data.items():
        enum_pyi += f"    {event_name} = ...\n"
        enum_pyi += '    """'
        enum_pyi += doc.replace("\n        ", "\n    ")
        enum_pyi += '"""\n'
    if "ServerEvent(StrEnum)" not in enum_pyi:
        enum_pyi += "\n\nclass ServerEvent(StrEnum):\n"
write(f"{script_dir}\\enum.pyi", enum_pyi)












