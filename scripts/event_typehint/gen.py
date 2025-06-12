# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-06-11
|
| ==============================================
"""


import os
import shutil
import re


typehint_data = []


root = "\\".join(os.getcwd().split("\\")[:-2])
types_dir = "\\".join([root, "nuoyanlib", "_core", "_types"])


with open(types_dir + r"\_events.pyi", "r") as f:
    flag = 0
    args = []
    while True:
        line = f.readline()
        if line == "":
            break
        line = line.strip()
        if line.startswith("【事件参数】"):
            flag = 1
        if flag:
            if line.startswith("-"):
                try:
                    # 提取参数名
                    name = line[line.index("``") + 2: line.rindex("``")]
                    # 提取类型
                    typ = line[line.index("--") + 3: line.index("，")]
                    # 提取说明
                    doc = line[line.index("，") + 3:] # +3是因为一个中文占3字节
                except ValueError:
                    continue
                name = name.replace("$", "")
                typ = (
                    typ.replace("dict[", "Dict[")
                    .replace("list[", "List[")
                    .replace("tuple[", "Tuple[")
                )
                args.append((name, typ, doc))
            elif line.startswith('"""'):
                # 到达文档注释末尾
                typehint_data.append(args)
                flag = 0
                args = []
                # print event
                # print args


print("events:", len(typehint_data))


shutil.copyfile(types_dir + r"\_events.pyi", "_events.pyi")
shutil.copyfile(types_dir + r"\_event_typing.pyi", "_event_typing.pyi")


with open("_events.pyi", "r") as f:
    _events = f.read()
with open("_events.pyi", "w") as f:
    # 重新编号EventArgs，第一次替换时附加三个下划线，目的是避免正则表达式总是匹配到第一个EventArgs
    for i, _ in enumerate(typehint_data):
        _events = re.sub(r"EventArgs[0-9]+\):", "EventArgs___%d):" % i, _events, 1)
    # 去掉所有三下划线
    _events = _events.replace("___", "")
    # 编辑事件枚举
    _events = re.sub(r"# clear.*", "# clear\n\n\n", _events, 1, re.S)
    match = re.search(r"class ClientEvent:.*# clear", _events, re.S)
    enum = match.group(0)[:-7]
    enum = (
        enum.replace("class ClientEvent:", "class ClientEventEnum:", 1)
        .replace("class ServerEvent:", "class ServerEventEnum:", 1)
        .replace("    def ", "    ")
    )
    enum = re.sub(r"\(self, event: EventArgs[0-9]+\):", ": str", enum)
    enum = enum.replace(" " * 8, " " * 4)
    _events += enum
    f.write(_events)


with open("_event_typing.pyi", "r") as f:
    _event_typing = f.read()
    # 截取文件内容到第一个“class”前，即去除所有的class
    _event_typing = _event_typing[:_event_typing.index("class")]
with open("_event_typing.pyi", "w") as f:
    # 按顺序编写事件参数注解
    for i, args in enumerate(typehint_data):
        _event_typing += 'class EventArgs%d(EventArgsProxy):\n' % i
        if args:
            for name, typ, doc in args:
                if name == "from":
                    name += "_"
                _event_typing += "    %s: %s\n" % (name, typ)
                _event_typing += '    """\n    %s\n    """\n' % doc
        else:
            _event_typing += "    pass\n"
        _event_typing += "\n"
    f.write(_event_typing)








