# Модель в виде которой ищем приближение
# Исходя из предметной области выбрал кубический полином
def model(x, teta0, teta1):
    # return teta0 + teta1 * x + teta2 * x ** 2 + teta3 * x ** 3
    return teta0 + teta1 * x