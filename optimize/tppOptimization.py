import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def tppOptimize(MR, MC, demand):
    # Создаем transformed_MR
    transformed_MR = {'pg': [pg / 720 for pg in MR['pg']], 'mr': MR['mr']}

    # Создаем transformed_demand
    transformed_demand = {'pg': [pg / 720 for pg in demand['pg']], 'price': demand['price']}

    # Находим линейную модель для transformed_MR
    slope_mr, intercept_mr, _, _, _ = linregress(transformed_MR['pg'], transformed_MR['mr'])

    def model_mr(x):
        return slope_mr * x + intercept_mr

    # Находим линейную модель для transformed_demand
    slope_demand, intercept_demand, _, _, _ = linregress(transformed_demand['pg'], transformed_demand['price'])

    def model_demand(x):
        return slope_demand * x + intercept_demand

    # Инициализируем массивы new_Mr и new_demand_price
    new_Mr = []
    new_demand_price = []

    # Перебираем массив MC['N']
    for n in MC['N']:
        # Добавляем значения model_mr(MC['N'][i]) в new_Mr
        new_Mr.append(model_mr(n))
        # Добавляем значения model_demand(MC['N'][i]) в new_demand_price
        new_demand_price.append(model_demand(n))

    # Формируем коллекции new_MR и new_Demand
    new_MR = {'pg': MC['N'], 'mr': new_Mr}
    new_Demand = {'pg': MC['N'], 'price': new_demand_price}

    # Находим точку пересечения моделей MR и MC
    intersection_point = None
    for i in range(len(MC['N']) - 1):
        x1, y1 = MC['N'][i], MC['b'][i]
        x2, y2 = MC['N'][i + 1], MC['b'][i + 1]
        m_mc = (y2 - y1) / (x2 - x1)
        b_mc = y1 - m_mc * x1
        m_mr = slope_mr
        b_mr = intercept_mr
        # Проверяем пересечение отрезка с прямой model_mr
        x = (b_mr - b_mc) / (m_mc - m_mr)
        y = m_mr * x + b_mr
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            intersection_point = (x, y)
            break

    # Находим y_opt
    if intersection_point:
        x_opt = intersection_point[0]
        y_opt = model_demand(x_opt)
    else:
        x_opt = None
        y_opt = None

    # Вызываем функцию plot_graph
    plot_graph(new_MR, new_Demand, MC, intersection_point, x_opt, y_opt)

    return x_opt, y_opt, new_MR, new_Demand, MC


def plot_graph(new_MR, new_Demand, MC, intersection_point, x_opt, y_opt):
    plt.figure(figsize=(10, 6))

    # График new_MR
    plt.plot(new_MR['pg'], new_MR['mr'], label='Transformed MR', marker='o')

    # График new_Demand
    plt.plot(new_Demand['pg'], new_Demand['price'], label='Transformed Demand', marker='o')

    # График MC
    plt.plot(MC['N'], MC['b'], label='MC', marker='o')

    # Точка intersection_point
    if intersection_point:
        plt.plot(intersection_point[0], intersection_point[1], 'ro', label='Intersection Point')

    # Точка (x_opt, 0)
    if x_opt is not None:
        plt.plot(x_opt, 0, 'go', label='Optimal Quantity')

    # Точка (0, y_opt)
    if y_opt is not None:
        plt.plot(0, y_opt, 'bo', label='Optimal Price')

    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.title('MR, Demand, and MC Graph')
    plt.legend()
    plt.grid(True)
    plt.show()

MR = {
    'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100],
    'mr': [611.812, 456.245, 338.518, 252.676, 155.787, 53.821, 6.768, 3.923]}

MC = {'N': [23, 36, 45, 49.9, 56, 67.5, 89.5, 112, 126.4],
      'b': [17.623, 17.721, 17.725, 17.732, 24.585, 24.596, 24.614, 24.687, 24.796]}

demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100, 30200],
          'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614, 705.6303418, 703.3085408,
                    700.9926952]}

# x_opt, y_opt = tppOptimize(MR, MC, demand)
#
# print(x_opt, y_opt)
#
# import matplotlib.pyplot as plt
#
# MR = {
#     'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100],
#     'mr': [611.812, 456.245, 338.518, 252.676, 155.787, 53.821, 6.768, 3.923]}
#
# MC = {'N': [23, 36, 45, 49.9, 56, 67.5, 89.5, 112, 126.4],
#       'b': [17.623, 17.721, 17.725, 17.732, 24.585, 24.596, 24.614, 24.687, 24.796]}
#
# demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100, 30200],
#           'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614, 705.6303418, 703.3085408,
#                     700.9926952]}
#
# # Деление значений на 720
# MR['pg'] = [pg / 720 for pg in MR['pg']]
# demand['pg'] = [pg / 720 for pg in demand['pg']]
#
# # Построение графиков
# plt.plot(MR['pg'], MR['mr'], label='MR')
# plt.plot(MC['N'], MC['b'], label='MC')
# plt.plot(demand['pg'], demand['price'], label='Demand')
# plt.xlabel('pg')
# plt.ylabel('Price or b or MR')
# plt.title('Графики MR, MC, и Demand')
# plt.legend()
# plt.grid(True)
# plt.show()
