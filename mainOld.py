from boilers.calc_boilers_hop import calc_boilers_hop_per_season
from boilers.calc_boilers_shop_hop import calc_boilers_shop_hop_per_season
from getTestEquipment import getTestEquipment
from optimize.calculateMC import calculate_mc
from optimize.calculateMR import calculate_mr
from turbines.calc_flow_char import calc_flow_char
from calc_optimal_equipment import calc_optimal_quipment
from station_hop import calc_station_hop
from optimize.tppOptimization import tppOptimize
from turbines.turbine_shop_hop import calc_turbines_shop_hop

# 1. --------------------------------------------
# Оптимальное оборудование

# Исходные данные
# to-do: перенести в БД
# В целом, как я понимаю, эти исходные данные для своих расчётов человек заносит и сохраняет сам
# Но у него должна оставаться возможность их выгрузить

turbines = [
    {'name': 'ТГ03', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 147.8},
    {'name': 'ТГ04', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 151.0},
    {'name': 'ТГ05', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 93.9},
    {'name': 'ТГ06', 'type': 'ПТ-65/75-130/13', 'electricity_power': 65, 'thermalPower': 139, 'powerGeneration': 252.7},
    {'name': 'ТГ07', 'type': 'ПТ-65/75-130/13', 'electricity_power': 65, 'thermalPower': 139, 'powerGeneration': 268.0},
    {'name': 'ТГ08', 'type': 'ПТ-80/100-130/13', 'electricity_power': 80, 'thermalPower': 190,
     'powerGeneration': 422.9},
    {'name': 'ТГ09', 'type': 'ПТ-80/100-130/13', 'electricity_power': 80, 'thermalPower': 190, 'powerGeneration': 304.6}
]

boilers = [
    {'stationNumber': '3', 'mark': 'ТП-170', 'heat_performance': 150, 'numberOfStarts': 461},
    {'stationNumber': '4', 'mark': 'ТП-170', 'heat_performance': 170, 'numberOfStarts': 491},
    {'stationNumber': '5', 'mark': 'ТП-170', 'heat_performance': 170, 'numberOfStarts': 530},
    {'stationNumber': '6', 'mark': 'ТП-80', 'heat_performance': 170, 'numberOfStarts': 562},
    {'stationNumber': '7', 'mark': 'ТП-87А', 'heat_performance': 420, 'numberOfStarts': 437},
    {'stationNumber': '8', 'mark': 'ТП-81', 'heat_performance': 420, 'numberOfStarts': 504},
    {'stationNumber': '9', 'mark': 'ТП-81', 'heat_performance': 420, 'numberOfStarts': 358}
]

# Годовое задание по выработке тепловой и электрической энергии по месяцам
# Январь это 1 -й месяц
# Декабрь это 12 -й месяц
# month - месяц
# powerGeneration - выработка электроэнергии
# output_power - выдаваемая мощность
# heatRelease - отпуск тепла
# hearPerformance - тепплопроизводительность
year_task = [
    {'month': 1, 'powerGeneration': 231.8, 'output_power': 311.6, 'heatRelease': 352.6, 'heat_performance': 800.93},
    {'month': 2, 'powerGeneration': 206, 'output_power': 294.5, 'heatRelease': 281.6, 'heat_performance': 683.77},
    {'month': 3, 'powerGeneration': 147.3, 'output_power': 197.9, 'heatRelease': 253.4, 'heat_performance': 575.59},
    {'month': 4, 'powerGeneration': 121.6, 'output_power': 168.8, 'heatRelease': 187.9, 'heat_performance': 441.0},
    {'month': 5, 'powerGeneration': 85.6, 'output_power': 115.1, 'heatRelease': 92.2, 'heat_performance': 209.42},
    {'month': 6, 'powerGeneration': 46.3, 'output_power': 64.3, 'heatRelease': 56.6, 'heat_performance': 132.85},
    {'month': 7, 'powerGeneration': 23.9, 'output_power': 32.1, 'heatRelease': 45.0, 'heat_performance': 102.22},
    {'month': 8, 'powerGeneration': 87.4, 'output_power': 117.5, 'heatRelease': 70.0, 'heat_performance': 159.01},
    {'month': 9, 'powerGeneration': 103.2, 'output_power': 143.3, 'heatRelease': 62.7, 'heat_performance': 147.19},
    {'month': 10, 'powerGeneration': 150, 'output_power': 201.6, 'heatRelease': 186.2, 'heat_performance': 423},
    {'month': 11, 'powerGeneration': 200, 'output_power': 277.8, 'heatRelease': 267.3, 'heat_performance': 627.41},
    {'month': 12, 'powerGeneration': 238, 'output_power': 319.9, 'heatRelease': 291.2, 'heat_performance': 661.46}
]

