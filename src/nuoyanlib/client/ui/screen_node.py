# -*- coding: utf-8 -*-
#  ================================================
#  ⠀
#    Copyright (c) 2026 Nuoyan
#  ⠀
#    Author: Nuoyan <https://github.com/charminglee>
#    Email : 1279735247@qq.com
#    Date  : 2026-9-11
#  ⠀
#  ================================================


from types import MethodType
import time
import itertools
import fnmatch
import mod.client.extraClientApi as api
from ...core.client.comp import CustomUIScreenProxy, ScreenNode, ViewBinder
from ...core import _logging, error, _env
from ...core.listener import is_listened, listen_event, unlisten_event, event
from ...core._utils import iter_obj_attrs, kwargs_defaults, try_exec, get_func, dualmethod
from ..setting import read_setting, save_setting
from .ui_utils import _UIControlType, _is_ui_registered, is_top_ui
from .nyc import NyControl, NyButton


__all__ = [
    "screen",
    "screen_proxy",
    "NyScreenNode",
    "NyScreenProxy",
]


NativeScreenManager = api.GetNativeScreenManagerCls().instance()


_is_ui_init_finished = False
_auto_show_screens = []
_proxy_screens = []


# @event
# def PushScreenEvent(args):
#     print(args)


@event(priority=999)
def UiInitFinished(args):
    global _is_ui_init_finished, _proxy_screens
    _is_ui_init_finished = True
    for screen in _auto_show_screens:
        if not screen.instance():
            screen.show()
    for screen in _proxy_screens:
        screen.register_proxy()
    _proxy_screens = []


@kwargs_defaults(
    is_hud=False,
    bind_entity_id=None,
    bind_offset=(0, 1, 0),
    bind_world_position=None,
    auto_scale=True,
    mini_map_root_path="",
    auto_show=True,
    push_to_ui_stack=False,
    enabled_deferred_init=False,
)
def screen(namespace, name="main", **kwargs):
    """
    [装饰器]

    注册一个UI界面，并为其设置创建方式和显示行为。

    说明
    ----

    装饰器会将界面配置保存为类属性，可通过 ``.`` 进行访问，如 ``MyScreen.is_hud`` 。

    示例
    ----

    >>> @nyl.screen(
    ...     "my_ui",
    ...     "main",
    ...     is_hud=True,
    ...     enabled_deferred_init=True
    ... )
    ... class MyScreen(nyl.NyScreenNode):
    ...     def __init__(self, namespace, name, param):
    ...         super(MyScreen, self).__init__(namespace, name, param)
    ...         self.button = nyl.NyButton(self, "/panel/button")
    ...         self.button.set_callback(self.on_button_up, nyl.NyButton.UP)
    ...
    ...     def on_button_up(self, args):
    ...         pass

    参见
    ----

    - ``NyScreenNode`` -- ScreenNode 扩展类。

    -----

    :param str namespace: UI命名空间，对应 UI json 中 "namespace" 字段的值
    :param str name: UI画布名称，对应 UI json 中想要创建的画布的名称；默认为 "main"
    :param bool is_hud: 是否为 HUD 界面的UI，默认为 False ；若设为 True ，UI生效时将屏蔽游戏原生操作
    :param str|None bind_entity_id: 绑定的实体ID，默认为 None；若传入这个参数， is_hud 强制为 True
    :param tuple[float,float,float] bind_offset: 与绑定实体的偏移量，默认为 (0, 1, 0)
    :param tuple[int,tuple[float,float,float]]|None bind_world_position: 第一个元素为绑定的维度，第二个为世界坐标，默认为 None；若传入这个参数， auto_scale 默认为 True ， is_hud 强制为 True ，其他参数无效
    :param bool auto_scale: 绑定实体或世界坐标时是否会自动根据目标与本地玩家的距离动态缩放UI大小，默认为 True
    :param str mini_map_root_path: 小地图控件根路径，默认为空字符串
    :param bool auto_show: 是否在 UiInitFinished 事件触发后自动创建并显示UI，默认为 True
    :param bool push_to_ui_stack: 是否使用堆栈管理的方式（Push）创建UI，默认为 False
    :param bool enabled_deferred_init: 是否启用延迟初始化，默认为 False ；开启后UI类的 __init__() 方法将推迟到UI创建完毕后触发，此时可以在 __init__() 方法内正常执行各种UI控件接口，从而不必写在 __ui_create__() 方法里。
    """
    def decorator(cls):
        cls.namespace = namespace
        cls.name = name
        cls.full_name = namespace + "." + name
        for k, v in kwargs.items():
            setattr(cls, k, v)
        auto_show = kwargs['auto_show']
        if auto_show:
            _auto_show_screens.append(cls)
            if _is_ui_init_finished:
                cls.show()
        return cls
    return decorator


