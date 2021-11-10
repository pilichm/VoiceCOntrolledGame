from Constants import SPRITE_ENEMY_1_LIFE, SPRITE_ENEMY_2_LIFES


class Enemy:
    def __init__(self, x=13, y=4):
        self.life_count = 2
        self.pos_x = x
        self.pos_y = y
        self.is_attacked = False

    def get_sprite(self):
        if self.life_count == 2:
            return SPRITE_ENEMY_2_LIFES
        elif self.life_count == 1:
            return SPRITE_ENEMY_1_LIFE
