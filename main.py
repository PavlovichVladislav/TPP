from calc_boilers_hop import calc_boilers_hop_per_season
from calc_optimal_equipment import calc_optimal_quipment

# 1. --------------------------------------------
# Оптимальное оборудование

# Исходные данные
# to-do: перенести в БД
# В целом, как я понимаю, эти исходные данные для своих расчётов человек заносит и сохраняет сам
# Но у него должна оставаться возможность их выгрузить

turbines = [
    {'name': 'ТГ03', 'type': 'Т-20-90', 'electricityPower': 20, 'thermalPower': 54, 'powerGeneration': 147.8},
    {'name': 'ТГ04', 'type': 'Т-20-90', 'electricityPower': 20, 'thermalPower': 54, 'powerGeneration': 151.0},
    {'name': 'ТГ05', 'type': 'Т-20-90', 'electricityPower': 20, 'thermalPower': 54, 'powerGeneration': 93.9},
    {'name': 'ТГ06', 'type': 'ПТ-65/75-130/13', 'electricityPower': 65, 'thermalPower': 139, 'powerGeneration': 252.7},
    {'name': 'ТГ07', 'type': 'ПТ-65/75-130/13', 'electricityPower': 65, 'thermalPower': 139, 'powerGeneration': 268.0},
    {'name': 'ТГ08', 'type': 'ПТ-80/100-130/13', 'electricityPower': 80, 'thermalPower': 190, 'powerGeneration': 422.9},
    {'name': 'ТГ09', 'type': 'ПТ-80/100-130/13', 'electricityPower': 80, 'thermalPower': 190, 'powerGeneration': 304.6}
]

boilers = [
    {'stationNumber': '3', 'mark': 'ТП-170', 'heatPerformance': 150, 'numberOfStarts': 461},
    {'stationNumber': '4', 'mark': 'ТП-170', 'heatPerformance': 170, 'numberOfStarts': 491},
    {'stationNumber': '5', 'mark': 'ТП-170', 'heatPerformance': 170, 'numberOfStarts': 530},
    {'stationNumber': '6', 'mark': 'ТП-80', 'heatPerformance': 170, 'numberOfStarts': 562},
    {'stationNumber': '7', 'mark': 'ТП-87А', 'heatPerformance': 420, 'numberOfStarts': 437},
    {'stationNumber': '8', 'mark': 'ТП-81', 'heatPerformance': 420, 'numberOfStarts': 504},
    {'stationNumber': '9', 'mark': 'ТП-81', 'heatPerformance': 420, 'numberOfStarts': 358}
]

# Годовое задание по выработке тепловой и электрической энергии по месяцам
# Январь это 1 -й месяц
# Декабрь это 12 -й месяц
# month - месяц
# powerGeneration - выработка электроэнергии
# outputPower - выдаваемая мощность
# heatRelease - отпуск тепла
# hearPerformance - тепплопроизводительность
year_task = [
    {'month': 1, 'powerGeneration': 231.8, 'outputPower': 311.6, 'heatRelease': 352.6, 'heatPerformance': 800.93},
    {'month': 2, 'powerGeneration': 206, 'outputPower': 294.5, 'heatRelease': 281.6, 'heatPerformance': 683.77},
    {'month': 3, 'powerGeneration': 147.3, 'outputPower': 197.9, 'heatRelease': 253.4, 'heatPerformance': 575.59},
    {'month': 4, 'powerGeneration': 121.6, 'outputPower': 168.8, 'heatRelease': 187.9, 'heatPerformance': 441.0},
    {'month': 5, 'powerGeneration': 85.6, 'outputPower': 115.1, 'heatRelease': 92.2, 'heatPerformance': 209.42},
    {'month': 6, 'powerGeneration': 46.3, 'outputPower': 64.3, 'heatRelease': 56.6, 'heatPerformance': 132.85},
    {'month': 7, 'powerGeneration': 23.9, 'outputPower': 32.1, 'heatRelease': 45.0, 'heatPerformance': 102.22},
    {'month': 8, 'powerGeneration': 87.4, 'outputPower': 117.5, 'heatRelease': 70.0, 'heatPerformance': 159.01},
    {'month': 9, 'powerGeneration': 103.2, 'outputPower': 143.3, 'heatRelease': 62.7, 'heatPerformance': 147.19},
    {'month': 10, 'powerGeneration': 150, 'outputPower': 201.6, 'heatRelease': 186.2, 'heatPerformance': 423},
    {'month': 11, 'powerGeneration': 200, 'outputPower': 277.8, 'heatRelease': 267.3, 'heatPerformance': 627.41},
    {'month': 12, 'powerGeneration': 238, 'outputPower': 319.9, 'heatRelease': 291.2, 'heatPerformance': 661.46}
]

(summer_boilers_combination,
 winter_boilers_combination,
 offSeason_boilers_combination,
 summer_turbines_combination,
 winter_turbines_combination,
 offSeason_turbines_combination) = calc_optimal_quipment(year_task, boilers, turbines)

print('summber_boilers', summer_boilers_combination)
print('winter_boilers', winter_boilers_combination)
print('offseason_boilers', offSeason_boilers_combination)
print('summber_turbines', summer_turbines_combination)
print('winter_turbines', winter_turbines_combination)
print('offseason_turbines', offSeason_turbines_combination)

# 2. --------------------------------------------
# Расчёт ХОП для котла

summer_boilers_hops = calc_boilers_hop_per_season(summer_boilers_combination)
winter_boilers_hops = calc_boilers_hop_per_season(winter_boilers_combination)
offSeason_boilers_hops = calc_boilers_hop_per_season(offSeason_boilers_combination)

print("summer_boilers_hops", summer_boilers_hops)
print("winter_boilers_hops", winter_boilers_hops)
print("offSeason_boilers_hops", offSeason_boilers_hops)
