from internal_math import *
from game_objects.bullet import Bullet
from constants import WORLD_WIDTH, WORLD_HEIGHT, FPS, ANGLE_SPEED,\
    TANK_DEFAULT_SPEED, TANK_DEFAULT_RADIUS, TANK_DEFAULT_WEIGHT, TANK_DEFAULT_ANGLE, \
    TANK_DEFAULT_HEALTH, TANK_DEFAULT_HEALTH_REGENERATION, TANK_DEFAULT_COOLDOWN


class Tank(CircleBody):
    def __init__(self):
        super().__init__()
        self.radius = TANK_DEFAULT_RADIUS
        self.angle = TANK_DEFAULT_ANGLE
        self.speed = TANK_DEFAULT_SPEED
        self.health = TANK_DEFAULT_HEALTH
        self.health_regeneration = TANK_DEFAULT_HEALTH_REGENERATION
        self.cooldown = TANK_DEFAULT_COOLDOWN
        self.weight = TANK_DEFAULT_WEIGHT

    def move(self, distance):
        distance_can = 1 / FPS * self.speed
        distance = min(distance, distance_can)
        vec = (math.cos(self.angle) * distance, math.sin(self.angle) * distance)
        self.center_x += vec[0]
        self.center_y += vec[1]

        if self.center_x < 0:
            self.center_x = 0
        if self.center_x >= WORLD_WIDTH:
            self.center_x = WORLD_WIDTH - 1
        if self.center_y < 0:
            self.center_y = 0
        if self.center_y >= WORLD_HEIGHT:
            self.center_y = WORLD_HEIGHT - 1

    def shoot(self):
        bullet = Bullet()
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        bullet.radius = 5
        bullet.angle = self.angle
        bullet.damage = 50
        bullet.speed = 200

        return bullet

    def turn(self, angle):
        sign = (-1 if angle < 0 else 1)
        angle = math.fabs(angle)
        angle_can = 1 / FPS * ANGLE_SPEED
        angle = min(angle, angle_can)
        angle *= sign
        self.angle += angle

        while self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        while self.angle < 0:
            self.angle += 2 * math.pi
