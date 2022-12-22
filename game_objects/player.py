from game_objects.tank import *
from constants import SCORE_NEED_FOR_UPDATE, PLAYER1_SPAWN_X, PLAYER1_SPAWN_Y, PLAYER3_SPAWN_X, PLAYER4_SPAWN_X, \
    PLAYER3_SPAWN_Y, PLAYER4_SPAWN_Y, PLAYER2_SPAWN_Y, PLAYER2_SPAWN_X


class Player:
    def __init__(self, uid: int):
        self.score = 0
        self.uid = uid
        self.tank = Tank()
        self.upgrage_count = 0

        self.color = None
        self.memory_string = ''
        self.program_path = None
        self.bullet_power = 0
        self.cur_speed = (0, 0)

        if uid == 0:
            self.tank.center_x = PLAYER1_SPAWN_X
            self.tank.center_y = PLAYER1_SPAWN_Y
        elif uid == 1:
            self.tank.center_x = PLAYER2_SPAWN_X
            self.tank.center_y = PLAYER2_SPAWN_Y
        elif uid == 2:
            self.tank.center_x = PLAYER3_SPAWN_X
            self.tank.center_y = PLAYER3_SPAWN_Y
        elif uid == 3:
            self.tank.center_x = PLAYER4_SPAWN_X
            self.tank.center_y = PLAYER4_SPAWN_Y

        self.bullets = []

    def move(self, to_point, game_tick):
        self.cur_speed = self.tank.move(to_point)

    def turn(self, angle, game_tick):
        self.tank.turn(angle)

    def shoot(self, game_tick):
        bullet = self.tank.shoot(game_tick)
        if bullet is not None:
            bullet.radius += self.bullet_power
            bullet.damage *= (self.bullet_power + 1)
            self.bullet_power = 0
            distance = 1 / FPS * bullet.speed
            vec = (math.cos(bullet.angle) * distance, math.sin(bullet.angle) * distance)
            m1 = self.tank.radius ** 2
            m2 = bullet.radius ** 2
            u = (-vec[0] * 10 * m2 / m1, -vec[1] * 10 * m2 / m1)
            self.add_velocity(u)
            self.bullets.append(bullet)

    def increase_power(self, game_tick):
        if self.tank.can_shoot(game_tick):
            self.bullet_power = min(self.bullet_power + 1, 10)
            self.tank.last_time_shoot = game_tick

    def add_velocity(self, u):
        self.tank.last_speed[0] = u[0]
        self.tank.last_speed[1] = u[1]

    def upgrade(self, type: UpgradeType, game_tick):
        if self.upgrage_count >= self.score // SCORE_NEED_FOR_UPDATE:
            return False
        self.upgrage_count += 1
        self.tank.upgrade(type)
        return True
