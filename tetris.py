import settings
from settings import *
from tetromino import Tetromino
import pygame.freetype as ft


class Button:
    def __init__(self, app, sprite, hover_sprite, size, rect, command):

        self.app = app
        self.rect = pg.Rect(rect, size)
        self.sprite = pg.transform.scale(pg.image.load(sprite),size )
        self.hover_sprite = pg.transform.scale(pg.image.load(hover_sprite), size)
        self.command = command
        self.hover = False

    def render(self):
        if self.hover:
            self.app.screen.blit(self.hover_sprite, self.rect)
        else:
            self.app.screen.blit(self.sprite, self.rect)

    def get_event(self, event):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.command()


class Menu:
    def __init__(self, app):
        self.app = app
        self.sprite_path = MENU_SPRITE_PATH
        self.start_button = Button(app, f"Sprites/MainMenu/Start0.png", f"Sprites/MainMenu/Start1.png",
                                   (WIN_W * 0.50, WIN_H * 0.10), (WIN_W * 0.26, WIN_H * 0.4), lambda: self.app.tetris.change_game_state('game', 'basic'))
        self.start_button_marathon = Button(app, f"Sprites/MainMenu/marathon0.png", f"Sprites/MainMenu/marathon1.png",
                                   (WIN_W * 0.55, WIN_H * 0.10), (WIN_W * 0.235, WIN_H * 0.52), lambda: self.app.tetris.change_game_state('game', 'marathon'))
        self.score_board_button = Button(app, f"Sprites/MainMenu/scoreboard0.png", f"Sprites/MainMenu/scoreboard1.png",
                                   (WIN_W * 0.60, WIN_H * 0.10), (WIN_W * 0.212, WIN_H * 0.64), lambda: self.app.tetris.change_game_state('scoreboard', None))

    def load_image(self, file, size):
        image = pg.transform.scale(pg.image.load(MENU_SPRITE_PATH + str(file) + '.png').convert_alpha(), (size[0], size[1]))
        return image

    def draw(self):
        if self.app.tetris.game_state == 'main_menu':
            self.app.screen.blit(self.load_image(0, (WIN_W * 0.5, WIN_H * 0.3)), (WIN_W * 0.25, WIN_H * 0.02))
            self.start_button.render()
            self.start_button_marathon.render()
            self.score_board_button.render()
        elif self.app.tetris.game_state == 'game':
            self.app.screen.blit(self.load_image(2, (WIN_W * 0.32, WIN_H * 0.35)), (WIN_W * 0.64, WIN_H * 0.25))
            self.app.screen.blit(self.load_image(1, (WIN_W * 0.32, WIN_H * 0.13)), (WIN_W * 0.64, WIN_H * 0.05))
            if self.app.tetris.game_mode == 'basic':
                self.app.screen.blit(self.load_image(1, (WIN_W * 0.28, WIN_H * 0.15)), (WIN_W * 0.66, WIN_H * 0.75))
            else:
                self.app.screen.blit(self.load_image(1, (WIN_W * 0.28, WIN_H * 0.15)), (WIN_W * 0.66, WIN_H * 0.62))
                self.app.screen.blit(self.load_image(1, (WIN_W * 0.28, WIN_H * 0.15)), (WIN_W * 0.66, WIN_H * 0.80))
        elif self.app.tetris.game_state == 'scoreboard':
            self.app.screen.blit(self.load_image(2, (WIN_W * 0.45, WIN_H * 0.82)), (WIN_W * 0.01, WIN_H * 0.19))
            self.app.screen.blit(self.load_image(2, (WIN_W * 0.48, WIN_H * 0.82)), (WIN_W * 0.515, WIN_H * 0.19))
            self.app.print_top_scores()


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        if self.app.tetris.game_state == 'game':
            self.font.render_to(self.app.screen, (WIN_W * 0.685, WIN_H * 0.1),
                                text='TETRIS', fgcolor='white',
                                size=TILE_SIZE * 1.65)
            self.font.render_to(self.app.screen, (WIN_W * 0.730, WIN_H * 0.28),
                                text='next', fgcolor='white',
                                size=TILE_SIZE * 1.4)
            if self.app.tetris.game_mode == 'basic':
                self.font.render_to(self.app.screen, (WIN_W * 0.705, WIN_H * 0.78),
                                    text='score', fgcolor='white',
                                    size=TILE_SIZE * 1.4)
                self.font.render_to(self.app.screen, (WIN_W * 0.688, WIN_H * 0.825),
                                    text=f'{self.app.tetris.score}', fgcolor='white',
                                    size=TILE_SIZE * 1.8)
            else:
                self.font.render_to(self.app.screen, (WIN_W * 0.705, WIN_H * 0.65),
                                    text='score', fgcolor='white',
                                    size=TILE_SIZE * 1.4)
                self.font.render_to(self.app.screen, (WIN_W * 0.688, WIN_H * 0.695),
                                    text=f'{self.app.tetris.score}', fgcolor='white',
                                    size=TILE_SIZE * 1.8)
                self.font.render_to(self.app.screen, (WIN_W * 0.735, WIN_H * 0.83),
                                    text='time', fgcolor='white',
                                    size=TILE_SIZE * 1.4)
                self.font.render_to(self.app.screen, (WIN_W * 0.710, WIN_H * 0.875),
                                    text=f'{self.app.convert(self.app.tetris.time)}', fgcolor='white',
                                    size=TILE_SIZE * 1.8)
        if self.app.tetris.game_state == 'scoreboard':
            self.font.render_to(self.app.screen, (WIN_W * 0.274, WIN_H * 0.08),
                                text='ScoreBoard', fgcolor='white',
                                size=TILE_SIZE * 2)

            self.font.render_to(self.app.screen, (WIN_W * 0.09, WIN_H * 0.28),
                                text='Classic', fgcolor='white',
                                size=TILE_SIZE * 2)
            self.font.render_to(self.app.screen, (WIN_W * 0.56, WIN_H * 0.28),
                                text='Marathon', fgcolor='white',
                                size=TILE_SIZE * 2)


