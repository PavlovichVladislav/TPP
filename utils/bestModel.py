import numpy as np
from numpy.linalg import lstsq

def find_best_fit_model(x, y, degree):
    """
    Находит модель, которая максимально точно описывает заданные точки x и y,
    используя полином указанной степени.

    Параметры:
    x : list или numpy массив
        Массив точек x.
    y : list или numpy массив
        Массив соответствующих точек y.
    degree : int
        Степень полинома.

    Возвращает:
    numpy.poly1d
        Модель, описывающая данные точки.
    """

    # Проверяем, что длины x и y совпадают
    if len(x) != len(y):
        raise ValueError("Размеры массивов x и y должны совпадать.")

    # Преобразуем x и y в numpy массивы
    x = np.array(x)
    y = np.array(y)

    # Строим матрицу X для МНК
    X = np.vander(x, degree + 1)

    # Вычисляем коэффициенты, оцениваем с помощью МНК
    coefficients, _, _, _ = lstsq(X, y, rcond=None)

    # Создаём полиномиальную модель
    model = np.poly1d(coefficients)

    return model