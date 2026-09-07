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


from nuoyanlib.core import error
from nuoyanlib.core._utils import assert_error
from nuoyanlib.core.listener import (
    _EventPool,
    event,
    listen_event,
    unlisten_event,
    listen_all_events,
    unlisten_all_events,
)


a = {
    'playerId': "-114514",
    'pos': (1, 1, 1),
    'itemDict': {'newItemName': "minecraft:apple", 'newAuxValue': 0, 'count': 1},
}
@event("CustomEvent", "a", "b")
def CustomEvent(event):
    print(event)
    assert event.playerId == a['playerId']
    assert event.pos == a['pos']
    assert event.get('itemDict') == a['itemDict']
    assert 'playerId' in event
    for k in event:
        assert event[k] == a[k]
    assert event == a
    assert len(event) == 3
    assert event.keys() == a.keys()
    assert event.values() == a.values()
    assert event.items() == a.items()
    event.playerId = "1919810"
    assert event.playerId == a['playerId'] == "1919810"
listen_event(CustomEvent, use_decorator=True)
_EventPool.get("CustomEvent", "a", "b")(a)


def f():
    @event("xxx")
    def cb(args):
        pass
assert_error(f, exc=error.EventSourceError)
def f():
    @event
    def cb(args):
        pass
assert_error(f, exc=error.EventSourceError)


def call(ns, sys_name, event_name, args):
    # 模拟引擎触发回调函数
    ep = _EventPool.get(event_name, ns, sys_name)
    func = getattr(ep, ep.__call__.__name__)
    func(args)


a = {'arg': 0}
@event()
@event(ns="abc", sys_name="system")
@event("LoadClientAddonScriptsAfter")
@event("event", "mihoyo", "StarRail", 6)
def LoadClientAddonScriptsAfter(args):
    args['arg'] += 1
listen_event(LoadClientAddonScriptsAfter, use_decorator=True)
call("Minecraft", "Engine", "LoadClientAddonScriptsAfter", a)
call("mihoyo", "StarRail", "event", a)
assert a['arg'] == 2
LoadClientAddonScriptsAfter(a)
assert a['arg'] == 3
assert LoadClientAddonScriptsAfter.__name__ == "LoadClientAddonScriptsAfter"
assert LoadClientAddonScriptsAfter._nyl__listen_args == [
    ("event", "mihoyo", "StarRail", 6),
    ("LoadClientAddonScriptsAfter", "Minecraft", "Engine", 0),
    ("LoadClientAddonScriptsAfter", "abc", "system", 0),
    ("LoadClientAddonScriptsAfter", "Minecraft", "Engine", 0),
]
unlisten_event(LoadClientAddonScriptsAfter, use_decorator=True)
assert not _EventPool.get("LoadClientAddonScriptsAfter", "Minecraft", "Engine", False)
assert not _EventPool.get("LoadClientAddonScriptsAfter", "abc", "system", False)
assert not _EventPool.get("event", "mihoyo", "StarRail", False)


n = [0]
class T(object):
    def __init__(self):
        listen_all_events(self)
    @event("LoadClientAddonScriptsAfter")
    @event(ns="x", sys_name="y")
    def CustomEvent(self, args):
        assert self is args[n[0]]
        n[0] += 1
t = T()
t2 = T()
tl = [t, t2]
t.CustomEvent(tl)
t2.CustomEvent(tl)
unlisten_all_events(t)
unlisten_event(t2.CustomEvent, use_decorator=True)
assert not _EventPool.get("CustomEvent", "x", "y", False)
assert not _EventPool.get("LoadClientAddonScriptsAfter", "Minecraft", "Engine", False)
