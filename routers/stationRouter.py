from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Tuple

from optimize.calculateMC import calculate_mc
from optimize.calculateMR import calculate_mr
from optimize.tppOptimization import tppOptimize
from optimize.station_hop import calc_station_hop

stationRouter = APIRouter(
    prefix="/station",
    tags=["Станция"]
)


class TurbineRgc(BaseModel):
    """
    Составная часть ХОП турбинного цеха

    :interval : диапазон мощностей для значения tangent
    :tangent : значение ХОП
    """
    interval: Tuple[float, float]
    tangent: float


class TurbinesShopHop(BaseModel):
    """
    ХОП турбинного цеха

    :data : массив интервалов и соответствующих им значений тангенса
    """
    data: List[TurbineRgc]


class BoilerShopHop(BaseModel):
    """
    ХОП котельного цеха

    :param b: значения ХОП
    :param Q: значения нагрузки
    """
    b: List[float]
    Q: List[float]


class ShopFlowChar(BaseModel):
    """
    Расходная характеристика станции

    :param start: начальная точка
    :param points: точки излома
    :param end: последняя точка
    """
    start: Tuple[float, float]
    points: List[Tuple[float, float]]
    end: Tuple[float, float]


class StationRgc(BaseModel):
    """
    ХОП станции

    :param N: диапазон мощностей
    :param b: значения ХОП
    """
    N: List[float]
    b: List[float]


@stationRouter.post("/station-rgc")
def get_station_rgc(
        turbineShopHop: List[TurbineRgc],
        boilersShopHop: BoilerShopHop,
        shopFlowChar: ShopFlowChar
) -> StationRgc:
    """
    Расчёт ХОП станции

    :param turbineShopHop: ХОП турбинного цеха
    :param boilersShopHop: ХОП котельного цеха
    :param shopFlowChar: расходная характеристика станции
    """
    turbineShopHop = [hopPerInterval.dict() for hopPerInterval in turbineShopHop]

    station_rgc = calc_station_hop(boilersShopHop.dict(), turbineShopHop, shopFlowChar.dict())

    return station_rgc


class MR(BaseModel):
    """
    Предельный доход станции

    :param pg: диапазон мощностей
    :param mr: значения предельного дохода
    """
    pg: List[float]
    mr: List[float]


class Demand(BaseModel):
    """
    Характеристика спроса

    :param pg: Характеристика спроса
    :param price: цена
    """
    pg: List[float]
    price: List[float]


class StationOptimizeData(BaseModel):
    """
    Данные для расчёта оптимального режима работы станции

    :param rgc: ХОП станции
    :param fuel_price: цены на топлива за год(кажд. месяц)
    :param demand: Характеристика спроса
    :param season: сезон года, для которого считается оптимальный режим
    """
    rgc: StationRgc
    fuel_price: List[float]
    demand: Demand
    season: str


# Оптимальный режим работы станции за сезон
@stationRouter.post("/optimize")
def get_station_optimal_mode(
        data: StationOptimizeData
):
    """
    Метод для расчёта оптимальных мощностей станции

    :param data: данные для оптимизации станции
    :return resultTalbeData: данные для составления таблицы результата
            содержат информацию о прибыли, выручке за год
    """
    # Преобразуем входные данные в словари
    hop = data.rgc.dict()
    demand = data.demand.dict()

    # Считаем предельный доход
    mr = calculate_mr(demand)
    # Считаем предельные издержки
    mc = calculate_mc(hop, data.fuel_price, data.season)

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
            "up_percent": up_percent,
            "mr_up": MR_2,
            "mc_up": MC_2,
            'demand_up': Demand_2}
