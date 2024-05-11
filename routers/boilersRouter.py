from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from boilers.calcBoilerRgc import calc_boiler_rgc
from boilers.calc_boilers_shop_rgc import calc_boilers_shop_rgc_per_season
from calc_optimal_equipment import optimal_equipment_combination_per_season
from consts import summer_month_numbers, winter_month_numbers, offSeason_month_numbers
from mainOld import year_task

boilersRouter = APIRouter(
    prefix="/boilers",
    tags=["Котлы"]
)


class Boiler(BaseModel):
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
    boilers: List[Boiler]


@boilersRouter.post("/optimal")
def get_boilers_optimal(
        data: BoilersInventory
):
    """
    Получение оптимального состава котлов на каждый сезон года.

    :param data: Состав котельного оборудования, имеющийся на станции.
    :return: Объект с оптимальным составом оборудования по сезонам года
    """
    boilers = [boiler.dict() for boiler in data.boilers]

    print('optimal')

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


class DataForBoilerRgc(BaseModel):
    """
    Данные для расчёта ХОП отдельного котла

    :param load: Загрузка.
    :param efficiency: Кпд
    """
    load: List[float]
    efficiency: List[float]


@boilersRouter.post("/boiler-rgc")
def calculate_boiler_hop(
        rgcData: DataForBoilerRgc
):
    """
    Расчёт ХОП для отдельного котла

    :param rgcData: Исходные данные для расчёта ХОП котла
    :return: ХОП котла с полями b_values, Q_values
    """
    rgc = calc_boiler_rgc({'load': rgcData.load, 'efficiency': rgcData.efficiency})

    return rgc


class BoilerRGC(BaseModel):
    """
    ХОП котла

    :param id: id котла в БД
    :param boiler_mark: марка котла
    :param b_values: значение ХОП
    :param Q_values: значения нагрузки
    """
    id: int
    boiler_mark: str
    b_values: List[float]
    Q_values: List[float]


@boilersRouter.post("/boiler-shop-rgc")
def calc_boilers_shop_hop(
        boilersRgc: List[BoilerRGC]
):
    """
    Расчёт ХОП для котельного цеха

    :param boilersRgc: ХОП инвентарных котлов
    :return: ХОП котельного цеха, содержит два поля b, Q
    """
    boilers_rgc = [
        {'mark': item.boiler_mark, 'b': item.b_values, 'Q': item.Q_values}
        for item in boilersRgc
    ]

    shop_rgc = calc_boilers_shop_rgc_per_season(boilers_rgc, False, False)

    return shop_rgc
