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


# def sum_flow_char(flow_char1, flow_char2):
#     sum_flow_char = {}
#
#     # Создание рабочих переменных flow_char1 и flow_char2
#     print('flow', flow_char1)
#     print('flow', flow_char2)
#     # Суммирование точек start
#     sum_start = (flow_char1['start'][0] + flow_char2['start'][0], flow_char1['start'][1] + flow_char2['start'][1])
#     sum_flow_char['start'] = sum_start
#
#     # Суммирование точек points
#     for i in range(len(flow_char1['points'])):
#         sum_point = (flow_char1['points'][i][0] + flow_char2['points'][i][0],
#                      flow_char1['points'][i][1] + flow_char2['points'][i][1])
#         sum_flow_char['points'] = [sum_point]
#
#     # Вычисление тангенсов
#     tg1 = (flow_char1['end'][1] - flow_char1['points'][-1][1]) / (flow_char1['end'][0] - flow_char1['points'][-1][0])
#     tg2 = (flow_char2['end'][1] - flow_char2['points'][-1][1]) / (flow_char2['end'][0] - flow_char2['points'][-1][0])
#
#     # Вычисление следующей точки в sum_flow_char
#     if tg1 < tg2:
#         next_point_x = sum_flow_char['points'][-1][0] + (flow_char1['end'][0] - flow_char1['points'][-1][0])
#         next_point_y = sum_flow_char['points'][-1][1] + (flow_char1['end'][1] - flow_char1['points'][-1][1])
#         sum_flow_char['points'].append((next_point_x, next_point_y))
#
#         last_point_x = sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0])
#         last_point_y = sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1])
#         sum_flow_char['points'].append((last_point_x, last_point_y))
#     elif tg1 > tg2:
#         next_point_x = sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0])
#         next_point_y = sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1])
#         sum_flow_char['points'].append((next_point_x, next_point_y))
#
#         next_point_x = sum_flow_char['points'][-1][0] + (flow_char1['end'][0] - flow_char1['points'][-1][0])
#         next_point_y = sum_flow_char['points'][-1][1] + (flow_char1['end'][1] - flow_char1['points'][-1][1])
#         sum_flow_char['points'].append((next_point_x, next_point_y))
#
#     # Если размерности flow_char1.points и flow_char2.points не равны
#     else:
#         if len(flow_char1['points']) + 1 < len(flow_char2['points']):
#             for i in range(len(flow_char1['points']) + 2, len(flow_char2['points'])):
#                 delta_x, delta_y = calculate_deltas(flow_char2['points'][i], flow_char2['points'][i - 1])
#                 next_point_x = sum_flow_char['points'][-1][0] + delta_x
#                 next_point_y = sum_flow_char['points'][-1][1] + delta_y
#                 sum_flow_char['points'].append((next_point_x, next_point_y))
#         else:
#             next_point_x = sum_flow_char['points'][-1][0] + \
#                            calculate_deltas(flow_char2['end'], flow_char2['points'][-1])[0]
#             next_point_y = sum_flow_char['points'][-1][1] + \
#                            calculate_deltas(flow_char2['end'], flow_char2['points'][-1])[1]
#             sum_flow_char['points'].append((next_point_x, next_point_y))
#
#     return sum_flow_char

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
        # Проверка условия размерности точек
        if len(flow_char1['points']) + 1 != len(flow_char2['points']):
            raise ValueError("Размерность точек неверна")

        # Добавление следующей точки в sum_flow_char
        sum_flow_char['points'].append((flow_char1['end'][0] + flow_char2['points'][len(flow_char1['points'])][0],
                                        flow_char1['end'][1] + flow_char2['points'][len(flow_char1['points'])][1]))

        if len(flow_char1['points']) + 1 < len(flow_char2['points']):
            for i in range(len(flow_char1['points']) + 2, len(flow_char2['points'])):
                delta_x, delta_y = delta(flow_char2['points'][i], flow_char2['points'][i - 1])
                next_point = (sum_flow_char['points'][-1][0] + delta_x, sum_flow_char['points'][-1][1] + delta_y)
                sum_flow_char['points'].append(next_point)

            sum_flow_char['end'] = (
            sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0]),
            sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1]))
        else:
            sum_flow_char['end'] = (
            sum_flow_char['points'][-1][0] + (flow_char2['end'][0] - flow_char2['points'][-1][0]),
            sum_flow_char['points'][-1][1] + (flow_char2['end'][1] - flow_char2['points'][-1][1]))

    return sum_flow_char

def plot_flow(flow_data):
    # Извлечение координат точек
    start_x, start_y = flow_data['start']
    end_x, end_y = flow_data['end']
    points_x, points_y = zip(*flow_data['points'])

    # Создание графика
    plt.figure(figsize=(8, 6))

    # Нанесение точек
    plt.plot(start_x, start_y, 'bo', label='Start')
    plt.plot(end_x, end_y, 'ro', label='End')
    plt.plot(points_x, points_y, 'go', label='Points')

    # Соединение точек линиями
    plt.plot([start_x] + list(points_x) + [end_x], [start_y] + list(points_y) + [end_y], 'k-')

    # Добавление легенды
    plt.legend()

    # Настройка осей
    plt.xlabel('N, МВТ/Ч')
    plt.ylabel('D, т/ч')
    plt.title('Расходная характеристика')

    # Отображение графика
    plt.grid(True)
    plt.show()

# Расчёт расходной характеристики для станции
# Это переходное звено для расчёта ХОП станции
def calc_flow_char(flow_chars):
    # Считаем кол-во турбин каждого типа и удаляем дубликаты
    transformed_flow_chars = calc_turbines(flow_chars)
    # Умножаем точки на графике на кол-во турбин
    transformed_flow_chars = transform_same_type_turbines(transformed_flow_chars)

    # --------
    # deprecated

    # Сортируем по возрастанию количества точек излома
    # to-do: проверить работу сортировки
    # sorted_flow_chars = sorted(transformed_flow_chars, key=lambda x: len(x['flow_char']['points']))

    # --------

    # результат
    flow_char = sum_flow_char(transformed_flow_chars[0]['flow_char'], transformed_flow_chars[1]['flow_char'])

    for i in range(2, len(transformed_flow_chars)):
        flow_char = sum_flow_char(flow_char, transformed_flow_chars[i]['flow_char'])

    print(flow_char)
    plot_flow(flow_char)

    return
