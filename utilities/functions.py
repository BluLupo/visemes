#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

MMD_JP_MAPPING = [
    ('あ',       'a',      'A (あ)',                  ['ah', 'a', 'A', 'vrc.v_aa', 'あ']),
    ('い',       'i',      'I / CH (い)',             ['ch', 'i', 'I', 'CH', 'vrc.v_ch', 'vrc.v_ih', 'い']),
    ('う',       'u',      'U (う)',                  ['u', 'U', 'vrc.v_ou', 'う']),
    ('え',       'e',      'E (え)',                  ['e', 'E', 'vrc.v_e', 'え']),
    ('お',       'o',      'O (お)',                  ['oh', 'o', 'O', 'vrc.v_oh', 'お']),
    ('笑い',     'warau',  'Blink Happy (笑い)',      ['blink_happy', 'BlinkHappy', 'blink happy', 'smile', '笑い']),
    ('はう',     'hau',    'Close >< (はう)',         ['close><', 'hau', 'はう']),
    ('ウィンク', 'wink',   'Wink (ウィンク)',         ['wink', 'Wink', 'ウィンク']),
    ('ウィンク右',  'wink_r',  'Wink Right (ウィンク右)',   ['wink_right', 'WinkRight', 'wink right', 'ウィンク右']),
    ('ウィンク２',  'wink2',   'Wink 2 (ウィンク２)',       ['wink_2', 'wink2', 'Wink2', 'wink 2', 'ウィンク２']),
    ('ウィンク２右','wink2_r', 'Wink 2 Right (ウィンク２右)',['wink_2_right', 'Wink2Right', 'wink 2 right', 'ウィンク２右']),
    ('にこり',   'nikori', 'Cheerful (にこり)',       ['cheerful', 'Cheerful', 'nikori', 'にこり']),
    ('真面目',   'majime', 'Serious (真面目)',        ['serious', 'Serious', 'stare', 'calm', '真面目']),
    ('怒り',     'ikari',  'Anger (怒り)',            ['anger', 'angry', 'Anger', 'Angry', '怒り']),
    ('困る',     'komaru', 'Sadness (困る)',          ['sadness', 'sad', 'Sadness', 'Sad', 'komaru', '困る']),
]

VRC_ORDER = [
    'vrc.v_sil',
    'vrc.v_aa',
    'vrc.v_ch',
    'vrc.v_dd',
    'vrc.v_e',
    'vrc.v_ff',
    'vrc.v_ih',
    'vrc.v_kk',
    'vrc.v_nn',
    'vrc.v_oh',
    'vrc.v_ou',
    'vrc.v_pp',
    'vrc.v_rr',
    'vrc.v_ss',
    'vrc.v_th',
    'vrc.blink',
]


def build_viseme_map(shape_a, shape_o, shape_ch):
    m = OrderedDict()
    m['vrc.v_aa']  = [(shape_a,  0.9998)]
    m['vrc.v_ch']  = [(shape_ch, 0.9996)]
    m['vrc.v_dd']  = [(shape_a,  0.3),    (shape_ch, 0.7)]
    m['vrc.v_e']   = [(shape_a,  0.5),    (shape_ch, 0.2)]
    m['vrc.v_ff']  = [(shape_a,  0.2),    (shape_ch, 0.4)]
    m['vrc.v_ih']  = [(shape_ch, 0.7),    (shape_o,  0.3)]
    m['vrc.v_kk']  = [(shape_a,  0.7),    (shape_ch, 0.4)]
    m['vrc.v_nn']  = [(shape_a,  0.2),    (shape_ch, 0.7)]
    m['vrc.v_oh']  = [(shape_a,  0.2),    (shape_o,  0.8)]
    m['vrc.v_ou']  = [(shape_o,  0.9994)]
    m['vrc.v_pp']  = [(shape_a,  0.0004), (shape_o,  0.0004)]
    m['vrc.v_rr']  = [(shape_ch, 0.5),    (shape_o,  0.3)]
    m['vrc.v_sil'] = [(shape_a,  0.0002), (shape_ch, 0.0002)]
    m['vrc.v_ss']  = [(shape_ch, 0.8)]
    m['vrc.v_th']  = [(shape_a,  0.4),    (shape_o,  0.15)]
    return m
