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


from __future__ import annotations
import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen
from zhconv import convert


MAIN_URL = "https://zh.minecraft.wiki/w/%E5%9F%BA%E5%B2%A9%E7%89%88%E6%95%B0%E6%8D%AE%E5%80%BC"
DEFAULT_OUTPUT = Path(__file__).resolve().with_name("minecraft_ids.json")
USER_AGENT = "nuoyanlib-wiki-crawler/1.0 (+https://github.com/charminglee/nuoyanlib)"
PAGE_TITLES = {
    "blocks": "基岩版数据值/方块ID",
    "items": "基岩版数据值/物品ID/1.16.100后",
    "entities": "基岩版数据值/实体ID",
    "biomes": "生物群系/ID/基岩版",
}
COMMON_ENUM_PYI = Path(__file__).resolve().parents[2] / "src" / "nuoyanlib" / "common" / "enum.pyi"
SCRIPT_ENUM_PYI = Path(__file__).resolve().with_name("enum.pyi")
ENUM_CLASSES = {
    "block": "Block",
    "item": "Item",
    "entity": "Entity",
    "biome": "Biome",
    "effect": "Effect",
    "enchantment": "Enchantment",
}
ENUM_VALUE_PREFIX_CATEGORIES = {"block", "item", "entity"}
MINECRAFT_NAMESPACE = "minecraft:"
CLASS_PATTERN = re.compile(r"^class (?P<name>[A-Za-z_][A-Za-z0-9_]*)\([^)]*\):(?:\r?\n)?$")
MEMBER_PATTERN = re.compile(
    r"^    (?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*.+?(?:\r?\n)?$"
)


class ParsedTable:
    def __init__(self, attributes: Dict[str, str]):
        self.attributes = attributes
        self.rows: List[List[Tuple[str, str]]] = []


class HTMLTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: List[ParsedTable] = []
        self._table_stack: List[ParsedTable] = []
        self._row_stack: List[Tuple[ParsedTable, List[Tuple[str, str]]]] = []
        self._cell_stack: List[Tuple[ParsedTable, List[Tuple[str, str]], str, List[str]]] = []
        self._ignored_tag_depth = 0

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        if tag == "sup":
            self._ignored_tag_depth += 1
            return

        if tag == "table":
            table = ParsedTable({key: value or "" for key, value in attrs})
            self.tables.append(table)
            self._table_stack.append(table)
            return

        if tag == "tr" and self._table_stack:
            self._row_stack.append((self._table_stack[-1], []))
            return

        if (
            tag in {"th", "td"}
            and self._row_stack
            and self._table_stack
            and self._row_stack[-1][0] is self._table_stack[-1]
        ):
            table, row = self._row_stack[-1]
            self._cell_stack.append((table, row, tag, []))
            return

        if tag == "br" and self._cell_stack and self._table_stack:
            if self._cell_stack[-1][0] is self._table_stack[-1]:
                self._cell_stack[-1][3].append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "sup":
            self._ignored_tag_depth = max(0, self._ignored_tag_depth - 1)
            return

        if tag in {"th", "td"} and self._cell_stack and self._table_stack:
            table, row, cell_tag, buffer = self._cell_stack[-1]
            if table is self._table_stack[-1] and cell_tag == tag:
                self._cell_stack.pop()
                row.append((cell_tag, _clean_text("".join(buffer))))
            return

        if tag == "tr" and self._row_stack and self._table_stack:
            table, row = self._row_stack[-1]
            if table is self._table_stack[-1]:
                self._row_stack.pop()
                table.rows.append(row)
            return

        if tag == "table" and self._table_stack:
            self._table_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._ignored_tag_depth == 0 and self._cell_stack and self._table_stack:
            if self._cell_stack[-1][0] is self._table_stack[-1]:
                self._cell_stack[-1][3].append(data)


def _clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return convert(value, "zh-cn")


def _read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as file:
        return file.read()


