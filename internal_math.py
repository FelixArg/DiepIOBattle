import math

from game_objects.circle import CircleBody

EPS = 1e-9


def circle_square(circle: CircleBody):
    return math.pi * circle.radius * circle.radius


def is_circle_intersect(circle_a: CircleBody, circle_b: CircleBody):
    d = math.sqrt((circle_a.center_x - circle_b.center_x) ** 2 + (circle_a.center_y - circle_b.center_y) ** 2)
    if d > circle_a.radius + circle_b.radius:
        return False
    return True


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


def projection_vector(a, b):
    return (a[0] * b[0] + a[1] * b[1])


def vector_norm(v):
    norm = math.sqrt(v[0] * v[0] + v[1] * v[1])
    return v[0] / norm, v[1] / norm


def vector_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def impulse_calculate(m1, m2, u1, u2, vc):
    vc = vector_norm(vc)
    un1 = projection_vector(u1, vc)
    un2 = projection_vector(u2, vc)
    ut1 = projection_vector(u1, [-vc[1], vc[0]])
    ut2 = projection_vector(u2, [-vc[1], vc[0]])
    a = m2 * m2 + m1 * m2
    b = -2 * m1 * m2 * un1 - 2 * m2 * m2 * un2
    c = m2 * m2 * un2 * un2 + 2 * m1 * m2 * un1 * un2 - m2 * m1 * un2 * un2
    unr2 = quadr_solve(a, b, c)
    unr1 = (m1 * un1 + m2 * un2 - m2 * unr2) / m1
    ur1 = [unr1 * vc[0] - ut1 * vc[1], unr1 * vc[1] + ut1 * vc[0]]
    ur2 = [unr2 * vc[0] - ut2 * vc[1], unr2 * vc[1] + ut2 * vc[0]]
    return ur1, ur2


def quadr_solve(a, b, c):
    d = b * b - 4 * a * c
    if d < 0:
        raise Exception
    return (-b + math.sqrt(d)) / 2 / a
