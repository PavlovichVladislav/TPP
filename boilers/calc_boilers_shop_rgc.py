from utils.calc_boiler_hop_model import calc_boiler_hop_model
from utils.regression_model import model


def calc_boilers_shop_rgc_per_season(boilers_hop):
    # Для началаа нужно найти все уникальные значения b - промежуток суммирования
    # Т.к. значение ХОП у котлов в одних пределах, но могут быть
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
        hop_models.append(calc_boiler_hop_model(hop))

    # Массив Q для результата по котельному цеху
    Q = [0] * len(unique_hops)

    # Принцип расчёта следующий для B[к1] = B[к2] = ... = [Bкn]
    # Суммируем Qкц = Qк1 + Qk2 + ... + Qkn
    # Т.е. для равных B у котлов находим их значения D и суммируем
    for i, b in enumerate(unique_hops):
        for params in (hop_models):
            teta1, teta2 = params
            # Вычисляем значение D зная параметры teta и нужную точку
            q_value = model(b, teta1, teta2)

            Q[i] += q_value

    # Округлим результат до 3 - х знаков после запятой
    Q = [round(q, 3) for q in Q]

    return {'b': unique_hops, 'Q': Q}
