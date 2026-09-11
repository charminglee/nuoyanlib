# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-9
#  ⠀
#  ================================================


# todo：库函数精简
# todo：完善接口的异常处理
# todo：完善Ny控件
# todo：UI动画框架
# todo：Entity类、Player类，对事件返回的entityId、playerId进行封装（可编写一个装饰器，仅对使用该装饰器的事件启用该功能，节约性能）
# todo：event热更新
# todo：nbt
# todo：@async
# todo：运镜框架
# todo：容器UI
# todo：event_filter


__version__ = "1.0.0-beta.1"
__author__ = "Nuoyan"
__author_qq__ = "1279735247"
__author_email__ = "1279735247@qq.com"


import traceback
from mod.common.mod import Mod
from .core import _env, _logging


_mod_clients = []
_mod_servers = []


def _load_extensions(is_client):
    if _env.ROOT == "nuoyanlib":
        ext_module_path = "nuoyanlib.extensions"
    else:
        ext_module_path = _env.ROOT + ".nuoyanlib.extensions"
    try:
        ext_module = __imp(ext_module_path)
        ext_list = ext_module.EXTENSION_LOADING_LIST
    except (ImportError, AttributeError):
        return []

    loaded_ext = []
    for name in ext_list:
        path = "%s.%s.%s" % (ext_module_path, name, "client" if is_client else "server")
        try:
            __imp(path).init()
        except:
            traceback.print_exc()
            _logging.error("Extension loading failed: %s", path)
            continue
        loaded_ext.append(name)

    _logging.info("Extensions loaded: %s", loaded_ext)
    return loaded_ext


def _load_modules(is_client):
    if is_client:
        modules = _mod_clients
        registered_modules = _env.CLIENT_MODULES
    else:
        modules = _mod_servers
        registered_modules = _env.SERVER_MODULES
    if not modules:
        return

    for name, path in modules: # noqa
        if name in registered_modules:
            _logging.warning("Module already exists; skip loading: (%s) %s", name, path)
            continue

        try:
            module = __imp(path)
            registered_modules[name] = module
            _logging.info("Module loaded: (%s) %s", name, path)
        except:
            traceback.print_exc()


def _load_systems(is_client):
    if is_client:
        import mod.client.extraClientApi as api
        system_cls = api.GetClientSystemCls()
        registered_modules = _env.CLIENT_MODULES
        registered_systems = _env.CLIENT_SYSTEMS
    else:
        import mod.server.extraServerApi as api
        system_cls = api.GetServerSystemCls()
        registered_modules = _env.SERVER_MODULES
        registered_systems = _env.SERVER_SYSTEMS

    for module in registered_modules.values():
        for k, v in module.__dict__.items():
            if not isinstance(v, type) or not issubclass(v, system_cls):
                continue
            cls_path = module.__name__ + "." + k
            if api.GetSystem(_env.MOD_NAME, k):
                _logging.warning(
                    "%sSystem already exists; skip registration: (%s) %s",
                    "Client" if is_client else "Server", k, cls_path
                )
            else:
                system = api.RegisterSystem(_env.MOD_NAME, k, cls_path)
                registered_systems[(module.__name__, k)] = system
                _logging.info(
                    "%sSystem registered: (%s) %s",
                    "Client" if is_client else "Server", k, cls_path
                )


