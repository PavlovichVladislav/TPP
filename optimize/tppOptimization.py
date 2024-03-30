import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def polynomial_fit(x, y, degree):
    # Функция для аппроксимации полиномиальной моделью
    coeffs = np.polyfit(x, y, degree)
    return np.poly1d(coeffs)


def find_intersection(model_mr, model_mc):
    # Находим точку пересечения моделей MR и MC
    def objective(x):
        return model_mr(x) - model_mc(x)

    x_opt = np.min(np.abs(np.roots(model_mr - model_mc)))
    return x_opt, model_mr(x_opt)


def plot_graph(new_MR, new_Demand, MC, intersection_point, x_opt, y_opt):
    # Функция для построения графиков
    plt.plot(new_MR['pg'], new_MR['mr'], label='New MR')
    plt.plot(new_Demand['pg'], new_Demand['price'], label='New Demand')
    plt.plot(MC['N'], MC['b'], label='MC')
    plt.scatter(intersection_point[0], intersection_point[1], color='red', label='Intersection Point')
    plt.scatter(x_opt, 0, color='green', label='x_opt')
    plt.scatter(0, y_opt, color='blue', label='y_opt')
    plt.xlabel('pg/N')
    plt.ylabel('mr/price/b')
    plt.legend()
    plt.show()


def tppOptimize(MR, MC, demand):
    model_mr = polynomial_fit(MR['pg'], MR['mr'], 2)
    model_demand = polynomial_fit(demand['pg'], demand['price'], 2)

    new_Mr = {'pg': [], 'mr': []}
    new_demand_price = []
    for n in MC['N']:
        new_Mr['pg'].append(n)
        new_Mr['mr'].append(model_mr(n))
        new_demand_price.append(model_demand(n))
    new_Demand = {'pg': MC['N'], 'price': new_demand_price}

    model_mc = polynomial_fit(MC['N'], MC['b'], 2)

    x_opt, y_opt = find_intersection(model_mr, model_mc)

    intersection_point = (x_opt, y_opt)

    plot_graph(new_Mr, new_Demand, MC, intersection_point, x_opt, y_opt)


# Пример использования
MR = {'pg': [14000, 17000, 20000, 22000, 24000], 'mr': [611.812, 456.245, 338.518, 252.676, 155.787]}
# MC = {'N': [44.17, 100, 130.5, 130.5, 150, 197.31, 197.31, 300, 350.31],
#       'b': [11.945, 12.06, 12.252, 18.645, 18.722, 18.798, 26.111, 26.341, 26.417]}

MC = {'N': [31802.4, 72000, 93960, 108000, 142063.2, 216000, 252223.2, 257760],
      'b': [11.945, 12.06, 12.252, 18.645, 18.722, 18.798, 26.111, 26.341]}

demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000],
          'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614]}

# tppOptimize(MR, MC, demand)