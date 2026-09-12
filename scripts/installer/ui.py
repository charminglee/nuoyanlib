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

from installer import install


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
    root.resizable(False, False)

    destination_var = tk.StringVar()
    copy_pyi_var = tk.BooleanVar(value=True)
    slim_install_var = tk.BooleanVar(value=False)
    install_ext_modules_var = tk.BooleanVar(value=False)
    open_after_install_var = tk.BooleanVar(value=True)

    container = ttk.Frame(root, padding=16)
    container.grid(sticky="nsew")
    container.columnconfigure(0, weight=1)

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
        if selected_path:
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

    def install_package():
        destination_text = destination_var.get().strip()
        if not destination_text:
            messagebox.showwarning("提示", "请选择安装路径。", parent=root)
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
    buttons_frame.grid(row=2, column=0, sticky="e", pady=(16, 0))
    ttk.Button(buttons_frame, text="安装", command=install_package).grid(padx=(0, 8))
    ttk.Button(buttons_frame, text="取消", command=root.destroy).grid(row=0, column=1)

    path_entry.focus_set()
    root.update_idletasks()
    root.deiconify()
    root.mainloop()
    return 0