def run(mod_name, **kwargs):
    """
    启动「nuoyanlib」和模组客户端/服务端。

    说明
    ----

    请在 ``modMain.py`` 中调用本函数。

    客户端/服务端将按列表顺序加载。
    默认情况下，「nuoyanlib」会扫描各模块中的下列类，将其注册到运行环境并初始化。

    - 继承了 ``ClientSystem`` 或 ``NyClientSystem`` 的客户端类
    - 继承了 ``ServerSystem`` 或 ``NyServerSystem`` 的服务端类

    示例
    ----

    >>> import nuoyanlib
    >>> nuoyanlib.run(
    ...     "MyMod",
    ...     clients=[
    ...         ("MyClient1", "scripts.client.my_client1"),
    ...         ("MyClient2", "scripts.client.my_client2"),
    ...     ],
    ...     servers=[
    ...         ("MyServer1", "scripts.server.my_server1"),
    ...         ("MyServer2", "scripts.server.my_server2"),
    ...     ]
    ... )

    -----

    :param str mod_name: 模组名称
    :param list[tuple[str,str]]|None clients: [仅关键字参数] 模组客户端模块列表；每个元素为一个元组，包含客户端名称（请确保在当前模组环境下唯一）和模块路径；默认为 None
    :param list[tuple[str,str]]|None servers: [仅关键字参数] 模组服务端模块列表；每个元素为一个元组，包含服务端名称（请确保在当前模组环境下唯一）和模块路径；默认为 None
    :param dict|None globals: [仅关键字参数] 一般情况下无需传入，若抛出了 RuntimeError 导致模组加载失败，请尝试传入 globals()

    :return: 无
    :rtype: None

    :raise TypeError: 如果调用了多次 nuoyanlib.run() ，则传入的 mod_name 必须相同，否则抛出此异常
    :raise RuntimeError: 找不到 modMain.py 的 globals 字典时抛出，此时请通过 globals 参数手动传入
    """
    _logging.info("Start loading, version: %s, script: %s", __version__, _env.ROOT)

    if _env.MOD_NAME and _env.MOD_NAME != mod_name:
        raise TypeError(
            "cannot set the same mod_name to two different names '%s' and '%s'"
            % (_env.MOD_NAME, mod_name)
        )
    _env.MOD_NAME = mod_name
    if 'clients' in kwargs:
        _mod_clients.extend(kwargs['clients'] or [])
    if 'servers' in kwargs:
        _mod_servers.extend(kwargs['servers'] or [])

    if 'globals' in kwargs and isinstance(kwargs['globals'], dict):
        globals_ = kwargs['globals']
    else:
        import builtin_modules._inspect as _inspect # noqa
        for stack in _inspect.stack():
            if stack[1].endswith((".modMain", "modMain.py")):
                globals_ = stack[0].f_globals
                break
        else:
            raise RuntimeError(
                "FATAL ERROR!!! Stop loading mod because the globals of modMain.py not be found, "
                "please try manually passing the 'globals' parameter when calling nuoyanlib.run()"
            )
    if 'NuoyanLibMain' in globals_:
        return

    @Mod.Binding(_env.LIB_NAME, _env.LIB_VERSION)
    class NuoyanLibMain(object):
        @Mod.InitServer()
        def init_server(self):
            _env._THREAD_LOCAL.IS_CLIENT = False
            from .core.server._lib_server import NuoyanLibServerSystem
            if not NuoyanLibServerSystem.run():
                _logging.error("NuoyanLibServerSystem run failed!")
            _load_extensions(False)
            _load_modules(False)
            from .core.listener import _process_event_listen
            _process_event_listen()
            _load_systems(False)

        @Mod.InitClient()
        def init_client(self):
            _env._THREAD_LOCAL.IS_CLIENT = True
            from .core.client._lib_client import NuoyanLibClientSystem
            if not NuoyanLibClientSystem.run():
                _logging.error("NuoyanLibClientSystem run failed!")
            _load_extensions(True)
            _load_modules(True)
            from .core.listener import _process_event_listen
            _process_event_listen()
            _load_systems(True)

    globals_['NuoyanLibMain'] = NuoyanLibMain


def __imp(p):
    return (
        globals()
        ['\x5f\x5f\x62\x75\x69\x6c\x74\x69\x6e\x73\x5f\x5f']
        ['\x5f\x5f\x69\x6d\x70\x6f\x72\x74\x5f\x5f']
        (p, fromlist=[""])
    )












