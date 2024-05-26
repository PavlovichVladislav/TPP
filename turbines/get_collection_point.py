from consts import summer_month_numbers
from consts import winter_month_numbers
from consts import  off_season_month_numbers

def get_collection_point(input_data, season):
    month_numbers = []

    if (season == 'summer'):
        month_numbers = summer_month_numbers
    if (season == 'winter'):
        month_numbers = winter_month_numbers
    if (season == 'offSeason'):
        month_numbers = off_season_month_numbers

    # Суммируем все отборы пара по соответствующим месяцам сезона
    # и делим на количество месяцев
    collection_point = 0

    for mounth in month_numbers:
        collection_point += input_data[mounth - 1]

    collection_point /= len(month_numbers)

    return round(collection_point, 2)