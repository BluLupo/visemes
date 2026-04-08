#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bpy
from utilities.constants import MMD_VISEME_COUNT
from utilities.functions import MMD_JP_MAPPING, VRC_ORDER, build_viseme_map


def viseme_enum_items(self, context):
    vmap = build_viseme_map('_', '_', '_')
    items = [(k, k, '') for k in vmap.keys()]
    items.append(('vrc.blink', 'vrc.blink', ''))
    return items


class VRCVIS_PT_Panel(bpy.types.Panel):
    bl_idname      = 'VIEW3D_PT_visemes_converter'
    bl_label       = 'Visemes Converter'
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = 'Visemes Tool'

    def draw(self, context):
        layout = self.layout
        scene  = context.scene

        box = layout.box()
        box.label(text='Mesh', icon='MESH_DATA')
        mesh_objects = [o for o in bpy.data.objects if o.type == 'MESH' and o.data.shape_keys]
        if not mesh_objects:
            box.label(text='Nessuna mesh con shape key', icon='ERROR')
            return
        box.prop_search(scene, 'vrcvis_mesh', bpy.data, 'objects', text='')

        mesh_name = scene.vrcvis_mesh
        if not mesh_name or mesh_name not in bpy.data.objects:
            layout.label(text='Seleziona una mesh', icon='INFO')
            return
        obj = bpy.data.objects[mesh_name]
        if obj.type != 'MESH' or not obj.data.shape_keys:
            layout.label(text='Mesh senza shape key', icon='ERROR')
            return

        layout.separator(factor=0.3)
        box2 = layout.box()
        box2.label(text='VRChat Visemes (MMD → vrc.*)', icon='SHAPEKEY_DATA')

        row = box2.row()
        row.operator('vrc_viseme.auto_detect', icon='VIEWZOOM', text='Auto-rileva (MMD → VRC)')
        box2.separator(factor=0.5)

        row = box2.row(align=True)
        row.label(text='A  (あ):')
        row.prop_search(scene, 'vrcvis_mouth_a', obj.data.shape_keys, 'key_blocks', text='')

        row = box2.row(align=True)
        row.label(text='O  (お):')
        row.prop_search(scene, 'vrcvis_mouth_o', obj.data.shape_keys, 'key_blocks', text='')

        row = box2.row(align=True)
        row.label(text='CH (い):')
        row.prop_search(scene, 'vrcvis_mouth_ch', obj.data.shape_keys, 'key_blocks', text='')

        row = box2.row(align=True)
        row.label(text='Blink:')
        row.prop_search(scene, 'vrcvis_blink', obj.data.shape_keys, 'key_blocks', text='')

        box2.separator(factor=0.5)
        box2.prop(scene, 'vrcvis_intensity', text='Intensità')
        box2.prop(scene, 'vrcvis_overwrite',  text='Sovrascrivi esistenti')

        box2.separator(factor=0.5)
        row = box2.row(align=True)
        row.scale_y = 1.2
        if scene.vrcvis_preview_active:
            row.operator('vrc_viseme.preview', text='Stop Preview', icon='PAUSE')
            row2 = box2.row(align=True)
            row2.prop(scene, 'vrcvis_preview_viseme', text='')
            row2.operator('vrc_viseme.update_preview', text='', icon='FILE_REFRESH')
        else:
            row.operator('vrc_viseme.preview', text='Preview Viseme', icon='PLAY')

        box2.separator(factor=0.5)
        row = box2.row(align=True)
        row.scale_y = 1.4
        row.operator('vrc_viseme.generate', icon='TRIA_RIGHT')

        row2 = box2.row(align=True)
        row2.operator('vrc_viseme.reorder', icon='SORTSIZE')
        row2.operator('vrc_viseme.remove_all', icon='X')

        if obj.data.shape_keys:
            existing_vrc = [k.name for k in obj.data.shape_keys.key_blocks if k.name.startswith('vrc.')]
            if existing_vrc:
                total = len(VRC_ORDER)
                box5 = box2.box()
                box5.label(text=f'{len(existing_vrc)}/{total} vrc.* presenti', icon='CHECKMARK')
                col = box5.column(align=True)
                for name in VRC_ORDER:
                    r = col.row(align=True)
                    r.label(text=name, icon='CHECKBOX_HLT' if name in existing_vrc else 'CHECKBOX_DEHLT')

        layout.separator(factor=0.3)
        box_mmd = layout.box()
        box_mmd.label(text='Converti in MMD (EN/VRC → JP)', icon='FILE_REFRESH')

        row = box_mmd.row()
        row.operator('vrc_viseme.mmd_auto_detect', icon='VIEWZOOM', text='Auto-rileva (EN → JP)')

        box_mmd.separator(factor=0.4)
        box_mmd.label(text='--- MMD Visemes ---', icon='SHAPEKEY_DATA')
        for _jp, suffix, en_label, _ in MMD_JP_MAPPING[:MMD_VISEME_COUNT]:
            row = box_mmd.row(align=True)
            row.label(text=en_label + ':')
            row.prop_search(scene, f'vrcvis_mmd_{suffix}',
                            obj.data.shape_keys, 'key_blocks', text='')

        box_mmd.separator(factor=0.4)
        box_mmd.label(text='--- Altre forme ---', icon='SHAPEKEY_DATA')
        for _jp, suffix, en_label, _ in MMD_JP_MAPPING[MMD_VISEME_COUNT:]:
            row = box_mmd.row(align=True)
            row.label(text=en_label + ':')
            row.prop_search(scene, f'vrcvis_mmd_{suffix}',
                            obj.data.shape_keys, 'key_blocks', text='')

        box_mmd.separator(factor=0.5)
        row = box_mmd.row(align=True)
        row.scale_y = 1.4
        row.operator('vrc_viseme.mmd_convert', icon='DUPLICATE')
        row.operator('vrc_viseme.mmd_remove', icon='X')
