# Visemes Converter Tool — Documentation

Blender add-on for generating VRChat visemes from MMD blendshapes and for converting shape key names to Japanese MMD format.

**Version:** 2.0.0
**Minimum Blender:** 3.0.0
**UI Location:** View3D › Sidebar (N) › Visemes Tool
**Category:** Rigging

---

## Installation

1. `Edit > Preferences > Add-ons > Install`
2. Select the `visemes.py` file (or the zipped folder)
3. Enable the add-on from the list

---

## Project Structure

```
plugin_blender/
├── visemes.py                  # Entry point: bl_info, register/unregister
├── operators/
│   ├── __init__.py             # Exports all operators
│   ├── vrc.py                  # VRChat viseme generation operators
│   └── mmd.py                  # Japanese MMD conversion operators
├── panels/
│   ├── __init__.py             # Exports the panel
│   └── main_panel.py           # UI panel and preview dropdown
└── utilities/
    ├── constants.py            # MMD constants and auto-detect candidates
    ├── functions.py            # Mapping data and build_viseme_map
    └── helpers.py              # Preview state and utility functions
```

---

## Modules

### `visemes.py`

Add-on entry point. Contains `bl_info`, the `_CLASSES` list of all classes to register, `_MMD_PROPS` with the dynamic MMD property names, and the `register()` / `unregister()` functions that manage the add-on lifecycle in Blender.

---

### `utilities/constants.py`

| Name | Type | Description |
|------|------|-------------|
| `MMD_VISEME_COUNT` | `int` | Number of primary MMD visemes (あいうえお = 5) |
| `MMD_SEP_1` | `str` | Separator shape key name for visemes (`---MMD Visemes---`) |
| `MMD_SEP_2` | `str` | Separator shape key name for other expressions (`^MMD Visemes / Other v`) |
| `MMD_CANDIDATES` | `dict` | Candidate names for auto-detection of source shape keys (keys: `a`, `o`, `ch`, `blink`) |

---

### `utilities/functions.py`

| Name | Type | Description |
|------|------|-------------|
| `MMD_JP_MAPPING` | `list[tuple]` | List of 15 entries `(jp_name, suffix, en_label, candidates)` mapping English/VRChat shape keys to Japanese MMD names |
| `VRC_ORDER` | `list[str]` | Standard VRChat order for the 16 visemes (`vrc.v_sil` … `vrc.blink`) |
| `build_viseme_map(shape_a, shape_o, shape_ch)` | `function` | Builds an `OrderedDict` mapping each VRChat name (`vrc.v_*`) to a list of `(shape_key, weight)` pairs computed from the three source shape keys |

#### `build_viseme_map` weights

| VRChat Viseme | Contributions |
|---------------|--------------|
| `vrc.v_aa` | A × 0.9998 |
| `vrc.v_ch` | CH × 0.9996 |
| `vrc.v_dd` | A × 0.3 + CH × 0.7 |
| `vrc.v_e`  | A × 0.5 + CH × 0.2 |
| `vrc.v_ff` | A × 0.2 + CH × 0.4 |
| `vrc.v_ih` | CH × 0.7 + O × 0.3 |
| `vrc.v_kk` | A × 0.7 + CH × 0.4 |
| `vrc.v_nn` | A × 0.2 + CH × 0.7 |
| `vrc.v_oh` | A × 0.2 + O × 0.8 |
| `vrc.v_ou` | O × 0.9994 |
| `vrc.v_pp` | A × 0.0004 + O × 0.0004 |
| `vrc.v_rr` | CH × 0.5 + O × 0.3 |
| `vrc.v_sil`| A × 0.0002 + CH × 0.0002 |
| `vrc.v_ss` | CH × 0.8 |
| `vrc.v_th` | A × 0.4 + O × 0.15 |

---

### `utilities/helpers.py`

| Name | Type | Description |
|------|------|-------------|
| `_PreviewState` | `class` | Holds `active` (bool) and `saved_values` (dict) representing the current preview state |
| `_ps` | `_PreviewState` | Global instance shared across all modules |
| `guess_shape(mesh_obj, candidates)` | `function` | Iterates over `candidates` and returns the first name found among the mesh's shape keys, or `''` |
| `_save_shapekey_values(mesh_obj)` | `function` | Saves the current values of all shape keys into `_ps.saved_values` |
| `_restore_shapekey_values(mesh_obj)` | `function` | Restores shape key values from `_ps.saved_values` |
| `_reset_all_shapekeys(mesh_obj)` | `function` | Sets the value of every shape key on the mesh to `0.0` |
| `_apply_mix(mesh_obj, mix, intensity)` | `function` | Resets all shape keys then applies the `mix` list of `(name, weight)` pairs scaled by `intensity` |

