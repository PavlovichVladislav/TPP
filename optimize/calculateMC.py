def get_average_fuel_price(fuel_price, season):
    # Номера месяцев по сезонам года
    summer_month_numbers = [6, 7, 8]
    winter_month_numbers = [11, 12, 1, 2, 3]
    offSeason_month_numbers = [9, 10, 4, 5]

    # Опеределяем какие номера месяцев в сезоне
    if season == 'summer':
        month_numbers = summer_month_numbers
    elif season == 'winter':
        month_numbers = winter_month_numbers
    elif season == 'offSeason':
        month_numbers = offSeason_month_numbers
    else:
        raise ValueError("Invalid season provided")

    # Расчитываем среднюю цену топлива
    total_price = sum(fuel_price[i - 1] for i in month_numbers)
    average_fuel_price = total_price / len(month_numbers)
    return average_fuel_price


def calculate_mc(station_hop, fuel_price, season):
    # Получаем среднюю цену топлива за сезон
    average_fuel_price = get_average_fuel_price(fuel_price, season)

    # Каждое значение b умножаем на среднюю цену топлива
    newB = [round(b * average_fuel_price, 3) for b in station_hop['b']]

    # Возвращаем хоп, где b уже умножено на цену топлива
    return {'N': station_hop['N'], 'b': newB}


# # ХОП станции
# station_hop = {'N': [44.17, 100, 130.5, 130.5, 150, 197.31, 197.31, 300, 350.31],
#                'b': [0.0312, 0.0315, 0.032, 0.0487, 0.0489, 0.0491, 0.0682, 0.0688, 0.069]}
# # Цены на топливо
# fuel_price = [314.66, 290.3, 346.13, 327.89, 306.26, 335.53, 409.96, 346.85, 371.01, 366.85, 427.21, 536]
#
# season = 'winter'
#
# result = calculate_mc(station_hop, season)
# print(result)
