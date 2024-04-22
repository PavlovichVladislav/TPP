

def getTestEquipment():
    summer_boilers_combination = [
        {'stationNumber': '3', 'mark': 'ТП-170', 'heat_performance': 150, 'numberOfStarts': 461},
        {'stationNumber': '4', 'mark': 'ТП-170', 'heat_performance': 170, 'numberOfStarts': 491},
        {'stationNumber': '8', 'mark': 'ТП-81', 'heat_performance': 420, 'numberOfStarts': 504}
    ]

    winter_boilers_combination = [
        {'stationNumber': '3', 'mark': 'ТП-170', 'heat_performance': 150, 'numberOfStarts': 461},
        {'stationNumber': '4', 'mark': 'ТП-170', 'heat_performance': 170, 'numberOfStarts': 491},
        {'stationNumber': '5', 'mark': 'ТП-170', 'heat_performance': 170, 'numberOfStarts': 530},
        {'stationNumber': '6', 'mark': 'ТП-80', 'heat_performance': 170, 'numberOfStarts': 562},
        {'stationNumber': '7', 'mark': 'ТП-87А', 'heat_performance': 420, 'numberOfStarts': 437},
        {'stationNumber': '8', 'mark': 'ТП-81', 'heat_performance': 420, 'numberOfStarts': 504},
        {'stationNumber': '9', 'mark': 'ТП-81', 'heat_performance': 420, 'numberOfStarts': 358}
    ]

    offSeason_boilers_combination = [
        {'stationNumber': '3', 'mark': 'ТП-170', 'heat_performance': 150, 'numberOfStarts': 461},
        {'stationNumber': '4', 'mark': 'ТП-170', 'heat_performance': 170, 'numberOfStarts': 491},
        {'stationNumber': '5', 'mark': 'ТП-170', 'heat_performance': 170, 'numberOfStarts': 530},
        {'stationNumber': '9', 'mark': 'ТП-81', 'heat_performance': 420, 'numberOfStarts': 358}
    ]

    summer_turbines_combination = [
        {'name': 'ТГ03', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 147.8},
        {'name': 'ТГ04', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 151.0},
        {'name': 'ТГ08', 'type': 'ПТ-80/100-130/13', 'electricity_power': 80, 'thermalPower': 190,
         'powerGeneration': 422.9}
    ]

    winter_turbines_combination = [
        {'name': 'ТГ03', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 147.8},
        {'name': 'ТГ04', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 151.0},
        {'name': 'ТГ05', 'type': 'Т-20-90', 'electricity_power': 20, 'thermalPower': 54, 'powerGeneration': 93.9},
        {'name': 'ТГ06', 'type': 'ПТ-65/75-130/13', 'electricity_power': 65, 'thermalPower': 139,
         'powerGeneration': 252.7},
        {'name': 'ТГ07', 'type': 'ПТ-65/75-130/13', 'electricity_power': 65, 'thermalPower': 139,
         'powerGeneration': 268.0},
        {'name': 'ТГ08', 'type': 'ПТ-80/100-130/13', 'electricity_power': 80, 'thermalPower': 190,
         'powerGeneration': 422.9},
        {'name': 'ТГ09', 'type': 'ПТ-80/100-130/13', 'electricity_power': 80, 'thermalPower': 190,
         'powerGeneration': 304.6}
    ]

    offSeason_turbines_combination = [
        {'name': 'ТГ08', 'type': 'ПТ-80/100-130/13', 'electricity_power': 80, 'thermalPower': 190,
         'powerGeneration': 422.9},
        {'name': 'ТГ09', 'type': 'ПТ-80/100-130/13', 'electricity_power': 80, 'thermalPower': 190,
         'powerGeneration': 304.6}
    ]

    return (
        summer_boilers_combination,
        winter_boilers_combination,
        offSeason_boilers_combination,
        summer_turbines_combination,
        winter_turbines_combination,
        offSeason_turbines_combination
    )