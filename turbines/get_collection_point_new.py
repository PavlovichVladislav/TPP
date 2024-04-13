# Дублируется, надо выносить
summer_month_numbers = [6, 7, 8]
winter_month_numbers = [11, 12, 1, 2, 3]
offSeason_month_numbers = [9, 10, 4, 5]

def get_collection_point(input_data, season):
    month_numbers = []

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

    return round(collection_point, 2)