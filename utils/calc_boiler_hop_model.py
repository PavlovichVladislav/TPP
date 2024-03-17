import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from utils.regression_model import model


# Функция, которая на одном графике строит исходный ХОП котла и
# его приближение с помощью регрессии
def plot_data_and_curve(params, boiler_hop):
    b = boiler_hop['b']
    D = boiler_hop['Q']

    # Генерируем 100 точек на интервале min(b) до max(b)
    x_values = np.linspace(min(b), max(b), 100)

    # Строим кривую с помощью модели
    teta0, teta1, teta2, teta3 = params
    y_values = model(x_values, teta0, teta1, teta2, teta3)

    # Если в boiler_hop нет поля 'mark', то это котельный цех
    if 'mark' not in boiler_hop:
        mark_value = 'котельного цеха'
    else:
        mark_value = boiler_hop['mark']

    # Наносим точки из коллекции на график
    plt.scatter(D, b, label='Исходные ХОП')

    # Строим кривую на графике
    plt.plot(y_values, x_values, color='red', label='Регрессия')
    plt.xlabel('b')
    plt.ylabel('D')
    plt.title('Регрессия ХОП для' + mark_value)
    plt.legend()
    plt.grid(True)
    plt.show()

# Функция для построения модели, которой описывается график ХОП
def calc_boiler_hop_model(boiler_hop, plot_for_boiler):
    # Используем curve_fit для подбора параметров регрессии
    params, covariance = curve_fit(model, boiler_hop['b'], boiler_hop['Q'])

    if (plot_for_boiler):
        plot_data_and_curve(params, boiler_hop)

    return params