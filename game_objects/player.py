from game_objects.tank import *
from constants import SCORE_NEED_FOR_UPDATE


class Player:
    def __init__(self, uid: int):
        self.score = 0
        self.uid = uid
        self.tank = Tank()
        self.upgrage_count = 0

        #
        if uid == 0:
            self.tank.center_x = 100
            self.tank.center_y = 100
        else:
            self.tank.center_x = 1000
            self.tank.center_y = 100
        #

        self.bullets = []

    def move(self, to_point, game_tick):
        self.tank.move(to_point)

    def turn(self, angle, game_tick):
        self.tank.turn(angle)

    def shoot(self, game_tick):
        bullet = self.tank.shoot(game_tick)
        if bullet is not None:
            self.bullets.append(bullet)

    def upgrage(self, type: UpgradeType, game_tick):
        if self.upgrage_count >= self.score // SCORE_NEED_FOR_UPDATE:
            return
        self.upgrage_count += 1
        self.tank.upgrade(type)
