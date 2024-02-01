import matplotlib.pyplot as plt
import numpy as np
import math

# Ф-я, которая вычисляет Евклидово расстояние между двумя точками
def calc_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Ф-я, для поиска ближайшей ломаной, относительно которой будет построение новой
def find_nearest_line(lines, entrance_collection_point):
    min_distance = float('inf')
    found_line = None

    for line in lines:
        collection_point = line['collection_point']
        dist = abs(collection_point - entrance_collection_point)

        if dist < min_distance:
            min_distance = dist
            found_line = line

    return found_line, min_distance

# Ф-я для поиска пересечений ломаной и контура
# Необходимо это, т.к. новую ломаную мы изначально получаем параллельным переносом,
# но эта новая ломаная может не пересечь контур или вовсе выйти за него, поэтому необходимо
# продлить её крайние отрезки и найти точки пересечения с контуром
# Аргументы:
# line - ломаная линия, пересечения которой будут искаться
# contour - массив точек контура
# Возвращаемые значения
# start_intersection - начальная точка пересечения(левая точка)
# end_intersection - конечная точка пересечения(правая точка)
def find_intersects_with_contour(line, contour):
    start = line['start']
    end = line['end']
    points = line['points']

    # Функция для вычисления расстояния между двумя точками
    def calc_distance_between_points(point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    # Функция которая ищет точки пересечения прямой, образованной двумя точками и
    # выбирает ту из них, которая ближе к target_point. Близость к target_point нужна
    # т.к. мы перебираем все прямые, которые образованы отрезками контура и ищем пересечения
    # с отрезком ломаной. Таких точек может быть множество, но нам нужна та, которая ближе всего лежит
    # к точке начала/конца отрезка, пересечения с которым мы ищем
    # Аргументы
    # point_start - начало отрезка
    # point_end - конец отрезка
    # target_point - точка относительно которой ищется результат
    def find_intersection(point_start, point_end, target_point):
        # to-do Обработка случая вертикальности отрезка ломаной. Вроде как нет необходимости,
        # но код оставил
        # -----------------
        # if point_end[0] - point_start[0] == 0:
        #     # Если отрезок вертикальный, то уравнение прямой x = const
        #     intersection_x = point_start[0]
        #     intersection_y = target_point[1]  # Произвольное значение y на отрезке
        #
        #     # Проверка, лежит ли точка внутри отрезка контура
        #     if (point_start[1] <= intersection_y <= point_end[1] or
        #             point_end[1] <= intersection_y <= point_start[1]):
        #         return (intersection_x, intersection_y)
        #     else:
        #         return None

        # Уравнение прямой по двум точкам
        k = (point_end[1] - point_start[1]) / (point_end[0] - point_start[0])
        b = point_start[1] - k * point_start[0]

        # массив для точек пересечения
        intersections = []

        # перебор всех возможных прямых, образованных отрезками контура
        for i in range(len(contour)):
            x1, y1 = contour[i]
            x2, y2 = contour[(i + 1) % len(contour)]

            # Уравнение прямой по двум точкам контура
            if x2 - x1 == 0:
                # Обработка случая вертикального отрезка, уравнение прямой x = const
                # т.к. x = const, то точка пересечения по x тривиальна
                intersection_x = x1
                intersection_y = k * intersection_x + b

                # Проверка, лежит ли точка внутри отрезка контура, а не только на прямой
                # Т.е. проверка на то, что прямая образованная ломаной реально пересекает контур,
                # а не продолжение отрезков, образующих контур
                if (y1 <= intersection_y <= y2 or y2 <= intersection_y <= y1):
                    intersections.append((intersection_x, intersection_y))
            else:
                # обработка случая не вертикального отрезка

                k_contour = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')  # Обработка вертикального отрезка
                b_contour = y1 - k_contour * x1

                # Решение системы уравнений для поиска точки пересечения
                if k - k_contour != 0:
                    intersection_x = (b_contour - b) / (k - k_contour)
                    intersection_y = k * intersection_x + b

                    # Проверка, лежит ли точка внутри отрезка контура
                    if (x1 <= intersection_x <= x2 or x2 <= intersection_x <= x1) and \
                            (y1 <= intersection_y <= y2 or y2 <= intersection_y <= y1):
                        intersections.append((intersection_x, intersection_y))

        if not intersections:
            return None

        # Находим ближайшую точку к целевой точке
        closest_intersection = min(intersections, key=lambda p: calc_distance_between_points(p, target_point))

        return closest_intersection

    # Находим точку пересечения с контуром для start
    start_intersection = find_intersection(start, points[0], start)

    # Находим точку пересечения с контуром для end
    end_intersection = find_intersection(points[-1], end, end)

    return start_intersection, end_intersection


def create_new_line(found_line, entrance_collection_point, dist):
    new_line = {
        'start': (found_line['start'][0], found_line['start'][1] + dist) if entrance_collection_point > found_line[
            'collection_point'] else (found_line['start'][0], found_line['start'][1] - dist),
        'points': [(point[0], point[1] + dist) if entrance_collection_point > found_line['collection_point'] else (
        point[0], point[1] - dist) for point in found_line['points']],
        'end': (found_line['end'][0], found_line['end'][1] + dist) if entrance_collection_point > found_line[
            'collection_point'] else (found_line['end'][0], found_line['end'][1] - dist)
    }
    return new_line

# изначально мы строим новую ломаную параллельным переносом,
# чтобы получить окончательную ломаную, нужно продлить её начальный и конечный отрезок до пересечения с контуром
def adjust_line_to_contour(new_line, contour):
    start_intersection, end_intersection = find_intersects_with_contour(new_line, contour)
    new_line['start'] = start_intersection
    new_line['end'] = end_intersection

    return new_line


def plot_lines(lines, contour, entrance_collection_point):
    plt.plot(*zip(*contour + [contour[0]]), marker='o', label='Contour', color='k')

    for line in lines:
        label = 0
        color = ''

        # Если точка из lines, то у неё есть collection_point
        # Иначе это точка нашей новой прямой, которая приходит на вход программы
        if ("collection_point" in line):
            label = line["collection_point"]
            color = 'orange'
        else:
            color = 'magenta'
            label = entrance_collection_point

        plt.plot(*zip(line['start'], *line['points'], line['end']), marker='o',
                 label=label, color=color)

    plt.legend()
    plt.gca().set_aspect(0.25)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

def calculate_tangents(line, transform_to_gkal):
    tangents = []
    # последовательно складываем все точки ломаной в массив для
    # удобного перебора
    points = [line['start']] + line['points'] + [line['end']]

    # при наличии фалага переводим из т/ч в гкал/ч
    if (transform_to_gkal):
        points = [(x, y * 0.59) for x, y in points]

    for i in range(len(points) - 1):
        # Первая точка
        x, y = points[i]
        # Вторая точка
        x_next, y_next = points[i + 1]
        # Точка образующая с первыми двумя треугольник
        new_point = (x_next, y)

        # Длина противолежащего катета
        len1 = math.sqrt((x_next - new_point[0]) ** 2 + (y_next - new_point[1]) ** 2)
        # Длина прилежащего катета
        len2 = math.sqrt((x - new_point[0]) ** 2 + (y - new_point[1]) ** 2)

        # Находим тангенс угла и добавляем его в массив
        tangent = len1 / len2
        tangents.append({'interval': [x, x_next], 'tangent': tangent})

    return tangents

# строим ХОП турбны по тангенсам для интервалов
# data - словарь из двух полей interval tangent
# построение происходит путём отложения прямых y = tangent
# для соответствующего интервала
def plot_hop(data):
    # инициализируем массивы для x и y
    x_values = []
    y_values = []

    # перебираем все словари из входных данных
    # по сути берём интервалы и их значения тангенсов
    # -----------------------------------------------
    # по сути чтобы построить график нужно одинаковое кол-во x и y
    # т.к. это координаты
    # в цикле мы кладём в x начало и конец интервала
    # а в y кладём соотвтетсвующих два значения тангенса для начала и конца интервала
    for entry in data:
        interval = entry['interval']
        tangent = entry['tangent']
        x_values.extend(interval)
        y_values.extend([tangent, tangent])

    plt.plot(x_values, y_values, marker='o')
    plt.xlabel('N, мвт')
    plt.ylabel('Гкал / мвт/ч')
    plt.title('хоп турбины')
    plt.show()

def main():
    contour = [(110, 470), (78.5, 470), (72, 444), (50, 296), (37.5, 226), (30, 174), (30, 132), (60, 220), (94, 336)]

    lines = [
        {'collection_point': 120, 'start': (61.5, 372), 'points': [(79.5, 427)], 'end': (89, 470)},
        {'collection_point': 90, 'start': (50.75, 300), 'points': [(62, 336), (85.5, 410)], 'end': (100, 470)},
        {'collection_point': 60, 'start': (37.5, 228), 'points': [(55, 284), (72, 346), (100, 426)], 'end': (108.5, 470)},
        {'collection_point': 30, 'start': (30, 146), 'points': [(80, 318)], 'end': (102, 403)}
    ]

    entrance_collection_point = int(input('Введите entrance_collection_point: '))
    # находим ломаную, относительно которой будет построение новой
    found_line, dist = find_nearest_line(lines, entrance_collection_point)
    # получаем новую ломаную
    new_line = create_new_line(found_line, entrance_collection_point, dist)
    # корректируем ломаную по контуру
    new_line = adjust_line_to_contour(new_line, contour)
    lines.append(new_line)

    # тангенсы ломаной к оси x для построения ХОП
    result_tangents = calculate_tangents(new_line, True)
    # строим диаграмму работ
    plot_lines(lines, contour, entrance_collection_point)
    # строим хоп турбины
    plot_hop(result_tangents)
if __name__ == "__main__":
    main()