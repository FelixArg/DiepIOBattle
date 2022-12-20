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
#

# game globals
tick = 0
clock = pygame.time.Clock()

point = [1000, 700]
player = Player()
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
    global player
    global bonus_marks

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, WORLD_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - WORLD_HEIGHT))

    pygame.draw.circle(screen, RED, (player.tank.center_x, player.tank.center_y), player.tank.radius)

    for bonus_mark in bonus_marks:
        pygame.draw.circle(screen, GREEN, (bonus_mark.center_x, bonus_mark.center_y), bonus_mark.radius)

    for bullet in player.bullets:
        pygame.draw.circle(screen, BLUE, (bullet.center_x, bullet.center_y), bullet.radius)

    pygame.display.update()


def process_game_logic():
    global point
    global player

    if math.fabs(point[0] - player.tank.center_x) < internal_math.EPS and \
            math.fabs(point[1] - player.tank.center_y) < internal_math.EPS:
        point = [random.random() * WORLD_WIDTH, random.random() * WORLD_HEIGHT]

    vec = (point[0] - player.tank.center_x, point[1] - player.tank.center_y)
    angle_cur = math.atan2(vec[1], vec[0])
    if angle_cur < 0:
        angle_cur += 2 * math.pi
    if math.fabs(angle_cur - player.tank.angle) < internal_math.EPS:
        distance = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
        player.move(distance, tick)
    else:
        angle = angle_cur - player.tank.angle
        player.turn(angle, tick)

    if tick % FPS == 0:
        player.shoot(tick)

    for bullet in player.bullets:
        bullet.move()


def process_collision():
    global player
    global bonus_marks

    new_bonus_marks = []
    new_bullets = []

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

    for bullet in player.bullets:
        if bullet.invalidate:
            continue
        if bullet.center_x < 0 or bullet.center_x >= WORLD_WIDTH \
                or bullet.center_y < 0 or bullet.center_y >= WORLD_HEIGHT:
            bullet.invalidate = True

    for bullet in player.bullets:
        if bullet.invalidate:
            continue
        new_bullets.append(bullet)

    for bonus_mark in bonus_marks:
        if bonus_mark.invalidate:
            continue
        new_bonus_marks.append(bonus_mark)

    player.bullets = new_bullets
    bonus_marks = new_bonus_marks


if __name__ == '__main__':
    main()
