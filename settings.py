import pygame as pg

vec = pg.math.Vector2

FPS = 60
FIELD_COLOR = (0, 0, 0)
BG_COLOR = (50, 50, 50)

SOUND_PATH = 'Sound/SoundEffects/'
MUSIC_PATH = 'Sound/Musics/'
SPRITE_DIR_PATH = 'Sprites/ColorsTheme/Colors'
MENU_SPRITE_PATH = 'Sprites/MainMenu/Menu'
FONT_PATH = 'Font/MatchupPro.ttf'

ANIM_TIME_INTERVAL = 500
FAST_ANIM_TIME_INTERVAL = 30
HOLD_INTERVAL = 0.75
TILE_SIZE = 40
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.3, FIELD_H * 0.45)
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

# User Option
VOLUME = 0.1
HELP_LINE = True
PLAYER_NAME = 'Clement'

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}