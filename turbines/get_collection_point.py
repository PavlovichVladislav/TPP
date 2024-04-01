# Дублируется, надо выносить
summer_month_numbers = [6, 7, 8]
winter_month_numbers = [11, 12, 1, 2, 3]
offSeason_month_numbers = [9, 10, 4, 5]

# Надо заносить в БД
t_20_90_steam_selection = [28.3, 35.7, 27, 25.2, 15.1, 10.6, 23.7, 17.2, 27.8, 29, 35.6, 36.6]
pt_65_75_130_13_steam_selection = [70.2, 47.6, 63.1, 53.1, 80, 85, 90, 95, 100, 105, 110, 115]
pt_80_100_130_13_steam_selection = [120, 125, 130, 135, 140, 145, 0, 5, 10, 15, 20, 25]

def get_collection_point(turbine_mark, season):
    input_data = []
    month_numbers = []

    # Потом это должен быть запрос к БД
    # Но сейчас эти данные захардкоженны в проге
    if (turbine_mark == 'Т-20-90'):
        input_data = t_20_90_steam_selection
    if (turbine_mark == 'ПТ-65/75-130/13'):
        input_data = pt_65_75_130_13_steam_selection
    if (turbine_mark == 'ПТ-80/100-130/13'):
        input_data = pt_80_100_130_13_steam_selection

    # Эти данные можно хранить в проге, но в другом месте
    # Можно вынести в функцию get_mounth_numbers
    if (season == 'summer'):
        month_numbers = summer_month_numbers
    if (season == 'winter'):
        month_numbers = winter_month_numbers
    if (season == 'offSeason'):
        month_numbers = offSeason_month_numbers

    # Сама точка забора считается легко
    # Нужно просуммировать все отборы пара по соответствующим
    # Месяцам и поделит ьна кол-во месяцев
    collection_point = 0

    for mounth in month_numbers:
        collection_point += input_data[mounth - 1]

    collection_point /= len(month_numbers)

    return collection_point