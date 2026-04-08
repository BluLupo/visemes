#!/usr/bin/env python
# -*- coding: utf-8 -*-


class _PreviewState:
    active = False
    saved_values: dict = {}


_ps = _PreviewState()


def guess_shape(mesh_obj, candidates):
    if not mesh_obj or not mesh_obj.data.shape_keys:
        return ''
    keys = [k.name for k in mesh_obj.data.shape_keys.key_blocks]
    for c in candidates:
        if c in keys:
            return c
    return ''


def _save_shapekey_values(mesh_obj):
    _ps.saved_values = {k.name: k.value for k in mesh_obj.data.shape_keys.key_blocks}


def _restore_shapekey_values(mesh_obj):
    for k in mesh_obj.data.shape_keys.key_blocks:
        k.value = _ps.saved_values.get(k.name, 0.0)


def _reset_all_shapekeys(mesh_obj):
    for k in mesh_obj.data.shape_keys.key_blocks:
        k.value = 0.0


def _apply_mix(mesh_obj, mix, intensity):
    _reset_all_shapekeys(mesh_obj)
    keys = mesh_obj.data.shape_keys.key_blocks
    for shape_name, weight in mix:
        if shape_name in keys:
            keys[shape_name].value = weight * intensity