---

### `operators/vrc.py`

Operators for VRChat viseme generation.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `VRCVIS_OT_AutoDetect` | `vrc_viseme.auto_detect` | Searches for common MMD shape key names and fills in the A/O/CH/Blink fields |
| `VRCVIS_OT_Preview` | `vrc_viseme.preview` | Toggles a live viewport preview of the selected viseme |
| `VRCVIS_OT_UpdatePreview` | `vrc_viseme.update_preview` | Refreshes the preview when the selected viseme or intensity changes |
| `VRCVIS_OT_Generate` | `vrc_viseme.generate` | Generates the 15 `vrc.v_*` shape keys plus `vrc.blink` by mixing the three source shape keys |
| `VRCVIS_OT_RemoveAll` | `vrc_viseme.remove_all` | Deletes all shape keys whose name starts with `vrc.` |
| `VRCVIS_OT_Reorder` | `vrc_viseme.reorder` | Reorders `vrc.*` shape keys according to `VRC_ORDER`, placing them immediately after `Basis` |

---

### `operators/mmd.py`

Operators for EN/VRChat → Japanese MMD conversion.

| Class | `bl_idname` | Description |
|-------|-------------|-------------|
| `VRCVIS_OT_MMDAutoDetect` | `vrc_viseme.mmd_auto_detect` | Automatically detects English/VRChat names and fills in the MMD fields |
| `VRCVIS_OT_MMDConvert` | `vrc_viseme.mmd_convert` | Duplicates shape keys with Japanese MMD names and inserts the separators |
| `VRCVIS_OT_MMDRemove` | `vrc_viseme.mmd_remove` | Removes all Japanese MMD shape keys and separators |

---

### `panels/main_panel.py`

| Name | Type | Description |
|------|------|-------------|
| `viseme_enum_items(self, context)` | `function` | Callback for the preview `EnumProperty`; returns all VRChat visemes plus `vrc.blink` |
| `VRCVIS_PT_Panel` | `bpy.types.Panel` | Main panel in the Blender Sidebar; `bl_idname = VIEW3D_PT_visemes_converter` |

---

## Scene Properties (`bpy.types.Scene`)

All properties are registered by `register()` in `visemes.py` with the `vrcvis_` prefix.

| Property | Type | Description |
|----------|------|-------------|
| `vrcvis_mesh` | `StringProperty` | Name of the target mesh |
| `vrcvis_mouth_a` | `StringProperty` | Open-mouth shape key (あ / A) |
| `vrcvis_mouth_o` | `StringProperty` | Round-mouth shape key (お / O) |
| `vrcvis_mouth_ch` | `StringProperty` | Narrow-mouth shape key (い / CH) |
| `vrcvis_blink` | `StringProperty` | Eyes-closed shape key (まばたき / Blink) |
| `vrcvis_intensity` | `FloatProperty` | Global weight multiplier (0.0 – 2.0, default 1.0) |
| `vrcvis_overwrite` | `BoolProperty` | If `True`, regenerates already-existing shape keys |
| `vrcvis_preview_active` | `BoolProperty` | Internal preview state (True = preview on) |
| `vrcvis_preview_viseme` | `EnumProperty` | Viseme selected for preview |
| `vrcvis_mmd_{suffix}` | `StringProperty` | One property per entry in `MMD_JP_MAPPING` (suffix from column 2) |

---

## Typical Workflow

```
1. Select a mesh with shape keys in the Mesh field
2. Press "Auto-detect (MMD → VRC)" to detect A / O / CH / Blink
   or select them manually
3. (Optional) Use "Preview Viseme" to check the result before generating
4. Press "Generate VRChat Visemes" → creates the vrc.v_* + vrc.blink shape keys
5. (Optional) Press "Reorder VRC Keys" to apply the standard VRChat order
6. (Optional) In the MMD section:
   a. "Auto-detect (EN → JP)" to map English names to Japanese
   b. "Convert to MMD" to create Japanese shape keys with separators
```
