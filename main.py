import argparse
import asyncio
import logging
import math
import random
import sys
import time

import pygame

import internal_math
from constants import *
from game_objects.bonus_mark import BonusMark
from game_objects.player import Player
from game_objects.upgrade import UpgradeType

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (255, 0, 255)
GREENBLUE = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (150, 150, 150)

RUSSIAN_COLORS = ['Красный', 'Синий', 'Бирюзовый', 'Оранжевый']
RUSSIAN_COLORS_GENITIVE = ['Красного', 'Синего', 'Бирюзового', 'Оранжевого']
#

# game globals
end_game = INFINITY * FPS
win = []
tick = 0
clock = pygame.time.Clock()
font = None

players = []
bonus_marks = []
events = []


async def main():
    global clock
    global tick
    global end_game

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('DiepIO Battle')

    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)

    parser = argparse.ArgumentParser()
    parser.add_argument('players_program_path', nargs='*')
    parser.add_argument('--time', type=int, help='Play for {time} seconds')
    args = parser.parse_args()

    init_game(args.players_program_path)
    if args.time is not None:
        end_game = args.time * FPS

    while True:
        await process_game_tick(screen)
        clock.tick(FPS)
        tick += 1
        logging.info("===============================Round " + str(tick) + "=================================")


def init_game(players_program):
    global bonus_marks
    global font

    random.seed(time.time())

    font = pygame.font.SysFont('Courier new', 18, bold=True)

    colors = (RED, BLUE, GREENBLUE, ORANGE)

    for i in range(len(players_program)):
        players.append(Player(i))
        players[i].program_path = players_program[i]
        players[i].color = colors[i]

    add_new_bonus_marks(BONUS_MARK_DEFAULT_COUNT)


async def process_game_tick(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if len(win) == 0:
        await process_game_logic()
        process_collision()
        process_post_game_logic()
    draw_all(screen)


def draw_all(screen):
    global players
    global bonus_marks
    global font
    global events

    screen.fill(WHITE)

    # Game objects
    for player in players:
        for bullet in player.bullets:
            pygame.draw.circle(screen, VIOLET, (bullet.center_x, bullet.center_y + 50), bullet.radius)

    for bonus_mark in bonus_marks:
        pygame.draw.circle(screen, GREEN, (bonus_mark.center_x, bonus_mark.center_y + 50), bonus_mark.radius)

    for player in players:
        if player.tank is None:
            continue
        canon_points = [[player.tank.radius / 4, player.tank.radius / 8],
                        [player.tank.radius / 4, -player.tank.radius / 8],
                        [3 * player.tank.radius / 2,
                         -(3 * player.tank.radius / 16 + player.bullet_power * player.tank.radius / 16)],
                        [3 * player.tank.radius / 2,
                         (3 * player.tank.radius / 16 + player.bullet_power * player.tank.radius / 16)]]
        new_canon_points = []
        for x, y in canon_points:
            new_x = x * math.cos(player.tank.angle) - y * math.sin(player.tank.angle)
            new_y = y * math.cos(player.tank.angle) + x * math.sin(player.tank.angle)
            new_canon_points.append([new_x + player.tank.center_x, new_y + player.tank.center_y + 50])
        canon_points = new_canon_points

        pygame.draw.polygon(screen, GRAY, canon_points)
        pygame.draw.aalines(screen, GRAY, True, canon_points)
        pygame.draw.circle(screen, player.color,
                           (player.tank.center_x, player.tank.center_y + 50), player.tank.radius)

        # draw healthbar
        health_bar_width = player.tank.radius * 2
        health_bar_heigth = player.tank.radius * 2 / 5
        health_bar_percent = player.tank.health / player.tank.max_health
        green_to_red = (255 - int(255 * health_bar_percent), int(255 * health_bar_percent), 0)
        pygame.draw.rect(screen, green_to_red,
                         (player.tank.center_x - player.tank.radius, player.tank.center_y + player.tank.radius + 2 + 50,
                          health_bar_width, health_bar_heigth), 1, 1)
        pygame.draw.rect(screen, green_to_red,
                         (player.tank.center_x - player.tank.radius + (1 - health_bar_percent) * health_bar_width,
                          player.tank.center_y + player.tank.radius + 2 + 50,
                          health_bar_width * health_bar_percent, health_bar_heigth), border_radius=1)
        # end draw healthbar

        if player.bullet_power != 0:
            pygame.draw.circle(screen, VIOLET,
                               (player.tank.center_x, player.tank.center_y + 50),
                               BULLET_DEFAULT_RADIUS + player.bullet_power)

    pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - WORLD_HEIGHT))

    margin = 17

    for player in players:
        player_info_str = 'Player ' + str(player.uid + 1) + ' Score: ' + str(player.score)
        player_score_img = font.render(player_info_str, True, player.color)
        screen.blit(player_score_img, (margin, 17))
        margin += player_score_img.get_width() + 17

    tick_img = font.render('Тик: ' + str(min(end_game, tick)), True, BLACK)
    screen.blit(tick_img, (margin, 17))
    margin += tick_img.get_width() + 17

    for idx, event in enumerate(events):
        player_score_img = font.render(event[0], True, BLACK)
        time_left = (tick - event[1]) / event[2]
        player_score_img.set_alpha(255 - int(255 * time_left))
        screen.blit(player_score_img, (margin, 17 + event[3] * (tick - event[1])))

    if len(win) != 0:
        font2 = pygame.font.SysFont('Courier new', 40, bold=True)
        winners = ''
        if len(win) == 1:
            winners = 'Абсолютный чемпион ' + RUSSIAN_COLORS[win[0]] + '!'
        else:
            winners = 'Разделили первое место ' + ', '.join([RUSSIAN_COLORS[uid] for uid in win]) + '.'

        winners_img = font2.render(winners, True, BLACK)
        screen.blit(winners_img, (WORLD_WIDTH / 2 - winners_img.get_width() / 2,
                                  WORLD_HEIGHT / 2 - winners_img.get_height() / 2 + 50))

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
    except Exception:
        logging.error("Timeout program error")
    return players_output


