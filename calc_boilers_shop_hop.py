import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Модель в виде которой ищем приближение
# Исходя из предметной области выбрал кубический полином
def model(x, teta0, teta1, teta2, teta3):
    return teta0 + teta1 * x + teta2 * x ** 2 + teta3 * x ** 3

def calc_boiler_hop_model(boiler_hop, plot_for_boiler):
    # Используем curve_fit для подбора параметров регрессии
    params, covariance = curve_fit(model, boiler_hop['b'], boiler_hop['D'])

    if (plot_for_boiler):
        plot_data_and_curve(params, boiler_hop)

    return params

# Вспомогательная функиця для построения графика
# В итоге график будет на фронте
# to-do: убрать функцию
def plot_graph(x, y, title="График", x_label="Ось X", y_label="Ось Y"):
    # Создаем график
    plt.plot(x, y, marker='o')

    # Добавляем заголовок и метки осей
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

# Функция, которая на одном графике строит исходный ХОП котла и
# его приближение с помощью регрессии
def plot_data_and_curve(params, boiler_hop):
    b = boiler_hop['b']
    D = boiler_hop['D']

    # Генерируем 100 точек на интервале min(b) до max(b)
    x_values = np.linspace(min(b), max(b), 100)

    # Строим кривую с помощью модели
    teta0, teta1, teta2, teta3 = params
    y_values = model(x_values, teta0, teta1, teta2, teta3)

    # Наносим точки из коллекции на график
    plt.scatter(b, D, label='Исходные ХОП')

    # Строим кривую на графике
    plt.plot(x_values, y_values, color='red', label='Регрессия')

    plt.xlabel('b')
    plt.ylabel('D')
    plt.title('Регрессия ХОП для' + boiler_hop['mark'] )
    plt.legend()
    plt.grid(True)
    plt.show()

def calc_boilers_shop_hop_per_season(boilers_hop, plot_for_shop, plot_for_boiler):
    # Для началаа нужно найти все уникальные значения b - промежуток суммирования
    # Т.к. значение hop у котлов в одних пределах, но могут быть
    # Немного разными
    # Например, 0.151 есть для одного котла, а для другого нет
    unique_hops = set()

    for hop in boilers_hop:
        unique_hops.update(hop['b'])

    # Отсортируем по возрастанию
    unique_hops = sorted(unique_hops)

    # Построим регрессию по известным значениям для ХОП каждого котла
    hop_models = []
    for hop in boilers_hop:
        hop_models.append(calc_boiler_hop_model(hop, plot_for_boiler))

    # Массив D для результата по котельному цеху
    D = [0] * len(unique_hops)

    # Принцип расчёта следующий для B[к1] = B[к2] = ... = [Bкn]
    # Суммируем Dкц = Dк1 + Dk2 + ... + Dkn
    # Т.е. для равных B у котлов находим их значения D и суммируем
    for i, b in enumerate(unique_hops):
        for params in (hop_models):
            teta1, teta2, teta3, teta4 = params
            # Вычисляем значение D зная параметры teta и нужную точку
            d_value = model(b, teta1, teta2, teta3, teta4)

            D[i] += d_value

    if (plot_for_shop):
        plot_graph(D, unique_hops, 'Хоп котельного цеха', 'Dк, т/x', 'b, т.у.т/Гкал')

    return {'b': unique_hops, 'D': D}
