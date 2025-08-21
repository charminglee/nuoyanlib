# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-08-21
|
| ==============================================
"""


from time import time
from itertools import product, cycle
from fnmatch import fnmatchcase
from types import GeneratorType
from ..._core._client.comp import CustomUIScreenProxy, ScreenNode
from ..._core import _error
from ..._core.event.listener import ClientEventProxy, listen_event, unlisten_event, has_listened, unlisten_all_events
from ..._core.event._events import ClientEventEnum as Events
from ..._core._utils import hook_method, iter_obj_attrs
from .ui_utils import (
    to_control, get_ui_pos_data, save_ui_pos_data,
    get_children_path_by_level, get_parent_path, to_path,
)
from ...utils.enum import ButtonCallbackType
from .nyc import *


__all__ = [
    "ScreenNodeExtension",
]


class ScreenNodeExtension(ClientEventProxy):
    """
    | ScreenNode扩展类，提供更多UI界面功能。
    | 已继承 ``ClientEventProxy`` ，监听事件更便捷。

    -----

    :raise ScreenNodeNotFoundError: 无法找到当前UI的ScreenNode实例
    :raise PathMatchError: ScreenNodeExtension.button_callback装饰器的按钮路径错误
    """

    _LIMIT_ATTR = [
        "namespace",
        "name",
        "full_name",
        "screen_name",
        "component_path",
        "parent",
        "children",
        "visible",
        "enable",
        "removed",
        "def_key",
        "org_key",
        "input_mode",
        "is_push_screen",
        "touch_with_mouse",
        "dirty",
        "fresh_async",
    ]
    ROOT_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"

    def __init__(self, *args):
        super(ScreenNodeExtension, self).__init__(*args)
        self._nyc_cache = {}
        self._ui_pos_data_key = ""
        self._screen_node = None
        self._frame_anim_data = {}
        self.cs = None
        self.root_panel = None
        if isinstance(self, CustomUIScreenProxy):
            # 兼容UI代理
            self._screen_node = args[1]
            hook_method(self.OnCreate, self.__create__) # NOQA
            hook_method(self.OnDestroy, self.__destroy__) # NOQA
        elif isinstance(self, ScreenNode):
            self._screen_node = self
            if len(args) == 3 and isinstance(args[2], dict):
                self.cs = args[2].get('__cs__')
            hook_method(self.Create, self.__create__) # NOQA
            hook_method(self.Destroy, self.__destroy__) # NOQA
        else:
            raise _error.ScreenNodeNotFoundError

    # def __setattr__(self, key, value):
    #     # 网易ScreenNode中某些属性被覆盖会导致功能异常且难以排查（如name），因此添加一个限制
    #     if key in ScreenNodeExtension._LIMIT_ATTR and hasattr(self, key):
    #         raise AttributeError("can't set attribute '%s' to '%s'" % (key, self.__class__.__name__))
    #     super(ScreenNodeExtension, self).__setattr__(key, value)

    def __create__(self):
        self._ui_pos_data_key = "nyl_ui_pos_data_%s_%s" % (self._screen_node.namespace, self._screen_node.name) # NOQA
        self._recover_ui_pos()
        root_panel = (
            self._screen_node.GetBaseUIControl(ScreenNodeExtension.ROOT_PANEL_PATH)
            or self._screen_node.GetBaseUIControl("")
        )
        if root_panel:
            self.root_panel = self.create_ny_control(root_panel)
        self._process_button_callback()

    def __destroy__(self):
        unlisten_all_events(self)
        unlisten_event(self._GameRenderTickEvent, Events.GameRenderTickEvent)
        for nyc in self._nyc_cache.values():
            nyc.__destroy__()
        self._nyc_cache.clear()
        self._screen_node = None
        self.cs = None
        self.root_panel = None

    def _GameRenderTickEvent(self, args):
        for path, data in self._frame_anim_data.items():
            if data['is_pausing']:
                continue
            now = time()
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

    # region Public APIs ===============================================================================================

    @staticmethod
    def button_callback(btn_path, *callback_types, **kwargs): # todo
        """
        [装饰器]

        | 设置按钮回调。
        | UI类需继承 ``ScreenNodeExtension`` 。

        -----

        :param str btn_path: 按钮路径，支持通配符"*"（目前仅支持最后一级控件名称使用通配符）
        :param str callback_types: [变长位置参数] 按钮回调类型，支持设置多种回调，请使用ButtonCallbackType枚举值，默认为ButtonCallbackType.UP
        :param dict|None touch_event_param: [仅关键字参数] 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: 返回原函数
        :rtype: function
        """
        if not callback_types:
            callback_types = (ButtonCallbackType.UP,)
        touch_event_param = kwargs.get('touch_event_params', None)
        def decorator(func):
            func._nyl_callback_types = callback_types
            func._nyl_btn_path = btn_path
            func._nyl_touch_event_param = touch_event_param
            return func
        return decorator

    def create_ny_control(self, path_or_control):
        """
        | 创建 ``NyControl`` 通用控件实例，可替代 ``.GetBaseUIControl()`` 的返回值使用。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyControl控件实例，创建失败返回None
        :rtype: NyControl|None
        """
        return self._create_nyc(path_or_control, NyControl)

    def create_ny_button(self, path_or_control, touch_event_params=None):
        """
        | 创建 ``NyButton`` 按钮实例，可替代 ``.asButton()`` 的返回值使用。
        | 创建后无需调用 ``.AddTouchEventParams()`` 或 ``.AddHoverEventParams()`` 接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param dict|None touch_event_params: 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: NyButton按钮实例，创建失败返回None
        :rtype: NyButton|None
        """
        return self._create_nyc(path_or_control, NyButton, touch_event_params=touch_event_params)

    def create_ny_grid(self, path_or_control, is_stack_grid=False):
        """
        | 创建 ``NyGrid`` 网格实例，可替代 ``.asGrid()`` 的返回值使用。
        | 对网格进行操作需要注意一些细节，详见开发指南-界面与交互- `UI说明文档 <https://mc.163.com/dev/mcmanual/mc-dev/mcguide/18-%E7%95%8C%E9%9D%A2%E4%B8%8E%E4%BA%A4%E4%BA%92/30-UI%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.html?key=grid&docindex=4&type=0>`_ 中对Grid控件的描述。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param bool is_stack_grid: 是否是StackGrid，默认为False

        :return: NyGrid网格实例，创建失败返回None
        :rtype: NyGrid|None
        """
        return self._create_nyc(path_or_control, NyGrid, is_stack_grid=is_stack_grid)

    def create_ny_label(self, path_or_control):
        """
        | 创建 ``NyLabel`` 文本实例，可替代 ``.asLabel()`` 的返回值使用。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyLabel文本实例，创建失败返回None
        :rtype: NyLabel|None
        """
        return self._create_nyc(path_or_control, NyLabel)

    def create_ny_progress_bar(self, path_or_control):
        """
        | 创建 ``NyProgressBar`` 进度条实例，可替代 ``.asProgressBar()`` 的返回值使用。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyProgressBar进度条实例，创建失败返回None
        :rtype: NyProgressBar|None
        """
        return self._create_nyc(path_or_control, NyProgressBar)

    def get_children_path_by_level(self, path_or_control, level=1):
        """
        [迭代器]

        | 获取控件的指定层级的所有子控件的路径，返回迭代器。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param int level: 子控件层级，默认为1

        :return: 控件指定层级所有子控件路径的迭代器，获取不到时返回空迭代器
        :rtype: GeneratorType
        """
        return get_children_path_by_level(path_or_control, self._screen_node, level)

    def get_children_control_by_level(self, path_or_control, level=1):
        """
        [迭代器]

        | 获取控件的指定层级的所有子控件的 ``NyControl`` 实例，返回迭代器。
        | 例如，某面板包含两个按钮，而每个按钮又包含三张图片，则按钮为面板的一级子控件，按钮下的图片为面板的二级子控件，以此类推。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param int level: 子控件层级，默认为1

        :return: 控件指定层级所有子控件的NyControl实例的迭代器，获取不到时返回空迭代器
        :rtype: GeneratorType
        """
        all_path = get_children_path_by_level(path_or_control, self._screen_node, level)
        for p in all_path:
            yield self._create_nyc(p, NyControl)

    def get_parent_path(self, path_or_control):
        """
        | 获取控件的父控件路径。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: 父控件路径，获取不到返回None
        :rtype: str|None
        """
        return get_parent_path(path_or_control)

    def get_parent_control(self, path_or_control):
        """
        | 获取控件的父控件 ``NyControl`` 实例。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: 父控件的NyControl实例，获取不到返回None
        :rtype: NyControl|None
        """
        parent_path = get_parent_path(path_or_control)
        if parent_path:
            return self._create_nyc(parent_path, NyControl)

    def clear_all_pos_data(self):
        """
        | 删除所有控件的位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        return save_ui_pos_data(self._ui_pos_data_key, {})

    def save_all_pos_data(self):
        """
        | 保存所有通过 ``.set_movable()`` 或 ``.set_movable_by_long_click()`` 设置了可拖动的控件的位置数据，下次进入游戏时自动恢复。
        | 为保证安全，超出屏幕边界的按钮不会被保存。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        for nyc in self._nyc_cache.values():
            if isinstance(nyc, NyButton) and nyc.is_movable:
                nyc.save_pos_data()
        return True

    CreateNyControl             = create_ny_control
    CreateNyButton              = create_ny_button
    CreateNyGrid                = create_ny_grid
    CreateNyLabel               = create_ny_label
    CreateNyProgressBar         = create_ny_progress_bar
    GetChildrenPathByLevel      = get_children_path_by_level
    GetChildrenNyControlByLevel = get_children_control_by_level
    GetParentPath               = get_parent_path
    GetParentNyControl          = get_parent_control
    ClearAllPosData             = clear_all_pos_data
    SaveAllPosData              = save_all_pos_data

    # endregion

    # region Image APIs ================================================================================================

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
            indexes = cycle(xrange(frame_count))
        else:
            indexes = iter(xrange(frame_count))
        if stop_frame < 0:
            stop_frame += frame_count
        self._frame_anim_data[ny_image.path] = {
            'control': ny_image,
            'tex_path': tex_path,
            'frame_time': 1.0 / frame_rate,
            'stop_frame': stop_frame,
            'last_time': time(),
            'indexes': indexes,
            'is_pausing': False,
            'callback': callback,
            'args': args or (),
            'kwargs': kwargs or {},
        }
        if not has_listened(self._GameRenderTickEvent, Events.GameRenderTickEvent):
            listen_event(self._GameRenderTickEvent, Events.GameRenderTickEvent)

    def _pause_frame_anim(self, ny_image):
        path = ny_image.path
        if path in self._frame_anim_data:
            self._frame_anim_data[path]['is_pausing'] = True

    def _stop_frame_anim(self, ny_image):
        path = ny_image.path
        if path in self._frame_anim_data:
            del self._frame_anim_data[path]

    # endregion

    # region Button APIs ===============================================================================================

    def _process_button_callback(self):
        for attr in iter_obj_attrs(self):
            if not hasattr(attr, "_nyl_callback_types"):
                continue
            path = attr._nyl_btn_path
            path_lst = self._expend_path(path)
            for p in path_lst:
                nyb = self._create_nyc(p, NyButton, touch_event_param=attr._nyl_touch_event_param)
                for t in attr._nyl_callback_types:
                    nyb.set_callback(t, attr)

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
                        raise _error.PathMatchError(path)
                    path_split[i] = [cn for cn in children_name if fnmatchcase(cn, ps)]
                    if not path_split[i]:
                        raise _error.PathMatchError(path)
                else:
                    path_split[i] = [ps]
                if i != 0:
                    parent_path += "/" + ps
            # 生成所有匹配的路径
            for p in product(*path_split):
                yield "/".join(p)

    # endregion

    # region Internal ==================================================================================================

    def _create_nyc(self, path_or_control, typ, **kwargs):
        path = to_path(path_or_control)
        if path in self._nyc_cache:
            nyc = self._nyc_cache[path]
            if type(nyc) is typ or type(nyc) is not NyControl:
                return nyc
        control = to_control(self._screen_node, path_or_control, typ._CONTROL_TYPE)
        if control:
            nyc = typ(self, control, **kwargs)
            self._nyc_cache[path] = nyc
            return nyc

    def _destroy_nyc(self, nyc):
        nyc.__destroy__()
        self._nyc_cache.pop(nyc.path, None)
        self._screen_node.RemoveChildControl(nyc.base_control)

    def _recover_ui_pos(self):
        data = get_ui_pos_data(self._ui_pos_data_key)
        for data_lst in data.values():
            for path, pos in data_lst:
                control = to_control(self._screen_node, path)
                if control:
                    control.SetPosition(pos)

    # endregion


def __test__():
    class SN(ScreenNodeExtension, ScreenNode):
        def __init__(self, namespace, name, param):
            super(SN, self).__init__(namespace, name, param)
    sn = SN("abc", "ui", {})
    c1 = sn.create_ny_control("/path/to/control1")
    c2 = sn.create_ny_button("/path/to/control2")
    c3 = sn.create_ny_grid("/path/to/control3")


















