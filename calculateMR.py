def calculate_mr(demand):
    MR = []  # Инициализация массива результата MR

    # Перебор массива demand['pg']
    for i in range(len(demand['pg'])):
        print('Итерация', i)
        # Определение индексов
        if i == len(demand['pg']) - 1:
            index1 = i - 1
            index2 = i
        else:
            index1 = i
            index2 = i + 1

        # Найдем изменение цены
        # P1 - P2
        deltaP = abs(demand['price'][index1] - demand['price'][index2])
        print('deltaP', deltaP)
        # Найдем выработку дополнительной единицы электроэнергии
        # Э2 - Э1
        deltaPg = abs(demand['pg'][index2] - demand['pg'][index1])
        print('deltaPg', deltaPg)
        # Найдем прирост общей выручки
        # Э1*deltaP - P2 * deltaЭ
        deltaTR = demand['pg'][index1] * deltaP - demand['price'][index2] * deltaPg
        print('deltaTR', deltaTR)
        # Найдем прирост общей выручки и добавим его в массив MR
        mr = deltaTR / deltaPg
        print('mr', mr)
        MR.append(mr)

    return MR


# Исходные данные
# demand = {'pg': [13300, 23900, 24000, 46300, 70900, 87400],
#           'price': [1244.94, 781.69, 779.11, 462.40, 329.66, 279.21]}

demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000],
          'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614]}

# Вызов функции и вывод результатов
result_MR = calculate_mr(demand)
print("Результаты MR:", result_MR)