@kwargs_defaults(
    enabled_deferred_init=False,
)
def screen_proxy(namespace, name, **kwargs):
    """
    [装饰器]

    注册UI界面代理。

    代理将自动执行，无需调用 ``RegisterScreenProxy()`` 接口。

    说明
    ----

    装饰器会将界面配置保存为类属性，可通过 ``.`` 进行访问，如 ``MyScreen.enabled_deferred_init`` 。

    示例
    ----

    >>> @nyl.screen_proxy(
    ...     "hud",
    ...     "hud_screen",
    ...     enabled_deferred_init=True
    ... )
    ... class MyScreen(nyl.NyScreenProxy):
    ...     def __init__(self, namespace, name, param):
    ...         super(MyScreen, self).__init__(namespace, name, param)

    参见
    ----

    - ``NyScreenProxy`` -- 用于UI界面代理，功能与 NyScreenNode 相同。

    -----

    :param str namespace: 要代理的UI命名空间，对应 UI json 中 "namespace" 字段的值
    :param str name: 要代理的UI画布名称，对应 UI json 中画布的名称
    :param bool enabled_deferred_init: 是否启用延迟初始化，默认为 False ；开启后UI类的 __init__() 方法将推迟到UI创建完毕后触发，此时可以在 __init__() 方法内正常执行各种UI控件接口，从而不必写在 OnCreate() 方法里。
    """
    def decorator(cls):
        cls.namespace = namespace
        cls.name = name
        cls.full_name = namespace + "." + name
        for k, v in kwargs.items():
            setattr(cls, k, v)
        if (namespace == "hud" and name == "hud_screen") or _is_ui_init_finished:
            cls.register_proxy()
        else:
            _proxy_screens.append(cls)
        return cls
    return decorator


