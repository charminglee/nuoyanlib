# -*- coding: utf-8 -*-
# =================================================
#  ⠀
#   Copyright (c) 2026 Nuoyan
#  ⠀
#   Author: Nuoyan <https://github.com/charminglee>
#   Email : 1279735247@qq.com
#   Date  : 2026-1-17
#  ⠀
# =================================================


from ..core._utils import kwargs_defaults
from ..core.client.comp import CF


__all__ = [
    "add_entity_render_resources",
]


@kwargs_defaults(rebuild=False)
def add_entity_render_resources(entity_id, *res_tuple, **kwargs):
    """
    一次性添加多个实体渲染资源。

    支持玩家与其他实体。

    说明
    ----

    使用本接口添加的资源的名称，需要遵循以下命名规范：

    - 模型：以 ``geometry.`` 开头；
    - 渲染控制器：以 ``controller.render.`` 开头；
    - 动画：以 ``animation.`` 开头；
    - 动画控制器：以 ``controller.animation.`` 开头；
    - 音效：音效名称至少包含一个 "."，如 ``sound.abc``；
    - 贴图：无特别要求；
    - 材质：无特别要求；
    - 微软粒子：无特别要求。

    示例
    ----

    >>> nyl.add_entity_render_resources(
    ...     entity_id,
    ...     ("default", "geometry.my_model"),
    ...     ("default", "entity_alphatest"),
    ...     ("default", "texture/my_model"),
    ...     ("walk", "animation.player.walk"),
    ...     ("walk_controller", "controller.animation.player.walk"),
    ...     ("walk", "player.walk"),
    ...     rebuild=True,
    ... )
    (True, True, True, True, True, True)

    -----

    :param str entity_id: 实体ID
    :param tuple[str,str] res_tuple: [变长位置参数] 渲染资源元组，元组第一个元素为资源键名（短名称），第二个元素为具体资源名称（模型ID、贴图路径、动画名称等）
    :param bool rebuild: [仅关键字参数] 是否重建实体的数据渲染器，传入 True 时会自动调用 Rebuild 接口

    :return: 返回一个元组，元素类型为 bool，表示各个渲染资源的添加结果（是否成功）
    :rtype: tuple[bool]
    """
    res = []
    cf = CF(entity_id)
    comp = cf.ActorRender
    etype = cf.EngineType.GetEngineTypeStr()

    if etype == "minecraft:player":
        for k, v in res_tuple:
            if v.startswith("geometry."):
                res.append(comp.AddPlayerGeometry(k, v))
            elif "/" in v:
                res.append(comp.AddPlayerTexture(k, v))
            elif k.startswith("controller.render."):
                res.append(comp.AddPlayerRenderController(k, v))
            elif v.startswith("animation."):
                res.append(comp.AddPlayerAnimation(k, v))
            elif v.startswith("controller.animation."):
                res.append(comp.AddPlayerAnimationController(k, v))
            elif ":" in v:
                res.append(comp.AddPlayerParticleEffect(k, v))
            elif "." in v:
                res.append(comp.AddPlayerSoundEffect(k, v))
            else:
                res.append(comp.AddPlayerRenderMaterial(k, v))
        if kwargs['rebuild']:
            comp.RebuildPlayerRender()

    else:
        for k, v in res_tuple:
            if v.startswith("geometry."):
                res.append(comp.AddActorGeometry(etype, k, v))
            elif "/" in v:
                res.append(comp.AddActorTexture(etype, k, v))
            elif k.startswith("controller.render."):
                res.append(comp.AddActorRenderController(etype, k, v))
            elif v.startswith("animation."):
                res.append(comp.AddActorAnimation(etype, k, v))
            elif v.startswith("controller.animation."):
                res.append(comp.AddActorAnimationController(etype, k, v))
            elif ":" in v:
                res.append(comp.AddActorParticleEffect(etype, k, v))
            elif "." in v:
                res.append(comp.AddActorSoundEffect(etype, k, v))
            else:
                res.append(comp.AddActorRenderMaterial(etype, k, v))
        if kwargs['rebuild']:
            comp.RebuildActorRender(etype)

    return tuple(res)
















