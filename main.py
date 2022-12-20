import math
import sys
import pygame
import os
import random

import internal_math
from game_objects.player import Player
from game_objects.bonus_mark import BonusMark
from constants import *

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#

# game globals
tick = 0
clock = pygame.time.Clock()

points = [[1000, 700], [1000, 700]]

players = []
bonus_marks = []
#


def main():
    global clock
    global tick

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DiepIO Battle')

    init_game()
    while True:
        process_game_tick(screen)
        clock.tick(FPS)
        tick += 1


def init_game():
    global bonus_marks

    players.append(Player(0))
    players.append(Player(1))

    random.seed(0)
    for i in range(20):
        bonus_mark = BonusMark()
        bonus_mark.center_x = random.random() * WORLD_WIDTH
        bonus_mark.center_y = random.random() * WORLD_HEIGHT
        bonus_marks.append(bonus_mark)


def process_game_tick(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    process_game_logic()
    process_collision()
    draw_all(screen)


def draw_all(screen):
    global players
    global bonus_marks

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, WORLD_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - WORLD_HEIGHT))

    for player in players:
        for bullet in player.bullets:
            pygame.draw.circle(screen, BLUE, (bullet.center_x, bullet.center_y), bullet.radius)

    for bonus_mark in bonus_marks:
        pygame.draw.circle(screen, GREEN, (bonus_mark.center_x, bonus_mark.center_y), bonus_mark.radius)

    for player in players:
        if player.tank is None:
            continue
        pygame.draw.circle(screen, (RED if player.uid == 0 else YELLOW),
                           (player.tank.center_x, player.tank.center_y), player.tank.radius)

    pygame.display.update()


def process_game_logic():
    global points
    global players
    global tick

    for player in players:
        if player.tank is None:
            continue
        if math.fabs(points[player.uid][0] - player.tank.center_x) < internal_math.EPS and \
                math.fabs(points[player.uid][1] - player.tank.center_y) < internal_math.EPS:
            points[player.uid] = [random.random() * WORLD_WIDTH, random.random() * WORLD_HEIGHT]

        if players[player.uid ^ 1].tank is not None and player.uid == 1:
            vec = (players[player.uid ^ 1].tank.center_x - player.tank.center_x,
                   players[player.uid ^ 1].tank.center_y - player.tank.center_y)
            angle_cur = math.atan2(vec[1], vec[0])
        else:
            if len(bonus_marks) > 0:
                vec = (bonus_marks[0].center_x - player.tank.center_x,
                       bonus_marks[0].center_y - player.tank.center_y)
            else:
                vec = (-player.tank.center_x, -player.tank.center_y)
            angle_cur = math.atan2(vec[1], vec[0])

        if angle_cur < 0:
            angle_cur += 2 * math.pi
        if math.fabs(angle_cur - player.tank.angle) > internal_math.EPS:
            angle = angle_cur - player.tank.angle
            player.turn(angle, tick)

        player.move(points[player.uid], tick)
        player.shoot(tick)


def process_collision():
    global players
    global bonus_marks

    for player in players:
        for bullet in player.bullets:
            bullet.move()

    for player in players:
        for bullet in player.bullets:
            if bullet.invalidate:
                continue
            for bonus_mark in bonus_marks:
                if bonus_mark.invalidate:
                    continue
                if internal_math.circle_intersection_square(bullet, bonus_mark) > internal_math.EPS:
                    bonus_mark.health -= bullet.damage
                    bullet.invalidate = True
                    if bonus_mark.health <= 0:
                        player.score += bonus_mark.gives_score
                        bonus_mark.invalidate = True
            for player_other in players:
                if player.uid == player_other.uid:
                    continue
                for bullet_other in player_other.bullets:
                    if bullet_other.invalidate:
                        continue
                    if internal_math.circle_intersection_square(bullet, bullet_other) > internal_math.EPS:
                        bullet.invalidate = True
                        bullet_other.invalidate = True
                if player_other.tank is not None and \
                        internal_math.circle_intersection_square(bullet, player_other.tank) > internal_math.EPS:
                    bullet.invalidate = True
                    player_other.tank.health -= bullet.damage
                    if player_other.tank.health <= 0:
                        player_other.tank.invalidate = True

    for player in players:
        for bullet in player.bullets:
            if bullet.invalidate:
                continue
            if bullet.center_x < 0 or bullet.center_x >= WORLD_WIDTH \
                    or bullet.center_y < 0 or bullet.center_y >= WORLD_HEIGHT:
                bullet.invalidate = True

    for player in players:
        new_bullets = []
        for bullet in player.bullets:
            if bullet.invalidate:
                continue
            new_bullets.append(bullet)
        player.bullets = new_bullets
        if player.tank is None:
            continue
        if player.tank.invalidate:
            player.tank = None

    new_bonus_marks = []
    for bonus_mark in bonus_marks:
        if bonus_mark.invalidate:
            continue
        new_bonus_marks.append(bonus_mark)
    bonus_marks = new_bonus_marks


if __name__ == '__main__':
    main()
