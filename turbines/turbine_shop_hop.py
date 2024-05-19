from matplotlib import pyplot as plt

from turbines.turbine_hop import calc_turbine_hop


def plot_hop(data):
    # инициализируем массивы для x и y
    x_values = []
    y_values = []

    # перебираем все словари из входных данных
    # по сути берём интервалы и их значения тангенсов
    # -----------------------------------------------
    # по сути чтобы построить график нужно одинаковое кол-во x и y
    # т.к. это координаты
    # в цикле мы кладём в x начало и конец интервала
    # а в y кладём соотвтетсвующих два значения тангенса для начала и конца интервала
    for entry in data:
        interval = entry['interval']
        tangent = entry['tangent']
        x_values.extend(interval)
        y_values.extend([tangent, tangent])

    plt.plot(x_values, y_values, marker='o')
    plt.xlabel('N, мвт')
    plt.ylabel('Гкал / МВт*ч')
    # plt.title('ХОП турбинного цеха')
    plt.show()

def process_turbines(turbines_hop):
    # Объединяем все словари в один массив
    temp_arr = []
    for turbine in turbines_hop:
        temp_arr.extend(turbine)

    # Сортируем temp_arr по «тангенсу» в порядке убывания
    temp_arr.sort(key=lambda x: x['tangent'], reverse=False)

    result_arr = [temp_arr[0]]  # Инициализируем result_arr первым элементом temp_arr

    # Перебираем temp_arr, начиная со второго элемента
    for i in range(1, len(temp_arr)):
        if temp_arr[i] == temp_arr[i - 1]:
            # Если текущий словарь равен предыдущему,
            # расширяем интервал предыдущего словаря
            result_arr[-1]['interval'][1] += temp_arr[i]['interval'][1] - temp_arr[i]['interval'][0]
        else:
            # В противном случае создайте новый словарь и добавьте его в result_arr
            new_interval = [
                result_arr[-1]['interval'][1],
                result_arr[-1]['interval'][1] + (temp_arr[i]['interval'][1] - temp_arr[i]['interval'][0])
            ]
            result_arr.append({'interval': new_interval, 'tangent': temp_arr[i]['tangent']})

    return result_arr

# Расчёт ХОП турбинного цеха
def calc_turbines_shop_hop(turbines, season, plot_for_turbines):
    turbines_hops = []
    flow_chars = []

    for turbine in turbines:
        turbine_hop = calc_turbine_hop(turbine['type'], season, plot_for_turbines)
        turbines_hops.append(turbine_hop['hop'])
        flow_chars.append({'mark': turbine_hop['mark'], 'flow_char': turbine_hop['flow_char']})

    # Посчитаем хоп турбинного цеха из ХОП отдельных турбин
    turbine_shop_hop = process_turbines(turbines_hops)
    plot_hop(turbine_shop_hop)

    return flow_chars, turbine_shop_hop


# summer_turbines_combination = [
#     {'name': 'ТГ03', 'type': 'Т-20-90', 'electricityPower': 20, 'thermalPower': 54, 'powerGeneration': 147.8},
#     {'name': 'ТГ08', 'type': 'ПТ-80/100-130/13', 'electricityPower': 80, 'thermalPower': 190, 'powerGeneration': 422.9},
#     {'name': 'ТГ09', 'type': 'ПТ-80/100-130/13', 'electricityPower': 80, 'thermalPower': 190, 'powerGeneration': 304.6}]
#
# summer_flow_chars, summer_turbines_shop_hop = calc_turbines_shop_hop(summer_turbines_combination, 'summer',
#                                                                      True)
#
# print(summer_flow_chars)
# print(summer_turbines_shop_hop)

