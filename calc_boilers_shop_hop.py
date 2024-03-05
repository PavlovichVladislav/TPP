import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# исходные данные
b_tp170 = [0.152, 0.154, 0.157, 0.158, 0.16, 0.159, 0.161, 0.161]
d_tp170 = [128.86, 133.08, 139.42, 147.36, 151.59, 156.32, 164.77, 170.18]

b_tp80 = [0.154, 0.157, 0.15, 0.159, 0.158, 0.157, 0.159, 0.16, 0.16, 0.161]
d_tp80 = [302.17, 312.65, 325.57, 334.02, 346.45, 357.85, 366.30, 380.92, 397.82, 412.86]

# Модель в виде которой ищем приближение
# Исходя из предметной области выбрал кубический полином
def model(x, teta0, teta1, teta2, teta3):
    return teta0 + teta1*x + teta2*x**2 + teta3*x**3

# Используем curve_fit для подбора параметров регрессии
tp170Params, covariance = curve_fit(model, b_tp170, d_tp170)
tp80Params, covariance = curve_fit(model, b_tp80, d_tp80)

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

def calc_boilers_shop_hop_per_season(boilers_hop):



plot_graph(b_tp170, d_tp170, "ХОП тп-170", "b", "D")
plot_model(tp170Params, np.min(b_tp170), np.max(b_tp170))
plt.show()

plot_graph(b_tp80, d_tp80, "ХОП тп-80", "b", "D")
plot_model(tp80Params, np.min(b_tp80), np.max(b_tp80))
plt.show()