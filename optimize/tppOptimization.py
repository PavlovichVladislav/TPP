import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def model_mr(x, a, b, c):
    return a * np.exp(-b * x) + c

def model_demand(x, a, b, c):
    return a * np.exp(-b * x) + c

def fit_curve(x, y, model):
    popt, _ = curve_fit(model, x, y)
    return popt

def tppOptimize(MR, MC, demand):
    # Предварительное деление значений на 720
    MR['pg'] = [pg / 720 for pg in MR['pg']]
    MC['N'] = [n / 720 for n in MC['N']]
    demand['pg'] = [pg / 720 for pg in demand['pg']]

    # Подгонка кривых для MR и demand
    popt_mr = fit_curve(MR['pg'], MR['mr'], model_mr)
    popt_demand = fit_curve(demand['pg'], demand['price'], model_demand)

    # Создание новых значений для MR и demand
    new_mr = [model_mr(n, *popt_mr) for n in MC['N']]
    new_demand_price = [model_demand(n, *popt_demand) for n in MC['N']]

    # Формирование новых коллекций
    new_MR = {'pg': MC['N'], 'mr': new_mr}
    new_demand = {'pg': MC['N'], 'price': new_demand_price}

    # Визуализация
    plot_graph(MC, new_MR, new_demand)

def plot_graph(MC, new_MR, new_demand):
    plt.figure(figsize=(10, 6))

    # График MR
    plt.plot(new_MR['pg'], new_MR['mr'], label='New MR', marker='o')
    plt.plot(MC['N'], MC['b'], label='MC', marker='x')

    # График demand
    plt.plot(new_demand['pg'], new_demand['price'], label='New Demand', marker='^')
    plt.plot(demand['pg'], demand['price'], label='Original Demand', marker='s')

    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.title('MR, MC, and Demand Graph')
    plt.legend()
    plt.grid(True)
    plt.show()

# Пример использования
MR = {'pg': [14000, 17000, 20000, 22000, 24000], 'mr': [611.812, 456.245, 338.518, 252.676, 155.787]}
MC = {'N': [23, 36, 45, 49.9, 56, 67.5, 89.5, 112, 126.4],
      'b': [17.623, 17.721, 17.725, 17.732, 24.585, 24.596, 24.614, 24.687, 24.796]}
demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100, 30200],
          'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614, 705.6303418, 703.3085408,
                    700.9926952]}

# tppOptimize(MR, MC, demand)