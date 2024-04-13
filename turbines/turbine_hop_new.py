import numpy as np
import math

from utils.get_work_diagram import get_work_diagram

# центр графика, пока что хардкоженый
middle_point = 70

# Ф-я, которая вычисляет Евклидово расстояние между двумя точками
def calc_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# функция, которая назходит ближайшую точку из структуры line
# к точке, которую мы передаём вторым аргументом
# [midle_point] - точка, относительно которой будет искаться ближайшая
def find_nearest_point(line, middle_point):
    # собираем все точки в один массив
    new_points = [line['start']] + line['points'] + [line['end']]
    # инициализируем ближайшую точку
    nearest_point = None
    #
    min_distance = float('inf')

    for point in new_points:
        dist = abs(point[0] - middle_point)
        if dist < min_distance:
            min_distance = dist
            nearest_point = point

    return nearest_point

# новая ломаная строится между двух других ломаных
# первую из них мы находим функцией find_nearest_line
# вторую мы находим с помощью написанной ниже функции
# мы находим вторую ломаную, т.к. нам нужна пропорция в расстояниях
def find_second_closest_line(entrance_collection_point, found_line, lines):
    if entrance_collection_point > found_line['collection_point']:
        filtered_lines = [line for line in lines if line['collection_point'] > found_line['collection_point']]
        closest_line = min(filtered_lines, key=lambda x: x['collection_point'] - found_line['collection_point'],
                           default=None)
    elif entrance_collection_point < found_line['collection_point']:
        filtered_lines = [line for line in lines if line['collection_point'] < found_line['collection_point']]
        closest_line = min(filtered_lines, key=lambda x: found_line['collection_point'] - x['collection_point'],
                           default=None)
    else:
        return None  # здесь стоит обработать исключение в будущем

    return closest_line


# to-do проблемно вычисляется, есть стандартный пакет на python
# функция, которая вычисляет расстояние от точки до прямой
# start, end - точки прямой
# point - точка, от которой считаем расстояние
def distance_to_line(point, segment):
    # Функция вычисляет расстояние от точки до отрезка (start, end)
    # Преобразуем координаты точки и отрезка в массивы NumPy
    point = np.array(point)
    segment = np.array(segment)

    # Вычисляем вектор от начала отрезка до точки
    v = point - segment[0]

    # Вычисляем нормированный вектор направления отрезка
    direction = segment[1] - segment[0]
    direction_normalized = direction / np.linalg.norm(direction)

    # Вычисляем проекцию вектора v на направление отрезка
    projection = np.dot(v, direction_normalized)

    # Расстояние от точки до отрезка - это длина вектора v минус проекция
    distance = np.linalg.norm(v) - projection

    # Если проекция находится внутри отрезка, расстояние остается прежним,
    # в противном случае, берем минимальное расстояние до концов отрезка
    if 0 <= projection <= np.linalg.norm(direction):
        return distance
    else:
        return min(np.linalg.norm(point - segment[0]), np.linalg.norm(point - segment[1]))


