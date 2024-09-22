from turbines.calc_flow_char import calc_flow_char
from turbines.turbine_hop import calc_turbine_hop
from turbines.get_collection_point import get_collection_point


def process_turbines(turbines_hop):
    # объединяем ХОП в один массив
    temp_arr = []
    for turbine in turbines_hop:
        temp_arr.extend(turbine)

    # сортируем массив по значению тангенса
    temp_arr.sort(key=lambda x: x['tangent'], reverse=False)

    # Инициализируем result_arr, первый элемент
    # - 0-й элемент отсортированного массива
    result_arr = [temp_arr[0]]

    # Перебираем temp_arr со второго элемента
    for i in range(1, len(temp_arr)):
        if temp_arr[i] == temp_arr[i - 1]:
            # Если предыдущий ХОП и текущий для оной турбины
            # то просто расширяем интервал
            result_arr[-1]['interval'][1] += round(temp_arr[i]['interval'][1] - temp_arr[i]['interval'][0], 3)
        else:
            # Иначе создаём новый кусочек интервала и добавляем в результат
            new_interval = [
                round(result_arr[-1]['interval'][1], 3),
                round(result_arr[-1]['interval'][1] + (temp_arr[i]['interval'][1] - temp_arr[i]['interval'][0]), 3)
            ]
            result_arr.append({'interval': new_interval, 'tangent': temp_arr[i]['tangent']})

    return result_arr


# Расчёт ХОП турбинного цеха
def calc_turbines_shop_hop(turbines, season):
    turbines_hops = []
    flow_chars = []

    for turbine in turbines:
        # Сезонный расход пара для отдельной турбины
        steam_consuption = get_collection_point(turbine['steam_consumption'], season)
        # Хоп турбины
        turbine_hop = calc_turbine_hop(turbine['turbine_mark'], steam_consuption)
        # Добавим в массив
        turbines_hops.append(turbine_hop['hop'])
        # Посчитаем расходную характеристику для турбины
        flow_chars.append({'mark': turbine_hop['mark'], 'flow_char': turbine_hop['flow_char']})

    # Посчитаем хоп турбинного цеха из ХОП отдельных турбин
    turbine_shop_hop = process_turbines(turbines_hops)

    print(turbine_shop_hop)

    def round_data(data):
        for item in data:
            item['interval'] = [round(num, 3) for num in item['interval']]
            item['tangent'] = round(item['tangent'], 3)
        return data

    turbine_shop_hop = round_data(turbine_shop_hop)

    print(turbine_shop_hop)

    # Посчитаем расхо   дную характеристику турбинного цеха

    flow_char = calc_flow_char(flow_chars)

    return flow_char, turbine_shop_hop
