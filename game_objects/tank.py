from constants import WORLD_WIDTH, WORLD_HEIGHT, FPS, ANGLE_SPEED, \
    TANK_DEFAULT_SPEED, TANK_DEFAULT_RADIUS, TANK_DEFAULT_WEIGHT, TANK_DEFAULT_ANGLE, \
    TANK_DEFAULT_HEALTH, TANK_DEFAULT_HEALTH_REGENERATION, TANK_DEFAULT_COOLDOWN, \
    TANK_DEFAULT_DAMAGE_ADD, TANK_DEFAULT_BULLET_SPEED_ADD, UPGRADE_SPEED, UPGRADE_DAMAGE, \
    UPGRADE_BULLET_SPEED, UPGRADE_MAX_HEALTH
from game_objects.bullet import Bullet
from game_objects.upgrade import UpgradeType
from internal_math import *


class Tank(CircleBody):
    def __init__(self):
        super().__init__()
        self.radius = TANK_DEFAULT_RADIUS
        self.angle = TANK_DEFAULT_ANGLE
        self.speed = TANK_DEFAULT_SPEED
        self.health = TANK_DEFAULT_HEALTH
        self.max_health = TANK_DEFAULT_HEALTH
        self.health_regeneration = TANK_DEFAULT_HEALTH_REGENERATION
        self.cooldown = TANK_DEFAULT_COOLDOWN
        self.weight = TANK_DEFAULT_WEIGHT
        self.damage_add = TANK_DEFAULT_DAMAGE_ADD
        self.bullet_speed_add = TANK_DEFAULT_BULLET_SPEED_ADD
        self.last_time_shoot = None
        self.last_speed = [0, 0]

    def _correct_last_speed(self):
        vec = self.last_speed
        if abs(vec[0]) + abs(vec[1]) > 1e-6:
            vector_angle = math.atan2(vec[1], vec[0])
            last_module = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
            real_speed = 1 / FPS * self.speed
            if last_module > real_speed:
                vec_neutral = (math.cos(vector_angle) * real_speed, math.sin(vector_angle) * real_speed)
                self.last_speed[0] -= vec_neutral[0]
                self.last_speed[1] -= vec_neutral[1]
            else:
                self.last_speed = [0, 0]

    def move(self, to_point):
        distance_can = 1 / FPS * self.speed
        self._correct_last_speed()
        vec = self.last_speed
        if abs(vec[0]) + abs(vec[1]) < 1e-6:
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

        return vec[0], vec[1]

    def can_shoot(self, current_game_tick):
        if self.last_time_shoot is not None and (current_game_tick - self.last_time_shoot) < self.cooldown * FPS:
            return False
        return True

    def shoot(self, current_game_tick):
        if self.last_time_shoot is not None and (current_game_tick - self.last_time_shoot) < self.cooldown * FPS:
            return None

        bullet = Bullet(current_game_tick)
        bullet.center_x = self.center_x + math.cos(self.angle) * self.radius
        bullet.center_y = self.center_y + math.sin(self.angle) * self.radius
        bullet.angle = self.angle
        bullet.damage += self.damage_add
        bullet.speed += self.bullet_speed_add
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

    def regenerate(self):
        self.health += 1 / FPS * self.health_regeneration
        if self.health > self.max_health:
            self.health = self.max_health

    def upgrade(self, type: UpgradeType):
        if type == UpgradeType.SPEED:
            self.speed += UPGRADE_SPEED
        elif type == UpgradeType.DAMAGE:
            self.damage_add += UPGRADE_DAMAGE
        elif type == UpgradeType.BULLET_SPEED:
            self.bullet_speed_add += UPGRADE_BULLET_SPEED
        elif type == UpgradeType.MAX_HEALTH:
            self.max_health += UPGRADE_MAX_HEALTH