class NyScreenBase(object):
    """
    ``NyScreenNode`` 与 ``NyScreenProxy`` 共用的UI生命周期和接口基类。

    说明
    ----

    该类为内部基类，不应直接继承使用。

    参见
    ----

    - ``NyScreenNode`` -- 用于创建自定义UI界面。
    - ``NyScreenProxy`` -- 用于UI界面代理，功能与 NyScreenNode 相同。
    """

    if _env.DEBUG:
        n = 0

    ROOT_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"
    AUTO_SAVE_INTERVAL = 30 * 30

    namespace = ""
    name = ""
    full_name = ""
    is_hud = False
    bind_entity_id = None
    bind_offset = (0, 1, 0)
    bind_world_position = None
    auto_scale = True
    mini_map_root_path = ""
    auto_show = True
    push_to_ui_stack = False
    enabled_deferred_init = False

    def __init__(self):
        if _env.DEBUG:
            NyScreenBase.n += 1 # noqa

        self._screen_node = None
        self._nyc_cache_map = {}
        self._ui_pos_data_key = ""
        self._ui_pos_data = {}
        self._ui_default_pos_data = {}
        self._frame_anim_data = {}
        self._binging_data = {}
        self._tick = 0
        self._is_dirty = False
        self.root_panel = None
        self.has_created = False
        self.is_base_screen = False
        self.is_destroyed  = False

        cls = self.__class__
        if not hasattr(cls, '_nyl__instances'):
            cls._nyl__instances = []
        cls._nyl__instances.append(self)

    def __ui_create__(self):
        """
        UI生命周期函数，UI创建完成时调用。

        示例
        ----

        >>> def __ui_create__(self):
        ...     super(MyScreen, self).__ui_create__()

        -----

        :return: 无
        :rtype: None
        """
        if self.is_control_exist(self.ROOT_PANEL_PATH):
            self.root_panel = NyControl(self, self.ROOT_PANEL_PATH)
            self.is_base_screen = True
        else:
            self.root_panel = NyControl(self, "")

        self._ui_pos_data_key = "nyl_ui_pos_data_v2_%s" % self.full_name
        self._ui_pos_data = self._get_all_ui_pos_data()
        for path, pos in self._ui_pos_data.items():
            try:
                nyc = NyControl(self, path)
            except error.ControlNotFoundError:
                continue
            self._ui_default_pos_data[path] = nyc.position
            nyc.position = pos

        self._process_button_callback()

    def __ui_destroy__(self):
        """
        UI生命周期函数，UI销毁时调用。

        示例
        ----

        >>> def __ui_destroy__(self):
        ...     super(MyScreen, self).__ui_destroy__()

        -----

        :return: 无
        :rtype: None
        """
        if self.is_destroyed:
            return
        unlisten_event(self.GameRenderTickEvent)
        for nyc in self._nyc_cache_map.values():
            try_exec(nyc.__ui_destroy__)
        self._save_all_ui_pos_data()
        self.__class__._nyl__instances.remove(self)
        self._screen_node = None
        self._nyc_cache_map = None
        self._ui_pos_data_key = ""
        self._ui_pos_data = None
        self._ui_default_pos_data = None
        self._frame_anim_data = None
        self._binging_data = None
        self._is_dirty = False
        self.root_panel = None
        self.has_created = False
        self.is_destroyed  = True

    def __ui_update__(self):
        """
        每帧调用， 1 秒有 30 帧。

        示例
        ----

        >>> def __ui_update__(self):
        ...     super(MyScreen, self).__ui_update__()

        -----

        :return: 无
        :rtype: None
        """
        try:
            if self.is_destroyed:
                return

            self._tick += 1
            if self._tick % self.AUTO_SAVE_INTERVAL == 0 and self._is_dirty:
                self._save_all_ui_pos_data()
        except AttributeError:
            pass

    def __ui_deactive__(self):
        """
        UI生命周期函数，当栈顶UI有其他UI入栈时调用。

        示例
        ----

        >>> def __ui_deactive__(self):
        ...     super(MyScreen, self).__ui_deactive__()

        -----

        :return: 无
        :rtype: None
        """

    def __ui_active__(self):
        """
        UI生命周期函数，当UI重新回到栈顶时调用。

        示例
        ----

        >>> def __ui_active__(self):
        ...     super(MyScreen, self).__ui_active__()

        -----

        :return: 无
        :rtype: None
        """

    # region Common APIs ===============================================================================================

    @property
    def is_on_top(self):
        """
        [只读属性]

        当前界面是否位于栈顶。

        :rtype: bool
        """
        if self.is_destroyed:
            return False
        return is_top_ui(self.full_name)

    @classmethod
    def instance(cls):
        """
        [类方法]

        获取UI界面实例。

        示例
        ----

        >>> screen = MyScreen.instance()
        >>> if screen:
        ...     screen.hide()

        参见
        ----

        - ``NyScreenBase.all_instances()`` -- 获取当前UI界面的全部实例。

        -----

        :return: UI界面实例；若无实例则返回 None ；若当前UI同时存在多个实例，返回最后创建且未销毁的实例
        :rtype: NyScreenNode|NyScreenProxy|None
        """
        if not hasattr(cls, '_nyl__instances') or not cls._nyl__instances:
            return
        return cls._nyl__instances[-1]

    @classmethod
    def all_instances(cls):
        """
        [类方法]

        获取当前UI界面的所有实例。

        说明
        ----

        返回的列表按实例创建顺序排序，且随UI实例的创建和销毁实时更新。

        示例
        ----

        >>> for screen in MyScreen.all_instances():
        ...     screen.hide()

        参见
        ----

        - ``NyScreenBase.instance()`` -- 获取最后创建的UI界面实例。
        - ``NyScreenBase.create_new()`` -- 创建新的UI界面实例。

        -----

        :return: UI界面实例列表；若无实例则返回空列表
        :rtype: list[NyScreenNode|NyScreenProxy]
        """
        if not hasattr(cls, '_nyl__instances'):
            return []
        return cls._nyl__instances

    @dualmethod
    def show(self):
        """
        显示UI界面。

        说明
        ----

        本方法有两种调用方式：

        - 类调用： ``MyScreen.show()`` ；若该UI界面尚未创建任何实例，则自动创建并显示；若已存在实例，则将最后创建且未销毁的UI界面设为显示。
        - 实例调用： ``screen.show()`` ；显示指定UI界面实例。

        示例
        ----

        >>> @nyl.screen(
        ...     "my_screen",
        ...     "main",
        ...     is_hud=False,
        ...     push_to_ui_stack=True,
        ...     auto_show=False,
        ... )
        ... class MyScreen(nyl.NyScreenNode):
        ...     def __init__(self, namespace, name, param):
        ...         super(MyScreen, self).__init__(namespace, name, param)
        ...
        >>> @nyl.event
        ... def UiInitFinished(args):
        ...     screen = MyScreen.show()

        参见
        ----

        - ``NyScreenBase.hide()`` -- 隐藏UI界面。
        - ``NyScreenBase.create_new()`` -- 创建新的UI界面实例并显示。
        - ``NyScreenBase.destroy()`` -- 销毁UI界面。

        -----

        :return: 返回显示的UI界面实例
        :rtype: NyScreenNode|NyScreenProxy|None
        """
        if isinstance(self, type):
            inst = self.instance()
            if not inst:
                inst = self.create_new()
        else:
            inst = self

        if not inst:
            return
        if inst.is_destroyed:
            return

        if inst.push_to_ui_stack:
            return inst
        inst._screen_node.SetScreenVisible(True)
        return inst

    @dualmethod
    def hide(self):
        """
        隐藏UI界面。

        说明
        ----

        本方法有两种调用方式：

        - 类调用： ``MyScreen.hide()`` ；将最后创建且未销毁的UI界面设为隐藏；若该界面尚未创建实例，则不执行任何操作。
        - 实例调用： ``screen.hide()`` ；隐藏指定UI界面实例。

        对于使用堆栈管理的UI，仅当其在栈顶时才能隐藏。

        示例
        ----

        >>> for screen in MyScreen.all_instances():
        ...     screen.hide()

        参见
        ----

        - ``NyScreenBase.show()`` -- 显示UI界面。
        - ``NyScreenBase.destroy()`` -- 销毁UI界面。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if isinstance(self, type):
            inst = self.instance()
            if not inst:
                return False
        else:
            inst = self

        if inst.is_destroyed:
            return False

        if inst.push_to_ui_stack:
            if inst.is_on_top:
                return api.PopScreen()
            else:
                return False
        else:
            inst._screen_node.SetScreenVisible(False)
            return True

    @classmethod
    def create_new(cls, param=None):
        """
        [类方法]

        创建一个新的UI界面实例并显示。

        同一个UI界面可同时创建多个实例。区别于 ``.show()`` 方法，本方法每次调用都会创建一个新实例。

        示例
        ----

        >>> MyScreen.create_new({'offset': (0, 1, 0)})
        <MyScreen object>

        参见
        ----

        - ``NyScreenBase.hide()`` -- 隐藏UI界面。
        - ``NyScreenBase.destroy()`` -- 销毁UI界面。

        -----

        :param dict|None param: UI创建参数，会传到UI类的 __init__() 方法中；默认为 None

        :return: UI界面实例，创建失败时返回 None
        :rtype: NyScreenNode|NyScreenProxy|None
        """
        ui_key = cls.namespace
        ui_def = cls.full_name
        cls_path = _env.get_cls_path(cls)
        if not _is_ui_registered(ui_key):
            api.RegisterUI(_env.MOD_NAME, ui_key, cls_path, ui_def)

        if cls.push_to_ui_stack:
            node = api.PushScreen(_env.MOD_NAME, ui_key, param)
        else:
            if cls.bind_world_position:
                _param = {
                    'bindWorldPosition': cls.bind_world_position,
                    'autoScale': int(cls.auto_scale),
                }
            elif cls.bind_entity_id:
                _param = {
                    'isHud': 1,
                    'bindEntityId': cls.bind_entity_id,
                    'bindOffset': cls.bind_offset,
                    'autoScale': int(cls.auto_scale),
                }
            else:
                _param = {
                    'isHud': int(cls.is_hud),
                }
            if param:
                _param.update(param)
            node = api.CreateUI(_env.MOD_NAME, ui_key, _param)
        return node

    @dualmethod
    def destroy(self):
        """
        销毁UI界面。

        说明
        ----

        本方法有两种调用方式：

        - 类调用： ``MyScreen.destroy()`` ；对最后创建且未销毁的UI界面进行销毁；若该界面尚未创建实例，则不执行任何操作。
        - 实例调用： ``screen.destroy()`` ；销毁指定UI界面实例。

        对于使用堆栈管理的UI，仅当其在栈顶时才能销毁。

        示例
        ----

        >>> for screen in MyScreen.all_instances():
        ...     screen.destroy()

        参见
        ----

        - ``NyScreenBase.hide()`` -- 隐藏UI界面。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if isinstance(self, type):
            inst = self.instance()
            if not inst:
                return False
        else:
            inst = self

        if not inst:
            return False
        if inst.is_destroyed:
            return False

        if inst.push_to_ui_stack:
            if inst.is_on_top:
                inst.__ui_destroy__()
                return api.PopScreen()
            else:
                return False
        else:
            inst.__ui_destroy__()
            inst._screen_node.SetRemove()
            return True

    def build_binding(self, func, flag, binding_name="", collection_name=""):
        """
        动态创建绑定（无需依赖 ``@ViewBinder`` 装饰器）。

        示例
        ----

        >>> def label_binding():
        ...     return "动态绑定文本"
        ...
        >>> self.build_binding(label_binding, ViewBinder.BF_BindString)
        True

        集合绑定需要同时传入集合名称：

        >>> def cell_visible(index):
        ...     return index <= 36
        ...
        >>> self.build_binding(
        ...     cell_visible,
        ...     ViewBinder.BF_BindBool,
        ...     collection_name="item_grid",
        ... )
        True

        参见
        ----

        - ``NyScreenBase.unbuild_binding()`` -- 移除动态创建的绑定。

        -----

        :param function func: 绑定函数，支持普通函数与实例方法
        :param int flag: 绑定标志，请使用 ViewBinder 枚举值
        :param str binding_name: 绑定名称；若不传入该参数，则自动生成绑定名称，格式为 "#<namespace>.<func_name>" ， <namespace> 为 UI json 文件中 "namespace" 字段的值， <func_name> 为绑定函数名
        :param str collection_name: 集合名称；若非集合绑定，忽略该参数即可；默认为空字符串

        :return: 是否成功
        :rtype: bool
        """
        if self.is_destroyed:
            return False
        if not binding_name:
            binding_name = "#%s.%s" % (self._screen_node.namespace, func.__name__)
        is_collection = bool(collection_name)

        proxy = self._create_binding_proxy(func, flag, binding_name, collection_name)
        if not proxy:
            return False
        if isinstance(func, MethodType):
            key = (func.__func__, func.__self__)
        else:
            key = func
        if key in self._binging_data:
            return False
        self._binging_data[key] = (proxy, is_collection)

        if is_collection:
            self._screen_node._process_collection(proxy, self._screen_node.screen_name) # noqa
        else:
            self._screen_node._process_default(proxy, self._screen_node.screen_name) # noqa
        return True

    def _create_binding_proxy(self, func, flag, binding_name="", collection_name=""):
        if self.is_destroyed:
            return
        if collection_name:
            binding = ViewBinder.binding_collection(flag, collection_name, binding_name)
        else:
            binding = ViewBinder.binding(flag, binding_name)
        proxy = binding(lambda *a: func(*a))
        name = "_nyl__binding_%s_%s" % (func.__name__, id(func))
        proxy.__name__ = name
        setattr(self._screen_node, name, proxy)
        return proxy

    def unbuild_binding(self, func):
        """
        移除通过 ``.build_binding()`` 动态创建的绑定。

        示例
        ----

        >>> def label_binding():
        ...     return "动态绑定文本"
        ...
        >>> self.build_binding(label_binding, ViewBinder.BF_BindString)
        True
        >>> self.unbuild_binding(label_binding)
        True

        参见
        ----

        - ``NyScreenBase.build_binding()`` -- 创建动态绑定。

        -----

        :param function func: 绑定函数

        :return: 是否成功
        :rtype: bool
        """
        if self.is_destroyed:
            return False
        if isinstance(func, MethodType):
            key = (func.__func__, func.__self__)
        else:
            key = func
        if key in self._binging_data:
            proxy, is_collection = self._binging_data.pop(key)
        else:
            return False

        if is_collection:
            self._screen_node._process_collection_unregister(proxy, self._screen_node.screen_name) # noqa
        else:
            self._screen_node._process_default_unregister(proxy, self._screen_node.screen_name) # noqa
        return True

    def is_control_exist(self, path):
        """
        判断指定路径的控件是否存在。

        示例
        ----

        >>> if self.is_control_exist("/panel/button"):
        ...     self.button = nyl.NyButton(self, "/panel/button")

        -----

        :param str path: 控件路径

        :return: 控件是否存在
        :rtype: bool
        """
        if self.is_destroyed:
            return False
        if _env.DEBUG:
            return True
        screen_name = self._screen_node.screen_name
        full_path = self._screen_node.component_path + path
        return NyScreenBase.__get_control_type(screen_name, full_path) != _UIControlType.UNKNOWN # noqa

    def reset_all_ui_pos(self):
        """
        将所有保存过位置数据的控件恢复到默认位置。

        说明
        ----

        默认位置指的是 UI json 中保存的原始位置。

        示例
        ----

        >>> self.reset_all_ui_pos()
        True

        参见
        ----

        - ``NyScreenBase.clear_all_ui_pos_data()`` -- 删除所有已保存的控件位置数据。
        - ``NyControl.reset_pos()`` -- 将指定控件恢复到默认位置。
        - ``NyControl.save_pos()`` -- 保存指定控件的位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if self.is_destroyed:
            return False
        if not self._ui_pos_data_key:
            return False
        self._ui_pos_data.update(self._ui_default_pos_data)
        self._is_dirty = True
        self._update_all_ui_pos()
        return True

    def _update_all_ui_pos(self):
        if self.is_destroyed:
            return
        for path, pos in self._ui_pos_data.items():
            try:
                if path in self._nyc_cache_map:
                    nyc = self._nyc_cache_map[path]
                else:
                    nyc = NyControl(self, path)
                nyc.position = pos
            except error.ControlNotFoundError:
                continue

    def clear_all_ui_pos_data(self):
        """
        删除所有已保存的控件位置数据。

        删除后，下一次创建UI时不再恢复控件位置。

        说明
        ----

        只删除数据，不影响控件当前的位置。如需恢复到默认位置请使用 ``.reset_all_ui_pos()`` 。

        示例
        ----

        >>> self.clear_all_ui_pos_data()
        True

        参见
        ----

        - ``NyScreenBase.reset_all_ui_pos()`` -- 将所有保存过位置数据的控件恢复到默认位置。
        - ``NyControl.clear_pos_data()`` -- 删除指定控件的位置数据。
        - ``NyControl.save_pos()`` -- 保存指定控件的位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if self.is_destroyed:
            return False
        if not self._ui_pos_data_key:
            return False
        self._ui_pos_data.clear()
        self._is_dirty = True
        return True

    def _set_ui_pos_data(self, path, pos):
        if self.is_destroyed:
            return
        if pos is None:
            self._ui_pos_data.pop(path, None)
        else:
            self._ui_pos_data[path] = pos
        self._is_dirty = True

    def _set_ui_default_pos_data(self, path, pos):
        if self.is_destroyed:
            return
        if pos:
            self._ui_default_pos_data[path] = pos

    def _save_all_ui_pos_data(self):
        if self.is_destroyed:
            return
        if save_setting(self._ui_pos_data_key, self._ui_pos_data, False):
            self._is_dirty = False
        else:
            _logging.error("Failed to save UI position data for key: %s", self._ui_pos_data_key)

    def _get_all_ui_pos_data(self):
        data = read_setting(self._ui_pos_data_key, {}, False)
        for key, value in data.items():
            data[key] = tuple(value)
        return data

    # endregion

    # region NyUI APIs =================================================================================================

    # endregion

    # region Button APIs ===============================================================================================

    @staticmethod
    @kwargs_defaults(touch_event_params=None)
    def button_callback(btn_path, *callback_types, **kwargs):
        """
        [静态方法] [装饰器]

        将函数注册为按钮回调函数。

        示例
        ----

        >>> @MyScreen.button_callback(
        ...     "/panel/button",
        ...     NyButton.UP,
        ...     NyButton.CANCEL,
        ...     touch_event_params={'isSwallow': False}
        ... )
        ... def on_button_up(self, args):
        ...     pass

        参见
        ----

        - ``NyButton.set_callback()`` -- 为指定按钮实例设置回调函数。

        -----

        :param str btn_path: 按钮路径，支持使用路径通配符 "*" （目前仅支持最后一级控件名称使用通配符）
        :param int callback_types: [变长位置参数] 按钮回调类型，支持同时设置多种回调，请使用 NyButton 枚举值
        :param dict|None touch_event_params: [仅关键字参数] 按钮参数字典；默认为 None，详细说明见 `AddTouchEventParams() <https://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E8%87%AA%E5%AE%9A%E4%B9%89UI/UI%E6%8E%A7%E4%BB%B6.html?key=AddTouchEventParams&docindex=1&type=0>`_

        :raise PathMatchError: 按钮路径存在错误时抛出
        """
        touch_event_params = kwargs['touch_event_params']
        def decorator(func):
            func._nyl__callback_types = callback_types
            func._nyl__btn_path = btn_path
            func._nyl__touch_event_params = touch_event_params
            return func
        return decorator

    def _process_button_callback(self):
        for attr in iter_obj_attrs(self):
            if not hasattr(attr, "_nyl__callback_types"):
                continue
            path = attr._nyl__btn_path
            path_lst = self._expend_path(path)
            for p in path_lst:
                nyb = NyButton(self, p, touch_event_params=attr._nyl__touch_event_params)
                nyb.set_callback(attr, *attr._nyl__callback_types)

    def _expend_path(self, path):
        if "*" not in path:
            yield path
        else:
            # 通配符匹配
            if not path.startswith("/"):
                path = "/" + path
            path_split = path.split("/")  # type: list[str | list[str]]
            parent_path = ""
            for i, ps in enumerate(path_split):
                if "*" in ps:
                    # 获取当前层级所有控件的名称并匹配
                    children_name = self._screen_node.GetChildrenName(parent_path)
                    if not children_name:
                        raise error.PathMatchError(path)
                    path_split[i] = [cn for cn in children_name if fnmatch.fnmatchcase(cn, ps)]
                    if not path_split[i]:
                        raise error.PathMatchError(path)
                else:
                    path_split[i] = [ps]
                if i != 0:
                    parent_path += "/" + ps
            # 生成所有匹配的路径
            for p in itertools.product(*path_split):
                yield "/".join(p)

    def _get_all_ui_paths(self):
        if not self.root_panel:
            return []
        paths = [self.root_panel.path]
        for path in self.root_panel.children_path(0):
            if self.is_base_screen and path.startswith("/safezone_screen_matrix"):
                path = "/variables_button_mappings_and_controls" + path
            if path not in paths:
                paths.append(path)
        return paths

    # endregion

    # region Image APIs ================================================================================================

    def GameRenderTickEvent(self, args):
        if self.is_destroyed:
            return
        for path, data in self._frame_anim_data.items():
            if data['is_pausing']:
                continue
            now = time.time()
            if now - data['last_time'] >= data['frame_time']:
                try:
                    index = next(data['indexes'])
                except StopIteration:
                    del self._frame_anim_data[path]
                    data['control'].texture = data['tex_path'] % data['stop_frame']
                    if data['callback']:
                        data['callback'](*data['args'], **data['kwargs'])
                else:
                    data['control'].texture = data['tex_path'] % index
                    data['last_time'] = now

    def _play_frame_anim(
            self,
            ny_image,
            tex_path,
            frame_count,
            frame_rate,
            stop_frame=-1,
            loop=False,
            callback=None,
            args=None,
            kwargs=None,
    ):
        if loop:
            indexes = itertools.cycle(xrange(frame_count))
        else:
            indexes = iter(xrange(frame_count))
        if stop_frame < 0:
            stop_frame += frame_count
        self._frame_anim_data[ny_image.path] = {
            'control': ny_image,
            'tex_path': tex_path,
            'frame_time': 1.0 / frame_rate,
            'stop_frame': stop_frame,
            'last_time': time.time(),
            'indexes': indexes,
            'is_pausing': False,
            'callback': callback,
            'args': args or (),
            'kwargs': kwargs or {},
        }
        if not is_listened(self.GameRenderTickEvent):
            listen_event(self.GameRenderTickEvent)

    def _pause_frame_anim(self, ny_image):
        path = ny_image.path
        if path in self._frame_anim_data:
            self._frame_anim_data[path]['is_pausing'] = True

    def _stop_frame_anim(self, ny_image):
        path = ny_image.path
        if path in self._frame_anim_data:
            del self._frame_anim_data[path]

    # endregion

    # region Grid APIs =================================================================================================

    # endregion

    # region Internal ==================================================================================================

    def _destroy_nyc(self, nyc):
        path = nyc.path
        self._screen_node.RemoveComponent(path, nyc.parent_path)
        if path in self._nyc_cache_map:
            del self._nyc_cache_map[path]
        nyc.__ui_destroy__()

    __get_control_type = staticmethod(
        get_func( # noqa
            ScreenNode,
            (103, 117, 105),
            (103, 101, 116, 95, 99, 111, 110, 116, 114, 111, 108, 95, 100, 101, 102, 95, 116, 121, 112, 101)
        )
    )

    # endregion

    set_bind_world_position  = lambda self, *args, **kwargs: self._screen_node.SetBindWorldPosition(*args, **kwargs)
    set_screen_visible       = lambda self, *args, **kwargs: self._screen_node.SetScreenVisible(*args, **kwargs)
    change_bind_entity_id    = lambda self, *args, **kwargs: self._screen_node.ChangeBindEntityId(*args, **kwargs)
    bind_virtual_world_model = lambda self, *args, **kwargs: self._screen_node.BindVirtualWorldModel(*args, **kwargs)
    change_bind_offset       = lambda self, *args, **kwargs: self._screen_node.ChangeBindOffset(*args, **kwargs)
    change_bind_auto_scale   = lambda self, *args, **kwargs: self._screen_node.ChangeBindAutoScale(*args, **kwargs)
    get_bind_entity_id       = lambda self, *args, **kwargs: self._screen_node.GetBindEntityId(*args, **kwargs)
    get_bind_world_position  = lambda self, *args, **kwargs: self._screen_node.GetBindWorldPosition(*args, **kwargs)
    get_bind_offset          = lambda self, *args, **kwargs: self._screen_node.GetBindOffset(*args, **kwargs)
    get_bind_auto_scale      = lambda self, *args, **kwargs: self._screen_node.GetBindAutoScale(*args, **kwargs)
    clone                    = lambda self, *args, **kwargs: self._screen_node.Clone(*args, **kwargs)
    get_children_name        = lambda self, *args, **kwargs: self._screen_node.GetChildrenName(*args, **kwargs)
    get_all_children_path    = lambda self, *args, **kwargs: self._screen_node.GetAllChildrenPath(*args, **kwargs)
    remove_component         = lambda self, *args, **kwargs: self._screen_node.RemoveComponent(*args, **kwargs)
    set_remove               = lambda self, *args, **kwargs: self._screen_node.SetRemove(*args, **kwargs)
    create_child_control     = lambda self, *args, **kwargs: self._screen_node.CreateChildControl(*args, **kwargs)
    remove_child_control     = lambda self, *args, **kwargs: self._screen_node.RemoveChildControl(*args, **kwargs)
    set_ui_model             = lambda self, *args, **kwargs: self._screen_node.SetUiModel(*args, **kwargs)
    set_ui_entity            = lambda self, *args, **kwargs: self._screen_node.SetUiEntity(*args, **kwargs)
    set_ui_model_scale       = lambda self, *args, **kwargs: self._screen_node.SetUiModelScale(*args, **kwargs)
    update_screen            = lambda self, *args, **kwargs: self._screen_node.UpdateScreen(*args, **kwargs)
    set_stack_grid_count     = lambda self, *args, **kwargs: self._screen_node.SetStackGridCount(*args, **kwargs)
    set_select_control       = lambda self, *args, **kwargs: self._screen_node.SetSelectControl(*args, **kwargs)
    get_rich_text_item       = lambda self, *args, **kwargs: self._screen_node.GetRichTextItem(*args, **kwargs)
    set_is_hud               = lambda self, *args, **kwargs: self._screen_node.SetIsHud(*args, **kwargs)
    get_is_hud               = lambda self, *args, **kwargs: self._screen_node.GetIsHud(*args, **kwargs)
    get_screen_name          = lambda self, *args, **kwargs: self._screen_node.GetScreenName(*args, **kwargs)
    get_self                 = lambda self, *args, **kwargs: self._screen_node.GetSelf(*args, **kwargs)
    get_base_uicontrol       = lambda self, *args, **kwargs: self._screen_node.GetBaseUicontrol(*args, **kwargs)


