#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bpy
from utilities.constants import MMD_VISEME_COUNT, MMD_SEP_1, MMD_SEP_2
from utilities.functions import MMD_JP_MAPPING
from utilities.helpers import _ps, guess_shape, _restore_shapekey_values


class VRCVIS_OT_MMDAutoDetect(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.mmd_auto_detect'
    bl_label    = 'Auto-rileva (EN → JP)'
    bl_description = (
        'Cerca automaticamente i nomi inglesi/VRChat comuni e precompila '
        'i campi di destinazione MMD giapponese'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        mesh_name = scene.vrcvis_mesh
        if not mesh_name or mesh_name not in bpy.data.objects:
            self.report({'ERROR'}, 'Nessuna mesh selezionata')
            return {'CANCELLED'}
        obj = bpy.data.objects[mesh_name]
        found = 0
        for _jp, suffix, _en, candidates in MMD_JP_MAPPING:
            result = guess_shape(obj, candidates)
            if result:
                setattr(scene, f'vrcvis_mmd_{suffix}', result)
                found += 1
        if found:
            self.report({'INFO'}, f'Rilevate {found} shape key')
        else:
            self.report({'WARNING'}, 'Nessun nome riconosciuto trovato')
        return {'FINISHED'}


class VRCVIS_OT_MMDConvert(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.mmd_convert'
    bl_label    = 'Converti in MMD'
    bl_description = (
        'Duplica le shape key selezionate con i nomi MMD giapponesi, '
        'aggiunge i separatori e posiziona tutto in fondo alla lista'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        mesh_name = scene.vrcvis_mesh
        if not mesh_name or mesh_name not in bpy.data.objects:
            self.report({'ERROR'}, 'Seleziona una mesh valida')
            return {'CANCELLED'}
        obj = bpy.data.objects[mesh_name]
        if not obj.data.shape_keys:
            self.report({'ERROR'}, 'La mesh non ha shape key')
            return {'CANCELLED'}

        if _ps.active:
            _restore_shapekey_values(obj)
            _ps.active = False
            scene.vrcvis_preview_active = False

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        obj.show_only_shape_key = False

        keys = obj.data.shape_keys.key_blocks
        overwrite = scene.vrcvis_overwrite
        created = []
        skipped = []

        def _add_empty(name):
            if name in keys:
                if overwrite:
                    obj.active_shape_key_index = keys.find(name)
                    bpy.ops.object.shape_key_remove()
                else:
                    skipped.append(name)
                    return
            bpy.ops.object.shape_key_clear()
            obj.shape_key_add(name=name, from_mix=True)
            created.append(name)

        def _add_copy(src_name, dst_name):
            if not src_name or src_name not in keys:
                return
            if dst_name in keys:
                if overwrite:
                    obj.active_shape_key_index = keys.find(dst_name)
                    bpy.ops.object.shape_key_remove()
                else:
                    skipped.append(dst_name)
                    return
            bpy.ops.object.shape_key_clear()
            keys[src_name].slider_max = max(keys[src_name].slider_max, 1.0)
            keys[src_name].value = 1.0
            obj.shape_key_add(name=dst_name, from_mix=True)
            bpy.ops.object.shape_key_clear()
            created.append(dst_name)

        _add_empty(MMD_SEP_1)
        for jp_name, suffix, _en, _ in MMD_JP_MAPPING[:MMD_VISEME_COUNT]:
            src = getattr(scene, f'vrcvis_mmd_{suffix}')
            _add_copy(src, jp_name)

        _add_empty(MMD_SEP_2)
        for jp_name, suffix, _en, _ in MMD_JP_MAPPING[MMD_VISEME_COUNT:]:
            src = getattr(scene, f'vrcvis_mmd_{suffix}')
            _add_copy(src, jp_name)

        obj.active_shape_key_index = 0

        msg_parts = []
        if created:
            msg_parts.append(f'Create: {len(created)}')
        if skipped:
            msg_parts.append(f'Saltate: {len(skipped)}')
        self.report({'INFO'}, ' | '.join(msg_parts) if msg_parts else 'Nessuna shape key creata')
        return {'FINISHED'}


class VRCVIS_OT_MMDRemove(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.mmd_remove'
    bl_label    = 'Rimuovi MMD'
    bl_description = (
        'Rimuove le shape key MMD giapponesi e i separatori '
        '(---MMD Visemes--- e ^MMD Visemes / Other v)'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        mesh_name = scene.vrcvis_mesh
        if not mesh_name or mesh_name not in bpy.data.objects:
            self.report({'ERROR'}, 'Nessuna mesh selezionata')
            return {'CANCELLED'}
        obj = bpy.data.objects[mesh_name]
        if not obj.data.shape_keys:
            self.report({'INFO'}, 'Nessuna shape key presente')
            return {'FINISHED'}

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        mmd_names = {jp for jp, _, _en, _ in MMD_JP_MAPPING} | {MMD_SEP_1, MMD_SEP_2}
        to_remove = [k.name for k in obj.data.shape_keys.key_blocks if k.name in mmd_names]
        count = 0
        for name in to_remove:
            keys = obj.data.shape_keys.key_blocks
            if name in keys:
                obj.active_shape_key_index = keys.find(name)
                bpy.ops.object.shape_key_remove()
                count += 1
        self.report({'INFO'}, f'Rimosse {count} shape key MMD')
        return {'FINISHED'}
