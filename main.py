import math
import sys
import pygame
import argparse
import random
import asyncio

import internal_math
from game_objects.player import Player
from game_objects.bonus_mark import BonusMark
from game_objects.upgrade import UpgradeType
from constants import *

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (255, 0, 255)
GREENBLUE = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
#

# game globals
tick = 0
clock = pygame.time.Clock()
font = None

points = [[1000, 700], [1000, 700]]

players = []
bonus_marks = []
#


async def main():
    global clock
    global tick

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DiepIO Battle')

    parser = argparse.ArgumentParser()
    parser.add_argument('players_program_path', nargs='*')
    args = parser.parse_args()

    init_game(args.players_program_path)
    while True:
        await process_game_tick(screen)
        clock.tick(FPS)
        tick += 1


def init_game(players_program):
    global bonus_marks
    global font

    if len(players_program) == 0:
        players_program = ['HelloWorld.class']

    random.seed(0)

    random.shuffle(players_program)

    font = pygame.font.SysFont('Courier new', 20)

    for i in range(len(players_program)):
        players.append(Player(i))
        players[i].program_path = players_program[i]

    add_new_bonus_marks(BONUS_MARK_DEFAULT_COUNT)


async def process_game_tick(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    await process_game_logic()
    process_collision()
    process_post_game_logic()
    draw_all(screen)


def draw_all(screen):
    global players
    global bonus_marks
    global font

    screen.fill(WHITE)

    # Game objects
    for player in players:
        for bullet in player.bullets:
            pygame.draw.circle(screen, VIOLET, (bullet.center_x, bullet.center_y), bullet.radius)

    for bonus_mark in bonus_marks:
        pygame.draw.circle(screen, GREEN, (bonus_mark.center_x, bonus_mark.center_y), bonus_mark.radius)

    for player in players:
        if player.tank is None:
            continue
        pygame.draw.circle(screen, (RED, BLUE, GREENBLUE, ORANGE)[player.uid],
                           (player.tank.center_x, player.tank.center_y), player.tank.radius)
    #

    pygame.draw.rect(screen, GRAY, (0, WORLD_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - WORLD_HEIGHT))
    pygame.draw.rect(screen, BLACK, (0, WORLD_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - WORLD_HEIGHT), 3)

    player_1_info_str = 'Player 1 [' + 'Score: ' + str(players[0].score) + ' ' + 'Health: ' + \
                        str(0 if players[0].tank is None else math.trunc(players[0].tank.health)) + ' ' + 'Speed: ' \
                        + str(0 if players[0].tank is None else players[0].tank.speed) + ' ' + 'Damage: ' \
                        + str(0 if players[0].tank is None else players[0].tank.damage_add + BULLET_DEFAULT_DAMAGE) \
                        + ']'
    player_1_score_img = font.render(player_1_info_str, True, RED)
    screen.blit(player_1_score_img, (15, WORLD_HEIGHT + 15))

    player_2_info_str = 'Player 2 [' + 'Score: ' + str(players[1].score) + ' ' + 'Health: ' + \
                        str(0 if players[1].tank is None else math.trunc(players[1].tank.health)) + ' ' + 'Speed: ' \
                        + str(0 if players[1].tank is None else players[1].tank.speed) + ' ' + 'Damage: ' \
                        + str(0 if players[1].tank is None else players[1].tank.damage_add + BULLET_DEFAULT_DAMAGE) \
                        + ']'
    player_2_score_img = font.render(player_2_info_str, True, BLUE)
    screen.blit(player_2_score_img, (WORLD_WIDTH - 15 - player_2_score_img.get_width(), WORLD_HEIGHT + 15))

    pygame.display.update()


async def run_player_program(player_uid, exec_string):
    player_info_string = collect_input_for_player(players[player_uid])
    players_output = None
    try:
        proc = await asyncio.create_subprocess_shell(exec_string, stdin=asyncio.subprocess.PIPE,
                                                     stdout=asyncio.subprocess.PIPE)
        players_output, err = await asyncio.wait_for(proc.communicate(input=player_info_string.encode('utf-8')),
                                                     PLAYER_PROGRAM_TIMEOUT)
        players_output = players_output.decode('utf-8')
    except asyncio.exceptions.TimeoutError:
        pass
    return players_output


async def process_game_logic():
    global points
    global players
    global tick

    to_run_parameters = []

    for player in players:
        exec_string = None
        if player.program_path.endswith('.py'):
            exec_string = 'python3 ' + player.program_path
        elif player.program_path.endswith('.exe'):
            exec_string = player.program_path
        elif player.program_path.endswith('.jar'):
            exec_string = 'java -jar' + player.program_path
        elif player.program_path.endswith('.class'):
            last_sep = max(player.program_path.rfind('\\'), player.program_path.rfind('/'))
            class_name = player.program_path[last_sep + 1:-6:]
            path_name = player.program_path[:last_sep + 1:]
            exec_string = 'java ' + path_name + ' ' + class_name
        else:
            exec_string = player.program_path
        to_run_parameters.append((player.uid, exec_string))

    players_output = await asyncio.gather(*(
        run_player_program(parameter[0], parameter[1]) for parameter in to_run_parameters))

    for i in range(len(to_run_parameters)):
        parse_player_output(to_run_parameters[i][0], players_output[i])

    for player in players:
        for bullet in player.bullets:
            bullet.move()


def process_collision():
    global players
    global bonus_marks

    for player in players:
        for bullet in player.bullets:
            if bullet.invalidate:
                continue
            for bonus_mark in bonus_marks:
                if bonus_mark.invalidate:
                    continue
                if internal_math.is_circle_intersect(bullet, bonus_mark):
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
                    if internal_math.is_circle_intersect(bullet, bullet_other):
                        bullet.invalidate = True
                        bullet_other.invalidate = True
                if player_other.tank is not None and \
                        internal_math.is_circle_intersect(bullet, player_other.tank):
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


def process_post_game_logic():
    add_new_bonus_marks(BONUS_MARK_DEFAULT_COUNT - len(bonus_marks))
    for player in players:
        if player.tank is None:
            continue
        player.tank.regenerate()


def add_new_bonus_marks(count):
    for i in range(count):
        bonus_mark = BonusMark()
        bonus_mark.center_x = random.random() * WORLD_WIDTH
        bonus_mark.center_y = random.random() * WORLD_HEIGHT
        can_place = True
        for j in range(BONUS_MARK_DEFAULT_PLACE_TRIES):
            for player in players:
                if player.tank is None:
                    continue
                if internal_math.is_circle_intersect(bonus_mark, player.tank):
                    can_place = False
            for bonus_mark_cur in bonus_marks:
                if internal_math.is_circle_intersect(bonus_mark, bonus_mark_cur):
                    can_place = False
            if can_place:
                break
        if can_place:
            bonus_marks.append(bonus_mark)


def collect_input_for_player(player):
    if player.tank is None:
        return 'Defeat'

    info_string = ''
    info_string += str(player.score) + '\n'
    info_string += str(player.tank.center_x) + ' ' + str(player.tank.center_y) + ' ' + str(player.tank.radius) + '\n'
    info_string += str(player.tank.health) + ' ' + str(player.tank.max_health) + '\n'
    info_string += str(player.tank.speed) + '\n'
    info_string += str(player.tank.bullet_speed_add + BULLET_DEFAULT_SPEED) + ' ' + \
                   str(player.tank.damage_add + BULLET_DEFAULT_DAMAGE) + '\n'

    info_string += str(len(player.bullets)) + '\n'
    for bullet in player.bullets:
        info_string += str(bullet.center_x) + ' ' + str(bullet.center_y) + ' ' + str(bullet.radius) + '\n'

    other_player_count = 0
    for player_cur in players:
        if player_cur.tank is None or player_cur.uid == player.uid:
            continue
        other_player_count += 1

    for player_cur in players:
        if player_cur.uid == player.uid:
            continue
        if player_cur.tank is None:
            info_string += str(0) + '\n'
            info_string += str(player_cur.score) + '\n'
        else:
            info_string += str(1) + '\n'
            info_string += str(player_cur.score) + '\n'
            info_string += str(player_cur.tank.center_x) + ' ' + str(player_cur.tank.center_y) + ' ' + \
                           str(player_cur.tank.radius) + '\n'
        info_string += str(len(player_cur.bullets)) + '\n'
        for bullet in player_cur.bullets:
            info_string += str(bullet.center_x) + ' ' + str(bullet.center_y) + ' ' + str(bullet.radius) + '\n'

    info_string += str(len(bonus_marks)) + '\n'
    for bonus_mark in bonus_marks:
        info_string += str(bonus_mark.center_x) + ' ' + str(bonus_mark.center_y) + ' ' + str(bonus_mark.radius) + '\n'

    info_string += player.memory_string
    return info_string


def parse_player_output(player_uid, player_output):
    global players
    if player_output is None:
        return

    player_moved = False
    player_shoot = False
    player_turn = False
    player_memory_string = False
    player_upgrade_count = 0

    for line in player_output.split('\n'):
        try:
            l = line.split()
            if l[0] == 'move' and not player_moved:
                player_moved = True
                x = float(l[1])
                y = float(l[2])
                players[player_uid].move((x, y), tick)
            elif l[0] == 'shoot' and not player_shoot:
                player_shoot = True
                players[player_uid].shoot(tick)
            elif l[0] == 'turn' and not player_turn:
                player_turn = True
                angle = float(l[1])
                if angle > 2 * math.pi:
                    raise Exception
                if angle < -2 * math.pi:
                    raise Exception
                players[player_uid].turn(angle)
            elif l[0] == 'upgrade' and player_upgrade_count < MAX_UPGRADE_COUNT_PER_TICK:
                player_upgrade_count += 1
                type = l[1]
                valid_types = ['max_health', 'speed', 'damage', 'health_regeneration', 'bullet_speed']
                if type not in valid_types:
                    raise Exception
                if type == 'max_health':
                    type = UpgradeType.MAX_HEALTH
                elif type == 'speed':
                    type = UpgradeType.SPEED
                elif type == 'damage':
                    type = UpgradeType.DAMAGE
                elif type == 'health_regeneration':
                    type = UpgradeType.HEALTH_REGENERATION
                elif type == 'bullet_speed':
                    type = UpgradeType.BULLET_SPEED
                players[player_uid].upgrade(type, tick)
            elif l[0] == 'memory' and not player_memory_string:
                player_memory_string = True
                players[player_uid].memory_string = line[7::]
                if len(players[player_uid].memory_string) > 256:
                    players[player_uid].memory_string = players[player_uid].memory_string[:256:]
            else:
                raise Exception
        except:
            continue


if __name__ == '__main__':
    asyncio.run(main())
