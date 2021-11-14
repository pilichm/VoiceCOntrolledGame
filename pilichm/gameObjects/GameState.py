import random
import subprocess
import time

import IPython.display
import PIL.Image
from IPython.display import clear_output, display

from pilichm.gameObjects.Constants import *
from pilichm.gameObjects.Enemy import Enemy
from pilichm.gameObjects.Player import Player
from pilichm.gameObjects.Utils import load_fire_gif

from lexicon import words_to_lexicon

class GameState:
    def __init__(self, player=Player(), enemy=Enemy()):
        self.screen = self.load_screen_from_state()
        self.player = player
        self.enemy = enemy

    def move_player_up(self):
        self.player.move_up(self.screen)

    def move_player_down(self):
        self.player.move_down(self.screen)

    def move_player_right(self):
        self.player.move_right(self.screen)

    def move_player_left(self):
        self.player.move_left(self.screen)

    def run_command(self, command):
        process = subprocess.Popen(command)
        try:
            outs, errs = process.communicate()
            print(f'Command result: {outs}')
            print(f'Command errors: {errs}')
        except Exception as e:
            process.kill()
            outs, errs = process.communicate()
            print(f'Command result: {outs}')
            print(f'Command errors: {errs}')

    # Load initial game screen based on game_init_state.csv file.
    def load_screen_from_state(self):
        screen = []

        with open(INIT_STATE_FILE, 'r') as f:
            lines = f.readlines()
            for line in lines:
                screen_line = []
                fields = line.split(',')
                for state in fields:
                    screen_line.append(screen_dict[int(state)])
                screen.append(screen_line)

        return screen

    def prepare_voice_model(self):
        # Download and prepare kaldi.
        # os.chdir("/content/")
        subprocess.run("wget https://github.com/danijel3/ASRforNLP/releases/download/v1.0/kaldi.tar.xz", shell=True)
        subprocess.run("tar xvf kaldi.tar.xz -C / > /dev/null", shell=True)
        subprocess.run("rm kaldi.tar.xz", shell=True)
        subprocess.run("for f in $(find /opt/kaldi -name *.so*) ; do ln -sf $f /usr/local/lib/$(basename $f) ; done",
                       shell=True)
        subprocess.run(
            "for f in $(find /opt/kaldi/src -not -name *.so* -type f -executable) ; do ln -s $f /usr/local/bin/$(basename $f) ; done",
            shell=True)
        subprocess.run(
            "for f in $(find /opt/kaldi/tools -not -name *.so* -type f -executable) ; do ln -s $f /usr/local/bin/$(basename $f) ; done",
            shell=True)

        subprocess.run("ldconfig", shell=True)

        # Download phonetic and acoustic model.
        subprocess.run("wget https://github.com/danijel3/ASRforNLP/releases/download/v1.2/models.tar.xz", shell=True)
        subprocess.run("tar xvf models.tar.xz > /dev/null", shell=True)
        subprocess.run("rm models.tar.xz", shell=True)

        # Prepare grammar dirs.
        subprocess.run("mkdir grammar", shell=True)
        os.chdir("grammar/")
        subprocess.run("ln -s ../phonetisaurus", shell=True)
        subprocess.run("ln -s ../online", shell=True)
        subprocess.run("ln -s ../nagrania", shell=True)

        # Download transcription.
        subprocess.run("wget https://raw.githubusercontent.com/danijel3/ASRforNLP/main/lexicon.py", shell=True)
        wordlist = ['dół', 'górę', 'Lewo', 'Prawo', 'W']
        psyms, wsyms, L = words_to_lexicon(wordlist)

    # Player attack always hits.
    def player_attack(self):

        if not self.player.is_armed or self.player.mana_count <= 0:
            return

        condition_one = self.player.pos_x + 1 == self.enemy.pos_x
        condition_two = self.player.pos_x - 1 == self.enemy.pos_x
        condition_three = self.player.pos_y + 1 == self.enemy.pos_y
        condition_four = self.player.pos_y - 1 == self.enemy.pos_y

        self.player.mana_count -= 2

        if condition_one or condition_two or condition_three or condition_four:
            self.enemy.life_count -= 1
            self.enemy.is_attacked = True

            if self.enemy.life_count == 0:
                self.screen[self.enemy.pos_x][self.enemy.pos_y] = SPRITE_GRASS_FILE

    # Enemy attack may miss.
    def enemy_attack(self):
        condition_one = self.enemy.pos_x + 1 == self.player.pos_x
        condition_two = self.enemy.pos_x - 1 == self.player.pos_x
        condition_three = self.enemy.pos_y + 1 == self.player.pos_y
        condition_four = self.enemy.pos_y - 1 == self.player.pos_y

        if condition_one or condition_two or condition_three or condition_four:
            if random.randint(3, 9) % 2 == 0:
                self.player.life_count -= 1
                self.player.is_attacked = True

    def get_animation_sprites(self, frames, new_image):
        if self.enemy.is_attacked and self.player.is_attacked:
            fire_blue = load_fire_gif('blue')
            fire_red = load_fire_gif('red')
            for index in range(min(len(fire_red), len(fire_blue))):
                temp_image = new_image.copy()
                temp_image.paste(fire_red[index], (self.enemy.pos_x * SPRITE_SIZE, self.enemy.pos_y * SPRITE_SIZE))
                temp_image.paste(fire_blue[index], (self.player.pos_x * SPRITE_SIZE, self.player.pos_y * SPRITE_SIZE))
                frames.append(temp_image)
        elif self.player.is_attacked:
            fire_blue = load_fire_gif('blue')
            for index in range(len(fire_blue)):
                temp_image = new_image.copy()
                temp_image.paste(fire_blue[index], (self.player.pos_x * SPRITE_SIZE, self.player.pos_y * SPRITE_SIZE))
                frames.append(temp_image)
        elif self.enemy.is_attacked:
            fire_red = load_fire_gif('red')
            for index in range(len(fire_red)):
                temp_image = new_image.copy()
                temp_image.paste(fire_red[index], (self.enemy.pos_x * SPRITE_SIZE, self.enemy.pos_y * SPRITE_SIZE))
                frames.append(temp_image)
        return frames

    def display_screen(self):
        # Create empty image
        new_image = PIL.Image.new('RGBA', (COL_COUNT * SPRITE_SIZE, ROW_COUNT * SPRITE_SIZE), (250, 250, 250))
        background = PIL.Image.open(MAIN_BACKGROUND_FILE)
        new_image.paste(background, (0, 0))

        for col_index in range(COL_COUNT):
            for row_index in range(ROW_COUNT):

                # Add heart and sword bonuses.
                if self.screen[col_index][row_index] == SPRITE_HEART_BONUS_FILE:
                    image = PIL.Image.open(SPRITE_HEART_BONUS_FILE)
                    new_image.paste(image, (col_index * SPRITE_SIZE, row_index * SPRITE_SIZE))
                elif self.screen[col_index][row_index] == SPRITE_SWORD_BONUS_FILE:
                    image = PIL.Image.open(SPRITE_SWORD_BONUS_FILE)
                    new_image.paste(image, (col_index * SPRITE_SIZE, row_index * SPRITE_SIZE))

        # Display player and player life count.
        if self.player and self.player.life_count > 0:
            image_heart = PIL.Image.open(SPRITE_HEART_EQUIPPED_FILE)
            image_hero = PIL.Image.open(self.player.get_sprite())
            new_image.paste(image_hero, (self.player.pos_x * SPRITE_SIZE, self.player.pos_y * SPRITE_SIZE))

            for index in range(self.player.life_count):
                new_image.paste(image_heart, (index * SPRITE_SIZE, 0))

        # Display mana count after life.
        mana_bottle_image = PIL.Image.open(SPRITE_MANA_BOTTLE)
        mana_count_image = PIL.Image.open(f"{SPRITE_MANA_COUNT}{self.player.mana_count}.png")
        new_image.paste(mana_count_image, ((self.player.life_count + 1) * SPRITE_SIZE, 0))
        new_image.paste(mana_bottle_image, ((self.player.life_count + 2) * SPRITE_SIZE, 0))

        # Display sword near life count if player is armed.
        if self.player and self.player.is_armed:
            image = PIL.Image.open(SPRITE_SWORD_EQUIPPED_FILE)
            new_image.paste(image, ((self.player.life_count + 4) * SPRITE_SIZE, 0))

        # Display enemy if it has any lives left.
        if self.enemy and self.enemy.life_count > 0:
            image = PIL.Image.open(self.enemy.get_sprite())
            new_image.paste(image, (self.enemy.pos_x * SPRITE_SIZE, self.enemy.pos_y * SPRITE_SIZE))

        # Add attack elements if attack happened.
        frames = [new_image]
        frames = self.get_animation_sprites(frames, new_image)

        new_image.save(f"{RESOURCES_DIR}screens/result.gif", save_all=True, append_images=frames, duration=100, loop=0)
        clear_output()
        display(IPython.display.Image(open(f"{RESOURCES_DIR}screens/result.gif", 'rb').read()))

        # Clear enemy and player state.
        self.player.is_attacked, self.enemy.is_attacked = False, False

    # Play mock game run without voice commands.
    def run(self):
        is_running = True
        gameState = GameState()
        gameState.display_screen()

        while is_running:

            for i in range(6):
                time.sleep(REFRESH_RATE)
                gameState.move_player_right()
                gameState.display_screen()

            for i in range(2):
                time.sleep(REFRESH_RATE)
                gameState.move_player_up()
                gameState.display_screen()

            time.sleep(REFRESH_RATE)
            gameState.move_player_down()
            gameState.display_screen()

            time.sleep(REFRESH_RATE)
            gameState.move_player_right()
            gameState.display_screen()

            while gameState.enemy.life_count > 0:
                time.sleep(REFRESH_RATE)
                gameState.enemy_attack()
                gameState.player_attack()
                gameState.display_screen()

            for i in range(5):
                time.sleep(REFRESH_RATE)
                gameState.move_player_right()
                gameState.display_screen()

            is_running = False
