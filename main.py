from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from calc_boilers_hop import calc_boiler_hop
from calc_boilers_shop_hop import calc_boilers_shop_hop_per_season
from calc_optimal_equipment import optimal_equipment_combination_per_season, summer_month_numbers, winter_month_numbers, \
    offSeason_month_numbers
from mainOld import year_task

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

@app.post("/boilers/boiler-hop")
def calc_boilers_shop_hop(
        boiler: BoilerData
):
    hop = calc_boiler_hop(boiler['mark'])

    # print(hop)

    return {'ХОП': None}

class BoilerHop(BaseModel):
    mark: str
    b: List[float]
    Q: List[float]

@app.post("/boilers/boiler-shop-hop")
def calc_boilers_shop_hop(
        boilersHop: List[BoilerHop]
):
    print(boilersHop)

    boilers_hop = [
        {'mark': item.mark, 'b': item.b, 'Q': item.Q}
        for item in boilersHop
    ]

    # to-do убрать параметры для графиков
    hop = calc_boilers_shop_hop_per_season(boilers_hop, False, False)

    print(hop)

    return {'ХОП': hop}