import os

COL_COUNT = 20
ROW_COUNT = 10
SPRITE_SIZE = 48
REFRESH_RATE = 1

RESOURCES_DIR = '/content/VoiceCOntrolledGame/pilichm/data/'
# RESOURCES_DIR = f'{os.path.dirname(os.path.abspath(__file__))}/pilichm/data/'

# Player spites.
SPRITE_PLAYER_UNARMED_RIGHT_FILE = f'{RESOURCES_DIR}player/hero_right.png'
SPRITE_PLAYER_UNARMED_LEFT_FILE = f'{RESOURCES_DIR}player/hero_left.png'
SPRITE_PLAYER_UNARMED_UP_FILE = f'{RESOURCES_DIR}player/hero_up.png'
SPRITE_PLAYER_UNARMED_DONW_FILE = f'{RESOURCES_DIR}player/hero_dawn.png'

SPRITE_PLAYER_ARMED_RIGHT_FILE = f'{RESOURCES_DIR}player/hero_armed_right.png'
SPRITE_PLAYER_ARMED_LEFT_FILE = f'{RESOURCES_DIR}player/hero_armed_left.png'
SPRITE_PLAYER_ARMED_UP_FILE = f'{RESOURCES_DIR}player/hero_armed_up.png'
SPRITE_PLAYER_ARMED_DOWN_FILE = f'{RESOURCES_DIR}player/hero_armed_down.png'

# Terrain sprites.
SPRITE_GRASS_FILE = f'{RESOURCES_DIR}terrain/grass_1.png'
SPRITE_WATER_FILE = f'{RESOURCES_DIR}terrain/water_1.png'
SPRITE_BRIDGE_FILE = f'{RESOURCES_DIR}terrain/bridge_1.png'
SPRITE_SCREEN_BORDER_FILE = f'{RESOURCES_DIR}terrain/screen_border_1.png'
SPRITE_STUMP_FILE = f'{RESOURCES_DIR}terrain/stump_1.png'
SPRITE_TREE_FILE = f'{RESOURCES_DIR}terrain/tree_1.png'
SPRITE_BUSH_FILE = f'{RESOURCES_DIR}terrain/bush_1.png'

# Main game screens.
MAIN_BACKGROUND_FILE = f'{RESOURCES_DIR}/screens/main_screen.png'
SCREEN_VICTORY_FILE = f'{RESOURCES_DIR}/screens/game_win_screen.jpg'
SCREEN_FAILURE_FILE = f'{RESOURCES_DIR}/screens/game_lose_screen.jpg'

# Mana bottle and count.
SPRITE_MANA_BOTTLE = f'{RESOURCES_DIR}mana/mana_bottle.png'
SPRITE_MANA_COUNT = f'{RESOURCES_DIR}mana/mana_count_'

# Other game objects.
SPRITE_HEART_EQUIPPED_FILE = f'{RESOURCES_DIR}other/heart_1.png'
SPRITE_HEART_BONUS_FILE = f'{RESOURCES_DIR}other/heart_bonus_1.png'
SPRITE_SWORD_EQUIPPED_FILE = f'{RESOURCES_DIR}other/sword_equipped.png'
SPRITE_SWORD_BONUS_FILE = f'{RESOURCES_DIR}other/sword_bonus.png'
SPRITE_ENEMY_1_LIFE = f'{RESOURCES_DIR}other/enemy_1.png'
SPRITE_ENEMY_2_LIVES = f'{RESOURCES_DIR}other/enemy_2.png'
SPRITE_FLAG_FILE = f'{RESOURCES_DIR}other/terrain/flag_1.png'
SPRITE_BOOK_FILE = f'{RESOURCES_DIR}other/book_1.png'
SPRITE_FIRE_RED_GIF = f"{RESOURCES_DIR}other/fire_red_gif.gif"
SPRITE_FIRE_BLUE_GIF = f"{RESOURCES_DIR}other/fire_blue_gif.gif"

# Sound files.
SOUND_PLAYER_ATTACK = f'{RESOURCES_DIR}sounds/player_attack.mp3'
SOUND_ENEMY_ATTACK = f'{RESOURCES_DIR}sounds/enemy_attack.mp3'
SOUND_POWER_UP_PICKED_ATTACK = f'{RESOURCES_DIR}sounds/power_up_picked_up.mp3'
SOUND_GAME_VICTORY = f'{RESOURCES_DIR}sounds/game_victory.mp3'
SOUND_GAME_LOSE = f'{RESOURCES_DIR}sounds/game_lose.mp3'

ALLOWED_TERRAIN = [SPRITE_GRASS_FILE, SPRITE_BRIDGE_FILE, SPRITE_HEART_BONUS_FILE, SPRITE_SWORD_BONUS_FILE,
                   SPRITE_BOOK_FILE]

INIT_STATE_FILE = f'{RESOURCES_DIR}game_init_state.csv'

FILE_RECORDINGS_TRANSCRIPTION = f'{RESOURCES_DIR}recordings/text.txt'
PATH_TO_GRAMMAR = '/content/grammar/'
RECORDING_FILENAME = 'Nagranie.wav'
PATH_TO_MODEL_CONF_FILE = '/content/online/conf/mfcc.conf'

screen_dict = {0: SPRITE_GRASS_FILE, 1: SPRITE_WATER_FILE, 3: SPRITE_BRIDGE_FILE, 4: SPRITE_STUMP_FILE,
               5: SPRITE_TREE_FILE, 6: SPRITE_BUSH_FILE, 7: SPRITE_SCREEN_BORDER_FILE, 8: SPRITE_HEART_BONUS_FILE,
               9: SPRITE_SWORD_BONUS_FILE, 10: SPRITE_ENEMY_2_LIVES, 11: SPRITE_FLAG_FILE, 12: SPRITE_BOOK_FILE}
