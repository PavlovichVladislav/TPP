import matplotlib.pyplot as plt

from utils.calc_boiler_hop_model import calc_boiler_hop_model
from utils.regression_model import model

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

    # Массив Q для результата по котельному цеху
    Q = [0] * len(unique_hops)

    # Принцип расчёта следующий для B[к1] = B[к2] = ... = [Bкn]
    # Суммируем Qкц = Qк1 + Qk2 + ... + Qkn
    # Т.е. для равных B у котлов находим их значения D и суммируем
    for i, b in enumerate(unique_hops):
        for params in (hop_models):
            teta1, teta2, teta3, teta4 = params
            # Вычисляем значение D зная параметры teta и нужную точку
            q_value = model(b, teta1, teta2, teta3, teta4)

            Q[i] += q_value

    if (plot_for_shop):
        plot_graph(Q, unique_hops, 'Хоп котельного цеха', 'Dк, т/x', 'b, т.у.т/Гкал')

    return {'b': unique_hops, 'Q': Q}
