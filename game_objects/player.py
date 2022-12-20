from game_objects.tank import *


class Player:
    def __init__(self):
        self.score = 0
        self.tank = Tank()

        #
        self.tank.center_x = 100
        self.tank.center_y = 100
        #

        self.bullets = []

    def move(self, to_point, game_tick):
        self.tank.move(to_point)

    def turn(self, angle, game_tick):
        self.tank.turn(angle)

    def shoot(self, game_tick):
        self.bullets.append(self.tank.shoot())