class NyScreenNode(NyScreenBase, ScreenNode):
    """
    ``ScreenNode`` 扩展类，提供更高级的UI生命周期管理、动态绑定、控件位置管理等功能。

    说明
    ----

    需配合 ``@screen`` 装饰器使用。

    UI创建完成后可通过 ``.root_panel`` 获取根面板控件实例。

    可在 ``@screen`` 装饰器中将 ``enabled_deferred_init`` 设为 ``True`` 以启用延迟初始化功能。
    启用后UI类的 ``__init__()`` 方法将推迟到UI创建完毕后触发，此时可以在 ``__init__()`` 方法内正常执行各种UI控件接口，从而不必写在 ``__ui_create__()`` 方法里。

    生命周期方法
    ============

    ``NyScreenNode`` 共有五个可重写的生命周期方法：

    - ``__ui_create__()`` -- UI创建完成时调用。
    - ``__ui_destroy__()`` -- UI销毁时调用。
    - ``__ui_update__()`` -- 每帧调用， 1 秒有 30 帧。
    - ``__ui_deactive__()`` -- 当栈顶UI有其他UI入栈时调用。
    - ``__ui_active__()`` -- 当UI重新回到栈顶时调用。

    重写这些生命周期方法和 ``__init__()`` 方法时请调用一次 ``super()`` 或手动调用父类同名方法，否则可能导致界面功能异常。

    示例
    ----

    >>> @nyl.screen(
    ...     "my_screen",
    ...     # "main", # 画布名称为main时可省略该参数
    ...     is_hud=True,
    ...     enabled_deferred_init=True,
    ...     auto_show=True,
    ... )
    ... class MyScreen(nyl.NyScreenNode):
    ...     def __init__(self, namespace, name, param):
    ...         super(MyScreen, self).__init__(namespace, name, param)
    ...         # 当前示例已开启延迟初始化，因此可以把__init__当成__ui_create__使用
    ...         # 创建按钮控件实例
    ...         self.button = (self.root_panel / "button").to_button()
    ...
    ...     def __ui_create__(self):
    ...         super(MyScreen, self).__ui_create__()
    ...
    ...     def __ui_destroy__(self):
    ...         super(MyScreen, self).__ui_destroy__()
    ...
    ...     def __ui_update__(self):
    ...         super(MyScreen, self).__ui_update__()
    ...
    ...     def __ui_deactive__(self):
    ...         super(MyScreen, self).__ui_deactive__()
    ...
    ...     def __ui_active__(self):
    ...         super(MyScreen, self).__ui_active__()

    参见
    ----

    - ``@screen`` -- 用于注册UI界面的装饰器。
    - ``NyScreenProxy`` -- 用于UI界面代理，功能与 NyScreenNode 相同。

    -----

    :param str namespace: UI命名空间，对应 UI json 中 "namespace" 字段的值
    :param str name: UI画布名称，对应 UI json 中画布（screen）的名称
    :param dict|None param: 创建UI时传入的参数字典
    """

    __user_init = None
    __user_init_args = None
    __inited = False

    def __new__(cls, namespace, name, param=None):
        if cls.enabled_deferred_init and not cls.__user_init and cls.__init__ is not NyScreenNode.__init__: # 如果用户没有编写init方法则跳过
            # 延迟初始化，先备份用户的init方法，然后将其覆盖
            cls.__user_init = cls.__init__ # noqa

            def init(self, *args):
                # 正常初始化内部逻辑
                NyScreenNode.__init__(self, *args)
                self.__user_init_args = args

            cls.__init__ = init

        return object.__new__(cls)

    def __init__(self, namespace, name, param=None): # noqa
        if self.__inited:
            return
        ScreenNode.__init__(self, namespace, name, param)
        NyScreenBase.__init__(self)
        self._screen_node = self
        self.__inited = True

    def __ui_create__(self):
        NyScreenBase.__ui_create__(self)
        if self.enabled_deferred_init and self.__class__.__user_init:
            self.__class__.__user_init(self, *self.__user_init_args)  # noqa
        self.has_created = True

    def Create(self):
        try_exec(self.__ui_create__)

    def Destroy(self):
        try_exec(self.__ui_destroy__)

    def Update(self):
        try_exec(self.__ui_update__)

    def OnDeactive(self):
        try_exec(self.__ui_deactive__)

    def OnActive(self):
        try_exec(self.__ui_active__)


