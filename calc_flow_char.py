from collections import defaultdict

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
def calculate_deltas(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    return delta_x, delta_y


def sum_flow_char(flow_char1, flow_char2):
    sum_flow_char = {}

    # Создание рабочих переменных flow_char1 и flow_char2
    print('flow', flow_char1)
    print('flow', flow_char2)
    # Суммирование точек start
    sum_start = (flow_char1['start'][0] + flow_char2['start'][0], flow_char1['start'][1] + flow_char2['start'][1])
    sum_flow_char['start'] = sum_start

    # Суммирование точек points
    for i in range(len(flow_char1['points'])):
        sum_point = (flow_char1['points'][i][0] + flow_char2['points'][i][0],
                     flow_char1['points'][i][1] + flow_char2['points'][i][1])
        sum_flow_char['points'] = [sum_point]

    # Вычисление тангенсов
    tg1 = (flow_char1['end'][1] - flow_char1['points'][-1][1]) / (flow_char1['end'][0] - flow_char1['points'][-1][0])
    tg2 = (flow_char2['end'][1] - flow_char2['points'][-1][1]) / (flow_char2['end'][0] - flow_char2['points'][-1][0])

    # Вычисление следующей точки в sum_flow_char
    if tg1 < tg2:
        next_point_x = sum_flow_char['points'][-1][0] + (flow_char1['end'][0] - flow_char1['points'][-1][0])
        next_point_y = sum_flow_char['points'][-1][1] + (flow_char1['end'][1] - flow_char1['points'][-1][1])
        sum_flow_char['points'].append((next_point_x, next_point_y))

        last_point_x = sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0])
        last_point_y = sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1])
        sum_flow_char['points'].append((last_point_x, last_point_y))
    elif tg1 > tg2:
        next_point_x = sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0])
        next_point_y = sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1])
        sum_flow_char['points'].append((next_point_x, next_point_y))

        next_point_x = sum_flow_char['points'][-1][0] + (flow_char1['end'][0] - flow_char1['points'][-1][0])
        next_point_y = sum_flow_char['points'][-1][1] + (flow_char1['end'][1] - flow_char1['points'][-1][1])
        sum_flow_char['points'].append((next_point_x, next_point_y))

    # Если размерности flow_char1.points и flow_char2.points не равны
    else:
        if len(flow_char1['points']) + 1 < len(flow_char2['points']):
            for i in range(len(flow_char1['points']) + 2, len(flow_char2['points'])):
                delta_x, delta_y = calculate_deltas(flow_char2['points'][i], flow_char2['points'][i - 1])
                next_point_x = sum_flow_char['points'][-1][0] + delta_x
                next_point_y = sum_flow_char['points'][-1][1] + delta_y
                sum_flow_char['points'].append((next_point_x, next_point_y))
        else:
            next_point_x = sum_flow_char['points'][-1][0] + \
                           calculate_deltas(flow_char2['end'], flow_char2['points'][-1])[0]
            next_point_y = sum_flow_char['points'][-1][1] + \
                           calculate_deltas(flow_char2['end'], flow_char2['points'][-1])[1]
            sum_flow_char['points'].append((next_point_x, next_point_y))

    return sum_flow_char

# Расчёт расходной характеристики для станции
# Это переходное звено для расчёта ХОП станции
def calc_flow_char(flow_chars):
    # Считаем кол-во турбин каждого типа и удаляем дубликаты
    transformed_flow_chars = calc_turbines(flow_chars)
    # Умножаем точки на графике на кол-во турбин
    transformed_flow_chars = transform_same_type_turbines(transformed_flow_chars)
    # Сортируем по возрастанию количества точек излома
    # to-do: проверить работу сортировки
    sorted_flow_chars = sorted(transformed_flow_chars, key=lambda x: len(x['flow_char']['points']))

    # результат
    flow_char = sum_flow_char(sorted_flow_chars[0]['flow_char'], sorted_flow_chars[1]['flow_char'])

    for i in range(2, len(sorted_flow_chars)):
        flow_char = sum_flow_char(flow_char, sorted_flow_chars[i]['flow_char'])

    print(flow_char)

    return
