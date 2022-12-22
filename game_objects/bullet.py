from constants import FPS, BULLET_DEFAULT_RADIUS, BULLET_DEFAULT_SPEED, BULLET_DEFAULT_DAMAGE, BULLET_LIFETIME_TICKS
from internal_math import *


class Bullet(CircleBody):
    def __init__(self, current_game_tick):
        super().__init__()
        self.angle = None
        self.radius = BULLET_DEFAULT_RADIUS
        self.speed = BULLET_DEFAULT_SPEED
        self.damage = BULLET_DEFAULT_DAMAGE
        self.lifetime = current_game_tick + BULLET_LIFETIME_TICKS

    def move(self):
        distance = 1 / FPS * self.speed
        vec = (math.cos(self.angle) * distance, math.sin(self.angle) * distance)
        self.center_x += vec[0]
        self.center_y += vec[1]
