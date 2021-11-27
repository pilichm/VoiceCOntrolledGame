from pilichm.gameObjects.Constants import *
from pilichm.gameObjects.Action import *


class Player:

    def __init__(self, x=5, y=5):
        self.life_count = 2
        self.mana_count = 6
        self.is_attacked = False
        self.pos_x = x
        self.pos_y = y
        self.is_armed = False
        self.last_direction = Action.MOVE_RIGHT

    def move_right(self, screen):
        if self.pos_x + 1 < 19 and screen[self.pos_x + 1][self.pos_y] in ALLOWED_TERRAIN:
            self.pos_x += 1
            self.refresh_heart_count(screen)
            self.last_direction = Action.MOVE_RIGHT

    def move_left(self, screen):
        if self.pos_x - 1 > 0 and screen[self.pos_x - 1][self.pos_y] in ALLOWED_TERRAIN:
            self.pos_x -= 1
            self.refresh_heart_count(screen)
            self.last_direction = Action.MOVE_LEFT

    def move_up(self, screen):
        if self.pos_y - 1 > 0 and screen[self.pos_x][self.pos_y - 1] in ALLOWED_TERRAIN:
            self.pos_y -= 1
            self.refresh_heart_count(screen)
            self.last_direction = Action.MOVE_UP

    def move_down(self, screen):
        if self.pos_y + 1 < 19 and screen[self.pos_x][self.pos_y + 1] in ALLOWED_TERRAIN:
            self.pos_y += 1
            self.refresh_heart_count(screen)
            self.last_direction = Action.MOVE_DOWN

    def pick_up_sword(self, screen):
        self.check_if_sword_was_picked(screen)

    def refresh_heart_count(self, screen):
        if screen[self.pos_x][self.pos_y] == SPRITE_HEART_BONUS_FILE:
            screen[self.pos_x][self.pos_y] = SPRITE_GRASS_FILE
            self.life_count += 1

    def check_if_sword_was_picked(self, screen):
        if screen[self.pos_x][self.pos_y] == SPRITE_SWORD_BONUS_FILE:
            screen[self.pos_x][self.pos_y] = SPRITE_GRASS_FILE
            self.is_armed = True

    def get_sprite(self):
        if self.is_armed:
            if self.last_direction == Action.MOVE_RIGHT:
                return SPRITE_PLAYER_ARMED_RIGHT_FILE
            elif self.last_direction == Action.MOVE_LEFT:
                return SPRITE_PLAYER_ARMED_LEFT_FILE
            elif self.last_direction == Action.MOVE_UP:
                return SPRITE_PLAYER_ARMED_UP_FILE
            elif self.last_direction == Action.MOVE_DOWN:
                return SPRITE_PLAYER_ARMED_DOWN_FILE
        else:
            if self.last_direction == Action.MOVE_RIGHT:
                return SPRITE_PLAYER_UNARMED_RIGHT_FILE
            elif self.last_direction == Action.MOVE_LEFT:
                return SPRITE_PLAYER_UNARMED_LEFT_FILE
            elif self.last_direction == Action.MOVE_UP:
                return SPRITE_PLAYER_UNARMED_UP_FILE
            elif self.last_direction == Action.MOVE_DOWN:
                return SPRITE_PLAYER_UNARMED_DONW_FILE
