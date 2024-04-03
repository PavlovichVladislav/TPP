from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple

from boilers.calcBoilerHopNew import calc_boiler_hop
from boilers.calc_boilers_shop_hop import calc_boilers_shop_hop_per_season
from calc_optimal_equipment import optimal_equipment_combination_per_season, summer_month_numbers, winter_month_numbers, \
    offSeason_month_numbers
from mainOld import year_task
from station_hop import calc_station_hop
from turbines.turbine_shop_hop_new import calc_turbines_shop_hop
from turbines.turbine_hop_new import calc_turbine_hop

app = FastAPI()

class BoilerData(BaseModel):
    """
    Информация об одном котле

    :param stationNumber: Станционный номер котла.
    :param mark: Марка котла.
    :param heatPerformance: Номинальная максимальная теплопроизводительность Т/Ч.
    :param numberOfStarts: Количество запусков с момента начала эксплуатации.
    """
    stationNumber: str
    mark: str
    heatPerformance: int
    numberOfStarts: int

class BoilersInventory(BaseModel):
    """
    Котлы имеющиеся в наличии

    :param data: Список котлов в наличии у станции.
    """
    data: List[BoilerData]


@app.post("/boilers/optimal")
def get_boilers_optimal(
        data: BoilersInventory
):
    """
    Получение оптимального состава котлов на каждый сезон года.

    :param data: Состав котельного оборудования, имеющийся на станции.
    :return: Объект с оптимальным составом оборудования по сезонам года
    """
    boilers = [boiler.dict() for boiler in data.data]

    summer_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers, summer_month_numbers,
                                                                          'boilers')
    winter_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers, winter_month_numbers,
                                                                          'boilers')
    offSeason_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers,
                                                                             offSeason_month_numbers, 'boilers')

    print(summer_boilers_combination)

    return ({
        'summerBoilers': summer_boilers_combination,
        'winterBoilers': winter_boilers_combination,
        'offSeasonBoilers': offSeason_boilers_combination
    })

class BoilersInventory(BaseModel):
    """
    Котлы имеющиеся в наличии

    :param data: Список котлов в наличии у станции.
    """
    data: List[BoilerData]

class DataForBoilerHop(BaseModel):
    """
    Данные для расчёта ХОП отдельного котла

    :param load: Загрузка.
    :param efficiency: Кпд
    """
    load: List[float]
    efficiency: List[float]

@app.post("/boilers/boiler-hop")
def calc_boilers_shop_hop(
        hopData: DataForBoilerHop
):

    hop = calc_boiler_hop({'load': hopData.load, 'efficiency': hopData.efficiency})

    print({'load': hopData.load, 'efficiency': hopData.efficiency})
    print(hopData)

    print(hop)

    return {'ХОП': hop}

class BoilerHop(BaseModel):
    mark: str
    b: List[float]
    Q: List[float]

@app.post("/boilers/boiler-shop-hop")
def calc_boilers_shop_hop(
        boilersHop: List[BoilerHop]
):
    boilers_hop = [
        {'mark': item.mark, 'b': item.b, 'Q': item.Q}
        for item in boilersHop
    ]

    # to-do убрать параметры для графиков
    hop = calc_boilers_shop_hop_per_season(boilers_hop, False, False)

    return {'ХОП': hop}

class TurbineData(BaseModel):
    """
    Информация об одном котле

    :param name: станционный номер.
    :param type: Марка турбины.
    :param electricityPower: установленная электрическая мощность.
    :param thermalPower: тепловая мощность гкал/ч.
    :param powerGeneration: выработка электроэнергии в отчётном.
    """
    name: str
    type: str
    electricityPower: int
    thermalPower: int
    powerGeneration: float

class TurbinesInventory(BaseModel):
    """
    Турбины имеющиеся в наличии

    :param data: Список турбин в наличии у станции.
    """
    data: List[TurbineData]

@app.post("/turbines/get-optimal")
def get_turbines_optimal(
        data: TurbinesInventory
):
    """
    Получение оптимального состава турбин на каждый сезон года.

    :param data: Состав котельного оборудования, имеющийся на станции.
    :return: Объект с оптимальным составом оборудования по сезонам года
    """
    turbines = [turbine.dict() for turbine in data.data]

    print(turbines)

    summer_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, summer_month_numbers,
                                                                          'turbines')
    winter_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, winter_month_numbers,
                                                                          'turbines')
    offSeason_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines,
                                                                             offSeason_month_numbers, 'turbines')

    print(summer_turbines_combination)

    return ({
        'summerTurbines': summer_turbines_combination,
        'winterTurbines': winter_turbines_combination,
        'offSeasonTurbines': offSeason_turbines_combination
    })

class TurbineDataForHop(BaseModel):
    type: str
    steam_consuption: float

@app.post("/turbines/turbine-hop")
def get_turbines_shop_hop(
        turbineData: TurbineDataForHop
):
    turbine = turbineData.dict()

    print(turbine)

    turbines_hop = calc_turbine_hop(turbine['type'], turbine['steam_consuption'])

    return {'hop': turbines_hop}

@app.post("/turbines/turbine-shop-hop")
def get_turbines_shop_hop(
        turbinesData: List[TurbineDataForHop]
):
    turbines = [turbine.dict() for turbine in turbinesData]

    print(turbines)

    flow_chars, turbines_shop_hop = calc_turbines_shop_hop(turbines)

    return {'ХОП': turbines_shop_hop, 'FlowChars': flow_chars}

class HopValuePerInterval(BaseModel):
    interval: Tuple[float, float]
    tangent: float

class TurbinesShopHop(BaseModel):
    data: List[HopValuePerInterval]

class BoilerShopHop(BaseModel):
    b: List[float]
    Q: List[float]

class ShopFlowChar(BaseModel):
    start: Tuple[float, float]
    points: List[Tuple[float, float]]
    end: Tuple[float, float]

@app.post("/station/station-hop")
def get_turbines_shop_hop(
        turbineShopHop: TurbinesShopHop,
        boilersShopHop: BoilerShopHop,
        shopFlowChar: ShopFlowChar
):
    turbineShopHop = [hopPerInterval.dict() for hopPerInterval in turbineShopHop.data]

    station_hop = calc_station_hop(boilersShopHop.dict(), turbineShopHop, shopFlowChar.dict())

    return {'stationHop': station_hop}