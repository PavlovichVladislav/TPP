import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def linear_model(x, a, b):
    x = np.array(x)

    return a * x + b


def quadratic_model(x, a, b, c):
    x = np.array(x)

    return a * x ** 2 + b * x + c


def cubic_model(x, a, b, c, d):
    x = np.array(x)

    return a * x ** 3 + b * x ** 2 + c * x + d


def find_best_fit(x, y):
    models = [linear_model, quadratic_model, cubic_model]
    best_model = None
    best_error = float('inf')

    for model in models:
        params, _ = curve_fit(model, x, y)
        y_pred = model(x, *params)
        error = np.mean((y - y_pred) ** 2)

        if error < best_error:
            best_error = error
            best_model = model

    return best_model, params


def find_intersection_point(x_data, y_data, model_mr, params_mr):
    for i in range(len(x_data) - 1):
        x1, x2 = x_data[i], x_data[i + 1]
        y1, y2 = y_data[i], y_data[i + 1]

        if y1 < model_mr(x1, *params_mr) and y2 > model_mr(x2, *params_mr):
            m = (y2 - y1) / (x2 - x1)
            x_opt = (model_mr(x1, *params_mr) - y1) / m + x1
            y_opt = model_mr(x_opt, *params_mr)
            return x_opt, y_opt

def plot_graph(transformed_mr, transformed_demand, MC, intersection_point, x_opt, y_opt):
    plt.figure(figsize=(10, 6))
    plt.plot(transformed_mr['pg'], transformed_mr['mr'], label='Transformed MR', marker='o')
    plt.plot(transformed_demand['pg'], transformed_demand['price'], label='Transformed Demand', marker='o')
    plt.plot(MC['N'], MC['b'], label='MC', marker='o')
    plt.plot([intersection_point[0], x_opt], [intersection_point[1], 0], 'ro')
    plt.plot([intersection_point[0], 0], [intersection_point[1], y_opt], 'ro')
    plt.xlabel('Quantity')
    plt.ylabel('Price/Cost')
    plt.title('Optimization')
    plt.legend()
    plt.grid(True)
    plt.show()


def tppOptimize(MR, MC, demand):
    transformed_mr = {'pg': [pg / 720 for pg in MR['pg']], 'mr': MR['mr']}
    transformed_demand = {'pg': [pg / 720 for pg in demand['pg']], 'price': demand['price']}

    model_mr, params_mr = find_best_fit(transformed_mr['pg'], transformed_mr['mr'])
    model_demand, _ = find_best_fit(transformed_demand['pg'], transformed_demand['price'])

    x_opt, y_opt = find_intersection_point(MC['N'], MC['b'], model_mr, transformed_mr['pg'])

    intersection_point = (x_opt, model_mr(x_opt))

    plot_graph(transformed_mr, transformed_demand, MC, intersection_point, x_opt, y_opt)

# Пример использования
MR = {
    'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100],
    'mr': [611.812, 456.245, 338.518, 252.676, 155.787, 53.821, 6.768, 3.923]}

MC = {'N': [23, 36, 45, 49.9, 56, 67.5, 89.5, 112, 126.4],
      'b': [17.623, 17.721, 17.725, 17.732, 24.585, 24.596, 24.614, 24.687, 24.796]}

demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100, 30200],
          'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614, 705.6303418, 703.3085408,
                    700.9926952]}

# tppOptimize(MR, MC, demand)
