#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Credits:
#   Thanks to https://github.com/ShyWolf42/Copy-to-MMD-Visemes
#   Thanks to https://github.com/teamneoneko/Cats-Blender-Plugin


bl_info = {
    "name": "Visemes Converter Tool",
    "author": "Custom",
    "version": (2, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Visemes Tool",
    "description": (
        "Generates VRChat visemes (vrc.v_* + vrc.blink) from MMD blendshapes, "
        "and converts blendshapes from English/VRChat to Japanese MMD format"
    ),
    "category": "Rigging",
}

import bpy
from operators import (
    VRCVIS_OT_AutoDetect,
    VRCVIS_OT_Preview,
    VRCVIS_OT_UpdatePreview,
    VRCVIS_OT_Generate,
    VRCVIS_OT_RemoveAll,
    VRCVIS_OT_Reorder,
    VRCVIS_OT_MMDAutoDetect,
    VRCVIS_OT_MMDConvert,
    VRCVIS_OT_MMDRemove,
)
from panels import VRCVIS_PT_Panel, viseme_enum_items
from utilities.functions import MMD_JP_MAPPING
from utilities.helpers import _ps, _restore_shapekey_values

_CLASSES = [
    VRCVIS_OT_AutoDetect,
    VRCVIS_OT_Preview,
    VRCVIS_OT_UpdatePreview,
    VRCVIS_OT_Generate,
    VRCVIS_OT_RemoveAll,
    VRCVIS_OT_Reorder,
    VRCVIS_OT_MMDAutoDetect,
    VRCVIS_OT_MMDConvert,
    VRCVIS_OT_MMDRemove,
    VRCVIS_PT_Panel,
]

_MMD_PROPS = [f'vrcvis_mmd_{suffix}' for _, suffix, _en, _ in MMD_JP_MAPPING]


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.Scene.vrcvis_mesh = bpy.props.StringProperty(
        name='Mesh', description='Mesh su cui operare', default='')
    bpy.types.Scene.vrcvis_mouth_a = bpy.props.StringProperty(
        name='Mouth A', description='Shape key bocca aperta (あ / A)', default='')
    bpy.types.Scene.vrcvis_mouth_o = bpy.props.StringProperty(
        name='Mouth O', description='Shape key bocca rotonda (お / O)', default='')
    bpy.types.Scene.vrcvis_mouth_ch = bpy.props.StringProperty(
        name='Mouth CH', description='Shape key bocca stretta (い / CH)', default='')
    bpy.types.Scene.vrcvis_blink = bpy.props.StringProperty(
        name='Blink', description='Shape key occhi chiusi (まばたき / Blink)', default='')
    bpy.types.Scene.vrcvis_intensity = bpy.props.FloatProperty(
        name='Intensità', description='Moltiplicatore globale dei pesi',
        default=1.0, min=0.0, max=2.0, step=1)
    bpy.types.Scene.vrcvis_overwrite = bpy.props.BoolProperty(
        name='Sovrascrivi esistenti',
        description='Rigenera le shape key già presenti',
        default=True)
    bpy.types.Scene.vrcvis_preview_active = bpy.props.BoolProperty(
        name='Preview attiva', default=False)
    bpy.types.Scene.vrcvis_preview_viseme = bpy.props.EnumProperty(
        name='Viseme', description='Viseme da mostrare in anteprima',
        items=viseme_enum_items)

    for jp_name, suffix, _en, _ in MMD_JP_MAPPING:
        setattr(bpy.types.Scene, f'vrcvis_mmd_{suffix}',
                bpy.props.StringProperty(
                    name=jp_name,
                    description=f'Shape key sorgente per {jp_name}',
                    default=''))


def unregister():
    scene = bpy.context.scene if bpy.context else None
    if _ps.active and scene:
        mesh_name = scene.get('vrcvis_mesh', '')
        if mesh_name and mesh_name in bpy.data.objects:
            _restore_shapekey_values(bpy.data.objects[mesh_name])
        _ps.active = False

    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)

    for prop in (
        'vrcvis_mesh', 'vrcvis_mouth_a', 'vrcvis_mouth_o', 'vrcvis_mouth_ch',
        'vrcvis_blink', 'vrcvis_intensity', 'vrcvis_overwrite',
        'vrcvis_preview_active', 'vrcvis_preview_viseme',
        *_MMD_PROPS,
    ):
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)


if __name__ == '__main__':
    register()
