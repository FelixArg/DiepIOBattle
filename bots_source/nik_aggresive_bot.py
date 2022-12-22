class Tank:
    x = -1
    y = -1
    r = -1
    angle = -1
    health = -1
    max_health = -1
    speed = -1
    damage = -1
    bullet_speed = -1


class Bullet:
    x = -1
    y = -1
    r = -1


class BonusMark:
    x = -1
    y = -1
    r = -1


if __name__ == '__main__':
    s = input()
    if s != "Defeat":
        my_score = int(s)

        my_tank = Tank()
        my_tank.x, my_tank.y, my_tank.r, my_tank.angle = map(float, input().split())
        my_tank.health, my_tank.max_health, my_tank.speed, my_tank.bullet_speed, my_tank.damage = map(float,
                                                                                                      input().split())

        my_bullets_count = int(input())
        my_bullets = []
        for i in range(my_bullets_count):
            bullet = Bullet()
            bullet.x, bullet.y, bullet.r = map(float, input().split())
            my_bullets.append(bullet)

        enemies_count = int(input())
        enemies = []
        for i in range(enemies_count):
            is_enemy_alive = int(input())
            enemy_score, enemy_uid = map(int, input().split())
            enemy_tank = Tank()
            if is_enemy_alive == 1:
                enemy_tank.x, enemy_tank.y, enemy_tank.r, enemy_tank.angle = map(float, input().split())

            enemy_bullets_count = int(input())
            enemy_bullets = []

            for i in range(enemy_bullets_count):
                bullet = Bullet()
                bullet.x, bullet.y, bullet.r = map(float, input().split())
                enemy_bullets.append(bullet)
            enemies.append((enemy_score, enemy_uid, enemy_tank, enemy_bullets))

        bonus_mark_count = int(input())

        bonus_marks = []
        for i in range(bonus_mark_count):
            bonus_mark = BonusMark()
            bonus_mark.x, bonus_mark.y, bonus_mark.r = map(float, input().split())
            bonus_marks.append(bonus_mark)

        memory_string = input()

        uid_mn = 1e9
        move_point = 0, 0

        for i in range(enemies_count):
            enemy_score, enemy_uid, enemy_tank, enemy_bullets = enemies[i]
            if enemy_tank.x == -1:
                continue

            if enemy_uid < uid_mn:
                uid_mn = enemy_uid
                move_point = enemy_tank.x, enemy_tank.y

        print("move", move_point[0], move_point[1])
        print("shoot")
        print(flush=True)
