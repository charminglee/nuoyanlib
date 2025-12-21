# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-21
#  ⠀
# =================================================


import mod.server.extraServerApi as s_api
from ..core.server.comp import LvComp
from ..core._utils import kwargs_defaults
from ..core.listener import event, ServerEventProxy


__all__ = [
    "LobbyDataMgr",
]


_IS_LOBBY = (s_api.GetPlatform() == -1)
_UID_DATA_KEY = "_nyl_lobby_uid_data"
_GLOBAL_DATA_KEY = "_nyl_lobby_global_data"


class LobbyDataMgr(ServerEventProxy):
    """
    联机大厅管理器。

    支持以下功能：

    - 便捷管理联机大厅云端数据，自动完成数据更新上传/数据获取/数据冲突等情况的处理。
    - 设置订单发货。
    - 在单机环境中模拟联机大厅环境。

    -----

    """

    def __init__(self):
        super(LobbyDataMgr, self).__init__()
        self._default = {}
        self._uid = {}
        self.global_data = {}
        self.uid_data = {}

    @event("UiInitFinished")
    def _on_player_join(self, args):
        player_id = args['__id__']
        uid = self._to_uid(player_id)
        for k, v in self.uid_data.items():
            if uid not in v:
                self.uid_data[k][uid] = self._default[k]()

    def _to_uid(self, player_id):
        if player_id not in self._uid:
            self._uid[player_id] = LvComp.Http.GetPlayerUid(player_id)
        return self._uid[player_id]

    def register(self, key, default=None, is_global=False):
        """
        注册云端数据。

        -----

        :param str key: 数据键
        :param str|int|float|bool|list|dict|None default: 数据默认值；需传入一个函数，无参数，返回值即为数据默认值；默认为None
        :param bool is_global: 是否为全局数据（即不依赖玩家uid），默认为False

        :return: 无
        :rtype: None

        :raise TypeError: 数据键必须为str类型，否则抛出此异常
        :raise KeyError: 数据键已注册
        """
        if type(key) is not str:
            raise TypeError("lobby data key must be 'str', got '%s'" % type(key).__name__)
        if key in self.global_data or key in self.uid_data:
            raise KeyError("lobby data key '%s' already exists" % key)
        if default is None:
            default = lambda: None
        if is_global:
            self.global_data[key] = default() # noqa
        else:
            self.uid_data[key] = {
                self._to_uid(pid): default()
                for pid in s_api.GetPlayerList()
            }
        self._default[key] = default

    def _simplify_response(self, response):
        entity = response.pop('entity')
        if 'data' in entity:
            response['data'] = {
                d['key']: d['value']
                for d in entity['data']
            }
        elif 'orders' in entity:
            for d in entity['orders']:
                order_id = d.pop('order_id')
                response[order_id] = d

    def _set_default(self, response, keys):
        data = response['data']
        for k in keys:
            if k not in data:
                data[k] = self._default[k]()

    def _update_cache(self, uid, data):
        if uid == 0:
            self.global_data.update(data)
        else:
            for k, v in data.items():
                self.uid_data[k][uid] = v

    @kwargs_defaults(callback=None, simulate=None)
    def fetch(self, player=0, *keys, **kwargs):
        """
        从云端获取数据并缓存。

        请先用 ``.register()`` 注册数据再调用本调接口。

        -----

        :param int|str player: 玩家UID或实体ID，传入0表示全局数据，默认为0
        :param str keys: [变长位置参数] 需要获取的数据键，省略该参数将获取所有已注册的数据
        :param function|None callback: [仅关键字参数] 获取结果回调函数，默认为None
        :param dict[str,int|str|dict]|None simulate: [仅关键字参数] 联机大厅模拟数据，传入该参数后获取结果将使用该数据，正式服环境会忽略该参数；默认为None

        :return: 无
        :rtype: None
        """
        if isinstance(player, str):
            player = self._to_uid(player)
        callback = kwargs['callback']
        simulate = kwargs['simulate']
        if not keys:
            keys = self.global_data.keys() if player == 0 else self.uid_data.keys()

        def cb(response):
            if response:
                self._simplify_response(response)
                self._set_default(response, keys)
                self._update_cache(player, response['data'])
            if callback:
                callback(response)

        if _IS_LOBBY:
            LvComp.Http.LobbyGetStorage(cb, player, keys) # noqa
        else:
            if simulate:
                d = [
                    {'key': k, 'value': v}
                    for k, v in simulate.items()
                ]
            else:
                if player == 0:
                    ex_data = LvComp.ExtraData.GetExtraData(_GLOBAL_DATA_KEY) or {}
                    d = [
                        {'key': k, 'value': v}
                        for k, v in ex_data
                        if k in keys
                    ]
                else:
                    ex_data = LvComp.ExtraData.GetExtraData(_UID_DATA_KEY) or {}
                    d = [
                        {'key': k, 'value': v[player]}
                        for k, v in ex_data.items()
                        if k in keys
                    ]
            cb({'entity': {'data': d}})

    def _set(self, callback, uid, order_id, getter):
        if _IS_LOBBY:
            LvComp.Http.LobbySetStorageAndUserItem(callback, uid, order_id, getter)
        else:
            callback({'entity': {'data': getter()}}) # noqa
            if uid == 0:
                LvComp.ExtraData.SetExtraData(_GLOBAL_DATA_KEY, self.global_data)
            else:
                LvComp.ExtraData.SetExtraData(_UID_DATA_KEY, self.uid_data)

    @kwargs_defaults(order_id=None, callback=None)
    def update(self, key, exp, player=0, **kwargs):
        """
        更新云端数据。

        -----

        :param str key: 数据键
        :param function exp: 更新表达式函数，接受当前数据值作为唯一参数，返回更新后的数据值；如lambda x: x + 1，表述数据自增1
        :param int|str player: 玩家UID或实体ID，传入0表示全局数据，默认为0
        :param int|None order_id: [仅关键字参数] 需要标记为发货的订单ID，默认为None
        :param function|None callback: [仅关键字参数] 设置结果回调函数，默认为None

        :return: 无
        :rtype: None
        """
        if isinstance(player, str):
            player = self._to_uid(player)
        order_id = kwargs['order_id']
        callback = kwargs['callback']

        def cb(response):
            if response:
                self._simplify_response(response)
                self._update_cache(player, response['data'])
            if callback:
                callback(response)
        def getter():
            value = exp(self.get(key, player))
            return [{'key': key, 'value': value}]

        self._set(cb, player, order_id, getter)

    @kwargs_defaults(order_id=None, callback=None)
    def set(self, key, value, player=0, **kwargs):
        """
        强制设置云端某个数据的值。

        注意：若出现数据冲突，本接口将 **强制** 覆盖数据的值，请谨慎使用。

        -----

        :param str key: 数据键
        :param str|int|float|bool|list|dict|None value: 数据值
        :param int|str player: 玩家UID或实体ID，传入0表示全局数据，默认为0
        :param int|None order_id: [仅关键字参数] 需要标记为发货的订单ID，默认为None
        :param function|None callback: [仅关键字参数] 设置结果回调函数，默认为None

        :return: 无
        :rtype: None
        """
        if isinstance(player, str):
            player = self._to_uid(player)
        order_id = kwargs['order_id']
        callback = kwargs['callback']

        def cb(response):
            if response:
                self._simplify_response(response)
                self._update_cache(player, response['data'])
            if callback:
                callback(response)
        def getter():
            return [{'key': key, 'value': value}]

        self._set(cb, player, order_id, getter)

    def get(self, key, player=0):
        """
        从服务端本地缓存中获取数据。

        请先用 ``.register()`` 注册数据再调用本调接口。

        -----

        :param str key: 数据键
        :param int|str player: 玩家UID或实体ID，传入0表示全局数据，默认为0

        :return: 数据值
        :rtype: str|int|float|bool|list|dict|None
        """
        if isinstance(player, str):
            player = self._to_uid(player)
        return self.global_data[key] if player == 0 else self.uid_data[key][player]

    @kwargs_defaults(callback=None)
    def ship(self, order_id, player, **kwargs):
        """
        设置订单发货。

        如需同时设置数据和发货，建议使用 ``.update()`` 或 ``.set()`` 接口。

        -----

        :param int order_id: 订单ID
        :param int|str player: 玩家UID或实体ID
        :param function|None callback: [仅关键字参数] 设置结果回调函数，默认为None

        :return: 无
        :rtype: None
        """
        if isinstance(player, str):
            player = self._to_uid(player)
        callback = kwargs['callback']

        def cb(response):
            if response:
                self._simplify_response(response)
            if callback:
                callback(response)

        if _IS_LOBBY:
            LvComp.Http.LobbySetStorageAndUserItem(cb, player, order_id)
        else:
            cb({'code': 0, 'entity': {'data': []}})

    @kwargs_defaults(callback=None, simulate=None)
    def query(self, player, **kwargs):
        """
        查询还未发货的订单。

        -----

        :param int|str player: 玩家UID或实体ID
        :param function|None callback: [仅关键字参数] 查询结果回调函数，默认为None
        :param dict[int,dict[str,int|str]]|None simulate: [仅关键字参数] 联机大厅模拟数据，传入该参数后查询结果将使用该数据，正式服环境会忽略该参数；默认为None

        :return: 无
        :rtype: None
        """
        if isinstance(player, str):
            player = self._to_uid(player)
        callback = kwargs['callback']
        simulate = kwargs['simulate']

        def cb(response):
            if response:
                self._simplify_response(response)
            if callback:
                callback(response)

        if _IS_LOBBY:
            LvComp.Http.QueryLobbyUserItem(cb, player)
        else:
            d = []
            if simulate:
                for k, v in simulate.items():
                    v['order_id'] = k
                    d.append(v)
            cb({'entity': {'orders': d}})
