async def process_game_logic():
    global points
    global players
    global tick

    to_run_parameters = []

    for player in players:
        exec_string = player.program_path
        if player.program_path.endswith('.py'):
            exec_string = 'python ' + player.program_path
        elif player.program_path.endswith('.exe'):
            exec_string = player.program_path
        elif player.program_path.endswith('.jar'):
            exec_string = 'java -jar ' + player.program_path
        elif player.program_path.endswith('.class'):
            last_sep = max(player.program_path.rfind('\\'), player.program_path.rfind('/'))
            class_name = player.program_path[last_sep + 1:-6:]
            path_name = player.program_path[:last_sep + 1:]
            exec_string = 'java ' + path_name + ' ' + class_name
        to_run_parameters.append((player.uid, exec_string))

    players_output = await asyncio.gather(*(
        run_player_program(parameter[0], parameter[1]) for parameter in to_run_parameters))

    for i in range(len(to_run_parameters)):
        parse_player_output(to_run_parameters[i][0], players_output[i])

    for player in players:
        for bullet in player.bullets:
            if bullet.lifetime >= tick:
                bullet.move()
            else:
                bullet.invalidate = True


def process_collision():
    global players
    global bonus_marks
    global events

    for player in players:
        for bullet in player.bullets:
            if bullet.invalidate:
                continue
            for bonus_mark in bonus_marks:
                if bullet.invalidate:
                    break
                if bonus_mark.invalidate:
                    continue
                if internal_math.is_circle_intersect(bullet, bonus_mark):
                    bonus_mark.health -= bullet.damage
                    bullet.invalidate = True
                    if bonus_mark.health <= 0:
                        player.score += bonus_mark.gives_score
                        bonus_mark.invalidate = True
            for player_other in players:
                if bullet.invalidate:
                    break
                if player.uid == player_other.uid:
                    continue
                for bullet_other in player_other.bullets:
                    if bullet.invalidate:
                        break
                    if bullet_other.invalidate:
                        continue
                    if internal_math.is_circle_intersect(bullet, bullet_other):
                        bullet.invalidate = True
                        bullet_other.invalidate = True
                if bullet.invalidate:
                    break
                if player_other.tank is not None and \
                        internal_math.is_circle_intersect(bullet, player_other.tank):
                    bullet.invalidate = True
                    player_other.tank.health -= bullet.damage
                    if player_other.tank.health <= 0:
                        events.append((RUSSIAN_COLORS[player.uid] + ' расщепил на атомы '
                                       + RUSSIAN_COLORS_GENITIVE[player_other.uid],
                                       tick, 3 * DEFAULT_EVENT_LIFE * FPS, len(events)))
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
        physical_interaction(player, players, bonus_marks)

    new_bonus_marks = []
    for bonus_mark in bonus_marks:
        if bonus_mark.invalidate:
            continue
        new_bonus_marks.append(bonus_mark)
    bonus_marks = new_bonus_marks


