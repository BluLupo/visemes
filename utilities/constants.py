#!/usr/bin/env python
# -*- coding: utf-8 -*-

MMD_VISEME_COUNT = 5
MMD_SEP_1 = '---MMD Visemes---'
MMD_SEP_2 = '^MMD Visemes / Other v'

MMD_CANDIDATES = {
    'a':  ['あ', 'a', 'A', 'mouth_a', 'Mouth_A', 'あ口', 'v_a'],
    'o':  ['お', 'o', 'O', 'mouth_o', 'Mouth_O', 'お口', 'v_o'],
    'ch': ['い', 'ch', 'CH', 'mouth_i', 'Mouth_I', 'い口', 'v_ch', 'i', 'I'],
    'blink': [
        'まばたき', '目閉じ', '眼閉じ', 'ウィンク２',
        'Blink', 'blink', 'blink_all',
        'eye_blink', 'Eye_Blink', 'eyes_blink', 'Eyes_Blink',
        'eye_close', 'Eye_Close', 'eyes_close', 'Eyes_Close',
    ],
}
