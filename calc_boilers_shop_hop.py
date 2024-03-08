import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Модель в виде которой ищем приближение
# Исходя из предметной области выбрал кубический полином
def model(x, teta0, teta1, teta2, teta3):
    return teta0 + teta1 * x + teta2 * x ** 2 + teta3 * x ** 3

def calc_boiler_hop_model(boiler_hop):
    # Используем curve_fit для подбора параметров регрессии
    params, covariance = curve_fit(model, boiler_hop['hop'], boiler_hop['d'])

    return params

# Вспомогательная функиця для построения графика
# В итоге график будет на фронте
# to-do: убрать функцию
def plot_graph(x, y, title="График", x_label="Ось X", y_label="Ось Y"):
    # Создаем график
    plt.scatter(x, y, marker='o')

    # Добавляем заголовок и метки осей
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def plot_model(params, x_min, x_max, num_points=100):
    # Генерируем значения x в указанном промежутке
    x_values = np.linspace(x_min, x_max, num_points)

    teta0, teta1, teta2, teta3 = params

    # Вычисляем значения y с использованием модели
    y_values = model(x_values, teta0, teta1, teta2, teta3)

    # Строим график
    plt.plot(x_values, y_values)

    # Добавляем заголовок и метки осей
    plt.title("ХОП ТП-170 (регрессия)")
    plt.xlabel("b")
    plt.ylabel("D")

def calc_boilers_shop_hop_per_season(boilers_hop, plot_for_shop, plot_for_boiler):
    # Для началаа нужно найти все уникальные значения b - промежуток суммирования
    # Т.к. значение hop у котлов в одних пределах, но могут быть
    # Немного разными
    # Например, 0.151 есть для одного котла, а для другого нет
    unique_hops = set()

    for hop in boilers_hop:
        unique_hops.update(hop['hop'])

    # Отсортируем по возрастанию
    unique_hops = sorted(unique_hops)

    # Построим регрессию по известным значениям для ХОП каждого котла
    hop_models = []
    for hop in boilers_hop:
        hop_models.append(calc_boiler_hop_model(hop))

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