def physical_interaction(player, players, bonus_marks):
    if player.tank is None:
        return
    for other_player in players:
        if other_player.tank is None:
            continue
        if other_player.uid != player.uid:
            if internal_math.is_circle_intersect(player.tank, other_player.tank):
                vc = (
                    other_player.tank.center_x - player.tank.center_x,
                    other_player.tank.center_y - player.tank.center_y)

                try:
                    u1, _ = internal_math.impulse_calculate(player.tank.radius ** 2, other_player.tank.radius ** 2,
                                                            player.cur_speed, other_player.cur_speed, vc)
                    real_speed = 1 / FPS * player.tank.speed * 40
                    if internal_math.vector_length(u1) > real_speed:
                        k = internal_math.vector_length(u1) / real_speed
                        u1[0] = u1[0] / k
                        u1[1] = u1[1] / k
                except:
                    u1 = [0, 0]
                logging.info("Player " + str(player.uid) + ": Face with player! New speed: " + str(u1))
                player.add_velocity((2 * u1[0], 2 * u1[1]))

    for bonus_mark in bonus_marks:
        if internal_math.is_circle_intersect(player.tank, bonus_mark):
            vc = (
                bonus_mark.center_x - player.tank.center_x,
                bonus_mark.center_y - player.tank.center_y)
            try:
                u1, _ = internal_math.impulse_calculate(player.tank.radius ** 2, BIG_MASS,
                                                        player.cur_speed, (0, 0), vc)
                real_speed = 1 / FPS * player.tank.speed
                if internal_math.vector_length(u1) < real_speed:
                    u1[0] = 2 * u1[0]
                    u1[1] = 2 * u1[1]
            except:
                u1 = [0, 0]
            logging.info("Player " + str(player.uid) + ": Obstacle! New speed: " + str(u1))
            player.add_velocity((u1[0], u1[1]))