class NyScreenProxy(NyScreenBase, CustomUIScreenProxy):
    """
    用于UI界面代理，功能与 ``NyScreenNode`` 相同。

    说明
    ----

    需配合 ``@screen_proxy`` 装饰器使用。

    UI创建完成后可通过 ``.root_panel`` 获取根面板控件实例。

    可在 ``@screen_proxy`` 装饰器中将 ``enabled_deferred_init`` 设为 ``True`` 以启用延迟初始化功能。
    启用后UI类的 ``__init__()`` 方法将推迟到UI创建完毕后触发，此时可以在 ``__init__()`` 方法内正常执行各种UI控件接口，从而不必写在 ``__ui_create__()`` 方法里。

    生命周期方法
    ============

    ``NyScreenProxy`` 共有三个可重写的生命周期方法：

    - ``__ui_create__()`` -- UI创建完成时调用。
    - ``__ui_destroy__()`` -- UI销毁时调用。
    - ``__ui_update__()`` -- 每帧调用， 1 秒有 30 帧。

    重写这些生命周期方法和 ``__init__()`` 方法时请调用一次 ``super()`` 或手动调用父类同名方法，否则可能导致界面功能异常。

    示例
    ----

    >>> @nyl.screen_proxy(
    ...     "hud",
    ...     "hud_screen",
    ...     enabled_deferred_init=True,
    ... )
    ... class MyScreen(nyl.NyScreenProxy):
    ...     def __init__(self, screen_name, screen_node):
    ...         super(MyScreen, self).__init__(screen_name, screen_node)
    ...         # 当前示例已开启延迟初始化，因此可以把__init__当成__ui_create__使用
    ...         # 创建按钮控件实例
    ...         self.button = (self.root_panel / "button").to_button()
    ...
    ...     def __ui_create__(self):
    ...         super(MyScreen, self).__ui_create__()
    ...
    ...     def __ui_destroy__(self):
    ...         super(MyScreen, self).__ui_destroy__()
    ...
    ...     def __ui_update__(self):
    ...         super(MyScreen, self).__ui_update__()

    参见
    ----

    - ``@screen_proxy`` -- 用于注册UI界面代理的装饰器。
    - ``NyScreenNode`` -- ScreenNode 扩展类。

    -----

    :param str screen_name: 被代理UI的名称
    :param ScreenNode screen_node: 被代理UI的原生 ScreenNode 实例
    """

    __user_init = None
    __user_init_args = None
    __inited = False

    def __new__(cls, screen_name, screen_node):
        if cls.enabled_deferred_init and not cls.__user_init and cls.__init__ is not NyScreenProxy.__init__:
            cls.__user_init = cls.__init__ # noqa

            def init(self, *args):
                NyScreenProxy.__init__(self, *args)
                self.__user_init_args = args

            cls.__init__ = init

        return object.__new__(cls)

    def __init__(self, screen_name, screen_node): # noqa
        if self.__inited:
            return
        CustomUIScreenProxy.__init__(self, screen_name, screen_node)
        NyScreenBase.__init__(self)
        self._screen_node = screen_node
        self.__inited = True

    def __ui_create__(self):
        NyScreenBase.__ui_create__(self)
        if self.enabled_deferred_init and self.__class__.__user_init:
            self.__class__.__user_init(self, *self.__user_init_args) # noqa
        self.has_created = True

    def OnCreate(self):
        try_exec(self.__ui_create__)

    def OnDestroy(self):
        try_exec(self.__ui_destroy__)

    def OnTick(self):
        try_exec(self.__ui_update__)

    @classmethod
    def register_proxy(cls):
        """
        [类方法]

        注册UI代理。

        一般情况下由「nuoyanlib」自动执行。

        -----

        :return: 是否成功
        :rtype: bool
        """
        return NativeScreenManager.RegisterScreenProxy(
            cls.namespace + "." + cls.name,
            _env.get_cls_path(cls)
        )

    get_screen_node = CustomUIScreenProxy.GetScreenNode
    get_screen_name = CustomUIScreenProxy.GetScreenName