# (summer_boilers_combination,
#  winter_boilers_combination,
#  offSeason_boilers_combination,
#  summer_turbines_combination,
#  winter_turbines_combination,
#  offSeason_turbines_combination) = calc_optimal_quipment(year_task, boilers, turbines)

(summer_boilers_combination,
 winter_boilers_combination,
 offSeason_boilers_combination,
 summer_turbines_combination,
 winter_turbines_combination,
 offSeason_turbines_combination) = getTestEquipment()

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

# 3. --------------------------------------------
# ХОП котельного цеха

plot_for_shop = False
plot_for_boilers = False

summer_boilers_shop_hop = calc_boilers_shop_hop_per_season(summer_boilers_hops, plot_for_shop, plot_for_boilers)
winter_boilers_shop_hop = calc_boilers_shop_hop_per_season(winter_boilers_hops, plot_for_shop, plot_for_boilers)
offSeason_boilers_shop_hop = calc_boilers_shop_hop_per_season(offSeason_boilers_hops, plot_for_shop, plot_for_boilers)

print('summer_boilers_shop_hop', summer_boilers_shop_hop)
print('winter_boilers_shop_hop', winter_boilers_shop_hop)
print('offSeason_boilers_shop_hop', offSeason_boilers_shop_hop)

# 4. --------------------------------------------
# ХОП турбинного цеха

plot_for_turbines = False

summer_flow_chars, summer_turbines_shop_hop = calc_turbines_shop_hop(summer_turbines_combination, 'summer',
                                                                     plot_for_turbines)
winter_flow_chars, winter_turbines_shop_hop = calc_turbines_shop_hop(winter_turbines_combination, 'winter',
                                                                     plot_for_turbines)
offSeason_flow_chars, offSeason_turbines_shop_hop = calc_turbines_shop_hop(offSeason_turbines_combination, 'offSeason',
                                                                           plot_for_turbines)

print('summer_turbines_shop_hop', summer_turbines_shop_hop)
print('winter_turbines_shop_hop', winter_turbines_shop_hop)
print('offSeason_turbines_shop_hop', offSeason_turbines_shop_hop)

# 5. --------------------------------------------
# Расходная характеристика
print('summer_flow_chars', summer_flow_chars)
print('winter_flow_chars', winter_flow_chars)
print('offSeason_flow_chars', offSeason_flow_chars)

summer_shop_flow_char = calc_flow_char(summer_flow_chars)
winter_shop_flow_char = calc_flow_char(winter_flow_chars)
offSeason_shop_flow_char = calc_flow_char(offSeason_flow_chars)

print('summer_shop_flow_char', summer_shop_flow_char)
print('winter_shop_flow_char', winter_shop_flow_char)
print('offSeason_shop_flow_char', offSeason_shop_flow_char)

# 6. --------------------------------------------
# ХОП станции

summer_station_hop = calc_station_hop(summer_boilers_shop_hop, summer_turbines_shop_hop, summer_shop_flow_char)
winter_station_hop = calc_station_hop(winter_boilers_shop_hop, winter_turbines_shop_hop, winter_shop_flow_char)
offSeason_station_hop = calc_station_hop(offSeason_boilers_shop_hop, offSeason_turbines_shop_hop,
                                         offSeason_shop_flow_char)

print('summer_station_hop', summer_station_hop)
print('winter_station_hop', winter_station_hop)
print('offSeason_station_hop', offSeason_station_hop)

# 7. Оптимизация работы станции

# demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000],
#           'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614]}

# demand = {
#     'pg': [13300, 23900, 24000, 46300, 70900, 87400],
#     'price': [1284.210526, 736.5690377, 794.7083333, 492.6133909, 259.026798, 335.1373]
# }

demand = {'pg': [14000, 17000, 20000, 22000, 24000, 27000, 30000, 30100, 30200],
          'price': [1153.823537, 1058.174361, 967.885009, 910.6697875, 855.837, 778.053614, 705.6303418, 703.3085408,
                    700.9926952]}

result_MR = calculate_mr(demand)

print('MR', result_MR)

# Цены на топливо
fuel_price = [314.66, 290.3, 346.13, 327.89, 306.26, 335.53, 409.96, 346.85, 371.01, 366.85, 427.21, 536]

MC_summer = calculate_mc(summer_station_hop, fuel_price, 'summer')
MC_winter = calculate_mc(winter_station_hop, fuel_price, 'winter')
MC_offSeason = calculate_mc(offSeason_station_hop, fuel_price, 'offSeason')

print('MC_summer', MC_summer)
print('MC_winter', MC_winter)
print('MC_offSeason', MC_offSeason)

# tppOptimize(result_MR, MC_summer, demand)
# tppOptimize(result_MR, MC_winter, demand)
# tppOptimize(result_MR, MC_offSeason, demand)
