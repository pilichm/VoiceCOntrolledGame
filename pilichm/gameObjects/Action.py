from enum import Enum


class Action(Enum):
    MOVE_UP = 'do góry'
    MOVE_DOWN = 'do dołu'
    MOVE_LEFT = 'w lewo'
    MOVE_RIGHT = 'w prawo'
    SPELL_FIRE_BALL = 'zaklęcie kula ognia'
    SPELL_HEALING = 'zaklęcie leczenie'
    PICK_UP_ITEM = 'podnieś przedmiot'
    ANSWER_CORRECT = 'witaj'
    UNKNOWN = 5
    EMPTY = 6
