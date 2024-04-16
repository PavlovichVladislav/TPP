from collections import defaultdict
import matplotlib.pyplot as plt

# Функция для подсчёта количества турбин
# каждого типа. Она нужна, т.к. изначально
# я возвращаю расходные характеристики с дублированием для турбин.
# В результате у нас массив с уникальными коллекциями, у которых
# Добавляется поле count
def calc_turbines(flow_chars):
    # Инициализация коллекции stock_turbines
    stock_turbines = defaultdict(int)

    # Подсчет количества турбин с различными марками
    for turbine in flow_chars:
        mark = turbine['mark']
        stock_turbines[mark] += 1

    # Добавление поля count
    for turbine in flow_chars:
        mark = turbine['mark']
        turbine['count'] = stock_turbines[mark]

    # Удаление дубликатов из исходного массива turbine_hops
    unique_turbines = []
    seen_marks = set()
    for turbine in flow_chars:
        mark = turbine['mark']
        if mark not in seen_marks:
            unique_turbines.append(turbine)
            seen_marks.add(mark)

    return unique_turbines

# Если турбин >=2, то её расходная харакетристика
# Умножается на кол-во турбин в парке
def transform_same_type_turbines(flow_chars):
    result = []

    # Перебираем все расходные характеристики
    # Умножаем x и y у каждой точки на кол-во турбин этого типа
    for item in flow_chars:
        count = item['count']
        transformed_item = item.copy()

        # Умножение координат каждой точки на count
        start_x, start_y = item['flow_char']['start']
        transformed_item['flow_char']['start'] = (start_x * count, start_y * count)

        points = item['flow_char']['points']
        transformed_points = [(x * count, y * count) for x, y in points]
        transformed_item['flow_char']['points'] = transformed_points

        end_x, end_y = item['flow_char']['end']
        transformed_item['flow_char']['end'] = (end_x * count, end_y * count)

        result.append(transformed_item)

    return result

# Расчитывает дельта
# Которое нужно для параллельного переноса
def delta(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    return delta_x, delta_y

def sum_flow_char(component1, component2):
    # Определение flow_char1 и flow_char2
    if len(component1['points']) <= len(component2['points']):
        flow_char1 = component1
        flow_char2 = component2
    else:
        flow_char1 = component2
        flow_char2 = component1

    # Инициализация sum_flow_char
    sum_flow_char = {
        'start': (flow_char1['start'][0] + flow_char2['start'][0],
                  flow_char1['start'][1] + flow_char2['start'][1]),
        'points': [],
        'end': ()
    }

    # Суммирование точек
    for i in range(len(flow_char1['points'])):
        sum_point = (flow_char1['points'][i][0] + flow_char2['points'][i][0],
                     flow_char1['points'][i][1] + flow_char2['points'][i][1])
        sum_flow_char['points'].append(sum_point)

    # Обработка внешнего условия
    if len(flow_char1['points']) == len(flow_char2['points']):
        # Вычисление тангенсов
        tg1 = (flow_char1['end'][1] - flow_char1['points'][-1][1]) / (
                    flow_char1['end'][0] - flow_char1['points'][-1][0])
        tg2 = (flow_char2['end'][1] - flow_char2['points'][-1][1]) / (
                    flow_char2['end'][0] - flow_char2['points'][-1][0])

        if tg1 < tg2:
            next_point = (sum_flow_char['points'][-1][0] + (flow_char1['end'][0] - flow_char1['points'][-1][0]),
                          sum_flow_char['points'][-1][1] + (flow_char1['end'][1] - flow_char1['points'][-1][1]))
            sum_flow_char['points'].append(next_point)
            sum_flow_char['end'] = (
            sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0]),
            sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1]))
        else:
            next_point = (sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0]),
                          sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1]))
            sum_flow_char['points'].append(next_point)
            sum_flow_char['end'] = (
            sum_flow_char['points'][-1][0] + (flow_char1['end'][0] - flow_char1['points'][-1][0]),
            sum_flow_char['points'][-1][1] + (flow_char1['end'][1] - flow_char1['points'][-1][1]))
    else:
        # Добавление следующей точки в sum_flow_char
        sum_flow_char['points'].append((flow_char1['end'][0] + flow_char2['points'][len(flow_char1['points'])][0],
                                        flow_char1['end'][1] + flow_char2['points'][len(flow_char1['points'])][1]))

        # Если точек в flow_char2 больше, чем в flow_char1 более чем на одну
        # т.е. на две и более
        if len(flow_char1['points']) + 1 < len(flow_char2['points']):
            # Начинаем перебор с +2 точек, т.к. +1 - ую мы уже прибавили к последней точке
            for i in range(len(flow_char1['points']) + 2, len(flow_char2['points'])):
                # считаем делта x и дельта y для оставшихся отрезков в flow_char2 и переносим их в сумму
                delta_x, delta_y = delta(flow_char2['points'][i], flow_char2['points'][i - 1])
                next_point = (sum_flow_char['points'][-1][0] + delta_x, sum_flow_char['points'][-1][1] + delta_y)
                sum_flow_char['points'].append(next_point)

            sum_flow_char['end'] = (
            sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0]),
            sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1]))

        # Если точек больше всего на одну,
        # то просто переносим оставшийся отрезок
        else:
            sum_flow_char['end'] = (
            sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0]),
            sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1]))

    return sum_flow_char

