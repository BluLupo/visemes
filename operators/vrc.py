#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bpy
from utilities.constants import MMD_CANDIDATES
from utilities.functions import build_viseme_map, VRC_ORDER
from utilities.helpers import _ps, guess_shape, _save_shapekey_values, _restore_shapekey_values, _apply_mix


class VRCVIS_OT_AutoDetect(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.auto_detect'
    bl_label    = 'Auto-rileva (MMD → VRC)'
    bl_description = (
        'Cerca automaticamente tra i nomi MMD comuni (あ/お/い/まばたき) '
        'e precompila i campi A/O/CH/Blink'
    )
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        mesh_name = scene.vrcvis_mesh
        if not mesh_name or mesh_name not in bpy.data.objects:
            self.report({'ERROR'}, 'Nessuna mesh selezionata')
            return {'CANCELLED'}
        obj = bpy.data.objects[mesh_name]
        found_a     = guess_shape(obj, MMD_CANDIDATES['a'])
        found_o     = guess_shape(obj, MMD_CANDIDATES['o'])
        found_ch    = guess_shape(obj, MMD_CANDIDATES['ch'])
        found_blink = guess_shape(obj, MMD_CANDIDATES['blink'])
        if found_a:     scene.vrcvis_mouth_a  = found_a
        if found_o:     scene.vrcvis_mouth_o  = found_o
        if found_ch:    scene.vrcvis_mouth_ch = found_ch
        if found_blink: scene.vrcvis_blink    = found_blink
        detected = ', '.join(filter(None, [found_a, found_o, found_ch, found_blink]))
        if detected:
            self.report({'INFO'}, f'Rilevate: {detected}')
        else:
            self.report({'WARNING'}, 'Nessun nome MMD riconosciuto trovato')
        return {'FINISHED'}


class VRCVIS_OT_Preview(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.preview'
    bl_label    = 'Preview Viseme'
    bl_description = 'Attiva/disattiva anteprima viseme in viewport'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        scene = context.scene
        mesh_name = scene.vrcvis_mesh
        if not mesh_name or mesh_name not in bpy.data.objects:
            self.report({'ERROR'}, 'Mesh non valida')
            return {'CANCELLED'}
        obj = bpy.data.objects[mesh_name]
        if not obj.data.shape_keys:
            self.report({'ERROR'}, 'La mesh non ha shape key')
            return {'CANCELLED'}

        if _ps.active:
            _restore_shapekey_values(obj)
            _ps.active = False
            scene.vrcvis_preview_active = False
        else:
            _save_shapekey_values(obj)
            _ps.active = True
            scene.vrcvis_preview_active = True
            sel = scene.vrcvis_preview_viseme
            if sel == 'vrc.blink':
                blink_src = scene.vrcvis_blink
                if blink_src:
                    _apply_mix(obj, [(blink_src, 1.0)], scene.vrcvis_intensity)
            else:
                vmap = build_viseme_map(
                    scene.vrcvis_mouth_a, scene.vrcvis_mouth_o, scene.vrcvis_mouth_ch)
                if sel in vmap:
                    _apply_mix(obj, vmap[sel], scene.vrcvis_intensity)
        return {'FINISHED'}


class VRCVIS_OT_UpdatePreview(bpy.types.Operator):
    bl_idname  = 'vrc_viseme.update_preview'
    bl_label   = 'Aggiorna Preview'
    bl_options = {'INTERNAL'}

    def execute(self, context):
        scene = context.scene
        if not _ps.active:
            return {'FINISHED'}
        mesh_name = scene.vrcvis_mesh
        if not mesh_name or mesh_name not in bpy.data.objects:
            return {'CANCELLED'}
        obj = bpy.data.objects[mesh_name]
        sel = scene.vrcvis_preview_viseme
        if sel == 'vrc.blink':
            blink_src = scene.vrcvis_blink
            if blink_src:
                _apply_mix(obj, [(blink_src, 1.0)], scene.vrcvis_intensity)
        else:
            vmap = build_viseme_map(
                scene.vrcvis_mouth_a, scene.vrcvis_mouth_o, scene.vrcvis_mouth_ch)
            if sel in vmap:
                _apply_mix(obj, vmap[sel], scene.vrcvis_intensity)
        return {'FINISHED'}


class VRCVIS_OT_Generate(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.generate'
    bl_label    = 'Genera Visemes VRChat'
    bl_description = (
        'Crea le 15 shape key vrc.v_* mescolando A/O/CH con i pesi standard VRChat, '
        'più vrc.blink se il sorgente blink è impostato'
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

        shape_a     = scene.vrcvis_mouth_a
        shape_o     = scene.vrcvis_mouth_o
        shape_ch    = scene.vrcvis_mouth_ch
        shape_blink = scene.vrcvis_blink
        intensity   = scene.vrcvis_intensity

        keys = obj.data.shape_keys.key_blocks
        for name, label in [(shape_a, 'A'), (shape_o, 'O'), (shape_ch, 'CH')]:
            if not name or name not in keys:
                self.report({'ERROR'}, f'Shape key {label} ("{name}") non trovata')
                return {'CANCELLED'}
        if len({shape_a, shape_o, shape_ch}) < 3:
            self.report({'ERROR'}, 'Le tre shape key sorgente devono essere diverse')
            return {'CANCELLED'}

        if _ps.active:
            _restore_shapekey_values(obj)
            _ps.active = False
            scene.vrcvis_preview_active = False

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        obj.show_only_shape_key = False

        vmap = build_viseme_map(shape_a, shape_o, shape_ch)
        if shape_blink and shape_blink in keys:
            vmap['vrc.blink'] = [(shape_blink, 1.0)]

        wm = bpy.context.window_manager
        wm.progress_begin(0, len(vmap))
        created = []
        skipped = []

        for idx, (vrc_name, mix) in enumerate(vmap.items()):
            wm.progress_update(idx)
            if vrc_name in keys:
                if scene.vrcvis_overwrite:
                    obj.active_shape_key_index = keys.find(vrc_name)
                    bpy.ops.object.shape_key_remove()
                else:
                    skipped.append(vrc_name)
                    continue

            bpy.ops.object.shape_key_clear()
            for shape_name, weight in mix:
                if shape_name in keys:
                    keys[shape_name].slider_max = 10.0
                    keys[shape_name].value = weight * intensity

            obj.shape_key_add(name=vrc_name, from_mix=True)

            bpy.ops.object.shape_key_clear()
            for shape_name, _ in mix:
                if shape_name in keys:
                    keys[shape_name].slider_max = 1.0

            created.append(vrc_name)

        obj.active_shape_key_index = 0
        wm.progress_end()

        msg_parts = []
        if created:
            msg_parts.append(f'Create: {len(created)}')
        if skipped:
            msg_parts.append(f'Saltate (già esistenti): {len(skipped)}')
        self.report({'INFO'}, ' | '.join(msg_parts) if msg_parts else 'Nessuna shape key generata')
        return {'FINISHED'}


class VRCVIS_OT_RemoveAll(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.remove_all'
    bl_label    = 'Rimuovi vrc.*'
    bl_description = 'Cancella tutte le shape key il cui nome inizia con "vrc." (visemi + blink)'
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
        to_remove = [k.name for k in obj.data.shape_keys.key_blocks if k.name.startswith('vrc.')]
        count = 0
        for name in to_remove:
            keys = obj.data.shape_keys.key_blocks
            if name in keys:
                obj.active_shape_key_index = keys.find(name)
                bpy.ops.object.shape_key_remove()
                count += 1
        self.report({'INFO'}, f'Rimosse {count} shape key vrc.*')
        return {'FINISHED'}


class VRCVIS_OT_Reorder(bpy.types.Operator):
    bl_idname   = 'vrc_viseme.reorder'
    bl_label    = 'Riordina VRC Keys'
    bl_description = "Riordina le shape key vrc.* nell'ordine standard VRChat subito sotto Basis"
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

        keys = obj.data.shape_keys.key_blocks
        target_pos = 1
        moved = 0

        for name in VRC_ORDER:
            if name not in keys:
                continue
            current_idx = keys.find(name)
            steps = current_idx - target_pos
            if steps > 0:
                obj.active_shape_key_index = current_idx
                for _ in range(steps):
                    bpy.ops.object.shape_key_move(type='UP')
            target_pos += 1
            moved += 1

        obj.active_shape_key_index = 0
        self.report({'INFO'}, f'Riordinate {moved} shape key')
        return {'FINISHED'}
