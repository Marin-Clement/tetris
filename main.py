from settings import *
from tetris import Tetris, Text, Menu
import sys
import pathlib
import random


class App:
    def __init__(self):
        pg.init()
        self.play_music()
        pg.display.set_caption("Tetris")
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.menu = Menu(self)
        self.hold = False
        self.last_key = None
        self.timer = 0

    def play_sound(self, sound):
        sound_loaded = pg.mixer.Sound(SOUND_PATH + sound + ".wav")
        sound_loaded.play()

    def play_music(self):
        pg.mixer.music.load(MUSIC_PATH + "MainTheme.mp3")
        pg.mixer.music.set_volume(0.15)
        pg.mixer.music.play(-1)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH + str(random.randrange(1, 10))).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        if self.tetris.game_state == 'game':
            self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        if self.tetris.game_state == 'main_menu':
            self.screen.fill(color=BG_COLOR)
        elif self.tetris.game_state == 'game':
            self.screen.fill(color=BG_COLOR)
            self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.menu.draw()
        self.text.draw()
        if self.tetris.game_state == 'game':
            self.tetris.draw()

        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if self.tetris.game_state == 'main_menu':
                self.menu.start_button.get_event(event)
                self.menu.start_button_marathon.get_event(event)
                self.menu.option_button.get_event(event)
                self.menu.score_board_button.get_event(event)
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) and self.tetris.game_state == 'game':
                self.tetris.change_game_state('main_menu')
                self.images = self.load_images()
                self.tetris.__init__(self)
            elif event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) and self.tetris.game_state == 'main_menu':
                quit()
            if self.tetris.game_state == 'game':
                if event.type == pg.KEYDOWN or self.hold and self.timer >= HOLD_INTERVAL:
                    if not self.last_key:
                        self.last_key = event.key
                    if self.last_key not in [pg.K_UP, pg.K_DOWN, pg.K_SPACE]:
                        self.hold = True
                    self.tetris.control(pressed_key=self.last_key)
                    self.timer = 0
                if event.type == pg.KEYUP:
                    self.hold = False
                    self.last_key = None
                    self.tetris.speed_up = False
                elif event.type == self.user_event:
                    self.anim_trigger = True
                elif event.type == self.fast_user_event:
                    self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            if self.timer < HOLD_INTERVAL:
                self.timer += 0.15

    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    app = App()
    app.run()