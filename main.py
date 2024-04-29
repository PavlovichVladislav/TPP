from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple, Literal

from boilers.calcBoilerHopNew import calc_boiler_hop
from boilers.calc_boilers_shop_hop import calc_boilers_shop_hop_per_season
from calc_optimal_equipment import optimal_equipment_combination_per_season, summer_month_numbers, winter_month_numbers, \
    offSeason_month_numbers
from mainOld import year_task
from optimize.calculateMC import calculate_mc
from optimize.calculateMR import calculate_mr
from optimize.tppOptimization import tppOptimize
from station_hop import calc_station_hop
from turbines.turbine_shop_hop_new import calc_turbines_shop_hop
from turbines.turbine_hop_new import calc_turbine_hop
from fastapi.middleware.cors import CORSMiddleware
from turbines.get_collection_point_new import get_collection_point

app = FastAPI()

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно настроить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы HTTP
    allow_headers=["*"],  # Разрешаем все заголовки HTTP
)


class BoilerData(BaseModel):
    """
    Информация об одном котле

    :param stationNumber: Станционный номер котла.
    :param mark: Марка котла.
    :param heatPerformance: Номинальная максимальная теплопроизводительность Т/Ч.
    :param numberOfStarts: Количество запусков с момента начала эксплуатации.
    """
    station_number: str
    mark: str
    heat_performance: int
    station_number: int


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
def calculate_boiler_hop(
        hopData: DataForBoilerHop
):
    hop = calc_boiler_hop({'load': hopData.load, 'efficiency': hopData.efficiency})

    return hop


class BoilerHop(BaseModel):
    id: int
    boiler_mark: str
    b_values: List[float]
    Q_values: List[float]


@app.post("/boilers/boiler-shop-hop")
def calc_boilers_shop_hop(
        boilersHop: List[BoilerHop]
):
    print(boilersHop)

    boilers_hop = [
        {'mark': item.boiler_mark, 'b': item.b_values, 'Q': item.Q_values}
        for item in boilersHop
    ]

    # to-do убрать параметры для графиков
    hop = calc_boilers_shop_hop_per_season(boilers_hop, False, False)

    return hop


class TurbineData(BaseModel):
    """
    Информация об одном котле

    :param name: станционный номер.
    :param type: Марка турбины.
    :param electricityPower: установленная электрическая мощность.
    :param thermalPower: тепловая мощность гкал/ч.
    :param powerGeneration: выработка электроэнергии в отчётном.
    """
    station_number: int
    mark: str
    electricity_power: int
    thermal_power: int
    power_generation: float


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

    summer_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, summer_month_numbers,
                                                                           'turbines')
    winter_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines, winter_month_numbers,
                                                                           'turbines')
    offSeason_turbines_combination = optimal_equipment_combination_per_season(year_task, turbines,
                                                                              offSeason_month_numbers, 'turbines')
    return ({
        'summerTurbines': summer_turbines_combination,
        'winterTurbines': winter_turbines_combination,
        'offSeasonTurbines': offSeason_turbines_combination
    })


class DataForCollectionPoint(BaseModel):
    steam_consumption: List[float]
    season: str


@app.post("/turbines/collection-point")
def get_turbines_shop_hop(
        data: DataForCollectionPoint
):
    collection_point = get_collection_point(data.steam_consumption, data.season)

    return collection_point


class TurbineData(BaseModel):
    turbine_mark: str
    steam_consumption: List[float]


class TurbineDataForHop(TurbineData):
    season: str


@app.post("/turbines/turbine-hop")
def get_turbine_hop(
        turbine_data: TurbineDataForHop
):
    steam_consuption = get_collection_point(turbine_data.steam_consumption, turbine_data.season)

    turbines_hop = calc_turbine_hop(turbine_data.turbine_mark, steam_consuption)

    return turbines_hop


class TurbinesShopHopData(BaseModel):
    turbines_data: List[TurbineData]
    season: str


@app.post("/turbines/turbine-shop-hop")
def get_turbines_shop_hop(
        data: TurbinesShopHopData
):
    turbines = [turbine.dict() for turbine in data.turbines_data]

    flow_char, turbines_shop_hop = calc_turbines_shop_hop(turbines, data.season)

    return {'flow_char': flow_char, 'turbines_shop_hop': turbines_shop_hop}


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


# предельный доход
class MR(BaseModel):
    pg: List[float]
    mr: List[float]


# предельный издержки
class Hop(BaseModel):
    N: List[float]
    b: List[float]


# спрос
class Demand(BaseModel):
    pg: List[float]
    price: List[float]


class stationOptimizeData(BaseModel):
    hop: Hop
    fuelPirce: List[float]
    demand: Demand
    season: str


# Оптимальный режим работы станции за сезон
@app.post("/station/optimize")
def get_turbines_shop_hop(
        data: stationOptimizeData
):
    # Преобразуем входные данные в словари
    hop = data.hop.dict()
    demand = data.demand.dict()

    # Считаем предельный доход
    mr = calculate_mr(demand)
    # Считаем предельные издержки
    mc = calculate_mc(hop, data.fuelPirce, data.season)

    # Считаем оптимальный режим работы станции
    n1_opt, p1_opt, MR_1, Demand_1, MC_1 = tppOptimize(mr, mc, demand)

    # Копируем pg из demand
    demand_25percent = Demand(pg=data.demand.pg, price=[])

    # Увеличиваем значения price на 25%
    demand_25percent.price = [price * 1.25 for price in data.demand.price]

    # Считаем предельный доход
    mr_25percent = calculate_mr(demand_25percent.dict())

    # Считаем оптимальный режим работы станции
    n2_opt, p2_opt, MR_2, Demand_2, MC_2 = tppOptimize(mr_25percent, mc, demand_25percent.dict())

    # Составляем таблицу - результат
    zero_percent = [round(n1_opt, 2), round(n1_opt * 720, 2), round(p1_opt, 2), round(n1_opt * p1_opt, 2), 0]
    up_percent = [round(n2_opt, 2), round(n2_opt * 720, 2), round(p2_opt, 2), round(n2_opt * p2_opt, 2),
                  round(n2_opt * p2_opt - n1_opt * p1_opt, 2)]

    return {'zero_percent': zero_percent,
            "mr": MR_1,
            "mc": MC_1,
            'demand': Demand_1,
            "25_percent": up_percent,
            "mr_25": MR_2,
            "mc_25": MC_2,
            'demand_25': Demand_2}