def process_post_game_logic():
    global events
    global win
    global end_game

    add_new_bonus_marks(BONUS_MARK_DEFAULT_COUNT - len(bonus_marks))
    for player in players:
        if player.tank is None:
            continue
        player.tank.regenerate()
        logging.info(
            f"Player {player.uid}. Health: {player.tank.health}, X: {player.tank.center_x}, Y: {player.tank.center_y}, Score: {player.score}, Speed: {player.cur_speed}")
    new_events = []
    for event in events:
        if tick - event[1] < event[2]:
            new_events.append(event)
    events = new_events

    player_alive_count = 0
    for player in players:
        if player.tank is not None:
            player_alive_count += 1

    if player_alive_count == 0:
        max_score = max((player.score for player in players))
        for player in players:
            if player.score == max_score:
                win.append(player.uid)
        end_game = tick
    elif player_alive_count == 1:
        max_score = max((player.score for player in players))
        count = 0
        for player in players:
            if player.score == max_score:
                count += 1
        if count == 1:
            for player in players:
                if player.tank is not None and player.score == max_score:
                    win.append(player.uid)
        end_game = tick
    elif tick == end_game:
        max_score = max((player.score for player in players))
        for player in players:
            if player.score == max_score:
                win.append(player.uid)


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
        return 'Dead\n'

    info_string = ''
    info_string += str(tick) + '\n'
    info_string += str(player.score) + '\n'
    info_string += "{:.3f}".format(player.tank.center_x) + ' ' + "{:.3f}".format(player.tank.center_y) + ' ' \
                   + "{:.3f}".format(player.tank.radius) + ' ' + "{:.10f}".format(player.tank.angle) + '\n'
    info_string += str(int(player.tank.health)) + ' ' + str(int(player.tank.max_health)) + ' ' \
                   + str(int(player.tank.speed)) + ' ' \
                   + str(int(player.tank.bullet_speed_add + BULLET_DEFAULT_SPEED)) + ' ' \
                   + str(int(player.tank.damage_add + BULLET_DEFAULT_DAMAGE)) + '\n'

    info_string += str(len(player.bullets)) + '\n'
    for bullet in player.bullets:
        info_string += "{:.3f}".format(bullet.center_x) + ' ' + "{:.3f}".format(bullet.center_y) \
                       + ' ' + "{:.3f}".format(bullet.radius) + '\n'

    info_string += str(len(players) - 1) + '\n'
    for player_cur in players:
        if player_cur.uid == player.uid:
            continue
        if player_cur.tank is None:
            info_string += str(0) + '\n'
            info_string += str(player_cur.score) + ' ' + str(player_cur.uid) + '\n'
        else:
            info_string += str(1) + '\n'
            info_string += str(player_cur.score) + ' ' + str(player_cur.uid) + ' ' + str(int(player_cur.tank.health)) + '\n'
            info_string += "{:.3f}".format(player_cur.tank.center_x) + ' ' \
                           + "{:.3f}".format(player_cur.tank.center_y) + ' ' \
                           + "{:.3f}".format(player_cur.tank.radius) + ' ' \
                           + "{:.10f}".format(player_cur.tank.angle) + '\n'
        info_string += str(len(player_cur.bullets)) + '\n'
        for bullet in player_cur.bullets:
            info_string += "{:.3f}".format(bullet.center_x) + ' ' + "{:.3f}".format(bullet.center_y) + ' ' \
                           + "{:.3f}".format(bullet.radius) + '\n'

    info_string += str(len(bonus_marks)) + '\n'
    for bonus_mark in bonus_marks:
        info_string += str(int(bonus_mark.health)) + '\n'
        info_string += "{:.3f}".format(bonus_mark.center_x) + ' ' + "{:.3f}".format(bonus_mark.center_y) + ' ' \
                       + "{:.3f}".format(bonus_mark.radius) + '\n'

    info_string += player.memory_string + '\n'
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
    logging.info("Player " + str(player_uid) + ":")
    logging.info(player_output)
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
            elif l[0] == 'power' and not player_shoot:
                player_shoot = True
                players[player_uid].increase_power(tick)
            elif l[0] == 'turn' and not player_turn:
                player_turn = True
                angle = float(l[1])
                if angle > 2 * math.pi:
                    raise Exception
                if angle < -2 * math.pi:
                    raise Exception
                players[player_uid].turn(angle, tick)
            elif l[0] == 'upgrade' and player_upgrade_count < MAX_UPGRADE_COUNT_PER_TICK:
                player_upgrade_count += 1
                type = l[1]
                valid_types = ['max_health', 'speed', 'damage', 'health_regeneration', 'bullet_speed']
                event_string = ''
                if type not in valid_types:
                    raise Exception
                if type == 'max_health':
                    type = UpgradeType.MAX_HEALTH
                    event_string = 'максимальное здоровье'
                elif type == 'speed':
                    type = UpgradeType.SPEED
                    event_string = 'скорость'
                elif type == 'damage':
                    type = UpgradeType.DAMAGE
                    event_string = 'урон'
                elif type == 'bullet_speed':
                    type = UpgradeType.BULLET_SPEED
                    event_string = 'скорость снаряда'
                success = players[player_uid].upgrade(type, tick)
                if success:
                    events.append((RUSSIAN_COLORS[player_uid] + ' улучшил ' + event_string,
                                   tick, DEFAULT_EVENT_LIFE * FPS, len(events)))
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
    logging.basicConfig(filename="game.log", filemode="w", level=logging.INFO)
    asyncio.run(main())
