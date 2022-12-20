import math
from game_objects.circle import CircleBody

EPS = 1e-9


def circle_square(circle: CircleBody):
    return math.pi * circle.radius * circle.radius


def circle_intersection_square(circle_a: CircleBody, circle_b: CircleBody):
    d = math.sqrt((circle_a.center_x - circle_b.center_x) ** 2 + (circle_a.center_y - circle_b.center_y) ** 2)
    if circle_a.radius + circle_b.radius < d or math.fabs(circle_a.radius + circle_b.radius - d) < EPS:
        return 0
    if d + circle_a.radius < circle_b.radius:
        return circle_square(circle_a)
    if d + circle_b.radius < circle_a.radius:
        return circle_square(circle_b)
    f1 = 2 * math.acos((circle_a.radius ** 2 - circle_b.radius ** 2 + d ** 2) / (2 * circle_a.radius * d))
    f2 = 2 * math.acos((circle_b.radius ** 2 - circle_a.radius ** 2 + d ** 2) / (2 * circle_b.radius * d))
    s1 = circle_a.radius ** 2 * (f1 - math.sin(f1)) / 2
    s2 = circle_b.radius ** 2 * (f2 - math.sin(f2)) / 2
    return s1 + s2