def _write_text(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        file.write(content)


def _normalize_header(value: str) -> str:
    value = _clean_text(value).replace(" ", "").lower()
    replacements = (
        ("圖示", "图示"),
        ("圖", "图"),
        ("塊", "块"),
        ("實體", "实体"),
        ("實", "实"),
        ("進", "进"),
        ("數", "数"),
        ("稱", "称"),
        ("間", "间"),
        ("羣", "群"),
    )
    for source, target in replacements:
        value = value.replace(source, target)
    return value


def _parse_tables(content: str) -> List[ParsedTable]:
    parser = HTMLTableParser()
    parser.feed(content)
    parser.close()
    return parser.tables


def _header_row(table: ParsedTable) -> Optional[List[Tuple[str, str]]]:
    for row in table.rows:
        if row and any(cell_type == "th" for cell_type, _ in row):
            return row
    return None


def _find_column(headers: Sequence[str], aliases: Iterable[str]) -> Optional[int]:
    normalized_aliases = {_normalize_header(alias) for alias in aliases}
    for index, header in enumerate(headers):
        if header in normalized_aliases:
            return index
    return None


def _find_tables(
    tables: Sequence[ParsedTable],
    required_columns: Dict[str, Set[str]],
) -> Iterable[Tuple[ParsedTable, List[List[Tuple[str, str]]], Dict[str, int]]]:
    for table in tables:
        header = _header_row(table)
        if header is None:
            continue

        headers = [_normalize_header(value) for _, value in header]
        columns: Dict[str, int] = {}
        for column_name, aliases in required_columns.items():
            index = _find_column(headers, aliases)
            if index is None:
                break
            columns[column_name] = index
        else:
            yield table, table.rows, columns


def _value_at(row: List[Tuple[str, str]], index: int) -> str:
    if index >= len(row):
        return ""
    return row[index][1]


def _parse_number(value: str) -> Optional[object]:
    value = _clean_text(value)
    if not value:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _parse_standard_ids(
    content: str,
    name_aliases: Set[str],
) -> List[Dict[str, object]]:
    required_columns = {
        "decimal": {"Dec", "十进制"},
        "hexadecimal": {"Hex", "十六进制"},
        "id": {"命名空间ID"},
        "name": name_aliases,
    }
    records: List[Dict[str, object]] = []
    for table, rows, columns in _find_tables(_parse_tables(content), required_columns):
        header = _header_row(table)
        if header is None:
            continue
        for row in rows:
            if row is header:
                continue
            identifier = _clean_text(_value_at(row, columns["id"]))
            if not identifier:
                continue
            records.append(
                {
                    "id": identifier,
                    "numeric_id": _parse_number(_value_at(row, columns["decimal"])),
                    "hex_id": _clean_text(_value_at(row, columns["hexadecimal"])),
                    "name": _clean_text(_value_at(row, columns["name"])),
                }
            )
    return records


def _parse_biomes(content: str) -> List[Dict[str, object]]:
    required_columns = {
        "name": {"名称"},
        "id": {"命名空间ID"},
        "decimal": {"数字ID"},
    }
    records: List[Dict[str, object]] = []
    for table, rows, columns in _find_tables(_parse_tables(content), required_columns):
        header = _header_row(table)
        if header is None:
            continue
        for row in rows:
            if row is header:
                continue
            identifier = _clean_text(_value_at(row, columns["id"]))
            if not identifier:
                continue
            records.append(
                {
                    "id": identifier,
                    "numeric_id": _parse_number(_value_at(row, columns["decimal"])),
                    "name": _clean_text(_value_at(row, columns["name"])),
                }
            )
    return records


def _parse_effects(content: str) -> List[Dict[str, object]]:
    required_columns = {
        "name": {"效果"},
        "decimal": {"ID"},
        "id": {"命名空间ID"},
    }
    records: List[Dict[str, object]] = []
    for table, rows, columns in _find_tables(_parse_tables(content), required_columns):
        header = _header_row(table)
        if header is None:
            continue
        for row in rows:
            if row is header:
                continue
            identifier = _clean_text(_value_at(row, columns["id"]))
            if not identifier:
                continue
            records.append(
                {
                    "id": identifier,
                    "numeric_id": _parse_number(_value_at(row, columns["decimal"])),
                    "name": _clean_text(_value_at(row, columns["name"])),
                }
            )
    return records


def _parse_enchantments(content: str) -> List[Dict[str, object]]:
    required_columns = {
        "name": {"附魔", "魔咒"},
        "id": {"名称"},
        "decimal": {"数字ID"},
    }
    records: List[Dict[str, object]] = []
    for table, rows, columns in _find_tables(_parse_tables(content), required_columns):
        header = _header_row(table)
        if header is None:
            continue
        for row in rows:
            if row is header:
                continue
            identifier = _clean_text(_value_at(row, columns["id"]))
            if not identifier:
                continue
            records.append(
                {
                    "id": identifier,
                    "numeric_id": _parse_number(_value_at(row, columns["decimal"])),
                    "name": _clean_text(_value_at(row, columns["name"])),
                }
            )
    return records


def _enum_member_name(identifier: str) -> str:
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", identifier)
    name = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_").upper()
    if not name:
        raise ValueError(f"无法根据 ID 生成枚举名：{identifier!r}")
    if name[0].isdigit():
        name = f"ID_{name}"
    return name


def _render_enum_members(
    records: Sequence[Dict[str, object]],
    newline: str,
    value_prefix: str = "",
) -> List[str]:
    members: List[str] = []
    used_names: Set[str] = set()
    for record in records:
        identifier = record.get("id")
        if not isinstance(identifier, str) or not identifier:
            raise ValueError(f"ID 数据缺少有效的字符串 id：{record!r}")

        member_name = _enum_member_name(identifier)
        if member_name in used_names:
            raise ValueError(f"ID 生成了重复的枚举名：{member_name}")
        used_names.add(member_name)
        value = (
            identifier
            if not value_prefix or ":" in identifier
            else f"{value_prefix}{identifier}"
        )
        members.append(
            f"    {member_name} = {json.dumps(value, ensure_ascii=False)}{newline}"
        )
        display_name = record.get("name")
        if not isinstance(display_name, str) or not display_name:
            raise ValueError(f"ID 数据缺少有效的中文名：{record!r}")
        punctuation = "" if display_name.endswith(("。", "！", "？")) else "。"
        members.append(f"    \"\"\" {display_name}{punctuation} \"\"\"{newline}")
    return members


def _read_member_documentation(
    lines: Sequence[str],
    start: int,
    end: int,
) -> Tuple[List[str], int]:
    documentation: List[str] = []
    index = start
    leading_blank_lines: List[str] = []
    while index < end:
        stripped = lines[index].strip()
        if not stripped:
            leading_blank_lines.append(lines[index])
            index += 1
            continue
        break

    if index == end or not (
        lines[index].strip().startswith("#")
        or lines[index].strip().startswith(('"""', "'''"))
    ):
        return [], start

    documentation.extend(leading_blank_lines)
    while index < end:
        stripped = lines[index].strip()
        if stripped.startswith("#"):
            documentation.append(lines[index])
            index += 1
            continue
        if stripped.startswith(('"""', "'''")):
            delimiter = stripped[:3]
            documentation.append(lines[index])
            if stripped.count(delimiter) < 2:
                index += 1
                while index < end:
                    documentation.append(lines[index])
                    if delimiter in lines[index]:
                        index += 1
                        break
                    index += 1
            else:
                index += 1
            continue
        break
    return documentation, index


def _replace_enum_class_body(
    body: str,
    records: Sequence[Dict[str, object]],
    newline: str,
    value_prefix: str = "",
) -> str:
    lines = body.splitlines(keepends=True)
    member_matches = [
        (index, match)
        for index, line in enumerate(lines)
        if (match := MEMBER_PATTERN.match(line)) is not None
    ]

    if member_matches:
        first_member_index = member_matches[0][0]
        last_member_index = member_matches[-1][0]
        _, last_documentation_end = _read_member_documentation(
            lines,
            last_member_index + 1,
            len(lines),
        )
        prefix = lines[:first_member_index]
        suffix = lines[last_documentation_end:]
        members = _render_enum_members(records, newline, value_prefix)
        return "".join(prefix + members + suffix)

    pass_index = next(
        (index for index, line in enumerate(lines) if line.strip() == "pass"),
        None,
    )
    members = _render_enum_members(records, newline, value_prefix)
    if pass_index is not None:
        return "".join(lines[:pass_index] + members + lines[pass_index + 1 :])

    insertion_index = len(lines)
    while insertion_index and not lines[insertion_index - 1].strip():
        insertion_index -= 1
    return "".join(lines[:insertion_index] + members + lines[insertion_index:])


def _update_enum_classes(content: str, data: Dict[str, object]) -> str:
    newline = "\r\n" if "\r\n" in content else "\n"
    lines = content.splitlines(keepends=True)
    class_matches: List[Tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = CLASS_PATTERN.match(line)
        if match is not None and match.group("name") in ENUM_CLASSES.values():
            class_matches.append((index, match.group("name")))

    found_classes = {class_name for _, class_name in class_matches}
    expected_classes = set(ENUM_CLASSES.values())
    if found_classes != expected_classes:
        missing_classes = ", ".join(sorted(expected_classes - found_classes))
        raise ValueError(f"enum.pyi 缺少指定的枚举类：{missing_classes}")

    class_spans: List[Tuple[int, int, str]] = []
    for header_index, class_name in class_matches:
        end_index = header_index + 1
        while end_index < len(lines):
            if lines[end_index].strip() and not lines[end_index][0].isspace():
                break
            end_index += 1
        class_spans.append((header_index + 1, end_index, class_name))

    for start_index, end_index, class_name in reversed(class_spans):
        category = next(
            category
            for category, target_class_name in ENUM_CLASSES.items()
            if target_class_name == class_name
        )
        records = data.get(category)
        if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
            raise ValueError(f"抓取结果缺少 {category} 枚举数据")
        body = "".join(lines[start_index:end_index])
        value_prefix = (
            MINECRAFT_NAMESPACE
            if category in ENUM_VALUE_PREFIX_CATEGORIES
            else ""
        )
        updated_body = _replace_enum_class_body(body, records, newline, value_prefix)
        lines[start_index:end_index] = updated_body.splitlines(keepends=True)

    return "".join(lines)


def _update_enum_file(data: Dict[str, object]) -> Path:
    shutil.copyfile(COMMON_ENUM_PYI, SCRIPT_ENUM_PYI)
    content = _read_text(SCRIPT_ENUM_PYI)
    _write_text(SCRIPT_ENUM_PYI, _update_enum_classes(content, data))
    return SCRIPT_ENUM_PYI


class WikiCrawler:
    def __init__(self, main_url: str = MAIN_URL, timeout: float = 30.0) -> None:
        self.main_url = main_url
        self.timeout = timeout
        parts = urlsplit(main_url)
        if not parts.scheme or not parts.netloc:
            raise ValueError("main_url must be an absolute HTTP(S) URL")
        self.site_root = f"{parts.scheme}://{parts.netloc}"

    def page_url(self, title: str) -> str:
        return f"{self.site_root}/w/{quote(title, safe='/-._')}"

    def fetch(self, url: str) -> str:
        request = Request(
            url,
            headers={
                "Accept": "text/html",
                "User-Agent": USER_AGENT,
            },
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset)
        except HTTPError as error:
            raise RuntimeError(f"获取维基页面失败（HTTP {error.code}）：{url}") from error

    def crawl(self) -> Dict[str, object]:
        main_content = self.fetch(self.main_url)
        page_content = {
            category: self.fetch(self.page_url(title))
            for category, title in PAGE_TITLES.items()
        }

        block_records = _parse_standard_ids(page_content["blocks"], {"方块"})
        data = {
            "block": [
                record
                for record in block_records
                if not str(record.get("id", "")).startswith("element_")
            ],
            "item": _parse_standard_ids(page_content["items"], {"物品"}),
            "entity": _parse_standard_ids(page_content["entities"], {"实体"}),
            "biome": _parse_biomes(page_content["biomes"]),
            "effect": _parse_effects(main_content),
            "enchantment": _parse_enchantments(main_content),
        }
        for category, records in data.items():
            if not records:
                raise ValueError(f"未能从维基页面解析出{category}数据")

        return {
            "source": self.main_url,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }


def _write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_name(f"{path.name}.tmp")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="抓取中文 Minecraft Wiki 的基岩版方块、物品、实体、生物群系、状态效果和魔咒 ID。"
    )
    parser.add_argument(
        "--url",
        default=MAIN_URL,
        help="基岩版数据值主页面 URL（默认：%(default)s）",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON 输出路径，使用 - 可输出到标准输出（默认：%(default)s）",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="单个页面的请求超时时间（秒，默认：%(default)s）",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_argument_parser().parse_args(argv)
    payload = WikiCrawler(args.url, args.timeout).crawl()
    data = payload["data"]
    if not isinstance(data, dict):
        raise ValueError("抓取结果的数据格式无效")
    for category, records in data.items():
        print(f"{category}: {len(records)}")

    enum_path = _update_enum_file(data)
    print(f"已更新 {enum_path}")

    if args.output == Path("-"):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        _write_json(args.output, payload)
        print(f"已写入 {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
