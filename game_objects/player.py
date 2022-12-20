from game_objects.tank import *


class Player:
    def __init__(self, uid: int):
        self.score = 0
        self.uid = uid
        self.tank = Tank()

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
