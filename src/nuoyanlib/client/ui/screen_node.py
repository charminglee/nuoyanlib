# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-18
#  ⠀
# =================================================


from types import MethodType
import time
import itertools
import fnmatch
from ...core.client.comp import CustomUIScreenProxy, ScreenNode, ViewBinder
from ...core import error
from ...core.listener import listen_event, unlisten_event
from ...core._utils import hook_method, iter_obj_attrs, kwargs_defaults, try_exec, get_func
from .ui_utils import to_control, to_path, _UIControlType
from ...utils.enum import ButtonCallbackType, ClientEvent
from .nyc import *
from ..setting import read_setting, save_setting


__all__ = [
    "ScreenNodeExtension",
]


class ScreenNodeExtension(object):
    """
    ``ScreenNode`` 扩展类，提供更多UI界面功能。

    说明
    ----

    继承 ``ScreenNodeExtension`` 时，必须将其放在继承序列的首位，例如：

    ::

        class MyUI(ScreenNodeExtension, ScreenNode)

    以下为错误写法：

    ::

        class MyUI(ScreenNode, ScreenNodeExtension)

    -----

    :raise ScreenNodeNotFoundError: 找不到当前UI的 ScreenNode 实例时抛出，请确保UI类正确继承了 ScreenNode 或 CustomUIScreenProxy
    :raise PathMatchError: @ScreenNodeExtension.button_callback 装饰器的按钮路径存在错误时抛出
    """

    ROOT_PANEL_PATH = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"

    def __init__(self, *args):
        super(ScreenNodeExtension, self).__init__(*args)
        self._nyc_cache_map = {}
        self._ui_pos_data_key = ""
        self._screen_node = None
        self._frame_anim_data = {}
        self._binging_data = {}
        self.cs = None
        self.root_panel = None
        self.has_created = False
        self.is_base_screen = False

        def set_has_created():
            self.has_created = True

        if isinstance(self, CustomUIScreenProxy):
            # 兼容UI代理
            self._screen_node = args[1]
            hook_method(self.OnCreate, self.__create__, set_has_created) # noqa
            hook_method(self.OnDestroy, after_hook=self.__destroy__) # noqa
        elif isinstance(self, ScreenNode):
            self._screen_node = self
            if len(args) == 3 and isinstance(args[2], dict):
                self.cs = args[2].get('__cs__')
            hook_method(self.Create, self.__create__, set_has_created) # noqa
            hook_method(self.Destroy, after_hook=self.__destroy__) # noqa
        else:
            raise error.ScreenNodeNotFoundError

    def __create__(self):
        self._ui_pos_data_key = "nyl_ui_pos_data_%s_%s" % (self._screen_node.namespace, self._screen_node.name)
        self._recover_ui_pos()
        if self._is_control_exist(ScreenNodeExtension.ROOT_PANEL_PATH):
            root_panel = self._screen_node.GetBaseUIControl(ScreenNodeExtension.ROOT_PANEL_PATH)
            self.is_base_screen = True
        else:
            root_panel = self._screen_node.GetBaseUIControl("")
        if root_panel:
            self.root_panel = self.create_ny_control(root_panel)
        self._process_button_callback()

    def __destroy__(self):
        unlisten_event(self._OnGridSizeChanged, ClientEvent.GridComponentSizeChangedClientEvent)
        unlisten_event(self._OnRenderTick, ClientEvent.GameRenderTickEvent)
        for nyc in self._nyc_cache_map.values():
            try_exec(nyc.__destroy__)
        self._nyc_cache_map.clear()
        self._ui_pos_data_key = ""
        self._screen_node = None
        self._frame_anim_data.clear()
        self._binging_data.clear()
        self.cs = None
        self.root_panel = None

    # region Common APIs ===============================================================================================

    def build_binding(self, func, flag, binding_name="", collection_name=""):
        """
        动态创建绑定（无需依赖 ``@ViewBinder`` 装饰器）。

        -----

        :param function func: 绑定函数，支持普通函数与实例方法
        :param int flag: 绑定标志，参考 ViewBinder 中的枚举值
        :param str binding_name: 绑定名称；默认为 "#<namespace>.<func_name>"，<namespace> 为 UI json 文件中 "namespace" 对应的值，<func_name> 为函数名
        :param str collection_name: 集合名称；若非集合绑定，忽略该参数即可；默认为空字符串

        :return: 是否成功
        :rtype: bool
        """
        if not binding_name:
            binding_name = "#%s.%s" % (self._screen_node.namespace, func.__name__)
        is_collection = bool(collection_name)

        proxy = self._create_binding_proxy(func, flag, binding_name, collection_name)
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

        -----

        :param function func: 绑定函数

        :return: 是否成功
        :rtype: bool
        """
        if isinstance(func, MethodType):
            key = (func.__func__, func.__self__)
        else:
            key = func
        if key not in self._binging_data:
            return False
        proxy, is_collection = self._binging_data.pop(key)

        if is_collection:
            self._screen_node._process_collection_unregister(proxy, self._screen_node.screen_name) # noqa
        else:
            self._screen_node._process_default_unregister(proxy, self._screen_node.screen_name) # noqa
        return True

    # endregion

    # region NyUI APIs =================================================================================================

    def create_ny_control(self, path_or_control, **kwargs):
        """
        创建 ``NyControl`` 通用控件实例。

        说明
        ----

        兼容 ModSDK ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyControl 控件实例，创建失败返回 None
        :rtype: NyControl|None
        """
        return self._create_nyc(path_or_control, NyControl, **kwargs)

    def create_ny_button(self, path_or_control, **kwargs):
        """
        创建 ``NyButton`` 按钮控件实例。

        说明
        ----

        兼容 ModSDK ``ButtonUIControl`` 和 ``BaseUIControl`` 的相关接口。
        创建后无需再调用 ``.AddTouchEventParams()`` 或 ``.AddHoverEventParams()`` 接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例
        :param dict|None touch_event_params: [仅关键字参数] 按钮参数字典；默认为 None，详细说明见 AddTouchEventParams

        :return: NyButton 按钮实例，创建失败返回 None
        :rtype: NyButton|None
        """
        return self._create_nyc(path_or_control, NyButton, **kwargs)

    def create_ny_combo_box(self, path_or_control, **kwargs):
        """
        创建 ``NyComboBox`` 下拉框控件实例。

        说明
        ----

        兼容 ModSDK ``NeteaseComboBoxUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyComboBox 下拉框实例，创建失败返回 None
        :rtype: NyComboBox|None
        """
        return self._create_nyc(path_or_control, NyComboBox, **kwargs)

    def create_ny_edit_box(self, path_or_control, **kwargs):
        """
        创建 ``NyEditBox`` 文本编辑框控件实例。

        说明
        ----

        兼容ModSDK ``TextEditBoxUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyEditBox 文本编辑框实例，创建失败返回 None
        :rtype: NyEditBox|None
        """
        return self._create_nyc(path_or_control, NyEditBox, **kwargs)

    def create_ny_grid(self, path_or_control, **kwargs):
        """
        创建 ``NyGrid`` 网格控件实例。

        说明
        ----

        兼容 ModSDK ``GridUIControl`` 和 ``BaseUIControl`` 的相关接口。

        关于 ``cell_visible_binding`` 与 ``collection_name`` 参数的说明：

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
        - 最后，将 **网格** json 中的 ``"collection_name"`` 字段的值设置给 ``collection_name`` 参数即可。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例
        :param bool is_stack_grid: [仅关键字参数] 是否是 StackGrid；默认为 False
        :param str template_name: [仅关键字参数] 网格模板控件名称，即 "grid_item_template" 字段或UI编辑器中的网格“内容”所使用的控件；仅模板控件名称以数字结尾时需要传入该参数
        :param str cell_visible_binding: [仅关键字参数] 用于控制网格元素显隐性的绑定名称，详见上方说明
        :param str collection_name: [仅关键字参数] 网格集合名称，详见上方说明

        :return: NyGrid网格实例，创建失败返回None
        :rtype: NyGrid|None
        """
        return self._create_nyc(path_or_control, NyGrid, **kwargs)

    def create_ny_image(self, path_or_control, **kwargs):
        """
        创建 ``NyImage`` 图片控件实例。

        说明
        ----

        兼容 ModSDK ``ImageUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyImage 图片实例，创建失败返回 None
        :rtype: NyImage|None
        """
        return self._create_nyc(path_or_control, NyImage, **kwargs)

    def create_ny_input_panel(self, path_or_control, **kwargs):
        """
        创建 ``NyInputPanel`` 输入面板控件实例。

        说明
        ----

        兼容ModSDK ``InputPanelUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyInputPanel 输入面板实例，创建失败返回 None
        :rtype: NyInputPanel|None
        """
        return self._create_nyc(path_or_control, NyInputPanel, **kwargs)

    def create_ny_item_renderer(self, path_or_control, **kwargs):
        """
        创建 ``NyItemRenderer`` 物品渲染器控件实例。

        说明
        ----

        兼容 ModSDK ``ItemRendererUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyItemRenderer 物品渲染器实例，创建失败返回 None
        :rtype: NyItemRenderer|None
        """
        return self._create_nyc(path_or_control, NyItemRenderer, **kwargs)

    def create_ny_label(self, path_or_control, **kwargs):
        """
        创建 ``NyLabel`` 文本控件实例。

        说明
        ----

        兼容 ModSDK ``LabelUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyLabel 文本实例，创建失败返回 None
        :rtype: NyLabel|None
        """
        return self._create_nyc(path_or_control, NyLabel, **kwargs)

    def create_ny_mini_map(self, path_or_control, **kwargs):
        """
        创建 ``NyMiniMap`` 小地图控件实例。

        说明
        ----

        兼容 ModSDK ``MiniMapUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyMiniMap 小地图实例，创建失败返回 None
        :rtype: NyMiniMap|None
        """
        return self._create_nyc(path_or_control, NyMiniMap, **kwargs)

    def create_ny_paper_doll(self, path_or_control, **kwargs):
        """
        创建 ``NyPaperDoll`` 纸娃娃控件实例。

        说明
        ----

        兼容 ModSDK ``NeteasePaperDollUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyPaperDoll 纸娃娃实例，创建失败返回 None
        :rtype: NyPaperDoll|None
        """
        return self._create_nyc(path_or_control, NyPaperDoll, **kwargs)

    def create_ny_progress_bar(self, path_or_control, **kwargs):
        """
        创建 ``NyProgressBar`` 进度条控件实例。

        说明
        ----

        兼容 ModSDK ``ProgressBarUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyProgressBar 进度条实例，创建失败返回 None
        :rtype: NyProgressBar|None
        """
        return self._create_nyc(path_or_control, NyProgressBar, **kwargs)

    def create_ny_scroll_view(self, path_or_control, **kwargs):
        """
        创建 ``NyScrollView`` 滚动视图控件实例。

        说明
        ----

        兼容 ModSDK ``ScrollViewUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyScrollView 滚动视图实例，创建失败返回 None
        :rtype: NyScrollView|None
        """
        return self._create_nyc(path_or_control, NyScrollView, **kwargs)

    def create_ny_selection_wheel(self, path_or_control, **kwargs):
        """
        创建 ``NySelectionWheel`` 轮盘控件实例。

        说明
        ----

        兼容 ModSDK ``SelectionWheelUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NySelectionWheel 轮盘实例，创建失败返回 None
        :rtype: NySelectionWheel|None
        """
        return self._create_nyc(path_or_control, NySelectionWheel, **kwargs)

    def create_ny_slider(self, path_or_control, **kwargs):
        """
        创建 ``NySlider`` 滑动条控件实例。

        说明
        ----

        兼容 ModSDK ``SliderUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NySlider 滑动条实例，创建失败返回 None
        :rtype: NySlider|None
        """
        return self._create_nyc(path_or_control, NySlider, **kwargs)

    def create_ny_stack_panel(self, path_or_control, **kwargs):
        """
        创建 ``NyStackPanel`` 栈面板控件实例。

        说明
        ----

        兼容 ModSDK ``StackPanelUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyStackPanel 栈面板实例，创建失败返回 None
        :rtype: NyStackPanel|None
        """
        return self._create_nyc(path_or_control, NyStackPanel, **kwargs)

    def create_ny_toggle(self, path_or_control, **kwargs):
        """
        创建 ``NyToggle`` 开关控件实例。

        说明
        ----

        兼容 ModSDK ``SwitchToggleUIControl`` 和 ``BaseUIControl`` 的相关接口。

        -----

        :param str|BaseUIControl path_or_control: 控件路径或 BaseUIControl 实例

        :return: NyToggle 开关实例，创建失败返回 None
        :rtype: NyToggle|None
        """
        return self._create_nyc(path_or_control, NyToggle, **kwargs)

    CreateNyControl = create_ny_control
    CreateNyButton = create_ny_button
    CreateNyComboBox = create_ny_combo_box
    CreateNyEditBox = create_ny_edit_box
    CreateNyGrid = create_ny_grid
    CreateNyImage = create_ny_image
    CreateNyInputPanel = create_ny_input_panel
    CreateNyItemRenderer = create_ny_item_renderer
    CreateNyLabel = create_ny_label
    CreateNyMiniMap = create_ny_mini_map
    CreateNyPaperDoll = create_ny_paper_doll
    CreateNyProgressBar = create_ny_progress_bar
    CreateNyScrollView = create_ny_scroll_view
    CreateNySelectionWheel = create_ny_selection_wheel
    CreateNySlider = create_ny_slider
    CreateNyStackPanel = create_ny_stack_panel
    CreateNyToggle = create_ny_toggle

    def _create_nyc(self, path_or_control, typ=NyControl, **kwargs):
        if isinstance(path_or_control, NyControl):
            return path_or_control
        path = to_path(path_or_control)
        cached_nyc = self._nyc_cache_map.get(path)
        if cached_nyc:
            cached_t = type(cached_nyc)
            if cached_t is typ or cached_t is not NyControl:
                return cached_nyc
        control = to_control(self._screen_node, path_or_control, typ.CONTROL_TYPE)
        if control:
            nyc = typ(self, control, **kwargs)
            self._nyc_cache_map[path] = nyc
            if typ is NyGrid:
                listen_event(self._OnGridSizeChanged, ClientEvent.GridComponentSizeChangedClientEvent)
            return nyc

    def _destroy_nyc(self, nyc):
        path = nyc.path
        self._screen_node.RemoveComponent(path, nyc.parent_path)
        if path in self._nyc_cache_map:
            del self._nyc_cache_map[path]
        nyc.__destroy__()

    # endregion

    # region Button APIs ===============================================================================================

    @staticmethod
    @kwargs_defaults(touch_event_params=None)
    def button_callback(btn_path, *callback_types, **kwargs): # todo
        """
        [静态方法] [装饰器]

        将函数设置为按钮回调函数。

        说明
        ----

        UI类需继承 ``ScreenNodeExtension`` 。

        -----

        :param str btn_path: 按钮路径，支持使用通配符 "*"（目前仅支持最后一级控件名称使用通配符）
        :param ButtonCallbackType callback_types: [变长位置参数] 按钮回调类型，支持同时设置多种回调，请使用 ButtonCallbackType 枚举值；默认为 ButtonCallbackType.UP
        :param dict|None touch_event_params: [仅关键字参数] 按钮参数字典；默认为 None，详细说明见 AddTouchEventParams
        """
        if not callback_types:
            callback_types = (ButtonCallbackType.UP,)
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
                nyb = self._create_nyc(p, NyButton, touch_event_params=attr._nyl__touch_event_params)
                for t in attr._nyl__callback_types:
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

    def clear_all_pos_data(self):
        """
        删除所有控件的位置数据。

        -----

        :return: 是否成功
        :rtype: bool
        """
        if not self._ui_pos_data_key:
            return False
        return self._save_ui_pos_data({})

    def save_all_pos_data(self):
        """
        保存所有通过 ``.set_movable()`` 或 ``.set_movable_by_long_click()`` 设置了可拖动的控件的位置数据，下次进入游戏时自动恢复。

        说明
        ----

        为保证安全，超出屏幕边界的控件不会被保存。

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

    ClearAllPosData = clear_all_pos_data
    SaveAllPosData = save_all_pos_data

    def _save_ui_pos_data(self, data):
        return save_setting(self._ui_pos_data_key, data, False)

    def _get_ui_pos_data(self):
        data = read_setting(self._ui_pos_data_key, False)
        if data:
            for key, pos_lst in data.items():
                data[key] = [
                    (str(path), tuple(pos))
                    for path, pos in pos_lst
                ]
            return data
        return {}

    def _recover_ui_pos(self):
        data = self._get_ui_pos_data()
        for pos_lst in data.values():
            for path, pos in pos_lst:
                control = to_control(self._screen_node, path)
                if control:
                    control.SetPosition(pos)

    # endregion

    # region Image APIs ================================================================================================

    def _OnRenderTick(self, args):
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
        listen_event(self._OnRenderTick, ClientEvent.GameRenderTickEvent)

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

    def _OnGridSizeChanged(self, args):
        path = args['path']
        idx = path.index("/", 1)
        root_name = path[1: idx]
        if root_name != self._screen_node.name:
            return
        path = path[idx:]
        grid = self._nyc_cache_map.get(path)
        if isinstance(grid, NyGrid):
            grid.__grid_update__()

    # endregion

    # region Internal ==================================================================================================

    __get_control_type = staticmethod(get_func(ScreenNode, (103, 117, 105), (103, 101, 116, 95, 99, 111, 110, 116, 114, 111, 108, 95, 100, 101, 102, 95, 116, 121, 112, 101)))

    def _is_control_exist(self, path):
        screen_name = self._screen_node.screen_name
        full_path = self._screen_node.component_path + path
        return ScreenNodeExtension.__get_control_type(screen_name, full_path) != _UIControlType.UNKNOWN # noqa

    # endregion


def __test__():
    class SN(ScreenNodeExtension, ScreenNode):
        def __init__(self, namespace, name, param):
            super(SN, self).__init__(namespace, name, param)
    sn = SN("abc", "ui", {})
    c1 = sn.create_ny_control("/path/to/control1")
    c2 = sn.create_ny_button("/path/to/control2")
    c3 = sn.create_ny_grid("/path/to/control3")


















