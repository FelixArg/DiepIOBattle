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
        self.last_time_shoot = None

    def move(self, to_point):
        distance_can = 1 / FPS * self.speed
        vector = (to_point[0] - self.center_x, to_point[1] - self.center_y)
        distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        distance = min(distance, distance_can)
        vector_angle = math.atan2(vector[1], vector[0])
        vec = (math.cos(vector_angle) * distance, math.sin(vector_angle) * distance)
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

    def shoot(self, current_game_tick):
        if self.last_time_shoot is not None and (current_game_tick - self.last_time_shoot) < self.cooldown * FPS:
            return None

        bullet = Bullet()
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        bullet.angle = self.angle

        self.last_time_shoot = current_game_tick

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
