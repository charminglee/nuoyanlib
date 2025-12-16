# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2025 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2025-12-17
#  ⠀
# =================================================


from ..core.client.comp import CF
from ..core.client import _lib_client


__all__ = [
    "set_query_mod_var",
    "add_player_render_resources",
    "add_entity_render_resources",
]


def set_query_mod_var(entity_id, name, value, sync=True):
    """
    设置指定实体 ``query.mod`` 变量的值。

    支持全局同步（即所有客户端同步设置该变量的值）。
    若不进行全局同步，则本次设置只对当前客户端有效。
    若设置的变量未注册，会自动进行注册。

    -----

    :param str entity_id: 实体ID
    :param str name: 变量名，仅支持query.mod开头的变量
    :param float value: 设置的值
    :param bool sync: 是否进行全局同步，默认为True

    :return: 无
    :rtype: None
    """
    lib_sys = _lib_client.instance()
    data = {'entity_id': entity_id, 'name': name, 'value': value}
    lib_sys._SetQueryVar(data)
    if sync:
        lib_sys.NotifyToServer("_SetQueryVar", data)


def add_player_render_resources(player_id, rebuild, *res_tuple):
    """
    一次性添加多个玩家渲染资源。

    支持添加模型、贴图、材质、渲染控制器、动画、动画控制器、音效和微软粒子特效。

    注意：使用本接口添加的资源的identifier，需要遵循以下命名规范：

    - 模型：以 ``geometry.`` 开头；
    - 贴图：无特别要求；
    - 材质：无特别要求；
    - 渲染控制器：以 ``controller.render.`` 开头；
    - 动画：以 ``animation.`` 开头；
    - 动画控制器：以 ``controller.animation.`` 开头；
    - 音效：音效名称至少包含一个“.”，如 ``sound.abc``；
    - 微软粒子特效：需要包含命名空间。

    -----

    :param str player_id: 玩家实体ID
    :param bool rebuild: 是否重建玩家的数据渲染器，传入True时会自动调用RebuildPlayerRender接口
    :param tuple[str,str] res_tuple: [变长位置参数] 渲染资源元组，第一个元素为资源键名（短名称），第二个参数为具体资源名称（模型ID、贴图路径、动画名称等）

    :return: 返回添加结果（是否成功），结果为一个元组，元素类型为bool，与res_tuple一一对应
    :rtype: tuple[bool]
    """
    res = []
    comp = CF(player_id).ActorRender
    for arg in res_tuple:
        if arg[1].startswith("geometry."):
            res.append(comp.AddPlayerGeometry(*arg))
        elif "/" in arg[1]:
            res.append(comp.AddPlayerTexture(*arg))
        elif arg[0].startswith("controller.render."):
            res.append(comp.AddPlayerRenderController(*arg))
        elif arg[1].startswith("animation."):
            res.append(comp.AddPlayerAnimation(*arg))
        elif arg[1].startswith("controller.animation."):
            res.append(comp.AddPlayerAnimationController(*arg))
        elif ":" in arg[1]:
            res.append(comp.AddPlayerParticleEffect(*arg))
        elif "." in arg[1]:
            res.append(comp.AddPlayerSoundEffect(*arg))
        else:
            res.append(comp.AddPlayerRenderMaterial(*arg))
    if rebuild:
        comp.RebuildPlayerRender()
    return tuple(res)


def add_entity_render_resources(entity_id, rebuild, *res_tuple):
    """
    一次性添加多个实体渲染资源。

    支持添加模型、贴图、材质、渲染控制器、动画、动画控制器、音效和微软粒子特效。

    注意：使用本接口添加的资源的identifier，需要遵循以下命名规范：

    - 模型：以 ``geometry.`` 开头；
    - 贴图：无特别要求；
    - 材质：无特别要求；
    - 渲染控制器：以 ``controller.render.`` 开头；
    - 动画：以 ``animation.`` 开头；
    - 动画控制器：以 ``controller.animation.`` 开头；
    - 音效：音效名称至少包含一个“.”，如 ``sound.abc``；
    - 微软粒子特效：需要包含命名空间。

    -----

    :param str entity_id: 实体ID
    :param bool rebuild: 是否重建实体的数据渲染器，传入True时会自动调用RebuildActorRender接口
    :param tuple[str,str] res_tuple: [变长位置参数] 渲染资源元组，第一个元素为资源键名（短名称），第二个参数为具体资源名称（模型ID、贴图路径、动画名称等）

    :return: 返回添加结果（是否成功），结果为一个元组，元素类型为bool，与res_tuple一一对应
    :rtype: tuple[bool]
    """
    res = []
    cf = CF(entity_id)
    render = cf.ActorRender
    etype = cf.EngineType.GetEngineTypeStr()
    for arg in res_tuple:
        if arg[1].startswith("geometry."):
            res.append(render.AddActorGeometry(etype, *arg))
        elif "/" in arg[1]:
            res.append(render.AddActorTexture(etype, *arg))
        elif arg[0].startswith("controller.render."):
            res.append(render.AddActorRenderController(etype, *arg))
        elif arg[1].startswith("animation."):
            res.append(render.AddActorAnimation(etype, *arg))
        elif arg[1].startswith("controller.animation."):
            res.append(render.AddActorAnimationController(etype, *arg))
        elif ":" in arg[1]:
            res.append(render.AddActorParticleEffect(etype, *arg))
        elif "." in arg[1]:
            res.append(render.AddActorSoundEffect(etype, *arg))
        else:
            res.append(render.AddActorRenderMaterial(etype, *arg))
    if rebuild:
        render.RebuildActorRender(etype)
    return tuple(res)
















