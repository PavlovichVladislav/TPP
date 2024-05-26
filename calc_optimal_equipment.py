from itertools import combinations

from consts import summer_month_numbers, winter_month_numbers, off_season_month_numbers


# Модуль по выполнению 1 - го задания
# Расчёт оптимального оборудования

# Оптимальное оборудования на сезон
# to-do: year_task тоже как параметр, причём это один столбец
# to-do: определение сезона в утилитку можно вынести
def optimal_equipment_combination_per_season(year_task, equipment_list, month_numbers, equipment_type):
    equipment_characteristic = ''
    year_task_column = ''

    if (equipment_type == 'boilers'):
        year_task_column = 'heat_performance'
        equipment_characteristic = 'heat_performance'

    if (equipment_type == 'turbines'):
        year_task_column = 'output_power'
        equipment_characteristic = 'electricity_power'

    # Плановая производительность на месяц сезона
    planned_perfomance_per_month = 0

    # Расчитываем плановую производительность на месяц сезона
    # Как среднюю арифметическую теплопроизводительность на этот сезон
    for task in year_task:
        if task['month'] in month_numbers:
            planned_perfomance_per_month += task[year_task_column]

    planned_perfomance_per_month /= len(month_numbers)

    # Оптимальная комбинация котлов
    optimalCombination = None
    # Минимальная излишняя выработка
    min_difference = float('inf')
    for i in range(2, len(equipment_list) + 1):
        for combo in combinations(equipment_list, i):
            # Общая производительность оборудования
            total_performance = sum(equipment[equipment_characteristic] for equipment in combo)
            # to-do: считаем ли среднюю?
            # Средняя производительность котлов за месяц
            # avgHeatPerformance = totalHearPerformance / i

            # Если средняя выработка котлов больше, чем плановая
            # То остаётся проверить излишнюю выработку
            if total_performance > planned_perfomance_per_month:
                difference = total_performance - planned_perfomance_per_month
                # Если излишняя выработка минимальная, то нам нужна эта комбинация
                if difference < min_difference:
                    min_difference = difference
                    optimalCombination = combo

    if optimalCombination:
        optimalCombination = list(optimalCombination)

    return optimalCombination


# to-do: не нужен для работы API
# Расчёт оптимального оборудования для всех сезонов года
def calc_optimal_quipment(year_task, boilers, turbines):
    summer_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers, summer_month_numbers,
                                                                          'boilers')
    winter_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers, winter_month_numbers,
                                                                          'boilers')
    offSeason_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers,
                                                                             off_season_month_numbers, 'boilers')

    summer_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, summer_month_numbers,
                                                                           'turbines')
    winter_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, winter_month_numbers,
                                                                           'turbines')
    offSeason_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines,
                                                                              off_season_month_numbers, 'turbines')

    return (
        summer_boilers_combination,
        winter_boilers_combination,
        offSeason_boilers_combination,
        summer_turbines_combination,
        winter_turbines_combination,
        offSeason_turbines_combination
    )
