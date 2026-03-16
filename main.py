"""
Задачи Максим:
1) Сделать нормальное ООП
2) Сделать ограничительную сферу для роботов и просчет коллизий робота
3) Решить что делать с координатной системой(сделать пиксельной??)
4) ужно сделать для каждой конечной точки, некоторую сферу, заезд в радиус которой, засчитывается как финиш (если ограничительная сфера касается точки)


Задачи для двоих:
1) первый тик - разворот всех роботов в направлении финиша
2) сверка со сферой коллизии, делей для роботов которые столкнутся
3) прострока пути


Нужно узнать как нам отдадут угол поворота и в каком формате координаты(если какая-то херня по типу 100000 на 100000,
то перевести в свои, условно 100 на 100 нужно будет.

И добавить ограничители чтобы роботы не въебались друг в друга.

Для ограничения карты хз, робот не квадрат, так что нужно с запасом сделать ограничение карты(в целом не проблема если
они едут не с края).

Если роботы едут с края, то нужно как-то ограничить повороты, чтобы не забуксовали в углу где-нибудь.


Для Максима, а нах переводить координаты в свою систему? только мы ведь с ними работать будем

Конкретно сейчас код просто может построить фигуру(многоугольник) - но на счет правильности не уверен

UPD Максим: нужно сделать для каждой конечной точки, некоторую сферу, заезд в радиус которой, засчитывается как финиш



"""

import math
from collections import namedtuple

# Структура для хранения данных робота
Robot = namedtuple('Robot', ['id', 'x', 'y', 'ygol'])

x = int
y = int
a: list[x, y] = [5,6]

b = x(6.7)
print(b)


pohody_debug = True


def get_robots():
    if pohody_debug:
        return [
            Robot(
                id=1,
                x=50,
                y=5,
                ygol=1,
            ),
            Robot(
                id=2,
                x=2,
                y=2,
                ygol=1,
            ),
            Robot(
                id=3,
                x=3,
                y=3,
                ygol=1,
            ),
            Robot(
                id=4,
                x=4,
                y=4,
                ygol=1,
            ),
            Robot(
                id=5,
                x=10,
                y=20,
                ygol = (1,)
            ),
        ]
    return None # данные с камеры



def get_target_coordinates(robots):
    map_size = 100  # размер карты
    collision_distance = 10  # дистанция между роботами и краями карты
    N = len(robots)
    if N == 0:
        return {}

    # Центр карты
    cx = map_size / 2
    cy = map_size / 2

    margin = collision_distance

    if N == 1:
        R = 0
    else:
        # радиусы для того чтобы не выехать за карту
        max_R_x = cx - margin
        max_R_y = cy - margin
        max_R = min(max_R_x, max_R_y)

        if N > 1:
            # Если роботов много(но вероятно больше 5 не будет)
            min_vertex_distance = 2 * max_R * math.sin(math.pi / N)
            if min_vertex_distance < collision_distance and N > 1:
                max_R = collision_distance / (2 * math.sin(math.pi / N))

        R = max_R

    # чтобы роботы ехали к ближайшей точке
    robots_with_angle = []
    for r in robots:
        angle = math.atan2(r.y - cy, r.x - cx)
        robots_with_angle.append((angle, r))
    robots_with_angle.sort(key=lambda x: x[0])

    targets = {}
    for i, (_, robot) in enumerate(robots_with_angle):
        if N == 1:
            tx, ty = cx, cy  # тупо в центр
        else:
            # Угол вершины (начинаем с 0 и идём против часовой стрелки)
            vertex_angle = i * 2 * math.pi / N
            # Вообще если мы будет использовать свои условные координаты, то это не нужно, т.к. можем отдать кривые
            # координаты (Round имею ввиду)
            tx = round(cx + R * math.cos(vertex_angle))
            ty = round(cy + R * math.sin(vertex_angle))

        targets[robot.id] = (tx, ty)

    return targets


def main():
    robots = get_robots()
    targets = get_target_coordinates(robots)
    print(targets)


if __name__ == "__main__":
    main()
