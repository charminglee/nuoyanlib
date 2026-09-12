# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-13
#  ⠀
#  ================================================


from pathlib import Path
import re
import shutil

from all_events import ClientEvent, ServerEvent


COMMON_ENUM_PYI = Path("src/nuoyanlib/common/enum.pyi")
EVENT_TYPING_PYI = Path("scripts/event_typing/_event_typing.pyi")
SCRIPTS_ENUM_PYI = Path("scripts/event_typing/enum.pyi")
EVENT_TYPING_PREFIX = (
    "# -*- coding: utf-8 -*-\n"
    "#  ================================================\n"
    "#  \u2800\n"
    "#    Copyright (c) 2026 Nuoyan\n"
    "#  \u2800\n"
    "#    Author: Nuoyan <https://github.com/charminglee>\n"
    "#    Email : 1279735247@qq.com\n"
    "#    Date  : 2026-9-7\n"
    "#  \u2800\n"
    "#  ================================================\n"
    "\n\n"
    "from typing import List, Tuple\n"
    "from ..listener import EventArgsWrapper\n"
    "\n\n"
)
PARAMETER_PATTERN = re.compile(
    r"^-\s+``(?P<name>[^`]+)``\s+--\s+"
    r"(?P<type>[^，]+)，(?P<doc>.*)$"
)
EVENT_ENUM_PATTERN = re.compile(
    r"^class (ClientEvent|ServerEvent)\(LazyEnum\):\n.*?(?=^class |\Z)",
    re.MULTILINE | re.DOTALL,
)


def read_text(path):
    with path.open("r", encoding="utf-8", newline="") as file:
        return file.read()


def write_text(path, content):
    with path.open("w", encoding="utf-8", newline="") as file:
        file.write(content)


def extract_events(event_class):
    events = []
    for event_name, function in event_class.__dict__.items():
        if event_name.startswith("_") or not callable(function):
            continue

        doc = function.__doc__
        if doc is None:
            raise ValueError(f"{event_class.__name__}.{event_name} has no documentation")
        if "事件参数" not in doc:
            raise ValueError(f"{event_class.__name__}.{event_name} has no parameter section")

        arguments = []
        parameter_section = doc[doc.index("事件参数"):]
        for line in parameter_section.splitlines():
            match = PARAMETER_PATTERN.match(line.strip())
            if match is None:
                continue

            argument_name = match.group("name").replace("$", "")
            argument_type = (
                match.group("type")
                .strip()
                .replace("dict[", "Dict[")
                .replace("list[", "List[")
                .replace("tuple[", "Tuple[")
            )
            argument_doc = match.group("doc").strip()
            arguments.append((argument_name, argument_type, argument_doc))

        events.append((event_name, arguments, doc))
    return events


def render_docstring(indent, doc):
    return f'{indent}"""{doc}"""\n'


def render_event_typing(event_groups):
    content = [EVENT_TYPING_PREFIX]

    for group_index, (group_name, events) in enumerate(event_groups):
        if group_index:
            content.append("\n\n\n")
        content.append(f"class {group_name}:\n")
        for event_index, (event_name, _, doc) in enumerate(events):
            index = sum(len(group[1]) for group in event_groups[:group_index]) + event_index
            content.append(f"    def {event_name}(self, args):\n")
            content.append(f"        # type: (EventArgs{index}) -> None\n")
            content.append(render_docstring("        ", doc))

    content.append("\n\n# region Client EventArgs\n\n\n")
    index = 0

    def render(events):
        nonlocal index
        for event_name, arguments, _ in events:
            content.append(f"# {event_name}\n")
            content.append(f"class EventArgs{index}(EventArgsWrapper):\n")
            if arguments:
                for argument_name, argument_type, argument_doc in arguments:
                    if argument_name == "from":
                        argument_name += "_"
                    content.append(f"    {argument_name}: {argument_type}\n")
                    content.append('    """\n')
                    content.append(f"    {argument_doc}\n")
                    content.append('    """\n')
            else:
                content.append("    pass\n")
            index += 1

    render(event_groups[0][1])
    content.append("\n\n# endregion\n\n\n# region Server EventArgs\n\n\n")
    render(event_groups[1][1])
    content.append("\n\n# endregion\n")

    return "".join(content)


def update_event_enum(enum_content, event_groups):
    newline = "\r\n" if "\r\n" in enum_content else "\n"
    enum_content = enum_content.replace("\r\n", "\n")
    groups = {group_name: events for group_name, events in event_groups}
    matches = list(EVENT_ENUM_PATTERN.finditer(enum_content))
    if [match.group(1) for match in matches] != ["ClientEvent", "ServerEvent"]:
        raise ValueError("enum.pyi must contain ClientEvent and ServerEvent LazyEnum definitions")

    def replace_group(match):
        group_name = match.group(1)
        events = groups[group_name]
        block = [f"class {group_name}(LazyEnum):\n"]
        start_index = 0 if group_name == "ClientEvent" else len(groups["ClientEvent"])
        for event_offset, (event_name, _, _) in enumerate(events):
            block.append(f"    {event_name} = EventArgs{start_index + event_offset}\n")
        block.append("\n\n")
        return "".join(block)

    return EVENT_ENUM_PATTERN.sub(replace_group, enum_content).replace("\n", newline)


def main():
    shutil.copyfile(COMMON_ENUM_PYI, SCRIPTS_ENUM_PYI)

    client_events = extract_events(ClientEvent)
    server_events = extract_events(ServerEvent)
    event_groups = [
        ("ClientEvent", client_events),
        ("ServerEvent", server_events),
    ]
    event_count = len(client_events) + len(server_events)
    print("events:", event_count)

    event_typing_content = render_event_typing(event_groups)
    write_text(EVENT_TYPING_PYI, event_typing_content)
    enum_content = update_event_enum(read_text(SCRIPTS_ENUM_PYI), event_groups)
    write_text(SCRIPTS_ENUM_PYI, enum_content)


if __name__ == "__main__":
    main()
