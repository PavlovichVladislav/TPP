from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from boilers.calcBoilerRgc import calc_boiler_rgc
from boilers.calc_boilers_shop_rgc import calc_boilers_shop_rgc_per_season
from calc_optimal_equipment import optimal_equipment_combination_per_season
from consts import summer_month_numbers, winter_month_numbers, off_season_month_numbers
from mainOld import year_task

boilersRouter = APIRouter(
    prefix="/boilers",
    tags=["Котлы"]
)


class Boiler(BaseModel):
    """
    Информация об одном котле

    :param station_number: Станционный номер котла.
    :param mark: Марка котла.
    :param heat_performance: Номинальная максимальная теплопроизводительность Т/Ч.
    :param starts_number: Количество запусков с момента начала эксплуатации.
    """
    station_number: int
    mark: str
    heat_performance: int
    starts_number: int


class BoilersInventory(BaseModel):
    """
    Котлы имеющиеся в наличии

    :param boilers: Список котлов в наличии у станции.
    """
    boilers: List[Boiler]


class BoilersOptimalCombination(BaseModel):
    """
    Оптимальная комбинация котлов для каждого сезона

    :param summer_boilers: Оптимальная комбинация котлов для летнего сезона.
    :param winter_boilers: Оптимальная комбинация котлов для зимнего сезона.
    :param off_season_boilers: Оптимальная комбинация котлов для межсезонья.
    """
    summerBoilers: List[Boiler]
    winterBoilers: List[Boiler]
    offSeasonBoilers: List[Boiler]


@boilersRouter.post("/optimal")
def get_boilers_optimal(
        data: BoilersInventory
) -> BoilersOptimalCombination:
    """
    Получение оптимального состава котлов на каждый сезон года.

    :param data: Состав котельного оборудования, имеющийся на станции.
    :return: Объект с оптимальным составом оборудования по сезонам года
    """
    boilers = [boiler.dict() for boiler in data.boilers]

    summer_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers, summer_month_numbers,
                                                                          'boilers')
    winter_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers, winter_month_numbers,
                                                                          'boilers')
    off_season_boilers_combination = optimal_equipment_combination_per_season(year_task, boilers,
                                                                              off_season_month_numbers, 'boilers')
    return BoilersOptimalCombination(
        summerBoilers=summer_boilers_combination,
        winterBoilers=winter_boilers_combination,
        offSeasonBoilers=off_season_boilers_combination
    )


class BoilerFactoryData(BaseModel):
    """
    Заводские данные для расчёта ХОП отдельного котла

    :param Q: нагрузка
    :param efficiency: КПД
    """
    Q: List[float]
    efficiency: List[float]


class BoilerRgc(BaseModel):
    """
    ХОП Котла

    :param b: значение ХОП
    :param Q: значения нагрузки
    """
    b: List[float]
    Q: List[float]


@boilersRouter.post("/boiler-rgc")
def calculate_boiler_hop(
        rgc_data: BoilerFactoryData
) -> BoilerRgc:
    """
    Расчёт ХОП для отдельного котла

    :param rgc_data: Исходные данные для расчёта ХОП котла
    :return: ХОП котла с полями b_values, Q_values
    """
    rgc = calc_boiler_rgc({'load': rgc_data.load, 'efficiency': rgc_data.efficiency})

    return rgc


class BoilerWithRGC(BaseModel):
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
        boilersRgc: List[BoilerWithRGC]
) -> BoilerRgc:
    """
    Расчёт ХОП для котельного цеха

    :param boilersRgc: ХОП инвентарных котлов
    :return: ХОП котельного цеха, содержит два поля b, Q
    """
    boilers_rgc = [
        {'mark': item.boiler_mark, 'b': item.b_values, 'Q': item.Q_values}
        for item in boilersRgc
    ]

    shop_rgc = calc_boilers_shop_rgc_per_season(boilers_rgc)

    return shop_rgc
