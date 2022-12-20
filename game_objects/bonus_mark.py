from internal_math import *
from constants import BONUS_MARK_DEFAULT_HEALTH, BONUS_MARK_DEFAULT_WEIGHT, \
     BONUS_MARK_DEFAULT_SPEED, BONUS_MARK_DEFAULT_GIVES_SCORE, BONUS_MARK_DEFAULT_RADIUS


class BonusMark(CircleBody):
    def __init__(self):
        super().__init__()
        self.radius = BONUS_MARK_DEFAULT_RADIUS
        self.gives_score = BONUS_MARK_DEFAULT_GIVES_SCORE
        self.health = BONUS_MARK_DEFAULT_HEALTH
        self.speed = BONUS_MARK_DEFAULT_SPEED
        self.weight = BONUS_MARK_DEFAULT_WEIGHT
