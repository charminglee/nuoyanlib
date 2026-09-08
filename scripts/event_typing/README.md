本脚本用于生成与事件补全相关的 `.py` / `.pyi` 文件。

更新新版本事件时，只需修改 `all_events.py` 文件，然后运行 `main.py` 即可，运行后会在当前位置生成新的代码文件。

```powershell
.venv3\Scripts\python.exe scripts\event_typing\main.py
```