def plot_flow(flow_data):
    # Извлечение координат точек
    start_x, start_y = flow_data['start']
    end_x, end_y = flow_data['end']
    points = flow_data.get('points', [])
    points_x, points_y = zip(*points) if points else ([], [])

    # Создание графика
    plt.figure(figsize=(8, 6))

    # Нанесение точек
    plt.plot(start_x, start_y, 'bo', label='Start')
    plt.plot(end_x, end_y, 'ro', label='End')

    # Соединение точек линиями
    plt.plot([start_x] + list(points_x) + [end_x], [start_y] + list(points_y) + [end_y], 'k-')

    # Если есть точки, нанести их
    if points:
        plt.plot(points_x, points_y, 'go', label='Points')

    # Добавление легенды
    plt.legend()

    # Настройка осей
    plt.xlabel('N, МВТ/Ч')
    plt.ylabel('D, т/ч')
    plt.title('Расходная характеристика станции')

    # Отображение графика
    plt.grid(True)
    plt.show()

# Функция апроксимирует начальный отрезок расходной
# характеристики до 0
def update_flow_char(flow_char):
    # Извлекаем координаты начальной точки
    # Вторая точка по уолмчанию считается последней, если
    # Же в массиве points есть точки, то второй будет 0 - я точка
    # из points
    start_x, start_y = flow_char['start']
    point_x, point_y = flow_char['end']

    if (len(flow_char['points']) > 0):
        point_x, point_y = flow_char['points'][0]

    # Вычисляем уравнение прямой через начальную точку и первую точку из списка points
    # y = mx + c, где m - наклон, c - точка пересечения с осью y
    m = (point_y - start_y) / (point_x - start_x)
    c = start_y - m * start_x

    # Вычисляем значение y при x = 0
    new_start_y = m * 0 + c

    # Обновляем координаты начальной точки во входном аргументе
    flow_char['start'] = (0, new_start_y)

    return flow_char

# Расчёт расходной характеристики для станции
# Это переходное звено для расчёта ХОП станции
def calc_flow_char(flow_chars):
    print(flow_chars)
    # Считаем кол-во турбин каждого типа и удаляем дубликаты
    transformed_flow_chars = calc_turbines(flow_chars)
    # Умножаем точки на графике на кол-во турбин
    transformed_flow_chars = transform_same_type_turbines(transformed_flow_chars)

    # Если у нас всего 1 различная турбина, то её расходную характеристику
    # и возвращаем
    if (len(transformed_flow_chars) == 1):
        # апроксимируем до 0
        flow_char = update_flow_char(transformed_flow_chars[0]['flow_char'])

        plot_flow(transformed_flow_chars[0]['flow_char'])

        return flow_char

    # результат
    flow_char = sum_flow_char(transformed_flow_chars[0]['flow_char'], transformed_flow_chars[1]['flow_char'])

    for i in range(2, len(transformed_flow_chars)):
        flow_char = sum_flow_char(flow_char, transformed_flow_chars[i]['flow_char'])

    # апроксимируем до 0
    flow_char = update_flow_char(flow_char)

    plot_flow(flow_char)

    return flow_char
