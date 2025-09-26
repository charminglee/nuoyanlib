# -*- coding: utf-8 -*-
"""
| ==============================================
|
|   Copyright (c) 2025 Nuoyan
|
|   Author: Nuoyan
|   Email : 1279735247@qq.com
|   Gitee : https://gitee.com/charming-lee
|   Date  : 2025-09-21
|
| ==============================================
"""


from time import time
from itertools import product, cycle
from fnmatch import fnmatchcase
from ..._core._client.comp import CustomUIScreenProxy, ScreenNode, ViewBinder
from ..._core import _error
from ..._core.event.listener import ClientEventProxy, listen_event, unlisten_event, has_listened, unlisten_all_events
from ..._core.event._events import ClientEventEnum as Events
from ..._core._utils import hook_method, iter_obj_attrs
from .ui_utils import to_control, get_ui_pos_data, save_ui_pos_data, to_path
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

    ROOT_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"

    def __init__(self, *args):
        super(ScreenNodeExtension, self).__init__(*args)
        self._nyc_cache_map = {}
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

        listen_event(self._GridComponentSizeChangedClientEvent, Events.GridComponentSizeChangedClientEvent)

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
        unlisten_event(self._GridComponentSizeChangedClientEvent, Events.GridComponentSizeChangedClientEvent)
        for nyc in self._nyc_cache_map.values():
            nyc.__destroy__()
        self._nyc_cache_map.clear()
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

    def _GridComponentSizeChangedClientEvent(self, args):
        path = args['path']
        path = path[path.index("/", 1):]
        grid = self._nyc_cache_map.get(path, None)
        if isinstance(grid, NyGrid):
            grid.__grid_update__()

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
        :param dict|None touch_event_params: [仅关键字参数] 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: 返回原函数
        :rtype: function
        """
        if not callback_types:
            callback_types = (ButtonCallbackType.UP,)
        touch_event_params = kwargs.get('touch_event_params', None)
        def decorator(func):
            func._nyl_callback_types = callback_types
            func._nyl_btn_path = btn_path
            func._nyl_touch_event_params = touch_event_params
            return func
        return decorator

    def create_ny_control(self, path_or_control, **kwargs):
        """
        | 创建 ``NyControl`` 通用控件实例。
        | 兼容ModSDK ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyControl控件实例，创建失败返回None
        :rtype: NyControl|None
        """
        return self._create_nyc(path_or_control, NyControl, **kwargs)

    def create_ny_button(self, path_or_control, **kwargs):
        """
        | 创建 ``NyButton`` 按钮实例。
        | 兼容ModSDK ``ButtonUIControl`` 和 ``BaseUIControl`` 的相关接口。
        | 创建后无需再调用 ``.AddTouchEventParams()`` 或 ``.AddHoverEventParams()`` 接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param dict|None touch_event_params: [仅关键字参数] 按钮参数字典，默认为None，详细说明见AddTouchEventParams

        :return: NyButton按钮实例，创建失败返回None
        :rtype: NyButton|None
        """
        return self._create_nyc(path_or_control, NyButton, **kwargs)

    def create_ny_grid(self, path_or_control, **kwargs):
        """
        | 创建 ``NyGrid`` 网格实例。
        | 兼容ModSDK ``GridUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        | 关于 ``cell_visible_binding`` 与 ``collection_name`` 参数的说明：
        - 该参数用于 ``.grid_size`` 、 ``.dimension`` 等接口，实现动态设置网格元素的数量（多余元素将通过设置 ``visible`` 为 ``False`` 的方式隐藏），不使用该接口可忽略这两个参数。
        - 由于网格控件的特性，设置元素的 ``visible`` 需要使用绑定，请在你的 **网格模板控件** 的json中添加以下绑定，然后将 ``"binding_name"`` 的值设置给 ``cell_visible_binding`` 参数 。
        ::

            "bindings": [
                {
                    "binding_type": "collection",
                    "binding_collection_name": "grid_collection_name", //此处需要与网格的"collection_name"字段相同
                    "binding_name": "#namespace.binding_name", //可自定义
                    "binding_name_override": "#visible",
                    "binding_condition": "always"
                }
            ]
        - 最后，将 **网格** json中的 ``"collection_name"`` 字段的值设置给 ``collection_name`` 参数即可。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例
        :param bool is_stack_grid: [仅关键字参数] 是否是StackGrid，默认为False
        :param str template_name: [仅关键字参数] 网格模板控件名称，即"grid_item_template"字段或UI编辑器中的网格“内容”所使用的控件；仅模板控件名称以数字结尾时需要传入该参数
        :param str cell_visible_binding: [仅关键字参数] 用于控制网格元素显隐性的绑定名称，详见上方说明
        :param str collection_name: [仅关键字参数] 网格集合名称，详见上方说明

        :return: NyGrid网格实例，创建失败返回None
        :rtype: NyGrid|None
        """
        return self._create_nyc(path_or_control, NyGrid, **kwargs)

    def create_ny_label(self, path_or_control, **kwargs):
        """
        | 创建 ``NyLabel`` 文本实例。
        | 兼容ModSDK ``LabelUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyLabel文本实例，创建失败返回None
        :rtype: NyLabel|None
        """
        return self._create_nyc(path_or_control, NyLabel, **kwargs)

    def create_ny_progress_bar(self, path_or_control, **kwargs):
        """
        | 创建 ``NyProgressBar`` 进度条实例。
        | 兼容ModSDK ``ProgressBarUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyProgressBar进度条实例，创建失败返回None
        :rtype: NyProgressBar|None
        """
        return self._create_nyc(path_or_control, NyProgressBar, **kwargs)

    def create_ny_toggle(self, path_or_control, **kwargs):
        """
        | 创建 ``NyToggle`` 开关实例。
        | 兼容ModSDK ``SwitchToggleUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyToggle开关实例，创建失败返回None
        :rtype: NyToggle|None
        """
        return self._create_nyc(path_or_control, NyToggle, **kwargs)

    def create_ny_scroll_view(self, path_or_control, **kwargs):
        """
        | 创建 ``NyScrollView`` 滚动视图实例。
        | 兼容ModSDK ``ScrollViewUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyScrollView滚动视图实例，创建失败返回None
        :rtype: NyScrollView|None
        """
        return self._create_nyc(path_or_control, NyScrollView, **kwargs)

    def create_ny_image(self, path_or_control, **kwargs):
        """
        | 创建 ``NyImage`` 图片实例。
        | 兼容ModSDK ``ImageUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyImage图片实例，创建失败返回None
        :rtype: NyImage|None
        """
        return self._create_nyc(path_or_control, NyImage, **kwargs)

    def create_ny_paper_doll(self, path_or_control, **kwargs):
        """
        | 创建 ``NyPaperDoll`` 纸娃娃实例。
        | 兼容ModSDK ``NeteasePaperDollUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或BaseUIControl实例

        :return: NyPaperDoll纸娃娃实例，创建失败返回None
        :rtype: NyPaperDoll|None
        """
        return self._create_nyc(path_or_control, NyPaperDoll, **kwargs)

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
        for nyc in self._nyc_cache_map.values():
            if isinstance(nyc, NyButton) and nyc.is_movable:
                nyc.save_pos_data()
        return True

    CreateNyControl     = create_ny_control
    CreateNyButton      = create_ny_button
    CreateNyGrid        = create_ny_grid
    CreateNyLabel       = create_ny_label
    CreateNyProgressBar = create_ny_progress_bar
    ClearAllPosData     = clear_all_pos_data
    SaveAllPosData      = save_all_pos_data

    # endregion

    # region Image APIs ================================================================================================

    def _play_frame_anim(
            self, ny_image, tex_path, frame_count, frame_rate,
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
                nyb = self._create_nyc(p, NyButton, touch_event_params=attr._nyl_touch_event_params)
                for t in attr._nyl_callback_types:
                    nyb.set_callback(attr, t)

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

    def _create_binding_proxy(self, func, flag, binding_name="", collection_name=""):
        if collection_name:
            binding = ViewBinder.binding_collection(flag, collection_name, binding_name)
        else:
            binding = ViewBinder.binding(flag, binding_name)
        @binding
        def proxy(*args):
            return func(*args)
        name = "_nyl_binding_%s_%s" % (func.__name__, id(func))
        proxy.__name__ = name
        setattr(self._screen_node, name, proxy)
        return proxy

    def _build_binding(self, func, flag, binding_name="", collection_name=""):
        if not binding_name:
            binding_name = "#%s.%s" % (self._screen_node.namespace, func.__name__)  # NOQA
        proxy = self._create_binding_proxy(func, flag, binding_name, collection_name)
        if collection_name:
            self._screen_node._process_collection(proxy, self._screen_node.screen_name) # NOQA
        else:
            self._screen_node._process_default(proxy, self._screen_node.screen_name) # NOQA

    def _unbuild_binding(self, func):
        self._screen_node._process_default_unregister(func, self._screen_node.screen_name) # NOQA

    def _create_nyc(self, path_or_control, typ, **kwargs):
        path = to_path(path_or_control)
        cached_nyc = self._nyc_cache_map.get(path)
        if cached_nyc:
            nyc_t = type(cached_nyc)
            if nyc_t is typ or nyc_t is not NyControl:
                return cached_nyc
        control = to_control(self._screen_node, path_or_control, typ._CONTROL_TYPE)
        if control:
            nyc = typ(self, control, **kwargs)
            self._nyc_cache_map[path] = nyc
            return nyc

    def _destroy_nyc(self, nyc):
        path = nyc.path
        self._screen_node.RemoveComponent(path, nyc.parent_path)
        if path in self._nyc_cache_map:
            del self._nyc_cache_map[path]
        nyc.__destroy__()

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


















