"""
Задачи Максим:
1) Сделать нормальное ООП +
2) Сделать ограничительную сферу для роботов и просчет коллизий робота +
3) Решить что делать с координатной системой(сделать пиксельной??)
4) нужно сделать для каждой конечной точки, некоторую сферу, заезд в радиус которой, засчитывается как финиш (если ограничительная сфера касается точки) +


Задачи для двоих:
1) первый тик - разворот всех роботов в направлении финиша
2) сверка со сферой коллизии, делей для роботов которые столкнутся +
3) простройка пути


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


# ============================================================
# Класс для представления робота
# ============================================================
class Robot:
    """
    Класс, описывающий робота.

    :param id: уникальный идентификатор
    :param x: координата x
    :param y: координата y
    :param ygol: угол поворота (в градусах или радианах)
    :param radius: радиус сферы коллизии (для проверки столкновений)
    :param target_x: целевая координата x
    :param target_y: целевая координата y
    :param finish_radius: радиус сферы, при попадании в которую финиш засчитывается

    finished - флаг, указывающий, достиг ли робот финиша
    has_collision - флаг, указывающий, что робот столкнулся с другим
    """

    def __init__(
        self, id, x, y, ygol, radius=5, finish_radius=5, target_x=None, target_y=None
    ):
        self.id = id
        self.x = x
        self.y = y
        self.ygol = ygol
        self.radius = radius
        self.has_collision = False
        self.target_x = target_x
        self.target_y = target_y
        self.finish_radius = finish_radius
        self.finished = False

    def __repr__(self):
        return (
            f"Robot(id={self.id}, x={self.x}, y={self.y}, ygol={self.ygol}, "
            f"radius={self.radius}, finished={self.finished})"
        )

    def distance_squared_to(self, other):
        """Возвращает квадрат расстояния до другого робота (для оптимизации)"""
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def check_collision_with(self, other):
        """Проверяет коллизию с другим роботом (использует квадраты расстояний)"""
        if self.id == other.id:
            return False
        r_sum = self.radius + other.radius
        return self.distance_squared_to(other) < r_sum * r_sum

    def set_target(self, x, y):
        """Устанавливает целевую точку и сбрасывает флаг finished"""
        self.target_x = x
        self.target_y = y
        self.finished = False

    def check_finish(self):
        """
        Проверяет, находится ли робот в сфере финиша (т.е. достиг ли цели).
        Если да, устанавливает флаг finished = True и возвращает True.
        """
        if self.target_x is None or self.target_y is None:
            return False  # цель не задана

        dx = self.x - self.target_x
        dy = self.y - self.target_y
        distance_sq = dx * dx + dy * dy
        if distance_sq <= self.finish_radius * self.finish_radius:
            self.finished = True
            return True
        return False


# ============================================================
# Функции для получения данных и расчёта целевых точек
# ============================================================
pohody_debug = True


def get_robots():
    """
    Возвращает список роботов.
    В режиме отладки возвращает тестовый набор.
    """
    if pohody_debug:
        return [
            Robot(id=1, x=62, y=12, ygol=1, radius=5, finish_radius=5),
            Robot(id=2, x=1, y=1, ygol=1, radius=5, finish_radius=5),
            Robot(id=3, x=5, y=5, ygol=1, radius=5, finish_radius=5),
            Robot(id=4, x=10, y=10, ygol=1, radius=5, finish_radius=5),
            Robot(id=5, x=10, y=20, ygol=1, radius=5, finish_radius=5),
        ]
    return None  # данные с камеры


def get_target_coordinates(robots):
    """
    Рассчитывает координаты целевых точек для каждого робота.
    Алгоритм остаётся неизменным.
    Возвращает словарь {id_робота: (x, y)}.
    """
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
            # Если роботов много (но вероятно больше 5 не будет)
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
            tx = round(cx + R * math.cos(vertex_angle))
            ty = round(cy + R * math.sin(vertex_angle))

        targets[robot.id] = (tx, ty)

    return targets


def assign_targets_to_robots(robots, targets):
    """Присваивает каждому роботу его целевую точку"""
    for robot in robots:
        if robot.id in targets:
            robot.set_target(targets[robot.id][0], targets[robot.id][1])
        else:
            robot.set_target(None, None)  # если цели нет (но по логике должна быть)


def check_all_collisions(robots):
    """
    Проверяет коллизии между всеми парами роботов.
    Использует квадраты расстояний для ускорения.
    Возвращает True, если хотя бы одна коллизия обнаружена.
    """
    # Сбросить флаги
    for robot in robots:
        robot.has_collision = False

    n = len(robots)
    collision_detected = False

    for i in range(n):
        for j in range(i + 1, n):
            if robots[i].check_collision_with(robots[j]):
                robots[i].has_collision = True
                robots[j].has_collision = True
                collision_detected = True

    return collision_detected


def check_all_finished(robots):
    """Проверяет для всех роботов, достигли ли они финиша.
    Возвращает True, если все роботы финишировали.
    """
    all_finished = True
    for robot in robots:
        robot.check_finish()
        if not robot.finished:
            all_finished = False
    return all_finished


def main():
    robots = get_robots()
    targets = get_target_coordinates(robots)
    assign_targets_to_robots(robots, targets)

    print("Целевые точки:")
    for robot in robots:
        print(f"Робот {robot.id}: ({robot.target_x}, {robot.target_y})")

    # Проверка коллизий между роботами (на начальных позициях)
    print("\nПроверка коллизий на начальных позициях:")
    if check_all_collisions(robots):
        print("Обнаружены коллизии:")
        for r in robots:
            if r.has_collision:
                print(f"Робот {r.id} в коллизии (координаты: ({r.x}, {r.y}))")
    else:
        print("Коллизий не обнаружено")

    # Проверка, достигли ли роботы финиша
    print("\nПроверка достижения финиша:")
    check_all_finished(robots)
    for robot in robots:
        status = "финишировал" if robot.finished else "в пути"
        print(f"Робот {robot.id}: {status}")


if __name__ == "__main__":
    main()
