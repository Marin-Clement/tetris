from settings import *
from tetris import Tetris, Text, Menu
import sys
import pathlib
import random
import json


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

    def print_top_scores(self):
        y_offset = 0
        try:
            with open("Data/scores.json", "r") as f:
                data = json.load(f)
        except:
            data = {"basic": {}, "marathon": {}}
        sorted_scores = sorted(data["basic"].items(), key=lambda x: x[1], reverse=True)
        for i in range(min(5, len(sorted_scores))):
            self.screen.blit(
                pg.font.Font(FONT_PATH, int(TILE_SIZE * 0.8)).render(f"{i + 1}. {sorted_scores[i][0]}: {sorted_scores[i][1]}", True,
                                                   (255, 255, 255)), (WIN_W * 0.07, (WIN_H * 0.37) + y_offset))
            y_offset += 100
        sorted_scores = sorted(data["marathon"].items(), key=lambda x: x[1], reverse=True)
        y_offset = 0
        for i in range(min(5, len(sorted_scores))):
            self.screen.blit(
                pg.font.Font(FONT_PATH, int(TILE_SIZE * 0.8)).render(f"{i + 1}. {sorted_scores[i][0]}: {sorted_scores[i][1]}", True,
                                                   (255, 255, 255)), (WIN_W * 0.57, (WIN_H * 0.37) + y_offset))
            y_offset += 100

    def save_score(self, player_name, score):
        try:
            with open("Data/scores.json", "r") as f:
                data = json.load(f)
        except:
            data = {"basic": {}, "marathon": {}}
        data[self.tetris.game_mode][player_name] = score
        with open("Data/scores.json", "w") as f:
            json.dump(data, f)

    def check_new_score(self, player_name, new_score):
        try:
            with open("Data/scores.json", "r") as f:
                data = json.load(f)
        except:
            data = {"basic": {}, "marathon": {}}
        if player_name in data:
            previous_score = data[player_name]
            if new_score > previous_score:
                self.save_score(player_name, new_score)
        else:
            self.save_score(player_name, new_score)

    def play_sound(self, sound):
        sound_loaded = pg.mixer.Sound(SOUND_PATH + sound + ".wav")
        sound_loaded.set_volume(VOLUME)
        sound_loaded.play()

    def play_music(self):
        pg.mixer.music.load(MUSIC_PATH + "MainTheme.mp3")
        pg.mixer.music.set_volume(VOLUME)
        pg.mixer.music.play(-1)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH + str(random.randrange(1, 10))).rglob('*.png') if
                 item.is_file()]
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
        elif self.tetris.game_state == 'scoreboard':
            self.screen.fill(color=BG_COLOR)
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
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) and self.tetris.game_state in ['game', 'scoreboard']:
                self.images = self.load_images()
                self.tetris.__init__(self)
                self.tetris.change_game_state('main_menu', None)

            elif event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) and self.tetris.game_state == 'main_menu':
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

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%02d:%02d" % (minutes, seconds)

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
