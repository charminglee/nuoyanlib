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


import os
from pathlib import Path
import shutil
import sys

from installer import (
    PACKAGE_DIRECTORY_NAME,
    SOURCE_DIRECTORY,
    install,
    is_ignored_name,
)


def get_icon_path() -> Path:
    bundle_directory = getattr(sys, "_MEIPASS", None)
    if bundle_directory is not None:
        return Path(bundle_directory) / "installer_icon.ico"
    return Path(__file__).resolve().parents[2] / "img" / "installer_icon.ico"


def run_installer_ui() -> int:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    root = tk.Tk()
    root.withdraw()
    root.iconbitmap(str(get_icon_path()))
    root.title("安装「nuoyanlib」")
    root.resizable(True, True)
    root.geometry("640x680")

    destination_var = tk.StringVar()
    copy_pyi_var = tk.BooleanVar(value=True)
    slim_install_var = tk.BooleanVar(value=False)
    install_ext_modules_var = tk.BooleanVar(value=False)
    open_after_install_var = tk.BooleanVar(value=True)

    style = ttk.Style(root)
    style.configure(
        "Preview.Treeview",
        rowheight=24,
        font=("Segoe UI", 9),
    )
    style.configure(
        "Preview.Treeview.Heading",
        font=("Segoe UI Semibold", 9),
    )
    style.map(
        "Preview.Treeview",
        background=[("selected", "#dbeafe")],
        foreground=[("selected", "#1e3a8a")],
    )
    style.configure(
        "Preview.Status.TLabel",
        foreground="#64748b",
    )

    container = ttk.Frame(root, padding=16)
    container.grid(row=0, column=0, sticky="nsew")
    container.columnconfigure(0, weight=1)
    container.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    path_frame = ttk.LabelFrame(container, text="安装路径", padding=8)
    path_frame.grid(sticky="ew")
    path_frame.columnconfigure(0, weight=1)

    path_entry = ttk.Entry(path_frame, textvariable=destination_var, width=52)
    path_entry.grid(sticky="ew", padx=(0, 8))

    def browse_destination():
        selected_path = filedialog.askdirectory(
            parent=root,
            title="选择「nuoyanlib」的安装目录",
        )
        if not selected_path:
            return
        if not (Path(selected_path) / "modMain.py").is_file():
            messagebox.showwarning(
                "路径无效",
                "所选路径下不存在 modMain.py 文件，请重新选择安装路径。",
                parent=root,
            )
            return
        destination_var.set(selected_path)

    ttk.Button(path_frame, text="浏览...", command=browse_destination, width=10).grid(row=0, column=1)

    options_frame = ttk.LabelFrame(container, text="安装选项", padding=8)
    options_frame.grid(sticky="ew", pady=(12, 0))

    ttk.Checkbutton(
        options_frame,
        text="复制 .pyi 文件",
        variable=copy_pyi_var,
    ).grid(sticky="w")
    ttk.Checkbutton(
        options_frame,
        text="安装扩展模块",
        variable=install_ext_modules_var,
    ).grid(sticky="w", pady=(4, 0))
    ttk.Checkbutton(
        options_frame,
        text="精简安装",
        variable=slim_install_var,
        state="disabled",
    ).grid(sticky="w", pady=(4, 0))
    ttk.Checkbutton(
        options_frame,
        text="安装后打开",
        variable=open_after_install_var,
    ).grid(sticky="w", pady=(4, 0))

    preview_frame = ttk.LabelFrame(container, text="预览", padding=8)
    preview_frame.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
    preview_frame.columnconfigure(0, weight=1)
    preview_frame.rowconfigure(1, weight=1)

    preview_tree = ttk.Treeview(
        preview_frame,
        columns=("type",),
        displaycolumns=("type",),
        show="tree headings",
        height=12,
        selectmode="browse",
        style="Preview.Treeview",
    )
    preview_tree.heading("#0", text="安装后文件结构", anchor="w")
    preview_tree.heading("type", text="类型", anchor="w")
    preview_tree.column("#0", width=500, minwidth=280, anchor="w")
    preview_tree.column("type", width=90, minwidth=70, stretch=False, anchor="w")
    preview_tree.grid(row=1, column=0, sticky="nsew")

    preview_scrollbar = ttk.Scrollbar(
        preview_frame,
        orient="vertical",
        command=preview_tree.yview,
    )
    preview_scrollbar.grid(row=1, column=1, sticky="ns")
    preview_tree.configure(yscrollcommand=preview_scrollbar.set)

    preview_horizontal_scrollbar = ttk.Scrollbar(
        preview_frame,
        orient="horizontal",
        command=preview_tree.xview,
    )
    preview_horizontal_scrollbar.grid(row=2, column=0, sticky="ew", pady=(6, 0))
    preview_tree.configure(xscrollcommand=preview_horizontal_scrollbar.set)

    preview_tree.tag_configure("root", foreground="#1d4ed8")
    preview_tree.tag_configure("target", foreground="#047857")
    preview_tree.tag_configure("existing_directory", foreground="#334155")
    preview_tree.tag_configure("existing_file", foreground="#64748b")
    preview_tree.tag_configure("installed_directory", foreground="#047857")
    preview_tree.tag_configure("installed_file", foreground="#059669")
    preview_tree.tag_configure("warning", foreground="#b45309")

    def is_valid_destination(path_text: str) -> bool:
        destination_path = Path(path_text).expanduser()
        return (
            destination_path.is_dir()
            and (destination_path / "modMain.py").is_file()
        )

    def get_sorted_children(source_directory: Path) -> list[Path]:
        return sorted(
            source_directory.iterdir(),
            key=lambda child: (not child.is_dir(), child.name.lower()),
        )

    def get_preview_children(
        source_directory: Path,
        copy_pyi: bool,
        copy_extensions: bool,
    ) -> list[Path]:
        return [
            child_path
            for child_path in get_sorted_children(source_directory)
            if not is_ignored_name(
                child_path.name,
                copy_pyi=copy_pyi,
                copy_extensions=copy_extensions,
            )
        ]

    def add_preview_node(
        parent_id: str,
        source_path: Path,
        copy_pyi: bool,
        copy_extensions: bool,
        expanded: bool = False,
    ) -> None:
        is_directory = source_path.is_dir() and not source_path.is_symlink()
        node_id = preview_tree.insert(
            parent_id,
            "end",
            text=source_path.name,
            values=("文件夹" if is_directory else "文件",),
            tags=("installed_directory" if is_directory else "installed_file",),
            open=expanded,
        )
        if not is_directory:
            return

        for child_path in get_preview_children(
            source_path,
            copy_pyi,
            copy_extensions,
        ):
            add_preview_node(
                node_id,
                child_path,
                copy_pyi,
                copy_extensions,
            )

    def add_existing_node(
        parent_id: str,
        source_path: Path,
        expanded: bool = False,
    ) -> None:
        is_link = source_path.is_symlink()
        is_directory = source_path.is_dir() and not is_link
        if is_link:
            item_type = "已有链接"
        elif is_directory:
            item_type = "已有文件夹"
        else:
            item_type = "已有文件"
        node_id = preview_tree.insert(
            parent_id,
            "end",
            text=source_path.name,
            values=(item_type,),
            tags=("existing_directory" if is_directory else "existing_file",),
            open=expanded,
        )
        if not is_directory:
            return

        for child_path in get_sorted_children(source_path):
            add_existing_node(node_id, child_path)

    def add_preview_children(
        parent_id: str,
        source_directory: Path,
        copy_pyi: bool,
        copy_extensions: bool,
    ) -> None:
        for child_path in get_preview_children(
            source_directory,
            copy_pyi,
            copy_extensions,
        ):
            add_preview_node(
                parent_id,
                child_path,
                copy_pyi,
                copy_extensions,
            )

    def add_installation_node(
        parent_id: str,
        target_path: Path,
        copy_pyi: bool,
        copy_extensions: bool,
    ) -> None:
        target_id = preview_tree.insert(
            parent_id,
            "end",
            text=PACKAGE_DIRECTORY_NAME,
            values=("覆盖安装" if target_path.exists() else "将安装",),
            tags=("target",),
            open=True,
        )
        if not SOURCE_DIRECTORY.is_dir():
            preview_tree.insert(
                target_id,
                "end",
                text="无法读取安装源文件",
                values=("预览失败",),
                tags=("warning",),
            )
            return

        add_preview_children(
            target_id,
            SOURCE_DIRECTORY,
            copy_pyi,
            copy_extensions,
        )

    def add_destination_children(
        parent_id: str,
        destination_path: Path,
        copy_pyi: bool,
        copy_extensions: bool,
    ) -> None:
        target_name = PACKAGE_DIRECTORY_NAME.lower()
        existing_target = None
        existing_children = []
        for child_path in get_sorted_children(destination_path):
            if child_path.name.lower() == target_name:
                existing_target = child_path
            else:
                existing_children.append(child_path)

        target_path = existing_target or (destination_path / PACKAGE_DIRECTORY_NAME)
        all_children = existing_children + [target_path]
        all_children.sort(
            key=lambda child: (
                not (
                    child.name.lower() == target_name
                    or (child.is_dir() and not child.is_symlink())
                ),
                child.name.lower(),
            )
        )
        for child_path in all_children:
            if child_path.name.lower() == target_name:
                add_installation_node(
                    parent_id,
                    child_path,
                    copy_pyi,
                    copy_extensions,
                )
            else:
                add_existing_node(parent_id, child_path)

    def refresh_preview(*_args) -> None:
        preview_tree.delete(*preview_tree.get_children())
        destination_text = destination_var.get().strip()
        if not destination_text:
            return

        destination_path = Path(destination_text).expanduser()
        root_id = preview_tree.insert(
            "",
            "end",
            text=str(destination_path),
            values=("所选目录",),
            tags=("root",),
            open=True,
        )
        if not is_valid_destination(destination_text):
            preview_tree.insert(
                root_id,
                "end",
                text="请重新选择包含 modMain.py 的文件夹",
                values=("无法预览",),
                tags=("warning",),
            )
            return

        add_destination_children(
            root_id,
            destination_path,
            copy_pyi_var.get(),
            install_ext_modules_var.get(),
        )

    destination_var.trace_add("write", refresh_preview)
    copy_pyi_var.trace_add("write", refresh_preview)
    install_ext_modules_var.trace_add("write", refresh_preview)

    def install_package():
        destination_text = destination_var.get().strip()
        if not destination_text:
            messagebox.showwarning("提示", "请选择安装路径。", parent=root)
            path_entry.focus_set()
            return
        if not is_valid_destination(destination_text):
            messagebox.showwarning(
                "路径无效",
                "所选路径下不存在 modMain.py 文件，请重新选择安装路径。",
                parent=root,
            )
            path_entry.focus_set()
            return

        try:
            target = install(
                destination_text,
                copy_pyi=copy_pyi_var.get(),
                copy_extensions=install_ext_modules_var.get(),
            )
        except (OSError, ValueError, shutil.Error) as error:
            messagebox.showerror("安装失败", "安装「nuoyanlib」时发生错误：\n{}".format(error), parent=root)
            return

        messagebox.showinfo(
            "安装完成",
            "已将「nuoyanlib」安装到 {}".format(target),
            parent=root,
        )
        if open_after_install_var.get():
            try:
                os.startfile(target)
            except OSError as error:
                messagebox.showerror(
                    "打开失败",
                    "无法打开安装目录：\n{}".format(error),
                    parent=root,
                )
        root.destroy()

    buttons_frame = ttk.Frame(container)
    buttons_frame.grid(row=3, column=0, sticky="e", pady=(16, 0))
    ttk.Button(buttons_frame, text="安装", command=install_package).grid(padx=(0, 8))
    ttk.Button(buttons_frame, text="取消", command=root.destroy).grid(row=0, column=1)

    path_entry.focus_set()
    root.update_idletasks()
    root.deiconify()
    root.mainloop()
    return 0
