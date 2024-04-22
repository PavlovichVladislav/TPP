from utils.bestModel import find_best_fit_model
from utils.calc_boiler_hop_model import calc_boiler_hop_model
from utils.regression_model import model


def find_correspond_Q(N, flow_char):
    print(N)
    print(flow_char)

    points = [flow_char['start']] + flow_char['points'] + [flow_char['end']]

    # Находим точки между которыми находится N
    point1_index = None
    point2_index = None
    for i in range(len(points) - 1):
        if points[i][0] <= N <= points[i + 1][0]:
            point1_index = i
            point2_index = i + 1
            break

    # Проверяем, что удалось найти две точки
    if point1_index is None or point2_index is None:
        raise ValueError("Cannot find two points for the given N")

    # Извлекаем координаты точек
    x1, y1 = points[point1_index]
    x2, y2 = points[point2_index]

    # Вычисляем коэффициенты прямой
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1

    # Вычисляем b_boilers_shop
    b_boilers_shop = k * N + b

    return b_boilers_shop

def calc_station_hop(boilers_hop, turbines_hop, flow_char):
    b = []
    N = []

    # teta1, teta2, teta3, teta4 = calc_boiler_hop_model(boilers_hop, True, True)
    model = find_best_fit_model(boilers_hop['Q'], boilers_hop['b'], 1)


    for turbine in turbines_hop:
        interval = turbine['interval']
        tangent = turbine['tangent']

        # Взяли первую точку с интервала
        N.append(interval[0])
        # Нашли по N соответствующую точку Q с помощью расходной характеристики
        Q = find_correspond_Q(interval[0], flow_char)
        # Вычисляем соответствующую точку на ХОП котельного цеха
        # b_boiler_value = model(Q, teta1, teta2, teta3, teta4)
        b_boiler_value = model(Q)

        # Добавили произведене в результат
        b.append(b_boiler_value * tangent)

        # Обработка второй точки интервала
        N.append(interval[1])
        # Нашли по N соответствующую точку Q с помощью расходной характеристики
        Q = find_correspond_Q(interval[1], flow_char)
        # b_boiler_value = model(Q, teta1, teta2, teta3, teta4)
        b_boiler_value = model(Q)
        # Добавили произведене в результат
        b.append(b_boiler_value * tangent)

    return {'b': b, 'N': N}
