import numpy as np

def calculate_mr(demand):
    MR = []  # Инициализация массива результата MR

    # Перебор массива demand['pg']
    for i in range(len(demand['pg']) - 1):
        index1 = i
        index2 = i + 1

        # Найдем изменение цены P1 - P2
        deltaP = abs(demand['price'][index1] - demand['price'][index2])
        # Найдем выработку дополнительной единицы электроэнергии Э2 - Э1
        deltaPg = abs(demand['pg'][index2] - demand['pg'][index1])
        # Найдем прирост общей выручки
        # Э1*deltaP - P2 * deltaЭ
        deltaTR = abs(demand['pg'][index1] * deltaP - demand['price'][index2] * deltaPg)
        # Найдем прирост общей выручки и добавим его в массив MR
        mr = deltaTR / deltaPg
        MR.append(round(mr, 3))

    return {'pg': demand['pg'][:-1], 'mr': MR}


# # Исходные данные
# demand = {'pg': [13300, 23900, 24000, 46300, 70900, 87400],
#           'price': [1244.94, 781.69, 779.11, 462.40, 329.66, 279.21]}
#
# demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100, 30200],
#           'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614, 705.6303418, 703.3085408,
#                     700.9926952]}
#
# # Вызов функции и вывод результатов
# result_MR = calculate_mr(demand)
# print("Результаты MR:", result_MR)
#
# import matplotlib.pyplot as plt
#
# # Построение графика
# plt.plot(demand['pg'], demand['price'], marker='o', linestyle='-', label='Спрос')
# plt.plot(result_MR['pg'], result_MR['mr'], marker='o', linestyle='-', label='MR')
#
# plt.title('Спрос и MR')
# plt.xlabel('pg')
# plt.ylabel('Себестоимость / MR')
# plt.grid(True)
# plt.legend()
# plt.show()