# Ф-я, для поиска ближайшей ломаной, относительно которой будет построение новой
def find_nearest_line(lines, entrance_collection_point):
    # инициализируем минимальную разность между точками забора
    min_collection_point_diff = float('inf')
    found_line = None

    # в цикле находим прямую с ближайшей к введённой в программу
    # точкой забора
    # по этой ломаной мы бдуем строить новую
    for line in lines:
        collection_point = line['collection_point']
        # collection_point_diff это разница между точками забора
        collection_point_diff = abs(collection_point - entrance_collection_point)

        if collection_point_diff < min_collection_point_diff:
            min_collection_point_diff = collection_point_diff
            found_line = line

    # у ломаной, относительно которой мы будем строить нашу новую ломаную ОПРТ
    # нужно найти точку излома, которая будет ближе всего лежать к центру
    nearest_point_to_midle = find_nearest_point(found_line, middle_point)
    # находим вторую прямую, наша новая ломаная будет лежать между found_line и second_line
    # вторая прямая нужна, чтоб можно было вычислить расстояние, на котором будет лежать наша новая ломаная
    second_line = find_second_closest_line(entrance_collection_point, found_line, lines)

    # найдём расстояние от nearest_point_to_midle до второй ломаной
    # складываем все её точки в один массив
    points = [second_line['start']] + second_line['points'] + [second_line['end']]
    min_dist = float('inf')

    # перебираем последовательно все прямые ломаной и вычисляем расстояние
    for i in range(len(points) - 1):
        dist = distance_to_line(nearest_point_to_midle, [points[i], points[i + 1]])

        if dist < min_dist:
            min_dist = dist

    # мы нашли полное расстояние между ломаными, между которыми будет лежать наша новая ломаная
    # теперь нужно взять это расстояния пропорционально collection_point этих двух прямых

    result_dist = min_dist * (min_collection_point_diff
                              / (abs(found_line['collection_point'] - second_line['collection_point'])))

    return found_line, min_collection_point_diff


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
                    intersection_x = round((b_contour - b) / (k - k_contour), 4)
                    intersection_y = round((k * intersection_x + b), 4)

                    # Из - за округления число не попадает в отрезок, корректируем
                    if (abs(intersection_y - 277.3) < 1):
                        intersection_y = 277.3

                    # Проверка, лежит ли точка внутри отрезка контура
                    if (x1 <= intersection_x <= x2 or x2 <= intersection_x <= x1) and \
                            ((y1 - 0.5) <= intersection_y <= (y2 + 0.5) or (y2 -0.5) <= intersection_y <= y1 + 0.5):
                        intersections.append((intersection_x, intersection_y))

        if not intersections:
            return None

        # Находим ближайшую точку к целевой точке
        closest_intersection = min(intersections, key=lambda p: calc_distance_between_points(p, target_point))

        return closest_intersection

    if (len(points) == 0):
        # Находим точку пересечения с контуром для start
        start_intersection = find_intersection(start, end, start)

        # Находим точку пересечения с контуром для end
        end_intersection = find_intersection(start, end, end)

        return start_intersection, end_intersection

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


# Изначально мы строим новую расходную характеристику(ломаную) параллельным переносом,
# т.е. она может не задевать контур или выходить за него.
# Чтобы получить окончательную расходную характеристику,
# нужно продлить её начальный и конечный отрезок до пересечения с ограничивающим контуром.
def adjust_line_to_contour(new_line, contour):
    start_intersection, end_intersection = find_intersects_with_contour(new_line, contour)
    new_line['start'] = start_intersection
    new_line['end'] = end_intersection

    return new_line

# Расчёт тангенсов между осью x и отрезками расходной характеристики(ломаная)
# Значения ХОП на интервалах, то тангенс отрезка с этого интервала
def calculate_tangents(line):
    tangents = []
    # последовательно складываем все точки ломаной в массив для
    # удобного перебора
    points = [line['start']] + line['points'] + [line['end']]

    for i in range(len(points) - 1):
        # Первая точка(левее, чем 2)
        x, y = points[i]
        # Вторая точка(правее и выше, чем 1)
        x_next, y_next = points[i + 1]
        # Точка образующая с первыми двумя треугольник
        new_point = (x_next, y)

        # Длина противолежащего катета
        len1 = math.sqrt((x_next - new_point[0]) ** 2 + (y_next - new_point[1]) ** 2)
        # Длина прилежащего катета
        len2 = math.sqrt((x - new_point[0]) ** 2 + (y - new_point[1]) ** 2)
        # Находим тангенс угла и добавляем его в массив
        tangent = round(len1 / len2, 3)

        tangents.append({'interval': [x, x_next], 'tangent': tangent})

    return tangents

# Расчёт хоп отдельной турбины
# turbine_mark - марка турбины для диаграммы режимов работ
# entrance_collection_point - отбор пара
def calc_turbine_hop(turbine_mark, entrance_collection_point):
    # По марке турбины определяем диаграмму режимов работ.
    # А именно ограничивающий контур и линии внутри контура
    contour, lines = get_work_diagram(turbine_mark)

    # находим ломаную в диаграмме режимов работ, относительно которой
    # будет построение расходной характеристики нашей турбины
    found_line, dist = find_nearest_line(lines, entrance_collection_point)

    # получаем расходную характеристику турбины(она неполная, т.к. строилась прааллельным переносом)
    new_line = create_new_line(found_line, entrance_collection_point, dist)
    # корректируем ломаную по контуру, т.е. продливаем концы до пересечения с контуром
    new_line = adjust_line_to_contour(new_line, contour)

    # тангенсы ломаной к оси x для построения ХОП
    result_tangents = calculate_tangents(new_line)

    return {'mark': turbine_mark, 'hop': result_tangents, 'flow_char': new_line}