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


from collections import defaultdict
from importlib import import_module
from inspect import isfunction
from pkgutil import walk_packages
from threading import Thread
import time


TESTS = [
    ("core._types._checker"  , "case.test__checker"),
    ("core._utils"           , "case.test__utils"),
    ("core.listener"         , "case.test_listener"),
    ("core.server.comp"      , "case.test_comp"),

    ("common.enum"           , "case.test_enum"),
    ("common.utils"          , "case.test_utils"),
    ("common.mc_math.vector" , "case.test_vector"),
    ("common.mc_math.mc_math", "case.test_mc_math"),
    ("common.item"           , "case.test_item"),

    ("client.ui.screen_node" , "case.test_screen_node"),
    ("client.ui.nyc.control" , "case.test_control"),
]
IGNORE_DUPLICATE = [
    "<lambda>",
    "__benchmark__",
    "__imp",
    "nuoyanlib.core.client._lib_client.instance",
    "nuoyanlib.core.server._lib_server.instance",
]


try:
    timer = time.perf_counter
except AttributeError:
    timer = time.clock


from nuoyanlib.core import _env
_env.DEBUG = True


def import_test():
    # 导入测试
    import nuoyanlib.client
    def import_server():
        import nuoyanlib.server
    t = Thread(target=import_server)
    t.start()
    t.join()


def iter_library_modules():
    import nuoyanlib
    yield nuoyanlib
    for _, name, _ in walk_packages(nuoyanlib.__path__, nuoyanlib.__name__ + "."):
        yield import_module(name)


def iter_module_functions(module):
    for attr_name, function in module.__dict__.items():
        function_module = getattr(function, "__module__", "")
        if (
            isfunction(function)
            and (
                function_module == "nuoyanlib"
                or function_module.startswith("nuoyanlib.")
            )
        ):
            yield attr_name, function


def get_function_sides(func_path):
    path_parts = func_path.split(".")[:-1]
    if "client" in path_parts:
        return ("client",)
    if "server" in path_parts:
        return ("server",)
    return ("client", "server")


def has_duplicate_function(locations):
    side_counts = defaultdict(int)
    for func_path in locations:
        for side in get_function_sides(func_path):
            side_counts[side] += 1
    return any(count > 1 for count in side_counts.values())


def check_duplicate_functions():
    # 重名函数检查
    functions_by_name = defaultdict(list)
    visited = set()

    for module in iter_library_modules():
        for attr_name, func in iter_module_functions(module):
            func_name = func.__name__
            func_path = module.__name__ + "." + attr_name
            if func_name in IGNORE_DUPLICATE or func_path in IGNORE_DUPLICATE:
                continue
            func_id = id(func)
            if func_id in visited:
                continue
            visited.add(func_id)
            functions_by_name[func_name].append(func_path)

    duplicate_functions = dict(
        (name, locations)
        for name, locations in functions_by_name.items()
        if has_duplicate_function(locations)
    )

    if duplicate_functions:
        print("\n\033[31mDuplicate function names found:\033[0m")
        for name in sorted(duplicate_functions):
            print("%s:" % name)
            for p in duplicate_functions[name]:
                print("    %s" % p)
    print("")


def run_test():
    for target, case_module in TESTS:
        n = 1
        t = timer()
        for _ in range(n):
            import_module(case_module)
        cost = (timer() - t) * 1000
        print(
            "Test passed: {:<35}".format(target)
            + " in {:<12.3f} avg {:<6.3f} (ms)".format(cost, cost / n)
        )
    print("\n\033[33mAll tests passed.\033[0m")


def main():
    import_test()
    check_duplicate_functions()
    run_test()


if __name__ == "__main__":
    main()