class Tetris:
    def __init__(self, app):
        self.app = app
        self.game_state = 'main_menu'
        self.game_mode = None
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.speed_up = False
        self.cheat = False

        self.delta = 0
        self.time = 120
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}

        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)

    def quit_game(self):
        self.app.check_new_score(settings.PLAYER_NAME,self.score)
        self.app.play_sound("ko")
        self.app.images = self.app.load_images()
        self.__init__(self.app)

    def change_game_state(self, state, gamemode):
        self.game_state = state
        self.game_mode = gamemode

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        if self.full_lines == 1:
            self.app.play_sound("single")
        elif self.full_lines == 2:
            self.app.play_sound("double")
        elif self.full_lines == 3:
            self.app.play_sound("triple")
        elif self.full_lines == 4:
            self.app.play_sound("tetris")
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.quit_game()
            else:
                self.app.play_sound("landing")
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP and self.tetromino.shape != "O":
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
        elif pressed_key == pg.K_SPACE:
            self.tetromino.instant_drop()
            self.app.last_key = None
        elif pressed_key == pg.K_i:
            self.cheat = True

    def draw_grid(self):
        for x in [block.pos.x for block in self.tetromino.blocks]:
            for y in range(FIELD_H):
                for z in [block.pos.y for block in self.tetromino.blocks]:
                    if z < y:
                        pg.draw.rect(self.app.screen, 'grey', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if self.game_mode == 'marathon':
            self.delta += 1
            if self.delta >= 60:
                self.delta = 0
                self.time -= 1
            if self.time <= 0:
                self.quit_game()

        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        if HELP_LINE:
            self.draw_grid()
        self.sprite_group.draw(self.app.screen)