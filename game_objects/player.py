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
        self.tank.move(to_point)

    def turn(self, angle, game_tick):
        self.tank.turn(angle)

    def shoot(self, game_tick):
        bullet = self.tank.shoot(game_tick)
        if bullet is not None:
            self.bullets.append(bullet)

    def upgrade(self, type: UpgradeType, game_tick):
        if self.upgrage_count >= self.score // SCORE_NEED_FOR_UPDATE:
            return False
        self.upgrage_count += 1
        self.tank.upgrade(type)
        return True
